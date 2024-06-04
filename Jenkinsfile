pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        GITHUB_CREDENTIALS = credentials('github-credentials') // Ajoutez cette ligne pour utiliser les informations d'identification GitHub
    }

    stages {
        stage('Clone repository') {
            steps {
                git branch: 'main', url: 'https://github.com/habob22/automatique.git', credentialsId: 'GITHUB_CREDENTIALS' // Ajout de la branche et des informations d'identification
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

    triggers {
        pollSCM('H/1 * * * *') // Ajout de la configuration pour le polling SCM
    }
}
