#!groovy
@Library('bcgov-library') _
import bcgov.GitHubHelper

// Notify stage status and pass to Jenkins-GitHub library
void notifyStageStatus (String name, String status) {
    GitHubHelper.createCommitStatus(
        this,
        sh(returnStdout: true, script: 'git rev-parse HEAD'), // this is the most recent commit ID
        status,
        "${BUILD_URL}",
        "Stage: ${name}",
        "${name}"
    )
}

// createDeployment gets a new deployment ID from GitHub.
// this lets us display notifications on GitHub when new environments
// are deployed (e.g. on a pull request page)
Long createDeployment (String suffix, String gitRef) {
    def ghDeploymentId = new GitHubHelper().createDeployment(
        this,
        gitRef,
        [
            'environment':"${suffix}",
            'task':"deploy:${gitRef}"
        ]
    )
    echo "deployment ID: ${ghDeploymentId}"
    return ghDeploymentId

}

// Create deployment status for a deployment ID (call createDeployment first)
void createDeploymentStatus (Long ghDeploymentId, String status, String stageUrl) {
    echo "creating deployment status (${status})"
    new GitHubHelper().createDeploymentStatus(
        this,
        ghDeploymentId,
        "${status}",
        ['targetUrl':"https://${stageUrl}/"]
    )

}

// Run an action in a stage with GitHub notifications and stage retries on failure.
// Because the GitHub notification uses the `name` argument, make sure name is unique
// each time using this wrapper.
def withStatus(String name, Closure body) {
  waitUntil {
      notifyStageStatus (name, 'PENDING')
      boolean isDone=false
      try {
          body()
          isDone=true
          notifyStageStatus(name, 'SUCCESS')
          echo "Completed Stage '${name}'"
      } catch (error){
          notifyStageStatus(name, 'FAILURE')
          echo "${stackTraceAsString(error)}"
          def inputAction = input(
              message: "This step (${name}) has failed. See related messages.",
              ok: 'Confirm',
              parameters: [
                  choice(
                      name: 'action',
                      choices: 'Re-run\nIgnore',
                      description: 'What would you like to do?'
                  )
              ]
          )
          if ('Ignore'.equalsIgnoreCase(inputAction)){
              isDone=true
          }
      }
      return isDone
  }
}


// Print stack trace of error
@NonCPS
private static String stackTraceAsString(Throwable t) {
    StringWriter sw = new StringWriter();
    t.printStackTrace(new PrintWriter(sw));
    return sw.toString()
}


