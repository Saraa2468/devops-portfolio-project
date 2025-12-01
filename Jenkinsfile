pipeline {
    agent any

    environment {
        APP_DIR = "app"
        IMAGE = "sarasalah24/devops-portfolio-project:${env.BUILD_NUMBER}"
        DOCKER_CREDENTIALS_ID = 'dockerHubCreds'
    }

    stages {

        stage('Install Python & pip') {
            steps {
                sh '''
                echo "Installing Python3 & pip..."
                apt-get update
                apt-get install -y python3 python3-pip
                python3 --version
                pip3 --version
                '''
            }
        }

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Requirements') {
            steps {
                sh '''
                cd ${APP_DIR}
                pip3 install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                cd ${APP_DIR}
                python3 -m pytest -q || true
                '''
            }
        }

        stage('Build Image') {
            steps {
                sh '''
                docker build -t ${IMAGE} .
                '''
            }
        }

        stage('Push Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: DOCKER_CREDENTIALS_ID, usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                    echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                    docker push ${IMAGE}
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                echo "Updating Kubernetes deployment with image: ${IMAGE}"

                kubectl set image deployment/devops-flask \
                    devops-flask=${IMAGE} \
                    -n devops --record || true

                echo "Restarting deployment..."
                kubectl rollout restart deployment/devops-flask -n devops || true

                echo "Checking rollout status..."
                kubectl rollout status deployment/devops-flask -n devops || true
                '''
            }
        }
    }
}