pipeline {
    agent any

    stages {
        stage('Clean') {
            steps {
                sh "ls -l"
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
            steps {
                sh "chmod +x test/runcontainer.sh && test/runcontainer.sh '${projectVersion}' '${env.BUILD_NUMBER}'"
            }
            timeout(time: 1, unit: 'MINUTES', failBuild: true)
        }
    }
    post {
        always {
            // Check if the Docker container is running
            def isContainerRunning = sh(script: 'docker inspect -f {{.State.Running}} ${env.dockerId}', returnStatus: true) == 0

            // Stop and remove the Docker container if it's running
            if (isContainerRunning) {
                sh 'docker stop ${env.dockerId}'
                sh 'docker rm ${env.dockerId}'
                sh 'docker ps'
                sh 'docker images -a'
            }
        }
    }
}
