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

**Core App structure**
- app/core/tests/
- app/core/models
- app/core/admin
- app/core/apps
- app/core/migrations/


### **EthnicGroup App**
- Used for creating, updating and viewing ethnic groups.

**EthnicGroup App structure**
- app/ethnicgroup/tests/
- app/ethnicgroup/urls
- app/ethnicgroup/serializers
- app/ethnicgroup/apps
- app/ethnicgroup/views

### **Culture App**
- Used for creating, updating and viewing cultures.

**Culture App structure**
- app/culture/tests/
- app/culture/urls
- app/culture/serializers
- app/culture/apps
- app/culture/views

### **Event App**
- Used for creating, updating and viewing events.

**Event App structure**
- app/event/tests/
- app/event/urls
- app/event/serializers
- app/event/apps
- app/event/views

### **Chief App**
- Used for creating, updating and viewing chiefs.

**Chiefs App structure**
- app/chief/tests/
- app/chief/urls
- app/chief/serializers
- app/chief/apps
- app/chief/views

### **Publisher App**
- Used for creating, updating and viewing published documents.

**Publisher App structure**
- app/publisher/tests/
- app/publisher/urls
- app/publisher/serializers
- app/publisher/apps
- app/publisher/views




| Syntax | Description |
| ----------- | ----------- |
| `docker-compose run --rm app sh -c "python manage.py startapp user"`| Create a user app |
<br/>

**EthnicGroup App image api**
| Syntax | Description |
| ----------- | ----------- |
| Pillow | Contains all the basic image processing functionality |
| zlib , zlib-dev | used for data compression |
<br/>

**User App**
    - Used for creating auth tokens, user registration, updating and viewing profiles
    - [API Status Codes Guide](https://www.django-rest-framework.org/api-guide/status-codes/)
<br/>
| Syntax | Description |
| ----------- | ----------- |
| `docker-compose run --rm app sh -c "python manage.py startapp user"`| Create a user app |


**Authentication**
- We are using a custom user model to allow for changes moving forward and also to use an email for the username.
- We implementing the token authentication for its simplicity and security
- [Token Authetication Guide](https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication)

    - **Custom User Model Classes**
    - set AUTH_USER_MODEL in settings.py for django to use the custom user model.

    | Syntax | Description |
    | ----------- | ----------- |
    | AbstractBaseUser | Provides the core implementation of a user model. |
    | BaseUserManager | Base class for managing users and has helper methods. |
    | PermissionsMixin | Support for the django permission system. |
    | UserManager | Allows creation of custom logic for creating objects. |
    | create_user | Custom method called when creating a user. |
    | create_superuser | Custom method used to create superusers. |

    - **User Api**
    - There are configurations that allow for the management of users

    | Syntax / Files | Description |
    | ----------- | ----------- |
    | Serializers | Serializers are responsible for converting complex data <br/>(e.g., querysets and model instances) to native Python datatypes that can then be rendered into <br/>JSON, XML, or other content types.|
    | Views | Determine how requests will be handled and which policy attributes to use. |
    | urls.py | We include all the endpoints that have view classess |



- Creating a super user `docker-compose run --rm app sh -c "python manage.py createsuperuser"`
<br/>


**Migrations**
-Django handels database structure and changes
- Migrations are handled by django -> `python manage.py makemigrations`
- Applying migrations `python manage.py migrate`
- Using docker compose `docker-compose run --rm app sh -c "python manage.py wait_for_db && python manage.py migrate"`


    - **Migration issues**

    | Description | Possible Solution |
    | ----------- | ----------- |
    | 0001_initial is applied before is dependency | clear the devdb volume |
    | django.db.utils.ProgrammingError: relation "core_user" does not exist | clear migrations and make migrations again for the core app |

<br/>


## Project Management
1. ### Test Driven Development
- A development practice to write test for functionalities before implementation

2. ### Pre-Installs/Configuration
    - Vs-Code / any IDE
    - GIT
    - Set up Docker and Docker-Compose
    - Setup linting
    - Configure Github actions
<br/>

3. ### Documentation
**Developers or any user of our APIs needs to know how to use them.**
- **Documentation is both Manual and Automatic(endpoints) -> tools**
    - [DRF Spectacular](https://drf-spectacular.readthedocs.io/en/latest/)
    - [DRF Spectacular benefits](https://levelup.gitconnected.com/drf-spectacular-the-ultimate-tool-for-automated-drf-api-documentation-61bd4cca36b7)

- **What we have documented**
    - Available endpoints
    - Application docker configurations
    - Authentication process
    - Endpoint payloads and responses


4. ### Testing
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
    | `import pdb; pdb.set_trace()`| Option 1 to debug |
    | `breakpoint()` | Option 2 to bebug |

5. ### Linking the Githup repo to DockerHub
<br/>

6. ### Adding a Docker file and dockerignore

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


7. ### Linting
    - [Flake8 Guide](https://flake8.pycqa.org/en/latest/)
    - [Flake8 Configuration](https://flake8.pycqa.org/en/latest/user/configuration.html)
    - Add flake 8 to requirements.dev.txt
    - Add a .flake8 to the app directory
    - Update docker-compose with the args

    **Using Flake 8**
    | Syntax | Description |
    | ----------- | ----------- |
    | `docker-compose run --rm app sh -c "flake8"`  | Running flake8 |
<br/>

8. ### Project Structure
| Syntax | Description |
| ----------- | ----------- |
| `docker-compose run --rm app sh -c "django-admin startproject app ."`  | Start project in the current directory |
| `docker-compose run --rm app sh -c "django-admin startapp core"`  | Start app |

**Management Commands**
| file | Description |
| ----------- | ----------- |
|  wait_for_db_command.py | We are fixing a database service race issue so that we wait for all the db subfuctions to finish |
<br/>

9. ### GitHub Actions
[Github Actions Guide](https://docs.github.com/en/actions)
[Action Features](https://github.com/features/actions)

**Why github actions**
- We use github actions to run jobs for (deployment, unit-tests, code linting)
- Add steps for running test and linting -> .github/workflows/checks.yml
- Authenticate with docker hub and add secretsto the github project
- Update or add the DOCKERHUB_TOKEN and DOCKERHUB_USER secrets on github
<br/>

## Steps
- Create the neccessary docker and docker-compose files.
- Add requirements files and create the app directory.
- run `docker build .` to build the docker image.
- run `docker-compose build` to use docker compose to build and tag the image or after updating the requirements.txt.
- Add flake 8 to requirements.dev.txt and create the .flake8 to ignore application files inside app/ from linting.
- Add args to the docker-compose file and update the docker file to install dev requirements when in development.
- Add a database service with environment variables set to the docker-compose file
- Configure postgresql for django by installing adaptors and update the settings files
- To fix database race issues create a core app and add a management command to check if the database is ready
- Add a custom authentication user model and include the admin configs (list, add)
- Add a user app for creating users, tokens and managing profiles
- Add a ethnic group app for creating,updating and viewing ethinic groups.
- Add a tag feature for tagging ethnic groups
- Add a image api for ethnic groups
- Add a filtering feature for ethinic groups
- Add a culture app for creating, updating and viewing different cultures
- Add a tag feature for tagging cultures
- Add a image api for culture and create a custom action to upload the image
- Add a event app for creating, updating and viewing events
- Add a chief app for creating, updating and viewing chiefs information
- Add a publisher app for creating, updating and viewing published documents


## Contributions
- After cloning the repo change to the dev branch and create pull requests from there.
-- git branch -M dev
- Check the available issues -> pick an issue to manage.
- Write tests for the feature or bug fix.
- Submit a pull request.
