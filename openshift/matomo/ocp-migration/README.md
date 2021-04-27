# Migration

## Assumptions
1. The steps included here depend on having the matomo and motomo-db deployments already deployed on the OCP4 Silver platform. The instructions for this are included in the parent directory.
2. You must use the same Matomo version when transfering data or else the data will not persist.

## Migration steps
Here are the steps to migrate an instance of Matomo with active user data from the Openshift Container Platform (OCP) version 3 to version 4.
To avoid confusion, let's call OCP3 Pathfinder and OCP4 Silver.

### Before you start
You need:

- [ ] Migrator CLI Deployment Config
   - Used to migrate the mariadb mysql database
- [ ] The following built image is required to deploy. This image was used for the GWELLS ocp v3-v4 migration.
   - image-registry.openshift-image-registry.svc:5000/openshift/cli@sha256:cc4eaab57638fe0b20e449dcc94ae5325dfd9cb69dc631b28420be85deb32e60

### Migration checklist 
- [ ] Make sure all services are down to prevent users from creating new actions and data
- [ ] Migrate database
- [ ] Access Matomo GUI in Silver and update the urls to match the new domain
- [ ] Double check everything on Silver.
- [ ] Make sure no traffic is getting processed in Pathfinder.

## Migration tools

### Setting up the Migrator CLI with the database migration scripts
**Migration scripts**
```bash
# Set namespace (will be used in the next script)
NAMESPACE4="d1b5d2-dev"

# Create a config map from the migration scripts
oc -n $NAMESPACE4 create configmap matomo-migration-scripts \
--from-file=scripts/
```

**migrator-cli (importer.dc.yaml)**
```bash
# Deploy migrator dc with oc cli
oc process -f matomo-migrator.dc.yaml -p NAMESPACE=$NAMESPACE4 | oc apply -f -
```

### Running the migration script
**NOTE:** You need your Pathfinder auth token and Silver auth token. Have it handy beforehand.

Inside the `matomo-migrator-cli` pod:
```/bin/bash
cd scripts

# Run the script
# This script does all the migration steps. 
# It will ask you for the environment, matomo database user, and matomo database password
./do_migration.sh
```

#### Smaller migration scripts
**`db_dump_and_copy.sh`**
```bash
# Runs `mysqldump` on Pathfinder and copies to migrator container
./db_dump_and_copy.sh [test/prod]
```

**`db_copy_and_restore.sh`**
```bash
# Copies the dump file from the migrator volume onto the Silver matomo-db pod volume
# Commits the .sql file insert into the matomo mysql database
./db_copy_and_restore.sh [test/prod]
```




**`scale_down.sh`**
```bash
# Scales down the `gwells-staging` application on Silver 
./activate_proxy.sh [test/prod]

# To scale it up, add `--revert` at the end
./activate_proxy.sh [test/prod] --revert
```

**`scale_up.sh`**
```bash
# Scales up the `gwells-staging` application on Silver 
./activate_proxy.sh [test/prod]

# To scale it up, add `--revert` at the end
./activate_proxy.sh [test/prod] --revert
```

#### Issues, tips and tricks
**Login to the migrator-cli pod terminal quickly**
I use a helper script named `rsh_migrator_cli.sh`

```bash
# Make it executable
chmod +x rsh_migrator_cli.sh 
```

```bash
# RSH into migrator-cli pod, first param is your namespace
./rsh_migrator_cli.sh d1b5d2-dev
```

**If you run into authorization issues while running one of the smaller migration scripts**  q
```bash
# Sample unauthorized message
error: You must be logged in to the server (Unauthorized)
```
Just delete the kubeconfig files `/tmp/KUBECONFIG` and `/tmp/KUBECONFIGSILVER`
