# Flask-URL-Shortener
Sometimes we need to share or send links and this can be tiresome and annoying to copy and paste long URLs. That is where URL Shortener comes. Not only it helps in shortening the URL but it also allows user to copy the shortened URL with a click of a button.
In this project, user can save the shortened URL and can view those URL anytime by logging into the account that user has created. Further, user can delete URL if he/she does not want it.

## Required Packages
# Install Some Necessary Packages and Softwares

### 1) Install Flask Package
* Type following command in CMD
    * pip install virtualenv
    * pip install Flask
### 2) Install Flask WTForms Package
* Type following command in CMD
    * pip install flask-WTF
### 3) Install Flask PyMongo Package
* Type following command in CMD
    * pip install Flask-PyMongo
### 4) Install Bitly API Package
* Type following command in CMD
    * pip install bitly_api

## Important Steps

### Setup [MLab](https://mlab.com/signup/) Account
* Create new account in Mlab
* After logging into MLab account, create new deployment with name 'url_registration'
* After creating deployment, click on 'url_registration' deployment
* Create two new Collections with name 'urlData' and 'urlRegisteration'

### Setup [Bitly](https://bitly.com/a/sign_up?utm_content=site-free-button&utm_source=organic&utm_medium=website&utm_campaign=null&utm_cta=site-free-button) Account
* Create new account in Bitly
* After logging into Bitly account,  Click on Setting box on top-right Corner
* Click on Setting
* Click on Advance Setting
* Click on API Support
* Now copy both Login Key and API Key. These Keys are required in Python File as 'API_USER' and 'API_KEY'
