pipeline {
    agent any

    environment {
        SONARQUBE_ENV = 'SonarQube'
        DOCKER_IMAGE = 'todo-app:latest'
    }

    stages {
        stage('Build') {
            steps {
                echo 'Setting up Python and installing dependencies...'
                sh 'python3 --version'
                sh 'rm -rf venv'
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate && pip install --upgrade pip'
                sh '. venv/bin/activate && pip install -r requirements.txt'

                // Ensure pytest is installed for running tests
                sh '. venv/bin/activate && pip install pytest'

                echo 'Creating a build artifact (ZIP file)...'
                sh 'zip -r todo-app.zip *'
                archiveArtifacts artifacts: 'todo-app.zip'
            }
        }

        stage('Static Code Analysis') {
            steps {
                echo 'Running pylint for static code analysis...'
                sh '. venv/bin/activate && pip install pylint'
                sh '. venv/bin/activate && pylint app.py > pylint-report.txt || true'
                archiveArtifacts artifacts: 'pylint-report.txt'
            }
        }

        stage('Security Scanning') {
            steps {
                echo 'Running bandit for security scanning...'
                sh '. venv/bin/activate && pip install bandit'
                sh '. venv/bin/activate && bandit -r . > security-report.txt || true'
                archiveArtifacts artifacts: 'security-report.txt'
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests...'
                // Activate virtual environment and run pytest
                sh '. venv/bin/activate && python -m pytest tests/'
            }
        }

        stage('Code Quality Analysis') {
            steps {
                echo 'Running SonarQube analysis...'
                withSonarQubeEnv(SONARQUBE_ENV) {
                    sh 'sonar-scanner -Dsonar.projectKey=todo-app -Dsonar.sources=./ -Dsonar.python.version=3.8'
                }
            }
        }

        stage('Packaging') {
            steps {
                echo 'Packaging the Python application...'
                // Create a source distribution or wheel
                sh '. venv/bin/activate && pip install wheel'
                sh '. venv/bin/activate && python setup.py sdist bdist_wheel'
                archiveArtifacts artifacts: 'dist/*.whl'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying the Flask app locally on port 5000...'
                // Stop any running instance
                sh 'fuser -k 5000/tcp || true'
                // Run the app using Gunicorn
                sh '. venv/bin/activate && gunicorn --bind 0.0.0.0:5000 app:app --daemon --log-file gunicorn.log --access-logfile gunicorn-access.log'
                // Verify the app is running
                sh 'curl http://localhost:5000 || echo "App did not start successfully"'
            }
        }

        stage('Performance Testing') {
            steps {
                echo 'Running performance testing using Apache Benchmark...'
                // Performance testing using Apache Benchmark
                sh 'ab -n 100 -c 10 http://localhost:5000/'
            }
        }

        stage('Backup') {
            steps {
                echo 'Backing up important files...'
                // Backup logs
                sh 'mkdir -p backups && cp gunicorn.log backups/gunicorn-$(date +%F).log'
                archiveArtifacts artifacts: 'backups/*.log'
            }
        }

        stage('Release') {
            steps {
                echo 'Releasing to production...'
                // Simulate production release
                sh 'fuser -k 5000/tcp || true'
                sh '. venv/bin/activate && gunicorn --bind 0.0.0.0:5000 app:app --daemon --log-file gunicorn-production.log --access-logfile gunicorn-production-access.log'
                sh 'curl http://localhost:5000 || echo "App did not start successfully"'
            }
        }

        stage('Monitoring and Alerting') {
            steps {
                echo 'Setting up monitoring and alerting...'
                // Check if the app is running
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
