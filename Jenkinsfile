pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'todo-app:latest'
    }

    stages {
        // Setup Stage: Prepares the environment by installing dependencies and pytest
        stage('Setup') {
            steps {
                echo 'Setting up environment and installing dependencies...'
                // Ensure Python and pip are available
                sh 'python3 --version'
                // Remove existing virtual environment and create a new one
                sh 'rm -rf venv'
                sh 'python3 -m venv venv'
                // Activate virtual environment and install dependencies from requirements.txt
                sh '. venv/bin/activate && pip install --upgrade pip'
                sh '. venv/bin/activate && pip install -r requirements.txt'
                // Install pytest for testing
                echo 'Installing pytest...'
                sh '. venv/bin/activate && pip install pytest'
                // Verify pytest installation
                echo 'Checking pytest installation...'
                sh '. venv/bin/activate && pytest --version'
            }
        }

        // Build Stage: Creates a zip archive of the project as a build artifact
        stage('Build') {
            steps {
                echo 'Creating build artifact...'
                sh 'zip -r todo-app.zip *'
                archiveArtifacts artifacts: 'todo-app.zip'
            }
        }

        // Linting Stage: Runs flake8 to check code formatting and syntax issues
        stage('Linting') {
            steps {
                echo 'Running flake8 for linting...'
                sh '. venv/bin/activate && pip install flake8'
                sh '. venv/bin/activate && flake8 --max-line-length=120 > lint-report.txt || true'
                archiveArtifacts artifacts: 'lint-report.txt'
            }
        }

        // Static Code Analysis: Uses pylint to identify code quality issues
        stage('Static Code Analysis') {
            steps {
                echo 'Running pylint...'
                sh '. venv/bin/activate && pip install pylint'
                sh '. venv/bin/activate && pylint app.py > pylint-report.txt || true'
                archiveArtifacts artifacts: 'pylint-report.txt'
            }
        }

        // Security Scanning: Uses bandit to perform security checks on the code
        stage('Security Scanning') {
            steps {
                echo 'Running bandit...'
                sh '. venv/bin/activate && pip install bandit'
                sh '. venv/bin/activate && bandit -r . > security-report.txt || true'
                archiveArtifacts artifacts: 'security-report.txt'
            }
        }

        // Test Stage: Runs unit tests using pytest
        stage('Test') {
            steps {
                echo 'Running tests...'
                sh '. venv/bin/activate && python -m pytest tests/'
            }
        }

        // Integration Testing Stage: Runs integration tests (modify based on your tests)
        stage('Integration Testing') {
            steps {
                echo 'Running integration tests...'
                sh '. venv/bin/activate && python -m pytest integration_tests/'
            }
        }

        // Deploy Stage: Deploys the app using Gunicorn on port 5000
        stage('Deploy') {
            steps {
                echo 'Deploying on port 5000...'
                // Kill any process using port 5000 and deploy the app
                sh 'fuser -k 5000/tcp || true'
                sh '. venv/bin/activate && gunicorn --bind 0.0.0.0:5000 app:app --daemon --log-file gunicorn.log --access-logfile gunicorn-access.log'
                // Check if the app is running
                sh 'curl http://localhost:5000 || echo "App did not start successfully"'
            }
        }

        // Performance Testing Stage: Runs performance tests using Apache Benchmark (ab)
        stage('Performance Testing') {
            steps {
                echo 'Running performance tests...'
                sh 'ab -n 100 -c 10 http://localhost:5000/'
            }
        }

        // Backup Stage: Backs up application logs for future reference
        stage('Backup') {
            steps {
                echo 'Backing up logs...'
                sh 'mkdir -p backups && cp gunicorn.log backups/gunicorn-$(date +%F).log'
                archiveArtifacts artifacts: 'backups/*.log'
            }
        }

        // Release Stage: Re-deploys the app to production mode using Gunicorn
        stage('Release') {
            steps {
                echo 'Releasing to production...'
                // Kill any process on port 5000 and restart the app in production mode
                sh 'fuser -k 5000/tcp || true'
                sh '. venv/bin/activate && gunicorn --bind 0.0.0.0:5000 app:app --daemon --log-file gunicorn-production.log --access-logfile gunicorn-production-access.log'
                // Check if the app is running in production mode
                sh 'curl http://localhost:5000 || echo "App did not start successfully"'
            }
        }

        // Monitoring and Alerting Stage: Ensures the app is running by sending a request
        stage('Monitoring and Alerting') {
            steps {
                echo 'Monitoring application...'
                // Check if the app is up and running
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
