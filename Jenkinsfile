pipeline {
    agent any

    stages {
        stage('Building Docker Image') {
            steps {
                cleanWs()
                checkout scm

                echo "Building ${env.JOB_NAME}..."
                withCredentials([
                    file(credentialsId: 'b5579978-8cbc-43d7-b62e-379ca2675dc4',
                        variable: 'SSL_PUB_KEY'),
                    file(credentialsId: '98cb51f5-281d-4fc0-a64c-05ab09e96346',
                        variable: 'SSL_PRIV_KEY'),
                ]) {
                    sh "docker build --build-arg SSL_PUB_KEY=${SSL_PUB_KEY} --build-arg SSL_PRIV_KEY=${SSL_PRIV_KEY} -t ${env.JOB_NAME} ."
                }

                echo "Built ${env.JOB_NAME} successfully!"
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying...'
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