pipeline {
    agent any

    environment {
        DOCKER_HOST = 'sjc.vultrcr.com/dong3registry'
        IMAGE_NAME = "${DOCKER_HOST}/gene:latest"
    }

    stages {
        stage('Building Docker Image') {
            steps {
                cleanWs()
                // sh 'docker logout'
                checkout scm

                echo "Building ${env.JOB_NAME}..."
                withCredentials([
                    file(credentialsId: 'b5579978-8cbc-43d7-b62e-379ca2675dc4',
                        variable: 'SSL_PUB_KEY'),
                    file(credentialsId: '98cb51f5-281d-4fc0-a64c-05ab09e96346',
                        variable: 'SSL_PRIV_KEY'),
                ]) {
                    sh "docker build -t test:latest ."
                    // echo "docker build -t ${IMAGE_NAME} ."
                }
                echo "Built ${IMAGE_NAME} successfully!"

                // echo "Pushing ${IMAGE_NAME}..."

                // withCredentials([
                //     usernamePassword(credentialsId: '03b5e0b6-bfdc-46d7-bafc-a8b5bf8cec00',
                //         usernameVariable: 'DOCKER_USER',
                //         passwordVariable: 'DOCKER_PASS')
                // ]) {
                //     sh 'docker login https://sjc.vultrcr.com/dong3registry --username $DOCKER_USER --password $DOCKER_PASS'
                // }
            }
        }

        stage('Pushing') {
            steps {
                echo 'Pushing...'
                // sh "docker push ${IMAGE_NAME}"
                sh 'docker tag test:latest sjc.vultrce.com/dong3registry/test:latest'
                sh 'docker push sjc.vultrce.com/dong3registry/test:latest'
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
