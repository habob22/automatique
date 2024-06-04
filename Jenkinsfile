pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
    }

    stages {
        stage('Clone repository') {
            steps {
                git 'https://github.com/habob22/automatique.git' // Utilisateur GitHub et nom du dépôt
            }
        }

        stage('Pull Docker image') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'DOCKERHUB_CREDENTIALS') {
                        docker.image('habib7/automatic:latest').pull() // Utilisateur Docker Hub et nom de l'image
                    }
                }
            }
        }

        stage('Run Docker container') {
            steps {
                script {
                    docker.image('habib7/automatic:latest').inside { // Utilisateur Docker Hub et nom de l'image
                        sh 'python3.8 src/monitor_traffic.py'
                    }
                }
            }
        }
    }
}
