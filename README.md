# Intervals
A Django/React webapp that trains the user to identify musical intervals in a progressive, quiz based system. 
Users can create accounts to save their progress.

Uses Django REST framework and a PostgreSQL database.
Automated tests can be found in the tests folder.
App is containerized with NGINX and Docker. 

A secret .env file (not shown on github) is used to conceal sensitive information such as the Django secret key and database information.

Currently the quiz interface looks like this: 

<img src="https://raw.githubusercontent.com/JJamali/Intervals/master/resources/quiz.png" alt="current_design" width="80%"/>

Our next steps are implementing a cleaner UI:

<img src="https://raw.githubusercontent.com/JJamali/Intervals/master/UI%20Concepts/Main%20Quiz%20Page.jpg" alt="future_design" width="80%"/>


Made by: Jordan Jamali, Lukas Boelling

Level design: Richard Duan

Special thanks go to Raymond Huynh for designing UI concepts. 
