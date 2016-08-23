# calendarApp
A single page django based application which let's you maintain your events and sync events with google calendar api. Follow the step given below to set up the application.

<p align="center">
  <a href="http://www.youtube.com/watch?v=Ntcw0H0hwPU" target="_blank">
    <img src="https://i.imgsafe.org/c829b0c10d.png">
  </a>
</p>

## Installation

1. Open a terminal and navigate to the project root folder and type `pip install -U -r requirements-1.txt`

2. After the execution, type `sudo apt-get install $(grep -vE "^\s*#" requirements-2.txt  | tr "\n" " ")`

3. Go to application root, then calendarApp and open settings.py.

4. Go to the DATABASES part and modify the database details.

5. For Google Calendar Sync -- Go to google developer console and create a project. Then enable the Google Calendar API and save your client secret ( as client-secret.json ) under application root >> calendarApp folder.

6. Now type `python manage.py migrate`

7. Finally type `python manage.py runserver <port>`

The port argument is optional. If the terminal throws an error of port  being unavailable, please add the port argument and execute the command. (Like,  `python manage.py runserver 8081`  .

Live Beta Version: https://calendarapplication.herokuapp.com/ 
