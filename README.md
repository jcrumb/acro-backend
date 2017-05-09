# acro-backend

This is the flask based backend for the acro android app. This project never made it to the play store, and was really intended as a learning exersice. The backend is written in python using flask and flask-restful, with postgres for account storage and redis for storage of current session data (such as tracking codes/pins, current alerts, etc). Twilio is used for sending SMS, and there is a small web frontend that displays a map overlayed with a pin of the user's last known location when tracking is active.

You can find the android part of this project [here](https://github.com/jcrumb/acro-android)
