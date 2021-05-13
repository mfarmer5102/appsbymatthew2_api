pipeline {
  agent any
  stages {

    // STARTING ////////////////////////////////////////////////////////////////////////////////////////////

    /* Print something to the console */
    stage('Say Hello') {
      steps {
        echo 'Hello world!'
      }
    }

    // BUILDING ////////////////////////////////////////////////////////////////////////////////////////////

    /* Build the Docker image */
    stage('Build') {
      steps {
        sh 'docker build -t apps-by-matthew-api:latest .'
      }
    }

    // PUSHING ////////////////////////////////////////////////////////////////////////////////////////////

    /* Push the image to Docker Hub */
    stage('Push to Docker Hub') {
      steps {
        script {
          docker.withRegistry('', 'Docker_Hub') {
            def customImage = docker.build("mfarmer5102/apps-by-matthew-api:latest")
            customImage.push()
          }
        }
      }
    }

    /* Push the image to Google Container Registry */
    stage('Push to GCR') {
      steps {
        script {
          docker.withRegistry('https://gcr.io', 'GCP_AppsByMatthew') {
            def customImage = docker.build("mfarmer5102/apps-by-matthew-api:latest")
            customImage.push()
          }
        }
      }
    }

  }
}