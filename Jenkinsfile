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
                sh 'docker logout'
                checkout scm

                echo "Building ${env.JOB_NAME}..."
                withCredentials([
                    file(credentialsId: '69cedf75-a5fe-4137-96a8-e7f6ac521635',
                        variable: 'SSL_PUB_KEY'),
                    file(credentialsId: '562d6d39-2a41-48aa-93be-8d264753fba7',
                        variable: 'SSL_PRIV_KEY'),
                ]) {
                    echo "building"
                    // echo "docker build -t ${IMAGE_NAME} ."
                }
                echo "Built ${IMAGE_NAME} successfully!"

                // echo "Pushing ${IMAGE_NAME}..."

                // echo 'Pushing...'
                // // sh "docker push ${IMAGE_NAME}"
                // sh 'docker tag test:latest sjc.vultrce.com/dong3registry/test:latest'
                // sh 'docker push sjc.vultrce.com/dong3registry/test:latest'

                withCredentials([
                    usernamePassword(credentialsId: 'vultr_dong3_registry',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS')
                ]) {
                    sh 'docker login https://sjc.vultrcr.com:5000/dong3registry --username $DOCKER_USER --password $DOCKER_PASS'
                }
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
