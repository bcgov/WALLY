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
        "Stage: ${name}",
        "${name}"
    )
}

// createDeployment gets a new deployment ID from GitHub.
// this lets us display notifications on GitHub when new environments
// are deployed (e.g. on a pull request page)
Long createDeployment (String suffix) {
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
                def bcWebTemplate = openshift.process('-f',
                  'openshift/frontend.build.yaml',
                  "NAME=${NAME}",
                  "GIT_REPO=${GIT_REPO}",
                  "GIT_REF=pull/${CHANGE_ID}/head"
                )

                def bcApiTemplate = openshift.process('-f',
                  'openshift/backend.build.yaml',
                  "NAME=${NAME}",
                  "GIT_REPO=${GIT_REPO}",
                  "GIT_REF=pull/${CHANGE_ID}/head"
                )

                def bcPdfTemplate = openshift.process('-f',
                  'openshift/reporting.build.yaml',
                  "NAME=${NAME}",
                  "GIT_REPO=${GIT_REPO}",
                  "GIT_REF=pull/${CHANGE_ID}/head"
                )

                timeout(10) {
                  echo "Starting build (frontend)"
                  def bcWeb = openshift.apply(bcWebTemplate).narrow('bc').startBuild()
                  def bcApi = openshift.apply(bcApiTemplate).narrow('bc').startBuild()
                  def bcPdf = openshift.apply(bcPdfTemplate).narrow('bc').startBuild()
                  def webBuilds = bcWeb.narrow('builds')
                  def apiBuilds = bcApi.narrow('builds')
                  def pdfBuilds = bcPdf.narrow('builds')

                  sleep(5)
                  webBuilds.untilEach(1) { // We want a minimum of 1 build
                      return it.object().status.phase == "Complete"
                  }
                  apiBuilds.untilEach(1) { // We want a minimum of 1 build
                      return it.object().status.phase == "Complete"
                  }
                  pdfBuilds.untilEach(1) { // We want a minimum of 1 build
                      return it.object().status.phase == "Complete"
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
      steps {
        script {
          def project = DEV_PROJECT
          def host = "wally-${NAME}.pathfinder.gov.bc.ca"
          openshift.withCluster() {
            openshift.withProject(project) {
              withStatus(env.STAGE_NAME) {

                // create deployment object at GitHub and give it a pending status.
                // this creates a notice on the pull request page indicating that a deployment
                // is pending.
                def deployment = createDeployment('DEV')
                createDeploymentStatus(deployment, 'PENDING', host)

                // apply frontend application template
                def frontend = openshift.apply(openshift.process("-f",
                  "openshift/frontend.deploy.yaml",
                  "NAME=${NAME}",
                  "HOST=${host}",
                  "NAMESPACE=${project}"
                ))

                // apply database template
                def database = openshift.apply(openshift.process("-f",
                  "openshift/database.deploy.yaml",
                  "NAME=wally-psql",
                  "REPLICAS=1",
                  "SUFFIX=-${NAME}",
                  "IMAGE_STREAM_NAMESPACE=${project}"
                ))

                def backend = openshift.apply(openshift.process("-f",
                  "openshift/backend.deploy.yaml",
                  "NAME=${NAME}",
                  "HOST=${host}",
                  "NAMESPACE=${project}"
                ))

                def reporting = openshift.apply(openshift.process("-f",
                  "openshift/reporting.deploy.yaml",
                  "NAME=${NAME}",
                  "HOST=${host}",
                  "NAMESPACE=${project}"
                ))

                echo "Deploying to a dev environment"

                // tag images into dev project.  This triggers re-deploy.
                openshift.tag("${TOOLS_PROJECT}/wally-web:${NAME}", "${DEV_PROJECT}/wally-web:${NAME}")
                openshift.tag("${TOOLS_PROJECT}/wally-api:${NAME}", "${DEV_PROJECT}/wally-api:${NAME}")

                // wait for any deployments to finish updating.
                frontend.narrow('dc').rollout().status()
                database.narrow('dc').rollout().status()
                backend.narrow('dc').rollout().status()
                reporting.narrow('dc').rollout().status()

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
