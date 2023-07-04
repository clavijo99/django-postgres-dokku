# project_name

- Django 4.0.4
- Postgres 12
- Dokku
- push notification 
## Push Notification Support

- Android: Push notifications are supported on Android devices using Firebase Cloud Messaging (FCM). You can integrate FCM into your Android app to enable push notifications.

- iOS: Push notifications are supported on iOS devices using Apple Push Notification service (APNs). You can configure your iOS app with APNs to enable push notifications.

- Web: Push notifications are supported on web browsers using the Web Push API. You can implement web push notifications in your web application to send notifications to users on supported browsers.
## config (Production Ready)

## Documentation ##

### Directory Tree ###
```

├── main (Main application of the project, use it to add main templates, statics and root routes)
│   ├── fixtures
│   │   ├── dev.json (Useful dev fixtures, by default it creates an `admin` user with password `admin`)
│   │   └── initial.json (Initial fixture loaded on each startup of the project)
│   ├── migrations
│   ├── static (Add here the main statics of the app)
│   ├── templates (Add here the main templates of the app)
│   ├── admin.py
│   ├── apps.py
│   ├── models.py (Main models like City, Config)
│   ├── tests.py (We hope you will put some tests here :D)
│   ├── urls.py (Main urls, place the home page here)
│   └── views.py
├── media
├── project_name
│   ├── settings
│   │   ├── partials
│   │   │   └── util.py (Useful functions to be used in settings)
│   │   ├── common.py (Common settings for different environments)
│   │   ├── development.py (Settings for the development environment)
│   │   └── production.py (Settings for production)
│   ├── urls.py
│   └── wsgi.py
├── scripts
│   ├── command-dev.sh (Commands executed after the development containers are ready)
│   └── wait-for-it.sh (Dev script to wait for the database to be ready before starting the django app)
├── static
├── Dockerfile (Instructions to create the project image with docker)
├── Makefile (Useful commands)
├── Procfile (Dokku or Heroku file with startup command)
├── README.md (This file)
├── app.json (Dokku deployment configuration)
├── docker-compose.yml (Config to easily deploy the project in development with docker)
├── manage.py (Utility to run most django commands)
└── requirements.txt (Python dependencies to be installed)
```

### How to install the template ###

Clone the repository, and update your origin url: 
```
git clone https://github.com/clavijo99/django-postgres-dokku project_name
cd project_name
```

Merge the addons required by your project (Optional):
```
git merge origin/rest
```
## Branch for Developing a Feature-Rich REST API with Notifications and a Spectacular Schema
This development branch aims to implement a comprehensive REST API with notification functionality and a spectacular schema. Below, the components and necessary configuration for achieving this goal are described:

# REST API
The API REST will be designed to offer a set of endpoints that enable CRUD (Create, Read, Update, Delete) operations on specific resources. We will follow the best practices for designing RESTful APIs, including the use of appropriate HTTP verbs (GET, POST, PUT, DELETE), proper structuring of routes, and JSON responses.

# Notifications
We will implement a robust notification system to keep users informed about important events in the application. This will be achieved by utilizing a push notification service such as Firebase Cloud Messaging (FCM) for mobile devices (Android and iOS) and the Web Push API for web browsers. We will configure registration tokens and utilize the subscription mechanism to send notifications to the corresponding users.

# Spectacular Schema
The API schema will be meticulously designed, following the best practices in the industry. We will employ efficient design patterns and utilize powerful data structures to ensure optimal performance and maintainable code. Key aspects like modularity, scalability, and security will be carefully considered. Additionally, we will document the API schema clearly and comprehensively, leveraging tools like OpenAPI (previously known as Swagger) to generate interactive and visually appealing documentation.

Rename your project files and directorys:
```
make name=project_name init
```
> Info: Make is required, for mac run `brew install make`

> After this command you can already delete the init command inside the `Makefile` 

The command before will remove the `.git` folder so you will have to initialize it again:
```
git init
git remote add origin <repository-url>
```

### How to run the project ###

The project use docker, so just run:

```
docker-compose up
```

> If it's first time, the images will be created. Sometimes the project doesn't run at first time because the init of postgres, just run again `docker-compose up` and it will work.

*Your app will run in url `localhost:8000`*

To recreate the docker images after dependencies changes run:

```
docker-compose up --build
```

To remove the docker containers including database (Useful sometimes when dealing with migrations):

```
docker-compose down
```

### Accessing Administration

The django admin site of the project can be accessed at `localhost:8000/admin`

By default the development configuration creates a superuser with the following credentials:

```
Username: admin
Password: admin
```

## Production Deployment: ##

The project is dokku ready, this are the steps to deploy it in your dokku server:

#### Server Side: ####

> This docs does not cover dokku setup, you should already have configured the initial dokku config including ssh keys

Create app and configure postgres:
```
dokku apps:create project_name
dokku postgres:create project_name
dokku postgres:link project_name project_name
```

> If you don't have dokku postgres installed, run this before:
> `sudo dokku plugin:install https://github.com/dokku/dokku-postgres.git`

Create the required environment variables:
```
dokku config:set project_name ENVIRONMENT=production DJANGO_SECRET_KEY=....
```

Current required environment variables are:

* ENVIRONMENT
* DJANGO_SECRET_KEY
* EMAIL_PASSWORD

Use the same command to configure secret credentials for the app

#### Local Side: ####

Configure the dokku remote:

```
git remote add production dokku@<my-dokku-server.com>:project_name
```

Push your changes and just wait for the magic to happens :D:

```
git push production master
```

Optional: To add SSL to the app check:
https://github.com/dokku/dokku-letsencrypt


> Further dokku configuration can be found here: http://dokku.viewdocs.io/dokku/
