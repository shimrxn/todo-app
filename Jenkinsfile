pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'todo-app:latest'
    }

    stages {
        // Build Stage
        stage('Build') {
            steps {
                echo 'Setting up environment and installing dependencies...'
                sh 'python3 --version'
                sh 'rm -rf venv'
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate && pip install --upgrade pip'
                sh '. venv/bin/activate && pip install -r requirements.txt'
                sh '. venv/bin/activate && pip install pytest'

                echo 'Creating build artifact...'
                sh 'zip -r todo-app.zip *'
                archiveArtifacts artifacts: 'todo-app.zip'
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
                sh '. venv/bin/activate && python -m pytest tests/'
            }
        }

        // Packaging the Python application
        stage('Packaging') {
            steps {
                echo 'Packaging application...'
                sh '. venv/bin/activate && pip install wheel'
                sh '. venv/bin/activate && python setup.py sdist bdist_wheel'
                archiveArtifacts artifacts: 'dist/*.whl'
            }
        }

        // Deploy Stage using Gunicorn
        stage('Deploy') {
            steps {
                echo 'Deploying on port 5000...'
                sh 'fuser -k 5000/tcp || true'
                sh '. venv/bin/activate && gunicorn --bind 0.0.0.0:5000 app:app --daemon --log-file gunicorn.log --access-logfile gunicorn-access.log'
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
                sh 'fuser -k 5000/tcp || true'
                sh '. venv/bin/activate && gunicorn --bind 0.0.0.0:5000 app:app --daemon --log-file gunicorn-production.log --access-logfile gunicorn-production-access.log'
                sh 'curl http://localhost:5000 || echo "App did not start successfully"'
            }
        }

        // Monitoring and Alerting Stage
        stage('Monitoring and Alerting') {
            steps {
                echo 'Monitoring application...'
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
