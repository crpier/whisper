# backend-boilerplate
Boilerplate for RESTful API written in python3.7 using FastAPI, leveraging MariaDB for storage, Celery for background tasks and HashiCorp Vault for secrets management.
Deployment is done with a Jenkins pipeline and the artifacts are Docker containers.
Made for the infrastructure setup in https://github.com/crpier/subsistence_infrastructure 

## Usage
Just create a new repository using this one as a template.

### TODO list
- Make the docker image slimmer with multi stage builds or smth
- Add pre-commit maybe
- Choose output port via config
