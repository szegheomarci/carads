pipeline {
    agent any

    stages {
        stage('Clean') {
            steps {
                sh "rm -rf test/processed/*.txt"
                sh "docker images -a"
            }
        }
        stage('Read project version') {
            steps {
                script {
                    def projectVersion = sh(script: 'git show HEAD:app/__version__.py | grep "__version__ =" | cut -d" " -f3 | tr -d \'"\n\'', returnStdout: true).trim()
                    echo "Project version: ${projectVersion}"
                    env.projectVersion = projectVersion
                    env.dockerId = "szegheomarci/dbloader:" + projectVersion + "-" + env.BUILD_NUMBER
                }
            }
        }/*
        stage('Run Pylint') {
            steps {
                script {
                    // Run Pylint on your Python files
                    def pylintReport = sh(script: 'pylint app/ || true', returnStdout: true).trim()

                    // Print the Pylint report
                    echo "Pylint Report:\n${pylintReport}"

                    // Optionally, you can set the build status based on the pylint score
                    def pylintScore = pylintReport.tokenize("\n").find { it.startsWith('Your final rating is') }
                    //if (pylintScore && pylintScore =~ /Your final rating is (\d+)/) {
                     //   def score = Integer.parseInt(RegExp.$1)
                        //currentBuild.result = score >= 8 ? 'SUCCESS' : 'FAILURE'
                     //   currentBuild.result = 'SUCCESS'
                    //}
                }
            }
        }*/
        stage('Build docker image') {
            steps {
                sh "docker build -t ${env.dockerId} ."
            }
        }
        stage('Create config file') {
            steps {
                withCredentials([
                    usernamePassword(credentialsId: 'testMySQL_address', usernameVariable: 'HOST', passwordVariable: 'PORT'),
                    usernamePassword(credentialsId: 'testMySQL_user', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD'),
                    string(credentialsId: 'testMySQL_dbname', variable: 'DBNAME')
                ]) {
                    sh "chmod +x test/createconfig.sh && test/createconfig.sh"
                }
            }
        }
        stage('Run the container') {
            options {
                timeout(time: 2, unit: 'MINUTES')
            }
            steps {
                    sh "chmod +x test/runcontainer.sh && test/runcontainer.sh '${projectVersion}' '${env.BUILD_NUMBER}'"
            }
        }
    }
    post {
        always {
            script {
                cleanWs()
                // Check if the Docker container is running
                /*def sContainerId = sh(script: 'docker ps | awk \'{print $1, $2}\' | grep \'${env.dockerId}\' | awk \'{print $1}\'')
                if (sContainerId.trim == "") {
                    echo "Stopping ${env.dockerId} container"
                    sh 'docker stop ${sContainerId}'
                } */
                def isContainerRunning = sh(script: "docker inspect -f {{.State.Running}} ${env.dockerId}", returnStatus: true) == 0

                // Stop the Docker container if it's running
                if (isContainerRunning) {
                    echo "Stopping ${env.dockerId} container"
                    sh "docker ps -q --filter ancestor=${env.dockerId} | xargs docker stop"
                }
                // Remove the Docker container
                echo "Deleting ${env.dockerId} container"
                sh 'docker ps -a'
                echo "sdf"
                sh "docker ps -a | grep '${env.dockerId}'"
                echo "dfgdsf"
               /* sh "docker ps -a | grep '${env.dockerId}' | awk '{print $1}' | xargs docker rm"
                echo "Deleting ${env.dockerId} image"
                sh "docker images | grep $(echo '${env.dockerId}' | sed 's|:|\\\s*|') | awk '{print $3}' | xargs docker rmi -f"*/
            }
        }
    }
}
