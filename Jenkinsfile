#!groovy
@Library('bcgov-library') _

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

pipeline {
  agent any
  environment {
    GIT_REPO = "git@github.com:bcgov-c/wally.git"
    NAME = JOB_BASE_NAME.toLowerCase()
  }
  stages {
    stage('Build') {
      steps {
        script {
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
          openshift.withCluster() {
            openshift.withProject() {
              echo "Deploying!"
            }
          }
        }
      }
    }
  }
}
