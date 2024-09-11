# Jenkins pipeline check 

# pipeline_template = """
# pipeline {
#     agent any
#     stages {
#         stage('Checkout Source Branch') {
#             steps {
#                 git branch: '%s', credentialsId: '%s', url: '%s'
#             }
#         }
#         stage('Create Pipeline') {
#             steps {
#                 script {
#                     // Placeholder for pipeline creation logic
#                 }
#             }
#         }
#     }
# }
# """

# Script to connect with AWS

# pipeline_template = """
# pipeline {
#     agent any
#     stages {
#         stage('Checkout Source Branch') {
#             steps {
#                 script {
#                     git branch: '%s', credentialsId: '%s', url: '%s'
#                 }
#             }
#         }
#         stage('Build Docker Image') {
#             steps {
#                 script {
#                     withCredentials([string(credentialsId: '%s', variable: 'DOCKER_CREDENTIALS')]) {
#                         sh "docker build -t %s ."
#                     }
#                 }
#             }
#         }
#         stage('Push Docker Image') {
#             steps {
#                 script {
#                     withCredentials([string(credentialsId: '%s', variable: 'DOCKER_CREDENTIALS')]) {
#                         sh "docker login -u $DOCKER_CREDENTIALS -p $DOCKER_CREDENTIALS"
#                         sh "docker push %s"
#                     }
#                 }
#             }
#         }
#         stage('Deploy To Amazon EKS') {
#             steps {
#                 withAWS(credentials: '%s', region: '%s') {
#                     sh 'aws eks update-kubeconfig --region %s --name %s'
#                     sh 'kubectl apply -f %s'
#                     sh 'kubectl apply -f %s'
#                     sh 'kubectl set image deployment/%s %s=%s --record'
#                 }
#             }
#         }
#     }
# }
# """

# Script to connect with Minikube

pipeline_template = """
pipeline {
    agent any
    stages {
        stage('Checkout Source Branch') {
            steps {
                script {
                    git branch: '%s', credentialsId: '%s', url: '%s'
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    withCredentials([string(credentialsId: '%s', variable: 'DOCKER_CREDENTIALS')]) {
                        sh "docker build -t %s ."
                    }
                }
            }
        }
        stage('Push Docker Image') {
            steps {
                script {
                    withCredentials([string(credentialsId: '%s', variable: 'DOCKER_CREDENTIALS')]) {
                        sh "docker login -u $DOCKER_CREDENTIALS -p $DOCKER_CREDENTIALS"
                        sh "docker push %s"
                    }
                }
            }
        }
        stage('Deploy To Minikube') {
            steps {
                script {
                    // Apply the deployment and service YAML files to Minikube
                    sh 'kubectl apply -f %s'
                    sh 'kubectl apply -f %s'
                    
                    // Update the image in the Minikube deployment
                    sh 'kubectl set image deployment/%s %s=%s --record'
                }
            }
        }
    }
}
"""

# pipeline_template = """
# pipeline {
#     agent any
#     stages {
#         stage('Checkout Source Branch') {
#             steps {
#                 script {
#                     git branch: '%s', credentialsId: '%s', url: '%s'
#                 }
#             }
#         }
#         stage('Build Docker Image') {
#             steps {
#                 script {
#                     withCredentials([string(credentialsId: '%s', variable: 'DOCKER_CREDENTIALS')]) {
#                         sh "docker build -t %s ."
#                     }
#                 }
#             }
#         }
#         stage('Push Docker Image') {
#             steps {
#                 script {
#                     withCredentials([string(credentialsId: '%s', variable: 'DOCKER_CREDENTIALS')]) {
#                         sh "docker login -u $DOCKER_HUB_USERNAME -p $DOCKER_HUB_PASSWORD"
#                         sh "docker push %s"
#                     }
#                 }
#             }
#         }
#         stage('Deploy To Minikube') {
#             steps {
#                 script {
#                     // Apply the deployment and service YAML files to Minikube
#                     sh 'kubectl apply -f %s'
#                     sh 'kubectl apply -f %s'
                    
#                     // Update the image in the Minikube deployment
#                     sh 'kubectl set image deployment/%s %s=%s --record'
#                 }
#             }
#         }
#     }
# }
# """


# pipeline_template = """
# pipeline {
#     agent any
#     stages {
#         stage('Checkout Source Branch') {
#             steps {
#                 script {
#                     git branch: '%s', credentialsId: '%s', url: '%s'
 
