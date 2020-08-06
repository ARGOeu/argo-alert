pipeline {
    agent any
    options {
        checkoutToSubdirectory('argo-alert')
    }
    environment {
        PROJECT_DIR="argo-alert"
    }
    stages {
        stage ('Test'){
            parallel {
                stage ('Test Centos 6') {
                    agent {
                        docker {
                            image 'argo.registry:5000/epel-6-ams'
                            args '-u jenkins:jenkins'
                        }
                    }
                    steps {
                        sh '''
                            cd ${WORKSPACE}/$PROJECT_DIR
                            pip install -r requirements.txt
                            python setup.py install
                            coverage run --source=./argoalert -m py.test
                            coverage xml
                            py.test ./ --junitxml=./junit.xml
                        '''
                        cobertura coberturaReportFile: '**/coverage.xml'
                    }
                }
                stage ('Test Centos 7') {
                    agent {
                        docker {
                            image 'argo.registry:5000/epel-7-ams'
                            args '-u jenkins:jenkins'
                        }
                    }
                    steps {
                        sh '''
                            cd ${WORKSPACE}/$PROJECT_DIR
                            pip install -r requirements.txt
                            python setup.py install
                            coverage run --source=./argoalert -m py.test
                            coverage xml
                            py.test ./ --junitxml=./junit.xml
                        '''
                        cobertura coberturaReportFile: '**/coverage.xml'
                    }
                }
            }
        }
    }
    post {
        always {
            cleanWs()
        }
    }
}