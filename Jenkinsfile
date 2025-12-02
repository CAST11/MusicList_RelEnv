pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                git branch: 'master',
                    url: 'https://github.com/CAST11/MusicList_RelEnv.git'
            }
        }

        stage('Install dependencies') {
            steps {
                bat """
                set PYTHON=C:\Users\dona_\AppData\Local\Microsoft\WindowsApps\python.exe
                "%PYTHON%" -m venv venv
                call venv\\Scripts\\activate
                "%PYTHON%" -m pip install --upgrade pip
                pip install -r requirements.txt
                """
            }
        }

        stage('Run Tests') {
            steps {
                bat """
                call venv\\Scripts\\activate
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
