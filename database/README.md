# WALLY Database

This folder contains the Dockerfile and startup scripts for the WALLY database.

## pgconf folder

`pgconf/setup.sql` will be copied to the /pgconf directory of the built container.  This script will
be automatically run when the database is first initialized.

## scripts folder

Scripts in the scripts folder will be copied to the /scripts directory of the container.  You can invoke them
from `setup.sql` by adding a `\i [filename]` line to the bottom.
