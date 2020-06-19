# Profiles REST API

Code for the first Nasci learning tool backend based on the Profiles REST API course code. A running instance of the 
 REST API can be found [here](https://us-east-2.console.aws.amazon.com/console/home?region=us-east-2). 

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

To get access to the full capability of the REST API, you have to get an Authorization token with the following steps. 
Then open [this link](http://127.0.0.1:8000/api) in the browser and navigate to the
[profile view](http://127.0.0.1:8000/api/profile/). Create a user profile and navigate to the 
[login view](http://127.0.0.1:8000/api/login/). Type in your credentials and get an authorization token. Add the [ModHeader](https://chrome.google.com/webstore/detail/modheader/idgpnmonknjnojddfkpgkljpfnnfcklj?hl=eng) 
Chrome extension to Chrome and create a new header. Select _Authorization_ and insert the token in the form 
_token mymocktoken_ in the field. Activate the request header and you should have access to all the functionality. 

To add learning materials to the REST API, you can use the Github repository [romanwixinger/database-initializer](https://github.com/romanwixinger/database-initializer) 
or you create your own learning materials and send them with HTTP POST requests. 


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
