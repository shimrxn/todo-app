pipeline {
    agent any

    environment {
        FLASK_APP = 'app.py'
    }

    stages {
        stage('Build') {
            steps {
                echo 'Setting up Python and installing dependencies...'
                // Ensure Python and pip are available and create a virtual environment
                sh 'python3 --version'
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate && pip install --upgrade pip'
                sh '. venv/bin/activate && pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests...'
                // Activate virtual environment and run tests
                sh '. venv/bin/activate && pytest tests/'
            }
        }

        stage('Code Quality Analysis') {
            steps {
                echo 'Running code quality analysis...'
                // Activate virtual environment and run flake8 (or replace with SonarQube)
                sh '. venv/bin/activate && pip install flake8'
                sh '. venv/bin/activate && flake8 --exit-zero app.py'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying the application to the test environment...'
                // Deploy the application to the test environment
                sh '. venv/bin/activate && nohup python app.py &'
            }
        }

        stage('Release') {
            steps {
                echo 'Releasing the application to production...'
                // Deploy the application to the production environment
                sh '. venv/bin/activate && nohup python app.py &'
            }
        }

        stage('Monitoring and Alerting') {
            steps {
                echo 'Setting up monitoring and alerting...'
                // Simulate monitoring the application
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
