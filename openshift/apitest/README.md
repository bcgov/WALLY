# apitest Jenkins agent

This folder contains a Dockerfile for running `apitest` in Jenkins.  The resulting image can be run as a Jenkins agent as part of a pipeline run.

Example:
```groovy
    stage('API tests') {
      steps {
        script {
          def host = "wally-${NAME}.pathfinder.gov.bc.ca"
          openshift.withCluster() {
            openshift.withProject(TOOLS_PROJECT) {
              withStatus(env.STAGE_NAME) {
                podTemplate(
                    label: "apitest-${NAME}",
                    name: "apitest-${NAME}",
                    serviceAccount: 'jenkins',
                    cloud: 'openshift',
                    activeDeadlineSeconds: 1800,
                    containers: [
                        containerTemplate(
                            name: 'jnlp',
                            image: 'docker-registry.default.svc:5000/bfpeyx-tools/apitest',
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
                                )
                            ]
                        )
                    ]
                ) {
                    node("apitest-${NAME}") {
                        checkout scm
                        dir('backend/api-tests') {
                            try {
                                sh """
                                  apitest -f hydat.apitest.yaml
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
```