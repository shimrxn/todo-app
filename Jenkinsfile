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
                // Remove existing virtual environment (to ensure clean install)
                sh 'rm -rf venv'
                // Create a new virtual environment
                sh 'python3 -m venv venv'
                // Activate the virtual environment and install dependencies
                sh '. venv/bin/activate && pip install --upgrade pip'
                sh '. venv/bin/activate && pip install -r requirements.txt'
                // Install pytest
                sh '. venv/bin/activate && pip install pytest'
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests...'
                // Activate the virtual environment and run pytest
                sh 'export PYTHONPATH=$PWD && . venv/bin/activate && venv/bin/pytest tests/'
            }
        }

        stage('Code Quality Analysis') {
            steps {
                echo 'Running code quality analysis...'
                // Activate the virtual environment and run flake8
                sh '. venv/bin/activate && pip install flake8'
                sh '. venv/bin/activate && flake8 --exit-zero app.py'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying the application to the test environment...'
                // Activate virtual environment and run the app
                sh '. venv/bin/activate && nohup python app.py &'
            }
        }

        stage('Release') {
            steps {
                echo 'Releasing the application to production...'
                // Activate virtual environment and run the app for production
                sh '. venv/bin/activate && nohup python app.py &'
            }
        }

        stage('Monitoring and Alerting') {
            steps {
                echo 'Setting up monitoring and alerting...'
                // Check if the application is running
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
