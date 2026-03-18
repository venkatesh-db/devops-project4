
pipeline {
    agent any

    tools {
        sonarScanner 'SonarScanner'
    }

    environment {
        IMAGE_NAME = "venkatesh/devop-project4"
        CONTAINER_NAME = "devop-project4-container"
        REPO_URL = "https://github.com/venkatesh-db/devop-project4.git"
        KUBE_CONFIG = credentials('kubeconfig')   // Jenkins credential (secret file)
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

                    # Update image in deployment dynamically
                    kubectl set image deployment/flask-app \
                    flask-app-container=$IMAGE_NAME --record || true

                    # Apply manifests (if first time)
                    kubectl apply -f k8s/deployment.yaml
                    kubectl apply -f k8s/service.yaml

                    # Verify rollout
                    kubectl rollout status deployment/flask-app
                    '''
                }
            }
        }

    }
}