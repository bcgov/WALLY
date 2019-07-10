#!groovy

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
}
