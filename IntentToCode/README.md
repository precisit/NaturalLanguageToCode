# IntentToCode
This is an implementation written as a part of a Uppsala university master thesis to study the possibility of using 
Natural language processing techniques to translate a user's intent, expressed in natural language, in code. 

The general idea is a proof of concept system that controls an game environment by interpreting natual language 
commands from the user and convert them to code.  
## Run 
To start the application, run `python api.py` to start the web server. The web interface can then be accessed through `http://localhost:5000/`.

## Requirements 

* Stanford CoreNLP

* Flask and Flask RESTful

   To use the web interface, [Flask](http://flask.pocoo.org/ "Install Flask") and [Flask RESTful](https://flask-restful.readthedocs.io/en/0.3.5/installation.html "Install Flask RESTful") is required. 
   
* Senna version higher than 3.0 

* To run the machine learning you need to first run the machine learning file to get out the models need. 

* Run `python word2vec.py` before running the system to build a model for synonyms.