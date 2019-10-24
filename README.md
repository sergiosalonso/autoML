# autoML
===========

## Description
This project makes ML accessible to everyone with a graphical interface. Its <br/>
a distributed app that uses RabbitMQ and EC2 instance.

## Installation
Install the requirements:
`pip install -r requirements.txt` <br/>
Add your db: <br/>
Go to autoML/settings.py <br/>
Change: <br/>
DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'your_database',
            'USER': 'your_user',
            'PASSWORD': 'your_password',
            'HOST': 'public_ip',
            'PORT': 'port',
        }
    }
`python manage.py migrate` <br/>
Get the server running:
`python manage.py runserver` <br/>
