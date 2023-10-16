pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code'
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building...'
            }
        }
        stage('Test') {
            steps {
                echo 'Testing...'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying...'
            }
        }
    }
}