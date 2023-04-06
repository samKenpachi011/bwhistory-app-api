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
    - Configure Github actions

3. ### Testing
    - We use the Django test suite and set tests per Django app

    **Steps**
    - Import test classes either SimpleTestCase(no database) or TestCase(database)
    [Django Testing Tools](https://docs.djangoproject.com/en/4.1/topics/testing/tools/)

    - Import objects to test
    - Define test class
    - Add test method that will fail
    - Setup inputs
    - Execute code and check failing output

    **Useful Links**
    - [Unit test](https://docs.python.org/3/library/unittest.html)
    - [Unit test example 1](https://www.digitalocean.com/community/tutorials/python-unittest-unit-test-example)
    - [Python testing](https://realpython.com/python-testing/)
    - [API Testing Guide](https://www.django-rest-framework.org/api-guide/testing/)
    - [Testing Best Practices](https://realpython.com/testing-in-django-part-1-best-practices-and-examples/)


    **Running tests**
    | Syntax | Description |
    | ----------- | ----------- |
    | `docker-compose run --rm app sh -c "python manage.py test"` | Using docker-compose to run application tests |

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
- [Postgres Guide](https://hub.docker.com/_/postgres)
- [Package installations on alpine](https://linuxopsys.com/topics/install-packages-in-alpine-linux)
- [PSYCOPG Guide](https://www.psycopg.org/docs/)

| Syntax | Description |
| ----------- | ----------- |
| `docker-compose up` | This runs services inside the docker compose file |
| services | Define services that will run containers or any job. |
| build: context: .| Builds the docker file inside the current directory. |
| args | Build arguments, which are environment variables accessible only during the build process. |
| ports: | Specify port mappings such that we connect port 8000 on our local machine to port 8000 inside the container. |
| volumes: - ./app:/app | Map the local app directory to sync with the running container files. |
| command: >
 `sh -c "python manage.py runserver 0.0.0.0:8000"` | Command to run the service which can be overridden from the terminal. |
| depends_on | Creates a network link between services |
| environment | Used to define environment variables |
| volumes: <volume> | Named volumes are used here to map container files from one service locally |


**Why environment variable**
- Easily passed to docker to be used in both local development and production

6. ### Linting
    - [Flake8 Guide](https://flake8.pycqa.org/en/latest/)
    - [Flake8 Configuration](https://flake8.pycqa.org/en/latest/user/configuration.html)
    - Add flake 8 to requirements.dev.txt
    - Add a .flake8 to the app directory
    - Update docker-compose with the args

    **Using Flake 8**
    | Syntax | Description |
    | ----------- | ----------- |
    | `docker-compose run --rm app sh -c "flake8"`  | Running flake8 |



7. ### Project Structure
| Syntax | Description |
| ----------- | ----------- |
| `docker-compose run --rm app sh -c "django-admin startproject app ."`  | Start project in the current directory |


8. ### GitHub Actions
[Github Actions Guide](https://docs.github.com/en/actions)
[Action Features](https://github.com/features/actions)

**Why github actions**
- We use github actions to run jobs for (deployment, unit-tests, code linting)
- Add steps for running test and linting -> .github/workflows/checks.yml
- Authenticate with docker hub and add secretsto the github project
- Update or add the DOCKERHUB_TOKEN and DOCKERHUB_USER secrets on github

## Steps
- Create the neccessary docker and docker-compose files.
- Add requirements files and create the app directory.
- run `docker build .` to build the docker image.
- run `docker-compose build` to use docker compose to build and tag the image.
- Add flake 8 to requirements.dev.txt and create the .flake8 to ignore application files inside app/ from linting.
- Add args to the docker-compose file and update the docker file to install dev requirements when in development.
- Add a database service with environment variables set to the docker-compose file
- Configure postgresql for django by installing adaptors
## Contributions
- After cloning the repo change to the dev branch and create pull requests from there.
-- git branch -M dev
