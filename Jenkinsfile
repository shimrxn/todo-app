pipeline {
    agent any

    environment {
        FLASK_APP = 'app.py'
    }

    stages {
        stage('Build') {
            steps {
                echo 'Building the application...'
                // Install Python dependencies
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests...'
                // Run unit tests using pytest
                sh 'pytest tests/'
            }
        }

        stage('Code Quality Analysis') {
            steps {
                echo 'Running code quality analysis...'
                // Use flake8 for basic code linting (or replace with SonarQube configuration)
                sh 'pip install flake8'
                sh 'flake8 --exit-zero app.py'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying the application to the test environment...'
                // Simulate deployment by running the app (this can be replaced with real deployment)
                sh 'nohup python app.py &'
            }
        }

        stage('Release') {
            steps {
                echo 'Releasing the application to production...'
                // Simulate production deployment (adapt this for real-world environments)
                sh 'nohup python app.py &'
            }
        }

        stage('Monitoring and Alerting') {
            steps {
                echo 'Setting up monitoring and alerting...'
                // Example of checking if the app is running (this could be integrated with New Relic, Datadog)
                sh 'curl http://localhost:5000 || echo "App is down!"'
            }
        }
    }

    post {
        always {
            echo 'Pipeline completed.'
            // Cleanup actions if necessary
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}