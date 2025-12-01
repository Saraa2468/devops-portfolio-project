pipeline {
    agent any

    environment {
        IMAGE = "sarasalah24/devops-portfolio-project:${env.BUILD_NUMBER}"
        DOCKER_CREDENTIALS_ID = 'dockerHubCreds'
        VENV = ".venv"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Create Python venv') {
            steps {
                sh """
                    python3 --version
                    python3 -m venv $VENV
                    . $VENV/bin/activate
                    pip install --upgrade pip
                """
            }
        }

        stage('Install Requirements') {
            steps {
                sh """
                    . $VENV/bin/activate
                    pip install -r app/requirements.txt
                """
            }
        }

        stage('Test') {
            steps {
                sh """
                    . $VENV/bin/activate
                    pytest -q || true
                """
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
                    sh """
                        echo \$DOCKER_PASS | docker login -u \$DOCKER_USER --password-stdin
                        docker push $IMAGE
                    """
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