#                 }
#             }
#         }
#         stage('Build Docker Image') {
#             steps {
#                 script {
#                     withCredentials([string(credentialsId: '%s', variable: 'GIT_PWD')]) {
#                         sh "docker build --build-arg git_user=%s --build-arg pwd=$%s -t telldusorahi/locate-dashboard-api-dev:$BUILD_NUMBER ."
#                     }
#                 }
#             }
#         }
#     }
# }
# """
#         stage('Push Docker Image') {
#             steps {
#                 script {
#                     withCredentials([string(credentialsId: 'DOCKER_HUB_CREDENTIALS_NEBULA', variable: 'docker_hub_credentials_nebula')]) {
#                         sh "docker login -u telldusorahi -p $DOCKER_HUB_CREDENTIALS_NEBULA"
#                         sh "docker push telldusorahi/locate-dashboard-api-dev:$BUILD_NUMBER"
#                     }
#                 }
#             }
#         }
#         stage('Cleaning up') {
#             steps {
#                 script {
#                     sh "docker rmi telldusorahi/locate-dashboard-api-dev:$BUILD_NUMBER"
#                 }
#             }
#         }
#         stage("Deploy To Amazon EKS") {
#             steps {
#                 withAWS(credentials: 'AWS_CREDENTIALS_NEBULA', region: 'eu-north-1') {
#                     sh 'aws eks update-kubeconfig --region eu-north-1 --name nebula-staging-ekscluster'
#                     sh 'kubectl apply -f deployment.yaml'
#                     sh 'kubectl apply -f service.yaml'
#                     sh 'kubectl set image deployment/locate-dashboard-api-dev-deployment locate-dashboard-api-dev-service=telldusorahi/locate-dashboard-api-dev:$BUILD_NUMBER -n locate-ruleengine --record'
#                 }
#             }
#         }
#     }
# }
# """

# pipeline_template = """
# pipeline {
#     agent any
#     stages {
#         stage('Checkout Source Branch') {
#             steps {
#                 script {
#                     git branch: '%s', credentialsId: '%s', url: '%s'
#                     sh 'env'  // Print environment variables
#                     sh 'ls -la'  // List files in the workspace
#                 }
#             }
#         }
#         stage('Build Docker Image') {
#             steps {
#                 script {
#                     withCredentials([string(credentialsId: '%s', variable: 'DOCKER_CREDENTIALS')]) {
#                         sh "docker build -t %s ."
#                         sh 'ls -la /Users/aayushagrawal/.jenkins/workspace/TEST-JENKINS-16@tmp'  // Check tmp directory
#                     }
#                 }
#             }
#         }
#         stage('Push Docker Image') {
#             steps {
#                 script {
#                     withCredentials([string(credentialsId: '%s', variable: 'DOCKER_CREDENTIALS')]) {
#                         sh "docker login -u $DOCKER_HUB_USERNAME -p $DOCKER_HUB_PASSWORD"
#                         sh "docker push %s"
#                     }
#                 }
#             }
#         }
#         stage('Deploy To Minikube') {
#             steps {
#                 script {
#                     // Apply the deployment and service YAML files to Minikube
#                     sh 'kubectl apply -f %s'
#                     sh 'kubectl apply -f %s'
                    
#                     // Update the image in the Minikube deployment
#                     sh 'kubectl set image deployment/%s %s=%s --record'
#                 }
#             }
#         }
#     }
# }
# """


# pipeline_template = """
# pipeline {
#     agent any
#     environment {
#         TMPDIR = '/tmp/jenkins'  // Set temporary directory
#     }
#     stages {
#         stage('Clean Workspace') {
#             steps {
#                 deleteDir()  // Clean the workspace before starting
#             }
#         }
#         stage('Checkout Source Branch') {
#             steps {
#                 script {
#                     git branch: '%s', credentialsId: '%s', url: '%s'
#                     sh 'env'  // Print environment variables
#                     sh 'ls -la'  // List files in the workspace
#                 }
#             }
#         }
#         stage('Build Docker Image') {
#             steps {
#                 script {
#                     withCredentials([string(credentialsId: '%s', variable: 'DOCKER_CREDENTIALS')]) {
#                         sh 'docker --version'  // Check Docker version
#                         sh 'docker info'  // Check Docker daemon status
#                         sh "docker build --progress=plain -t %s ."
#                         sh 'ls -la /Users/aayushagrawal/.jenkins/workspace/TEST-JENKINS-16@tmp'  // Check tmp directory
#                     }
#                 }
#             }
#         }
#         stage('Push Docker Image') {
#             steps {
#                 script {
#                     withCredentials([string(credentialsId: '%s', variable: 'DOCKER_CREDENTIALS')]) {
#                         sh "docker login -u $DOCKER_HUB_USERNAME -p $DOCKER_HUB_PASSWORD"
#                         sh "docker push %s"
#                     }
#                 }
#             }
#         }
#         stage('Deploy To Minikube') {
#             steps {
#                 script {
#                     // Apply the deployment and service YAML files to Minikube
#                     sh 'kubectl apply -f %s'
#                     sh 'kubectl apply -f %s'
                    
#                     // Update the image in the Minikube deployment
#                     sh 'kubectl set image deployment/%s %s=%s --record'
#                 }
#             }
#         }
#     }
#     post {
#         always {
#             echo 'Cleaning up...'
#             deleteDir()  // Clean up workspace after build
#         }
#         success {
#             echo 'Build completed successfully!'
#         }
#         failure {
#             echo 'Build failed!'
#         }
#     }
# }
# """

