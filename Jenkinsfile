pipeline {
  environment {
    // Pipeline-wide settings - app name, repo
  }
  agent any
  stages {
    stage('Start pipeline') {
      steps {
        script {
          abortAllPreviousBuildInProgress(currentBuild)
          echo "!!!!"
        }
      }
    }
  }
}
