#!groovy

pipeline {
  agent any
  environment {
    GIT_REPO = "https://www.github.com/bcgov-c/wally.git"
    NAME = JOB_BASE_NAME.toLowerCase()
  }
  stages {
    stage('Build') {
      steps {
        script {
          abortAllPreviousBuildInProgress(currentBuild)
          openshift.withCluster() {
            openshift.withProject() {
              notifyStageStatus('Backend', 'PENDING')

              echo "Applying frontend template..."
              def bcWeb = openshift.process('-f',
                'openshift/frontend.build.yaml',
                "NAME=${NAME}",
                "GIT_REPO=${GIT_REPO}",
                "GIT_REF=pull/${CHANGE_ID}/head"
              )

              echo "Building ImageStream ${REPO_NAME}-backend..."
              openshift.apply(bcWeb).narrow('bc').startBuild('-w').logs('-f')
            }
          }
        }
      }
    }
  }
}
