pipeline {
  agent none
  stages {
    stage('Build dev image') {
      agent {
          kubernetes {
              yaml '''
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: docker
    image: docker:19.03.1-dind
    securityContext:
      privileged: true
'''
              defaultContainer 'docker'
            }
        }
      environment {
        registry = "crpier/whisper"
        registryCredential = 'dockertoken'
      }
      steps {
        script {
          // If this is the first run for build, the image won't exist and pull command will fail
          sh "docker pull crpier/whisper:latest-dev || true"
          dockerImage = docker.build registry + ":latest-dev", "-f build/dockerfiles/Dockerfile --build-arg INSTALL_DEV=true --cache-from crpier/whisper:latest-dev ."
          docker.withRegistry('https://index.docker.io/v1/', registryCredential) {
            dockerImage.push()
          }
        }
      }
    }
    stage('Commit stage') {
      agent {
          kubernetes {
              yaml '''
spec:
  containers:
  - name: whisper-dev
    image: crpier/whisper:latest-dev
    imagePullPolicy: Always
    command:
    - sleep
    args:
    - 99d
              '''
              defaultContainer 'whisper-dev'
            }
      }
      stages {
        stage('Linting') {
          steps {
            sh "scripts/lint.sh"
          }
        }
        stage('Unit tests') {
          steps {
            // TODO: run tests for real
            sh ". app/tests/test_env.sh; PYTHONPATH=. pytest app/services/test/test_user_services.py::TestCreateUser::test_password_is_not_added_as_is"
          }
        }
      }
    }
    stage('Build image') {
      agent {
          kubernetes {
              yaml '''
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: docker
    image: docker:19.03.1-dind
    securityContext:
      privileged: true
'''
              defaultContainer 'docker'
            }
        }
      environment {
        registry = "crpier/whisper"
        registryCredential = 'dockertoken'
      }
      steps {
        script {
          // God I just hate jenkins. If this is what modern software development
          // looks like I'm writing my mcdonalds aplication form right now
          sh "docker pull crpier/whisper:latest || true"
          dockerImage = docker.build registry + ":latest", "-f build/dockerfiles/Dockerfile --build-arg INSTALL_DEV=true --cache-from crpier/whisper:latest ."
          docker.withRegistry('https://index.docker.io/v1/', registryCredential) {
            dockerImage.push()
          }
        }
      }
    }
    stage('Component tests') {
      agent {
          kubernetes {
              yaml '''
spec:
  containers:
  - name: whisper
    image: crpier/whisper:latest
    imagePullPolicy: Always
    command:
    - sleep
    args:
    - 99d
  - name: mariadbtest
    image: mariadb:10.7.1-focal
    imagePullPolicy: Always
    ports:
    - containerPort: 3306
    env:
    - name: MARIADB_ROOT_PASSWORD
      value: changethislol
    - name: MARIADB_DATABASE
      value: app
              '''
              defaultContainer 'whisper'
            }
        }
        steps{
          container("whisper") {
            sh ". app/tests/test_env.sh; ./prestart.sh"
            sh ". app/tests/test_env.sh; python app/initial_data.py"
            sh ". app/tests/test_env.sh; PYTHONPATH=. pytest -m 'component and not celery'"
          }
        }
      }
    stage('Deployment: Staging') {
      agent {
        label 'python-ci'
      }
      steps {
        // Workaround because kubectl doesn't do things in order and the 
        // namespace doesn't exist when the deployment is applied
        sh "kubectl apply -f deploy/kubernetes/namespace.yaml"
        sh "kubectl apply -f deploy/kubernetes/"
      }
    }
  }
}
