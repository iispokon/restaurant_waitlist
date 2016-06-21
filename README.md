# Restaurant Waitlist App
_Repository of a simple Twilio demo app. Idea borrowed from [appointment-reminders-django](https://github.com/TwilioDevEd/appointment-reminders-django)_


## Setup
To view this demo. Run the app locally:

You should already have a Twilio account. You will set environment variables to your TWILIO_NUMBER and Twilio app credentials (steps below). 
This demo will work with a Twilio free trial account. Just be sure to use "Verified Caller Id" numbers, so that Twilio can message those numbers when you try this demo.
    
This app allows anonymous users to access a "guestlist" webpage. In order to access the webpage over the internet, we will need to use [ngrok](https://ngrok.com/) to expose your local machine to the internet.

### Local setup

1. Clone this repository. Then 'cd' into its directory
1. Create a virtualenv environment
    ```
    $ virtualenv venv
    $ source venv/bin/activate
    ```
1. Install requirements
    ```
    $ pip install -r requirements.txt
    ```
1. Run migrations
    ```
    $ python manage.py makemigrations guestlist
    $ python manage.py migrate
    ```
1. Create a superuser
    ```
    # python manage.py createsuperuser
    ```
1. Install [ngrok](https://ngrok.com/)
    Note:
    - Ngrok allows you to expose a web server running on your local machine to the internet. Just tell ngrok what port your web server is listening on.
    - Expose your local web server to the internet:
    ```
    $ ngrok http 8000 -host-header="localhost:8000"
    ```
1. Rename ".example_env" to ".env"
1. Edit .env and provide your TWILIO_NUMBER, TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN. Set APP_DOMAIN to ```<your-ngrok-subdomain>.ngrok.io```, obtained from the previous step
1. Source env
    ```
    $ source .env
    ```
1. Set your Twilio phone number's message webhook URL to POST  ```http://<your-ngrok-subdomain>.ngrok.io/guestlist/action/```
1. Start the server
    ```
    $ python manage.py runserver
    ```

## Demo app
Here's a familiar scenario: You and your friends arrive at a busy restaurant. You don't have a reservation. The host informs you that there is a long wait and you put your name on a list.
There are plenty of shops and bars around that you can patronize while you wait. However, you instead hover near the door for fear that you might miss your name being called when your table is ready. 
This demo app is a modern take on the good old pen, paper and clipboard approach used by many small restaurants. It makes it easy to put your name on the list, keep track of your position, and make changes. The host can inform you that your table is ready with a click of a button.

## Usage
- Anonymous users are basically restaurant customers. As a customer, you can add your name to the list by providing a name, number of guests, and your phone number.

- Restaurant staff logs-in to the app. (Use the django superuser created in the previous steps). Once logged in, you can edit things on the list, and page customers to let them know their table is ready. 
