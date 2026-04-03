pipeline {
    agent any

    options {
        disableConcurrentBuilds()
        timestamps()
    }

    environment {
        IMAGE_NAME = 'aceest-fitness'
        GITHUB_CREDENTIALS = 'github-token'   // Jenkins credential ID for GitHub PAT
        DOCKER_HUB_CREDENTIALS = 'dockerhub-creds' // Jenkins credential ID for Docker Hub
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'release-1.0',
                    url: 'https://github.com/2025ht66016-cell/my_learning_devops.git',
                    credentialsId: "${GITHUB_CREDENTIALS}"
            }
        }

        stage('Lint & Build Validation') {
            steps {
                sh '''
                    python3 -m compileall app.py src tests
                    ruff check app.py src tests
                '''
            }
        }

        stage('Unit Tests') {
            steps {
                sh '''
                    pytest --junitxml=pytest-report.xml
                '''
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} .'
            }
        }

        stage('Push to Docker Hub') {
            when {
                branch 'release-1.0'
            }
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', "${DOCKER_HUB_CREDENTIALS}") {
                        sh "docker tag ${IMAGE_NAME}:${BUILD_NUMBER} ${IMAGE_NAME}:latest"
                        sh "docker push ${IMAGE_NAME}:${BUILD_NUMBER}"
                        sh "docker push ${IMAGE_NAME}:latest"
                    }
                }
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, testResults: 'pytest-report.xml'
            cleanWs deleteDirs: true, disableDeferredWipeout: true
        }
        success {
            echo '✅ Build, tests, and push completed successfully!'
        }
        failure {
            echo '❌ Build failed or tests did not pass.'
        }
    }
}
