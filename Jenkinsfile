pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        GITHUB_CREDENTIALS = credentials('github-credentials')
        SCANNER_HOME= tool 'sonar-scanner'

    }

    stages {
        stage('Clone repository') {
            steps {
                git branch: 'main', url: 'https://github.com/habob22/automatique.git', credentialsId: 'github-credentials'
            }
        }

        stage('SonarQube Analsyis') {
            steps {
                withSonarQubeEnv('sonar') {
                    sh ''' $SCANNER_HOME/bin/sonar-scanner -Dsonar.url=http://localhost:9000/ -Dsonar.login=squ_73d2d635d79f65e4511e6ac5eb4782ffdfc572dd -Dsonar.projectName=automatique \
                            -Dsonar.java.binaries=. \
                            -Dsonar.projectKey=automatique
                    '''
                }
            }
        }

        stage('Pull Docker image') {
            steps {
                script {
                    retry(3) {
                        withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', passwordVariable: 'DOCKERHUB_PASSWORD', usernameVariable: 'DOCKERHUB_USERNAME')]) {
                            bat """
                            echo %DOCKERHUB_PASSWORD% | docker login -u %DOCKERHUB_USERNAME% --password-stdin
                            docker pull habib7/automatic:latest
                            """
                        }
                    }
                }
            }
        }

        stage('Run Docker container') {
            steps {
                script {
                    def tempDir = pwd(tmp: true).replaceAll('\\\\', '/')
                    echo "Temp directory: ${tempDir}"

                    // Exécuter le conteneur Docker avec des commandes batch explicites
                    bat """
                    docker run -d --name automatic_container -v "${tempDir}:/workspace" -w /workspace habib7/automatic:latest python3.8 src/monitor_traffic.py
                    """
                }
            }
        }
    }

    triggers {
        pollSCM('H/1 * * * *')
    }
}
