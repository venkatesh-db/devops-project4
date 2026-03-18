
pipeline {
    agent any

    environment {
        IMAGE_NAME = "venkatesh/devop-project4"
        CONTAINER_NAME = "devop-project4-container"
        REPO_URL = "https://github.com/venkatesh-db/devop-project4.git"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main', url: "${REPO_URL}"
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip3 install -r requirements.txt || true'
            }
        }

        stage('Check Sonar Scanner') {
            steps {
                sh 'which sonar-scanner'
                sh 'sonar-scanner --version'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube-Server') {
                    sh '''
                    sonar-scanner \
                    -Dsonar.projectKey=flask-app \
                    -Dsonar.sources=. \
                    -Dsonar.language=py
                    '''
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 2, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        stage('Docker Login & Push') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'docker-cred',
                    usernameVariable: 'USER',
                    passwordVariable: 'PASS'
                )]) {
                    sh '''
                    echo $PASS | docker login -u $USER --password-stdin
                    docker push $IMAGE_NAME
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
                    sh '''
                    export KUBECONFIG=$KUBECONFIG

                    kubectl set image deployment/flask-app \
                    flask-app-container=$IMAGE_NAME --record || true

                    kubectl apply -f k8s/deployment.yaml
                    kubectl apply -f k8s/service.yaml

                    kubectl rollout status deployment/flask-app
                    '''
                }
            }
        }

    }
}