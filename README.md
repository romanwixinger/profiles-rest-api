# Profiles REST API

Code for the first Nasci learning tool backend based on the Profiles REST API course code.

## Installation

To run a local instance of the REST API you first install the requirements in your console. 

   ```
   pip install -r requirements.txt
   ``` 
   
Then you have to make the migrations with the following commands.

   ```python
   python manage.py makemigrations
   python manage.py migrate
   ``` 
 
Now you are ready to launch the local instance. 

   ```python
   python manage.py runserver
   ``` 

Depending on the configurations of your IDE you have to specify the host. Normally you get a message with this 
[link](http://127.0.0.1:8000/api) to see the running instance. 

## REST-API documentation

In the following, all possible requests to the API are listed with links to their documentation. The requests are 
grouped according to their underlying model and arranged after increasing complexity. 

* UserProfile: [POST](https://github.com/romanwixinger/profiles-rest-api/blob/master/documentation/UserProfilePOST.md) and 
[GET](https://github.com/romanwixinger/profiles-rest-api/blob/master/documentation/UserProfileGET.md) user profiles. 

* Login: [POST](https://github.com/romanwixinger/profiles-rest-api/blob/master/documentation/Login.md) the credentials and get an authorization token with the 
response. 

* Topic: [POST and GET](https://github.com/romanwixinger/profiles-rest-api/blob/master/documentation/Topic.md) topics. 

* Subtopic: [POST](https://github.com/romanwixinger/profiles-rest-api/blob/master/documentation/SubtopicPOST.md) and 
             [GET](https://github.com/romanwixinger/profiles-rest-api/blob/master/documentation/SubtopicGET.md) subtopics. 
            
* Question: [POST](https://github.com/romanwixinger/profiles-rest-api/blob/master/documentation/QuestionPOST.md) and 
             [GET](https://github.com/romanwixinger/profiles-rest-api/blob/master/documentation/QuestionGET.md) questions.
 
* Answer: [POST](https://github.com/romanwixinger/profiles-rest-api/blob/master/documentation/AnswerPOST.md) and 
           [GET](https://github.com/romanwixinger/profiles-rest-api/blob/master/documentation/AnswerGET.md) answers.
          
* Test: [POST](https://github.com/romanwixinger/profiles-rest-api/blob/master/documentation/TestPOST.md) and 
         [GET](https://github.com/romanwixinger/profiles-rest-api/blob/master/documentation/TestGET.md) tests.
         
* RecommendedTest: [GET](https://github.com/romanwixinger/profiles-rest-api/blob/master/documentation/RecommendedTestGET.md) recommended tests.
                  
* CompletedTest: [POST](https://github.com/romanwixinger/profiles-rest-api/blob/master/documentation/CompletedTestPOST.md) and 
                  [GET](https://github.com/romanwixinger/profiles-rest-api/blob/master/documentation/CompletedTestGET.md) completed tests.

* TheoryPage: [POST](https://github.com/romanwixinger/profiles-rest-api/blob/master/documentation/TheoryPagePOST.md) and 
              [GET](https://github.com/romanwixinger/profiles-rest-api/blob/master/documentation/TheoryPageGET.md) theory pages. 

* RecommendedTheoryPage: [GET](https://github.com/romanwixinger/profiles-rest-api/blob/master/documentation/RecommendedTheoryPageGET.md) recommended theory pages. 