pipeline {
  agent any
  environment {
    GIT_REPO = "https://github.com/bcgov-c/wally.git"
    NAME = JOB_BASE_NAME.toLowerCase()

    // project names
    TOOLS_PROJECT = "bfpeyx-tools"
    DEV_PROJECT = "bfpeyx-dev"
    TEST_PROJECT = "bfpeyx-test"
    PROD_PROJECT = "bfpeyx-prod"
  }
  stages {
    stage('Build') {
      steps {
        script {
          echo "Cancelling previous builds..."
          timeout(10) {
              abortAllPreviousBuildInProgress(currentBuild)
          }
          echo "Previous builds cancelled"

          // ref defaults to the master branch, but if this is a pull
          // request, set the git ref to the pull request ref.
          def ref = "master"
          if (env.JOB_BASE_NAME != 'master') {
            ref = "pull/${CHANGE_ID}/head"
          }

          openshift.withCluster() {
            openshift.withProject() {
              withStatus(env.STAGE_NAME) {
                echo "Applying templates"
                def bcWebTemplate = openshift.process('-f',
                  'openshift/frontend.build.yaml',
                  "NAME=${NAME}",
                  "GIT_REPO=${GIT_REPO}",
                  "GIT_REF=${ref}"
                )

                def bcApiTemplate = openshift.process('-f',
                  'openshift/backend.build.yaml',
                  "NAME=${NAME}",
                  "GIT_REPO=${GIT_REPO}",
                  "GIT_REF=${ref}"
                )

                timeout(15) {
                  echo "Starting builds"
                  def bcWeb = openshift.apply(bcWebTemplate).narrow('bc').startBuild()
                  def bcApi = openshift.apply(bcApiTemplate).narrow('bc').startBuild()
                  def webBuilds = bcWeb.narrow('builds')
                  def apiBuilds = bcApi.narrow('builds')

                  sleep(5)

                  // wait for builds to run.
                  webBuilds.untilEach(1) {
                      return it.object().status.phase == "Complete" || it.object().status.phase == "Failed"
                  }
                  apiBuilds.untilEach(1) {
                      return it.object().status.phase == "Complete" || it.object().status.phase == "Failed"
                  }

                  // the previous step waited for builds to finish (whether successful or not),
                  // so here we check for errors.
                  webBuilds.withEach {
                    if (it.object().status.phase == "Failed") {
                      bcWeb.logs()
                      error('Frontend build failed')
                    }
                  }

                  apiBuilds.withEach {
                    if (it.object().status.phase == "Failed") {
                      bcApi.logs()
                      error('Backend build failed')
                    }
                  }

                }
                echo "Success! Builds completed."
              }
            }
          }
        }
      }
    }
    stage('Deploy') {
      when {
          expression { env.JOB_BASE_NAME != 'master' }
      }
      steps {
        script {
          def project = DEV_PROJECT
          def host = "wally-${NAME}.pathfinder.gov.bc.ca"
          def ref = "pull/${CHANGE_ID}/head"
          // Get full describe info including # of commits & last commit hash
          def git_tag = sh(returnStdout: true,
            script: 'git describe'
          ).trim()
          openshift.withCluster() {
            openshift.withProject(project) {
              withStatus(env.STAGE_NAME) {

                // create deployment object at GitHub and give it a pending status.
                // this creates a notice on the pull request page indicating that a deployment
                // is pending.
                def deployment = createDeployment('dev', ref)
                createDeploymentStatus(deployment, 'PENDING', host)

                // apply database service account.
                // this is a pre-requisite for the database statefulset.
                openshift.apply(openshift.process("-f",
                  "openshift/database.rolebinding.yaml",
                  "NAME=wally-psql",
                  "SUFFIX=-${NAME}"
                ))

                sleep(3)

                // apply frontend application template
                def frontend = openshift.apply(openshift.process("-f",
                  "openshift/frontend.deploy.yaml",
                  "NAME=${NAME}",
                  "HOST=${host}",
                  "REPLICAS=1",
                  "NAMESPACE=${project}"
                ))

                // apply database template
                def database = openshift.apply(openshift.process("-f",
                  "openshift/database.deploy.yaml",
                  "NAME=wally-psql",
                  "REPLICAS=1",
                  "CPU_REQUEST=100m",
                  "CPU_LIMIT=200m",
                  "SUFFIX=-${NAME}",
                  "IMAGE_STREAM_NAMESPACE=${project}",
                  "STORAGE_CLASS=netapp-file-standard"
                ))

                def backend = openshift.apply(openshift.process("-f",
                  "openshift/backend.deploy.yaml",
                  "NAME=${NAME}",
                  "HOST=${host}",
                  "NAMESPACE=${project}",
                  "REPLICAS=1",
                  "ENVIRONMENT=DEV",
                  "WALLY_VERSION=${git_tag}",
                ))

                def gatekeeper = openshift.apply(openshift.process("-f",
                  "openshift/gatekeeper.deploy.yaml",
                  "NAME=${NAME}",
                  "HOST=${host}",
                  "NAMESPACE=${project}",
                  "REPLICAS=1",
                  "ENVIRONMENT=DEV"
                ))
                
                echo "Deploying to a dev environment"

                // tag images into dev project.  This triggers re-deploy.
                openshift.tag("${TOOLS_PROJECT}/wally-web:${NAME}", "${DEV_PROJECT}/wally-web:${NAME}")
                openshift.tag("${TOOLS_PROJECT}/wally-api:${NAME}", "${DEV_PROJECT}/wally-api:${NAME}")

                // wait for any deployments to finish updating.
                frontend.narrow('dc').rollout().status()
                database.narrow('dc').rollout().status()
                backend.narrow('dc').rollout().status()
                gatekeeper.narrow('dc').rollout().status()

                // update GitHub deployment status.
                createDeploymentStatus(deployment, 'SUCCESS', host)
                echo "Successfully deployed"
              }
            }
          }
        }
      }
    }
    stage('API tests') {
      when {
          expression { env.JOB_BASE_NAME != 'master' }
      }
      steps {
        script {
          def host = "wally-${NAME}.pathfinder.gov.bc.ca"
          openshift.withCluster() {
            openshift.withProject(TOOLS_PROJECT) {
              withStatus(env.STAGE_NAME) {
                podTemplate(
                    label: "apitest-${NAME}-${BUILD_NUMBER}",
                    name: "apitest-${NAME}-${BUILD_NUMBER}",
                    serviceAccount: 'jenkins',
                    cloud: 'openshift',
                    activeDeadlineSeconds: 1800,
                    containers: [
                        containerTemplate(
                            name: 'jnlp',
                            image: 'docker-registry.default.svc:5000/bfpeyx-tools/apitest',
                            imagePullPolicy: 'Always',
                            resourceRequestCpu: '500m',
                            resourceLimitCpu: '800m',
                            resourceRequestMemory: '512Mi',
                            resourceLimitMemory: '1Gi',
                            activeDeadlineSeconds: '600',
                            podRetention: 'never',
                            workingDir: '/tmp',
                            command: '',
                            args: '${computer.jnlpmac} ${computer.name}',
                            envVars: [
                                envVar(
                                    key:'BASE_URL',
                                    value: "https://${host}"
                                ),
                                secretEnvVar(
                                    key: 'AUTH_HOST',
                                    secretName: 'apitest-test-creds',
                                    secretKey: 'AUTH_HOST'
                                ),
                                secretEnvVar(
                                    key: 'AUTH_PASS',
                                    secretName: 'apitest-test-creds',
                                    secretKey: 'AUTH_PASS'
                                ),
                                secretEnvVar(
                                    key: 'AUTH_USER',
                                    secretName: 'apitest-test-creds',
                                    secretKey: 'AUTH_USER'
                                ),
                                secretEnvVar(
                                    key: 'CLIENT_ID',
                                    secretName: 'apitest-test-creds',
                                    secretKey: 'CLIENT_ID'
                                ),
                                secretEnvVar(
                                    key: 'CLIENT_SECRET',
                                    secretName: 'apitest-test-creds',
                                    secretKey: 'CLIENT_SECRET'
                                ),
                            ]
                        )
                    ]
                ) {
                    node("apitest-${NAME}-${BUILD_NUMBER}") {
                        checkout scm
                        dir('backend/api-tests') {
                            try {
                                sh """
                                  apitest -f data_endpoints.apitest.yaml \
                                  -e host=$BASE_URL \
                                  -e auth_user=$AUTH_USER \
                                  -e auth_pass=$AUTH_PASS \
                                  -e auth_url=$AUTH_HOST \
                                  -e auth_id=$CLIENT_ID \
                                  -e auth_secret=$CLIENT_SECRET &&
                                  apitest -f geocoder.apitest.yaml \
                                  -e host=$BASE_URL \
                                  -e auth_user=$AUTH_USER \
                                  -e auth_pass=$AUTH_PASS \
                                  -e auth_url=$AUTH_HOST \
                                  -e auth_id=$CLIENT_ID \
                                  -e auth_secret=$CLIENT_SECRET &&
                                  apitest -f catalogue.apitest.yaml \
                                  -e host=$BASE_URL \
                                  -e auth_user=$AUTH_USER \
                                  -e auth_pass=$AUTH_PASS \
                                  -e auth_url=$AUTH_HOST \
                                  -e auth_id=$CLIENT_ID \
                                  -e auth_secret=$CLIENT_SECRET
                                  """
                                }
                            finally {
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
    stage('Deploy to staging') {
      when {
          expression { env.JOB_BASE_NAME == 'master' }
      }
      steps {
        script {
          // Get full describe info including # of commits & last commit hash
          def git_tag = sh (
              returnStdout: true,
              script: 'git describe'
            ).trim()
          def project = TEST_PROJECT
          def env_name = "staging"
          def host = "wally-staging.pathfinder.gov.bc.ca"
          def ref = "refs/heads/master"
          openshift.withCluster() {
            openshift.withProject(project) {
              withStatus(env.STAGE_NAME) {

                // create deployment object at GitHub and give it a pending status.
                // this creates a notice on the pull request page indicating that a deployment
                // is pending.
                def deployment = createDeployment('staging', ref)
                createDeploymentStatus(deployment, 'PENDING', host)

                // apply database service account.
                // this is a pre-requisite for the database statefulset.
                openshift.apply(openshift.process("-f",
                  "openshift/database.rolebinding.yaml",
                  "NAME=wally-psql",
                  "SUFFIX=-${env_name}"
                ))

                sleep(3)

                // apply frontend application template
                def frontend = openshift.apply(openshift.process("-f",
                  "openshift/frontend.deploy.yaml",
                  "NAME=${env_name}",
                  "HOST=${host}",
                  "NAMESPACE=${project}",
                  "REPLICAS=2"
                ))

                // apply database template
                def database = openshift.apply(openshift.process("-f",
                  "openshift/database.deploy.yaml",
                  "NAME=wally-psql",
                  "REPLICAS=3",
                  "SUFFIX=-${env_name}",
                  "PVC_SIZE=30Gi",
                  "CPU_REQUEST=200m",
                  "CPU_LIMIT=2",
                  "MEMORY_REQUEST=1Gi",
                  "MEMORY_LIMIT=3Gi",
                  "IMAGE_STREAM_NAMESPACE=${project}"
                ))

                def backend = openshift.apply(openshift.process("-f",
                  "openshift/backend.deploy.yaml",
                  "NAME=${env_name}",
                  "HOST=${host}",
                  "NAMESPACE=${project}",
                  "ENVIRONMENT=STAGING",
                  "WALLY_VERSION=${git_tag}",
                  "API_VERSION=${API_VERSION}",
                  "REPLICAS=2"
                ))

                def gatekeeper = openshift.apply(openshift.process("-f",
                  "openshift/gatekeeper.deploy.yaml",
                  "NAME=${env_name}",
                  "HOST=${host}",
                  "NAMESPACE=${project}",
                  "ENVIRONMENT=STAGING",
                  "REPLICAS=2"
                ))
                
                echo "Deploying to a dev environment"

                // tag images into dev project.  This triggers re-deploy.
                openshift.tag("${TOOLS_PROJECT}/wally-web:${NAME}", "${project}/wally-web:${env_name}")
                openshift.tag("${TOOLS_PROJECT}/wally-api:${NAME}", "${project}/wally-api:${env_name}")

                // wait for any deployments to finish updating.
                frontend.narrow('dc').rollout().status()
                database.narrow('dc').rollout().status()
                backend.narrow('dc').rollout().status()
                gatekeeper.narrow('dc').rollout().status()

                // update GitHub deployment status.
                createDeploymentStatus(deployment, 'SUCCESS', host)
                echo "Successfully deployed"
              }
            }
          }
        }
      }
    }
    stage('Deploy to production') {
      when {
        allOf {
         tag "v*";
         expression { env.JOB_BASE_NAME == 'master' }
        }
      }
//       when {
//           expression { env.JOB_BASE_NAME == 'master' }
//       }
      steps {
        script {

          input "Deploy to production?"

          def project = PROD_PROJECT
          def env_name = "production"
          def host = "wally.pathfinder.gov.bc.ca"
          def ref = "refs/heads/master"
          openshift.withCluster() {
            openshift.withProject(project) {
              withStatus(env.STAGE_NAME) {

                // create deployment object at GitHub and give it a pending status.
                // this creates a notice on the pull request page indicating that a deployment
                // is pending.
                def deployment = createDeployment('production', ref)
                createDeploymentStatus(deployment, 'PENDING', host)

                // apply database service account.
                // this is a pre-requisite for the database statefulset.
                openshift.apply(openshift.process("-f",
                  "openshift/database.rolebinding.yaml",
                  "NAME=wally-psql",
                  "SUFFIX=-${env_name}"
                ))

                sleep(3)

                // apply frontend application template
                def frontend = openshift.apply(openshift.process("-f",
                  "openshift/frontend.deploy.yaml",
                  "NAME=${env_name}",
                  "HOST=${host}",
                  "NAMESPACE=${project}",
                  "REPLICAS=2"
                ))

                // apply database template
                def database = openshift.apply(openshift.process("-f",
                  "openshift/database.deploy.yaml",
                  "NAME=wally-psql",
                  "REPLICAS=3",
                  "SUFFIX=-${env_name}",
                  "PVC_SIZE=40Gi",
                  "CPU_REQUEST=500m",
                  "CPU_LIMIT='3'",
                  "MEMORY_REQUEST=1Gi",
                  "MEMORY_LIMIT=4Gi",
                  "IMAGE_STREAM_NAMESPACE=${project}"
                ))

                def backend = openshift.apply(openshift.process("-f",
                  "openshift/backend.deploy.yaml",
                  "NAME=${env_name}",
                  "HOST=${host}",
                  "NAMESPACE=${project}",
                  "ENVIRONMENT=PRODUCTION",
                  "WALLY_VERSION=${git_tag}",
                  "API_VERSION=${API_VERSION}",
                  "REPLICAS=2"
                ))

                def gatekeeper = openshift.apply(openshift.process("-f",
                  "openshift/gatekeeper.deploy.yaml",
                  "NAME=${env_name}",
                  "HOST=${host}",
                  "NAMESPACE=${project}",
                  "ENVIRONMENT=PRODUCTION",
                  "REPLICAS=2"
                ))
                
                echo "Deploying to a dev environment"

                // tag images into dev project.  This triggers re-deploy.
                openshift.tag("${TOOLS_PROJECT}/wally-web:${NAME}", "${project}/wally-web:${env_name}")
                openshift.tag("${TOOLS_PROJECT}/wally-api:${NAME}", "${project}/wally-api:${env_name}")

                // wait for any deployments to finish updating.
                frontend.narrow('dc').rollout().status()
                database.narrow('dc').rollout().status()
                backend.narrow('dc').rollout().status()
                gatekeeper.narrow('dc').rollout().status()

                // update GitHub deployment status.
                createDeploymentStatus(deployment, 'SUCCESS', host)
                echo "Successfully deployed"
              }
            }
          }
        }
      }
    }
  }
}
