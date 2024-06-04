pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        GITHUB_CREDENTIALS = credentials('github-credentials')
    }

    stages {
        stage('Clone repository') {
            steps {
                git branch: 'main', url: 'https://github.com/habob22/automatique.git', credentialsId: 'github-credentials'
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
                            docker pull habib7/bandit_image:latest
                            docker pull habib7/flake8_image:latest
                            docker pull habib7/trivy_image:latest
                            """
                        }
                    }
                }
            }
        }

        stage('Run Bandit') {
            steps {
                script {
                    bat """
                    docker run -d --name bandit_container -v %CD%:/app habib7/bandit_image:latest bandit -r /app/src -f json -o /app/bandit_report.json
                    """
                }
            }
        }

        stage('Run Flake8') {
            steps {
                script {
                    bat """
                    docker run -d --name flake8_container -v %CD%:/app habib7/flake8_image:latest flake8 /app/src --format=json --output-file=/app/flake8_report.json
                    """
                }
            }
        }

        stage('Run Trivy') {
            steps {
                script {
                    bat """
                    docker run -d --name trivy_container -v /var/run/docker.sock:/var/run/docker.sock -v %CD%:/app habib7/trivy_image:latest image --format json -o /app/trivy_report.json habib7/automatic:latest
                    """
                }
            }
        }

        stage('Convert Reports to HTML') {
            steps {
                script {
                    bat """
                    docker run -v %CD%:/app --name bandit_html_converter python:3.8-slim bash -c "pip install json2html && python -c \\"import json; from json2html import *; print(json2html.convert(json = json.load(open('/app/bandit_report.json'))))\\" > /app/bandit_report.html"
                    docker run -v %CD%:/app --name flake8_html_converter python:3.8-slim bash -c "pip install json2html && python -c \\"import json; from json2html import *; print(json2html.convert(json = json.load(open('/app/flake8_report.json'))))\\" > /app/flake8_report.html"
                    docker run -v %CD%:/app --name trivy_html_converter python:3.8-slim bash -c "pip install json2html && python -c \\"import json; from json2html import *; print(json2html.convert(json = json.load(open('/app/trivy_report.json'))))\\" > /app/trivy_report.html"
                    """
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
                    docker run -d --network host --name automatic_container -v "${tempDir}:/workspace" -w /workspace habib7/automatic:latest python3.8 src/monitor_traffic.py
                    """
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'bandit_report.html, flake8_report.html, trivy_report.html', allowEmptyArchive: true

            publishHTML(target: [
                reportDir: '',
                reportFiles: 'bandit_report.html,flake8_report.html,trivy_report.html',
                reportName: 'Security and Code Quality Reports',
                keepAll: true,
                alwaysLinkToLastBuild: true,
                allowMissing: true
            ])
        }
    }

    triggers {
        pollSCM('H/1 * * * *')
    }
}
