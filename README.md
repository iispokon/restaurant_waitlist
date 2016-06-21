# Restaurant Waitlist App
_Repository of a simple Twilio demo app. The idea for this app is borrowed from [appointment-reminders-django](https://github.com/TwilioDevEd/appointment-reminders-django)_


## Demo app
Here's a familiar scenario: You and your friends arrive at a busy restaurant. You don't have a reservation. The host informs you that there is a long wait and you'd have to place your name on a list. 
Once there is a table available, the host will call out your name. Hopefully, you haven't wandered off and lost your place in line.
There are plenty of shops and bars around that you can patronize while you wait. However, for fear that you might miss your name called, you suffer waiting in the crowded waiting area.

This demo app is a modern take on the good old pen, paper and clipboard approach used by many restaurants. A simple interface makes it easy for a customer to put their name on a wait list, keep track of their position anywhere using their cellphone, and also make changes (like update the number of guests to be seated). 
With a button click, the restaurant/host informs the customer that their table is ready. The customer is notified via SMS.

## Usage
- Anonymous users of this app are basically restaurant customers. As a customer, you can add your name to the list by providing a name, number of guests, and your phone number.

- Restaurant staff are users who have logins to the app. (Use the django superuser created in the steps below). Once logged in, you can edit names on the list. You can use the "page" functionality to let customers know that their table is ready. 

## Setup
To view this demo. Run the app locally:

You should already have a Twilio account. Keep note of the important steps below to make sure to set environment variables to your TWILIO_NUMBER and Twilio app credentials. 

Note:
- This demo will work with a Twilio free trial account, but just be sure to use "Verified Caller Id" numbers, so that Twilio can message those numbers when you try this demo.
- This app allows anonymous users to access a "guestlist" webpage -- In order to access the webpage over the internet, we will need to use [ngrok](https://ngrok.com/) to expose your local machine to the internet.

### Local setup

1. Clone this repository. Then 'cd' into its directory.

1. Create a virtualenv environment.

    ```
    virtualenv venv
    source venv/bin/activate
    ```

1. Install requirements.

    ```
    pip install -r requirements.txt
    ```
1. Run migrations.

    ```
    python manage.py makemigrations guestlist
    python manage.py migrate
    ```

1. Create a superuser.

    ```
    python manage.py createsuperuser
    ```

1. Install [ngrok](https://ngrok.com/)
    Note:
    - Ngrok allows you to expose a web server running on your local machine to the internet. Just tell ngrok what port your web server is listening on.
    - Expose your local web server to the internet:
    ```
    ngrok http 8000 -host-header="localhost:8000"
    ```

1. Rename ".example_env" to ".env". Then edit .env and provide your TWILIO_NUMBER, TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN. Set APP_DOMAIN to ```<your-ngrok-subdomain>.ngrok.io```, obtained from the previous step.

    ```
    export TWILIO_NUMBER="+1<your twilio number>"
    export TWILIO_ACCOUNT_SID="<your twilio account sid>"
    export TWILIO_AUTH_TOKEN="<your twilio auth token>"
    export APP_DOMAIN="<your-ngrok-subdomain>.ngrok.io"    
    ```

1. Source env.

    ```
    source .env
    ```

1. Set your Twilio phone number's message webhook URL to POST  ```http://<your-ngrok-subdomain>.ngrok.io/guestlist/action/```.

1. Start the server.

    ```
    python manage.py runserver
    ```