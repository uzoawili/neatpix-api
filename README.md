# neatpix &nbsp;&nbsp;[![Circle CI](https://circleci.com/gh/andela-uawili/photo-editing-application/tree/develop.svg?style=svg)](https://circleci.com/gh/andela-uawili/photo-editing-application/tree/develop) [![Coverage Status](https://coveralls.io/repos/andela-uawili/photo-editing-application/badge.svg?branch=develop&service=github)](https://coveralls.io/github/andela-uawili/photo-editing-application?branch=develop)
Upload. Prettify. Share.


#### Overview
Neatpix is a simple web app that allows users to upload their photos to the cloud, apply and save filters/effects to these photos and then share them on social media. In addition, the app also lets users download their edited photos to desktop. Social media support is limited to Facebook for this version.


#### Tech
The Neatpix app will be built using a number of web development technologies and services, some of which include:
+ [Django](https://www.djangoproject.com/) &nbsp;- Python web development framework for building web apps quickly and with less code.
+ [PostgreSQL](http://www.postgresql.org/) &nbsp;- relational database management system.
+ [Bower](http://bower.io/) &nbsp;- front end javascript dependency manager.
+ [Flexgrid](https://github.com/andela-cnnadi/flexgrid/) &nbsp;- front-end flexbox framework for layout.
+ [jQuery](http://jquery.com/) &nbsp;- fast, small, and feature-rich JavaScript library.
+ [Python Image Library (Pillow)](http://pillow.readthedocs.org/en/3.0.x/) &nbsp;- image manipulation and effects.
+ [Facebook Javascript SDK](https://developers.facebook.com/docs/javascript) &nbsp;- Facebook SDK for JavaScript for integrating client-side Facebook functionality into your web apps.


#### Installation
Follow the steps below to install Neatpix on your local machine: 

1. Ensure you have Python >= 2.7 installed. You can get it [here](https://www.python.org/downloads/). Using a virtual environment is also recommended.
2. Ensure you have **npm** and **bower** installed. You can get **npm** [here](https://www.npmjs.com/).
3. Ensure you have PostgreSQL installed and create a database with the name `neatpix`.
4. Clone this repository to your machine.
5. In the project root, add a `.env.yml` file to hold all your environment variables, such your secret key (required) and database credentials e.g:
    ```
    SECRET_KEY:
    'very-very-very-secret-key'
    DATABASE_USER:
    'foo_user'
    DEBUG_MODE:
    'debug-mode-for-current-deploy'
    DATABASE_PASSWORD:
    'youcannotguessme'
    FACEBOOK_APP_ID:
    'your-own-facebook-appi-id'
    ```

6. Install all python and front end dependencies by running the followings commands in order, from in the project root:
    ```
    $ npm install -g bower
    $ bower install
    $ pip install -r requirements.txt
    ```

7. To setup static files and database migrations, run (also in the project root):
    ```
    $ neatpix/python manage.py collectstatic
    $ python neatpix/manage.py makemigrations
    $ python neatpix/manage.py migrate
    ```
 
#### Running the Server

Run `$ neatpix/python manage.py runserver` to start the server.

#### Testing
+ To run tests:  
```$ python neatpix/manage.py test --settings=neatpix.settings.testing```

+ For the coverage report:    
  1. ```$ coverage run --source=webapp neatpix/manage.py test neatpix --settings=neatpix.settings.testing ```
  2. ```$ coverage report ```
  3. ```$ coverage html ```

