<h1>ToDoList</h1>
<hr style="border: 1px solid white;">
<h2>Web application - task manager</h2>
educational project, simple Django backend for application for task management
<br>
frontend was provided to me
<hr>
<h2>Stack</h2>

1. Python 3.10
2. Django 4.2.3
3. PostgreSQL
4. Django Rest Framework
<hr>

<h2>Features:</h2>
Create, update, delete your goals, categories and boards of goals<br>
Add other users to your boards<br>
Authentication via username and password or VK account<br>
Use my Telegram bot to get your goals, and even create them.
<hr>

<h2>Using application:</h2>
You can use application online, it's available on http://51.250.100.71
<hr>

<h2>Telegram bot</h2>
You can use this telegram bot to read your goals and create new goals
http://t.me/todolist_production_bot
<hr>

<h2>Launching application:</h2>

You can run this application locally.<br>
Clone this repository<br>
To set up environment variables create .env file like:<br>

DB_ENGINE=django.db.backends.postgresql<br>
DB_NAME=<br>
DB_USER=<br>
DB_PASSWORD=<br>
SECRET_KEY=<br>
DEBUG=<br>
DB_HOST=<br>
POSTGRES_HOST=<br>
DOCKERHUB_USER=<br>
SOCIAL_AUTH_VK_OAUTH2_KEY=<br>
SOCIAL_AUTH_VK_OAUTH2_SECRET=<br>
BOT_TOKEN_DEV=<br>
BOT_TOKEN_PROD=<br>

Note that BOT_TOKEN_DEV or BOT_TOKEN_PROD was used optionally, choose right one in settings.py

<h3>Test:</h3>
For testing:<br> 
first change settings file<br>
comment # this string:<br> 
'HOST': env.str('DB_HOST', default='127.0.0.1'),<br>
make this string readable for python:<br>
'HOST': "localhost",
