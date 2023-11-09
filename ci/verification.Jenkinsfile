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
                    def projectVersion = sh(script: 'git show HEAD:src/__version__.py | grep "__version__ =" | cut -d" " -f3 | tr -d \'"\n\'', returnStdout: true).trim()
                    echo "Project version: ${projectVersion}"
                    env.projectVersion = projectVersion
                }
            }
        }
        stage('Run Pylint') {
            steps {
                script {
                    // Run Pylint on your Python files
                    def pylintReport = sh(script: 'pylint src/ || true', returnStdout: true).trim()

                    // Print the Pylint report
                    echo "Pylint Report:\n${pylintReport}"

                    // Optionally, you can set the build status based on the pylint score
                    def pylintScore = pylintReport.tokenize("\n").find { it.startsWith('Your final rating is') }
                    //if (pylintScore && pylintScore =~ /Your final rating is (\d+)/) {
                     //   def score = Integer.parseInt(RegExp.$1)
                        //currentBuild.result = score >= 8 ? 'SUCCESS' : 'FAILURE'
                     //   currentBuild.result = 'SUCCESS'
                    //}
                    echo "move on"
                }
            }
        }
        stage('Build docker image') {
            steps {
                echo "docker version: ${projectVersion}-${env.BUILD_NUMBER}"
                sh "docker build -t szegheomarci/dbloader:${projectVersion}-${env.BUILD_NUMBER} ."
            }
        }
        stage('Create config file') {
            steps {
                withCredentials([
                    usernamePassword(credentialsId: 'testMySQL_address', usernameVariable: 'HOST', passwordVariable: 'PORT'),
                    usernamePassword(credentialsId: 'testMySQL_user', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD'),
                    string(credentialsId: 'testMySQL_dbname', variable: 'DBNAME')
                ]) {
                    sh """
                        chmod +x test/createconfig.sh && \
                        test/createconfig.sh '${HOST}' '${PORT}' '${USERNAME}' '${PASSWORD}' '${DBNAME}'
                    """
                }
            }
        }
    }
}
