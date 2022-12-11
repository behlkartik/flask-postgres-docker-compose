pipeline{
    agent { docker { image 'python:3.10.7-alpine' } }
    stages{
        stage("build"){
            steps{
            echo 'Building the application....'
            sh 'python --version'
            }
        }
        stage("test"){
            steps{
            echo 'Testing the application....'
            sh 'pwd'
            }
        }
        stage("deploy"){
            steps{
            echo 'Deploying the application....'
            sh 'pwd'
            }
        }
    }
}