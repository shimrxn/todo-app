pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Setting up Python and installing dependencies...'
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
                // Activate virtual environment and run pytest as a Python module
                sh '. venv/bin/activate && python -m pytest tests/'
            }
        }

        stage('Code Quality Analysis') {
            steps {
                echo 'Running code quality analysis...'
                sh '. venv/bin/activate && pip install flake8'
                sh '. venv/bin/activate && flake8 --exit-zero app.py'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying the application to the test environment...'
                sh 'fuser -k 5000/tcp || true'
                sh '. venv/bin/activate && gunicorn --bind 0.0.0.0:5001 app:app --daemon'
                sh 'curl http://localhost:5001 || echo "App did not start successfully"'
            }
        }

        stage('Release') {
            steps {
                echo 'Releasing the application to production...'
                sh 'fuser -k 5001/tcp || true'
                sh '. venv/bin/activate && gunicorn --bind 0.0.0.0:5001 app:app --daemon'
                sh 'curl http://localhost:5001 || echo "App did not start successfully"'
            }
        }

        stage('Monitoring and Alerting') {
            steps {
                echo 'Setting up monitoring and alerting...'
                sh 'curl http://localhost:5001 || echo "App is down!"'
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
