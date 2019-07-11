#!groovy
@Library('bcgov-library') _
import bcgov.GitHubHelper

// Notify stage status and pass to Jenkins-GitHub library
void notifyStageStatus (String name, String status) {
    GitHubHelper.createCommitStatus(
        this,
        GitHubHelper.getPullRequestLastCommitId(this),
        status,
        "${BUILD_URL}",
        "${name}",
        "Stage: ${name}"
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

Integer createDeployment (String suffix) {
    def ghDeploymentId = new GitHubHelper().createDeployment(
        this,
        "pull/${CHANGE_ID}/head",
        [
            'environment':"${suffix}",
            'task':"deploy:pull:${CHANGE_ID}"
        ]
    )
    echo "deployment ID: ${ghDeploymentId}"
    return ghDeploymentId

}

// Create deployment status and pass to Jenkins-GitHub library
void createDeploymentStatus (Integer ghDeploymentId, String status, String stageUrl) {
    echo "creating deployment status (${status})"
    new GitHubHelper().createDeploymentStatus(
        this,
        ghDeploymentId,
        "${status}",
        ['targetUrl':"https://${stageUrl}/gwells"]
    )

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
    GIT_REPO = "git@github.com:bcgov-c/wally.git"
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
          openshift.withCluster() {
            openshift.withProject() {
              withStatus(env.STAGE_NAME) {
                echo "Applying template (frontend)"
                def bcWeb = openshift.process('-f',
                  'openshift/frontend.build.yaml',
                  "NAME=${NAME}",
                  "GIT_REPO=${GIT_REPO}",
                  "GIT_REF=pull/${CHANGE_ID}/head"
                )

                echo "Starting build (frontend)"
                openshift.apply(bcWeb).narrow('bc').startBuild('-w').logs('-f')
                echo "Success! Build completed."
              }
            }
          }
        }
      }
    }
    stage('Deploy') {
      steps {
        script {
          def project = DEV_PROJECT
          def host = "wally-${NAME}.pathfinder.gov.bc.ca"
          openshift.withCluster() {
            openshift.withProject(project) {
              withStatus(env.STAGE_NAME) {

                echo 'Creating pending deployment at GitHub'
                def deployment = createDeployment('DEV')
                createDeploymentStatus(deployment, 'PENDING', host)
                echo 'done creating pending deployment'

                def frontend = openshift.apply(openshift.process("-f",
                  "openshift/frontend.deploy.yaml",
                  "NAME=${NAME}",
                  "HOST=${host}",
                  "NAMESPACE=${project}"
                ))

                def database = openshift.apply(openshift.process("-f",
                  "openshift/database.deploy.yaml",
                  "NAME=wally-psql",
                  "REPLICAS=1",
                  "SUFFIX=-${NAME}",
                  "IMAGE_STREAM_NAMESPACE=${project}"
                ))

                echo "Deploying to a dev environment"
                openshift.tag("${TOOLS_PROJECT}/wally-web:${NAME}", "${DEV_PROJECT}/wally-web:${NAME}")
                frontend.narrow('dc').rollout().status()
                database.narrow('dc').rollout().status()

                createDeploymentStatus(deployment, 'PENDING', host)
                echo "Successfully deployed"
              }
            }
          }
        }
      }
    }
  }
}
