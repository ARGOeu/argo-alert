pipeline {
    agent any
    options {
        checkoutToSubdirectory('argo-alert')
    }
    environment {
        PROJECT_DIR="argo-alert"
    }
    stages {
        stage ('Test Centos 7') {
            agent {
                docker {
                    image 'argo.registry:5000/python3'
                    args '-u jenkins:jenkins'
                }
            }
            steps {
                sh '''
                    cd ${WORKSPACE}/$PROJECT_DIR
                    pipenv install -r requirements.txt
                    pipenv run python setup.py install
                    pipenv run coverage run --source=./argoalert -m pytest
                    pipenv run coverage xml
                    pipenv run py.test ./ --junitxml=./junit.xml
                '''
                cobertura coberturaReportFile: '**/coverage.xml'
            }
        }
    }
    post {
        always {
            cleanWs()
        }
    }
}