# Buyer's App

## Whats the plan?

I'm creating a web app, powered by three components.  In the background 
will be a mongoDB hosting data on houses for sale.  Handling the 
requests for data will be an actor/service, created using Flask in 
python.  The interface the user sees will be a JavaScript-powered web 
page.  The system will use RESTful API's to handle client-actor 
interractions through http requests.


### The database

- Initially, it'll be a local mongoDB instance.
- It'll be created by fudging some HMRC data on property prices for 
recent sale, I'll include the creation/upload script for that too.
- The DB will be moved to the web ASAP, so that it can be shared with 
others.


### The server/actor (terminology?)

- It'll be constructed in python 3.  It's a particularly clean and 
understandable language to program in.
- The Flask library/api makes creating a web API really easy.
- Google App Engine, on which it will be deployed, supports python and 
flask without issues.


### The frontend/GUI/webpage

- On different repo, see;  


## Resources


### For creating the API server
The tutorial that taught me to create a RESTful API server/actor is 
at https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask

The example I created following this is in example_app.py but if you 
plan to create this service using python I recommend following the 
original tutorial.


### For creating the GUI
The tricky part is making the requests over http from the GUI (in html,
with JavaScript code) to the server.  The tutorial I've followed in 
making my example can be found at https://www.taniarascia.com/how-to-connect-to-an-api-with-javascript/

The example I've created is in example_gui.html, and will connect to the
example_app.py if running.
