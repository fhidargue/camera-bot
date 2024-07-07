# camera-bot
This is a personal bot to look for a camera availability online

# Project setup
Before we can run the bot, we need to configure the SMTP provider from Google in case we plan to use Gmail to send emails. If you are going to use another provider, please make sure your account gets authenticated as expected. Otherwise, this bot will not be able to send you the availability notifications.

 **For Gmail**: 
 1. Open your Google account and go into `Manage your Google Account` 
 2. Go inside `Security` and activate `2-Step Verification`. We can do this using our phone number, authenticator app or other options.
 3. Open you account's app passwords and create one for this bot: https://myaccount.google.com/u/0/apppasswords
    1. You can call it however you want, for example: `Python bot`
    2. You will then receive a 16 character password similar to this one: `xxxx xxxx xxxx xxxx`
 4. Open up this project's code and go inside the `.env` file
 5. Enter your account's email as `SENDER_EMAIL` and add this new password as `SENDER_PASS`
 6. Lastly, enter the email where you want to receive the notifications as `RECEIVER_EMAIL`

# How to run the project

1. Install Python 3.11
2. Install pipenv so we can install all the dependencies. Then, run the `pipenv install` command
3. Open a local environment with the `pipenv shell` command
4. Run the bot using the `python camera-bot.py`