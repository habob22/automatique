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
    stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('sonar') {
                    script {
                        bat """
                            %SCANNER_HOME%/bin/sonar-scanner -Dsonar.projectName=automatique -Dsonar.projectKey=automatique -Dsonar.login=squ_2cdfa144e8ec8544328468efcac01738ff0b4478 \
                            -Dsonar.url=http://localhost:9000 \
                            -Dsonar.java.binaries=.
                        """
                    }
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
