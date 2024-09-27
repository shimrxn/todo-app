pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'todo-app:latest'
    }

    stages {
        // Setup Stage: Prepares environment and installs dependencies
        stage('Setup') {
            steps {
                echo 'Setting up environment and installing dependencies...'
                // Check Python version and setup virtual environment
                sh 'python3 --version'
                sh 'rm -rf venv'
                sh 'python3 -m venv venv'
                // Activate virtual environment and upgrade pip
                sh '. venv/bin/activate && pip install --upgrade pip'
                // Install all required dependencies including pytest
                sh '. venv/bin/activate && pip install -r requirements.txt'

                // Ensure pytest is installed
                echo 'Installing pytest...'
                sh '. venv/bin/activate && pip install pytest'

                // Validate pytest installation
                echo 'Validating pytest installation...'
                sh '. venv/bin/activate && pytest --version'
            }
        }

        // Build Stage: Creates a zip archive of the project
        stage('Build') {
            steps {
                echo 'Creating build artifact...'
                sh 'zip -r todo-app.zip *'
                archiveArtifacts artifacts: 'todo-app.zip'
            }
        }

        // Linting Stage: Runs flake8 to check code formatting
        stage('Linting') {
            steps {
                echo 'Running flake8 for linting...'
                sh '. venv/bin/activate && pip install flake8'
                sh '. venv/bin/activate && flake8 --max-line-length=120 > lint-report.txt || true'
                archiveArtifacts artifacts: 'lint-report.txt'
            }
        }

        // Static Code Analysis with pylint
        stage('Static Code Analysis') {
            steps {
                echo 'Running pylint...'
                sh '. venv/bin/activate && pip install pylint'
                sh '. venv/bin/activate && pylint app.py > pylint-report.txt || true'
                archiveArtifacts artifacts: 'pylint-report.txt'
            }
        }

        // Security Scanning with bandit
        stage('Security Scanning') {
            steps {
                echo 'Running bandit...'
                sh '. venv/bin/activate && pip install bandit'
                sh '. venv/bin/activate && bandit -r . > security-report.txt || true'
                archiveArtifacts artifacts: 'security-report.txt'
            }
        }

        // Test Stage using pytest
        stage('Test') {
            steps {
                echo 'Running tests...'
                // Activate virtual environment and run pytest
                sh '. venv/bin/activate && python -m pytest tests/'
            }
        }

        // Integration Testing Stage
        stage('Integration Testing') {
            steps {
                echo 'Running integration tests...'
                sh '. venv/bin/activate && python -m pytest integration_tests/'
            }
        }

        // Deploy Stage using Gunicorn
        stage('Deploy') {
            steps {
                echo 'Deploying on port 5000...'
                // Stop any app running on port 5000
                sh 'fuser -k 5000/tcp || true'
                // Deploy the app using Gunicorn
                sh '. venv/bin/activate && gunicorn --bind 0.0.0.0:5000 app:app --daemon --log-file gunicorn.log --access-logfile gunicorn-access.log'
                // Check if the app is running
                sh 'curl http://localhost:5000 || echo "App did not start successfully"'
            }
        }

        // Performance Testing Stage
        stage('Performance Testing') {
            steps {
                echo 'Running performance tests...'
                sh 'ab -n 100 -c 10 http://localhost:5000/'
            }
        }

        // Backup Stage
        stage('Backup') {
            steps {
                echo 'Backing up logs...'
                sh 'mkdir -p backups && cp gunicorn.log backups/gunicorn-$(date +%F).log'
                archiveArtifacts artifacts: 'backups/*.log'
            }
        }

        // Release Stage
        stage('Release') {
            steps {
                echo 'Releasing to production...'
                // Stop any app running on port 5000 and start a new one
                sh 'fuser -k 5000/tcp || true'
                // Deploy the app in production mode
                sh '. venv/bin/activate && gunicorn --bind 0.0.0.0:5000 app:app --daemon --log-file gunicorn-production.log --access-logfile gunicorn-production-access.log'
                // Check if the app is running in production
                sh 'curl http://localhost:5000 || echo "App did not start successfully"'
            }
        }

        // Monitoring and Alerting Stage
        stage('Monitoring and Alerting') {
            steps {
                echo 'Monitoring application...'
                // Ensure the app is still running
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
