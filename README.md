# NaturalLanguageToCode
This is an implementation written as a part of a Uppsala university master thesis to study the possibility of using 
Natural language processing techniques to translate a user's intent, expressed in natural language, in code. 

The general idea is a proof of concept system that controls an game environment by interpreting natual language 
commands from the user and convert them to code.  

New version of the project IntentTocode made in 2017. This version includes machine learning to handle part of speech 
tagging and synonyms.  

## Run 
To get the models compared to be used for part of speech tagging in the program go to `trainingMLModels.ipynb`
and select wanted model that you then drag over to the `IntentToCode` file or in `machine_learning.py `
or change path when opening model. 

To get synonym handling model you need to start `word2vec.py`

To start the system, switch over to the `IntentToCode` file and read its `Readme`
## Requirements 

* Python 3

* Keras and Tensorflow

* Jupyter notebook 

* Stanford CoreNLP

* Flask and Flask RESTful

   To use the web interface, [Flask](http://flask.pocoo.org/ "Install Flask") and [Flask RESTful](https://flask-restful.readthedocs.io/en/0.3.5/installation.html "Install Flask RESTful") is required. 
   
* Senna version higher than 3.0 