pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'master', url: 'https://github.com/CAST11/MusicList_RelEnv.git'
            }
        }

        stage('Install dependencies') {
            steps {
                sh '''
                    echo "Python version:"
                    python3 --version

                    echo "Creating virtual env"
                    python3 -m venv venv

                    echo "Activating virtualenv"
                    . venv/bin/activate

                    echo "Upgrading pip"
                    pip install --upgrade pip

                    echo "Installing requirements"
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest --junitxml=results.xml || true
                '''
            }
            post {
                always {
                    junit 'results.xml'
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished'
        }
        failure {
            echo 'Tests failed!'
        }
    }
}