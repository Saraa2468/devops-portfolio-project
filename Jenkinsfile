pipeline {
    agent {
        docker {
            image 'python:3.11'
            args '-u root:root -v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    environment {
        IMAGE = "sarasalah24/devops-portfolio-project:${env.BUILD_NUMBER}"
        DOCKER_CREDENTIALS_ID = 'dockerHubCreds'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Requirements') {
            steps {
                sh """
                    python -m pip install --upgrade pip
                    pip install -r app/requirements.txt
                """
            }
        }

        stage('Test') {
            steps {
                sh "pytest -q || true"
            }
        }

        stage('Build Image') {
            steps {
                sh "docker build -t $IMAGE ."
            }
        }

        stage('Push Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: DOCKER_CREDENTIALS_ID, usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh "echo \$DOCKER_PASS | docker login -u \$DOCKER_USER --password-stdin"
                    sh "docker push $IMAGE"
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh "kubectl rollout restart deployment/devops-flask -n devops || true"
            }
        }

    }
}