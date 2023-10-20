pipeline {
    agent any

    stages {
        stage('Preparation') {
            steps {
                echo 'Preparing...'
                echo 'Cleaning workspace...'
                cleanWs()
                script {
                    sh 'docker-compose down || true'
                    sh 'docker rmi gene:latest || true'
                }
            }
        }

        stage('Checkout SCM') {
            steps {
                echo 'Checking out SCM...'
                checkout scm
                echo 'Checked out SCM successfully!'
            }
        }

        stage('Building Docker Image') {
            steps {
                echo "Building ${env.JOB_NAME}..."
                withCredentials([
                    file(credentialsId: 'b5579978-8cbc-43d7-b62e-379ca2675dc4',
                        variable: 'SSL_PUB_KEY_PATH'),
                    file(credentialsId: '98cb51f5-281d-4fc0-a64c-05ab09e96346',
                        variable: 'SSL_PRIV_KEY_PATH'),
                ]) {
                    sh "ls -alh"
                    sh "pwd"
                    sh "cp '${SSL_PUB_KEY_PATH}' ."
                    sh "cp '${SSL_PRIV_KEY_PATH}' ."
                    sh 'docker build -t gene:latest .'
                }
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying...'
                sh 'docker-compose up -d'
            }
        }
    }
    post {
        always {
            cleanWs(cleanWhenNotBuilt: false,
                    deleteDirs: true,
                    disableDeferredWipeout: true,
                    notFailBuild: true,
                    patterns: [[pattern: '.gitignore', type: 'INCLUDE'],
                                [pattern: '*.pem', type: 'INCLUDE'],
                                [pattern: '.propsfile', type: 'EXCLUDE']])
        }
    }
}
