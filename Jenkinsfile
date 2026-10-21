
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/tejagandham18/ecommerce-devops-platform.git'
            }
        }

        stage('Test') {
            steps {
                echo 'Running backend tests...'
                bat 'python -m pip install -r app\\backend\\requirements.txt'
                bat 'python -m pip install pytest'
                bat 'python -m pytest -v'
            }
        }
    }

    post {
        success {
            echo 'CI Pipeline completed successfully!'
        }
        failure {
            echo 'CI Pipeline failed. Check the console output.'
        }
    }
}
