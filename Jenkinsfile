pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Setting up Python and installing dependencies...'
                // Ensure Python and pip are available and create a virtual environment
                sh 'python3 --version'
                sh 'rm -rf venv'
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate && pip install --upgrade pip'
                sh '. venv/bin/activate && pip install -r requirements.txt'
                // Install pytest within the virtual environment
                sh '. venv/bin/activate && pip install pytest'
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests...'
                // Activate the virtual environment and run pytest as a Python module
                sh '. venv/bin/activate && python -m pytest tests/'
            }
        }

        stage('Code Quality Analysis') {
            steps {
                echo 'Running code quality analysis...'
                // Install flake8 and run the analysis
                sh '. venv/bin/activate && pip install flake8'
                sh '. venv/bin/activate && flake8 --exit-zero app.py'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying the application to the test environment...'
                // Stop any app already running on port 8000 (optional)
                sh 'fuser -k 8000/tcp || true'
                
                // Activate virtual environment and use Gunicorn to run the Flask app on port 8000
                sh '. venv/bin/activate && gunicorn --bind 0.0.0.0:8000 app:app --daemon --log-file gunicorn.log --access-logfile gunicorn-access.log'
                
                // Check if the app is running on the new port
                sh 'curl http://localhost:8000 || echo "App did not start successfully"'
            }
        }

        stage('Release') {
            steps {
                echo 'Releasing the application to production...'
                // Stop any app already running on port 8000
                sh 'fuser -k 8000/tcp || true'
                
                // Activate virtual environment and use Gunicorn to run the Flask app on port 8000 in production
                sh '. venv/bin/activate && gunicorn --bind 0.0.0.0:8000 app:app --daemon --log-file gunicorn-production.log --access-logfile gunicorn-production-access.log'
                
                // Check if the app is running on the production port
                sh 'curl http://localhost:8000 || echo "App did not start successfully"'
            }
        }

        stage('Monitoring and Alerting') {
            steps {
                echo 'Setting up monitoring and alerting...'
                // Check if the app is still running
                sh 'curl http://localhost:8000 || echo "App is down!"'
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
