pipeline {
    agent any

    environment {
        SONARQUBE_ENV = 'SonarQube'  // Ensure SonarQube is configured in Jenkins
        DOCKER_IMAGE = 'todo-app:latest'
    }

    stages {
        stage('Build') {
            steps {
                echo 'Building the Docker image...'
                // Ensure Docker is installed and build the image
                sh 'docker build -t ${DOCKER_IMAGE} .'
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests...'
                // Activate the virtual environment and run pytest
                sh 'docker run --rm ${DOCKER_IMAGE} sh -c "pytest tests/"'
            }
        }

        stage('Code Quality Analysis') {
            steps {
                echo 'Running SonarQube analysis...'
                // Run SonarQube scanner
                withSonarQubeEnv(SONARQUBE_ENV) {
                    sh 'sonar-scanner -Dsonar.projectKey=todo-app -Dsonar.sources=./ -Dsonar.python.version=3.8'
                }
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying the Docker container to test environment...'
                // Stop any running container and start a new one
                sh 'docker stop todo-app || true'
                sh 'docker run -d -p 5000:5000 --name todo-app ${DOCKER_IMAGE}'
                // Check if the app is running on port 5000
                sh 'curl http://localhost:5000 || echo "App did not start successfully"'
            }
        }

        stage('Release') {
            steps {
                echo 'Releasing to production with AWS CodeDeploy...'
                // Create a release with AWS CodeDeploy (you must configure AWS CLI and CodeDeploy in Jenkins)
                sh 'aws deploy create-deployment --application-name todo-app --deployment-group-name prod --github-location repository=shimrxn/todo-app,commitId=$GIT_COMMIT'
            }
        }

        stage('Monitoring and Alerting') {
            steps {
                echo 'Setting up Datadog monitoring...'
                // Check Datadog agent status (assuming Datadog is configured)
                sh 'datadog-agent status || echo "Datadog monitoring not available"'
                // Check if the app is still running
                sh 'curl http://localhost:5000 || echo "App is down!"'
            }
        }
    }

    post {
        always {
            echo 'Pipeline completed.'
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
