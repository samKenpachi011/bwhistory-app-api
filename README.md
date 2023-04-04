# Botswana History App API

## Objectives of this project
- To create api endpoint for the history of Botswana
- To document browsable api's using swagger

## Technologies
- Python
- Django ( admin site, ORM, url mappings)
- Django Rest
- PostgreSQL
- Docker
- Swagger

## Project Structure
- app -> holds all application code
- app/core -> code shared between mulitple apps
- app/user -> user related code
- app/history -> history related code
- requirements.txt -> for the application/production
- requirements.dev.text -> for local development

## Project Management
1. ### Test Driven Development
- A development practice to write test for functionalities before implementation

2. ### Pre-Installs/Configuration
    - Vs-Code / any IDE
    - GIT
    - Set up Docker and Docker-Compose
    - Setup linting

3. ### Testing

4. ### Linking the Githup repo to DockerHub
5. ### Adding a Docker file and dockerignore
**Why Docker**
- Helps to capture all dependencies as code which leads to consistent development and production environments
- [Docker Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
> A .dockerignore is a configuration file that describes files and directories that you want to exclude when building a Docker image.
- [Read more on Docker Ignore 1](https://www.geeksforgeeks.org/how-to-use-a-dockerignore-file/)
- [Read more on Docker Ignore 2](https://shisho.dev/blog/posts/how-to-use-dockerignore/)

**Docker file Description**
| Syntax | Description |
| ----------- | ----------- |
| FROM python:3.9-alpine3.13 | Defining the base image |
| ENV PYTHONUNBUFFERED 1 | To print outputs from the running application to the console |
| COPY ./source /destination | Copy local files to the directory specified in the container |
| WORKDIR /dir | Set the working directory as the default directory to run all commands from |
| EXPOSE <port> | Expose the specified port on the container to our machine |
| RUN | We are using a format to allow us to run multiple commands e.g installing requirements, adding a user to the container |
| ENV PATH="<path>:$PATH" | Adding our executables path to the system path |
| USER <user> | Setting the user inside the container |


**Docker Compose file Description**
- [DockerCompose Overview](https://docs.docker.com/compose/)
- [DockerCompose features](https://docs.docker.com/compose/features-uses/)

| Syntax | Description |
| ----------- | ----------- |
| services | Define services that will run containers or any job |
| build: context: .| Builds the docker file inside the current directory |
| ports: | Specify port mappings such that we connect port 8000 on our local machine to port 8000 inside the container |
| volumes: - ./app:/app | Map the local app directory to sync with the running container files |
| command: >
 `sh -c "python manage.py runserver 0.0.0.0:8000"` | Command to run the service which can be overridden from the terminal |

## Steps
- Create the neccessary docker and docker-compose files
- Add requirements files and create the app directory
- run `docker build .` to build the docker image
- run `docker-compose build` to use docker compose to build and tag the image


## Contributions
- After cloning the repo change to the dev branch and create pull requests from there.
-- git branch -M dev





