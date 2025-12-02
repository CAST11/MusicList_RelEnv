pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/TU_USUARIO/MusicList.git'
            }
        }

        stage('Install dependencies') {
            steps {
                sh """
                python -m venv venv
                source venv/bin/activate
                pip install -r requirements.txt
                """
            }
        }

        stage('Run Tests') {
            steps {
                sh """
                source venv/bin/activate
                pytest --junitxml=test-results.xml
                """
            }
        }

        stage('Publish Results') {
            steps {
                junit 'test-results.xml'
            }
        }
    }

    post {
        always {
            echo "Pipeline finished"
        }
        success {
            echo "Tests passed!"
        }
        failure {
            echo "Tests failed!"
        }
    }
}


