pipeline {
    agent any
    environment {
        // Docker registry details
        registryName = 'unfydrepo'
        registryUrl = 'unfydrepo.azurecr.io'
        registryCredential = 'UnfydRepository'
        dockerImage = ''
    }

    stages {
        stage('Clone Repository') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'GitLab-User', usernameVariable: 'GITLAB_USER', passwordVariable: 'GITLAB_TOKEN')]) {
                        checkout([$class: 'GitSCM',
                            branches: [[name: '*/DEV']], // Replace with your branch if different
                            doGenerateSubmoduleConfigurations: false,
                            extensions: [],
                            userRemoteConfigs: [[
                                url: "https://${GITLAB_USER}:${GITLAB_TOKEN}@gitlab.unfyd.com/unfyd/v2/unfyd-channel-api/unfyd-facebook-app/unfyd-facebook-api.git"
                            ]]
                        ])
                    }
                }
            }
        }

        stage('navigate to backend and build image') {
            steps {
                    sh 'ls'
                    script {
                        dockerImage = docker.build("${registryName}/unfyd-facebook-api-lg")
                        docker.withRegistry("http://${registryUrl}", registryCredential) {
                            dockerImage.push("$BUILD_NUMBER")
                        }
                    }
            }
        }

       stage('deploy Admin app and service') {
                steps {
                    script {
                        def imageTag = sh(returnStdout: true, script: 'echo $BUILD_NUMBER').trim()
                        sh "sed -i 's/{{IMAGE_TAG}}/${imageTag}/' UNFYD-FACEBOOK-API.yaml"
                        withKubeConfig(caCertificate: '', clusterName: '', contextName: '', credentialsId: 'K8s-uat', namespace: '', restrictKubeConfigAccess: false, serverUrl: '') {
                        sh "kubectl apply -f UNFYD-FACEBOOK-API.yaml"
                        }
                    }
            }
        }   
    }
    post {
        success {
            // Clean up the workspace after a successful build
            cleanWs()

            // Send email notification upon successful build with attached logs
            emailext (
                subject: "Build Successful: ${currentBuild.fullDisplayName}",
                body: """
                   Congrats, Build ${currentBuild.fullDisplayName} was successful.

                    View the build details at ${env.BUILD_URL}
                    
                    For more details please check attached logs
                """,
                to: "pintup@unfyd.com,avinashk@unfyd.com,ivekanandr@unfyd.com,abhisheku@unfyd.com,rajany@smartconnectt.com,tejaswinim@unfyd.com",
                recipientProviders: [[$class: 'CulpritsRecipientProvider']],
                attachLog: true // Attach the build log to the email
            )
        }
    }
}