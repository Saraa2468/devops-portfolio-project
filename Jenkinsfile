pipeline {
  agent any

  environment {
    PATH ="/opt/venv/bin:${env.PATH}"
    IMAGE = "sarasalah24/devops-portfolio-project:${env.BUILD_NUMBER}"
    DOCKER_CREDENTIALS_ID = 'dockerHubCreds' // set this in Jenkins credentials
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }
    stage('Test') {
      steps {
        sh 'python -m pytest -q || true'
      }
    }
    stage('Build Image') {
      steps {
        sh 'docker build -t $IMAGE .'
      }
    }
    stage('Push Image') {
      steps {
        withCredentials([usernamePassword(credentialsId: DOCKER_CREDENTIALS_ID, usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
          sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
          sh 'docker push $IMAGE'
        }
      }
    }
    stage('Deploy to K8s') {
      steps {
        // Assumes kubectl configured on Jenkins agent
        sh 'kubectl rollout restart deployment/devops-flask -n devops || true'
      }
    }
  }
}
