**Create answers**
----
  This is a simple for creating answers. The corrected answer is send as answer. 
  
* **URL**

  custom-answer/

* **Method:**

  `POST` 
  
*  **URL Params**

    There are no query-parameters. 
  
  
* **Data Params**

    An authorization header has to be provided. The key is 'token' 
    and the value should be a string of the form "token 3e8XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX3481". 
    
    The body should be a JSON object of the following form: <br>
    
    `{"question": 1, "duration": 12.5, "answers": "5/2", "skipped": false, "comment": "I am not sure about the answer."}` <br>
    
    The field 'question' is strictly required, 'comment' and 'duration' are optional. The field 'answers' can only be left out 
    if the field 'skipped' is set to true. 
    
    
* **Success Response:**

  * **Code:** 201 Created <br />
    **Content:** ` {"id": 107, "user_profile": 1, "created_on": "2020-04-16T20:24:12.371529Z", "question": 32, 
    "duration": "12.50", "answers": "5/2", "correct": false, "skipped": false, 
    "comment": "I am not sure about the answer."}`
    
 
* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** `{ detail : "Authentication credentials were not provided." }`

  OR
    
  If one of the conditions on the data mentioned above is not fulfilled, a response similar to the following is send. 
  * **Code:** 400 Bad Request <br />
    **Content:** `{ "non_field_errors": [ "No answer was provided and the question was not skipped."]}`

* **Sample Call:**

    ```python
    import requests
    base_url = 'http://127.0.0.1:8000/api/'
    token = '3e8eXXXXXXXXXXXXXXXXXXXXXXXXXXX3481'
    headers =  {'Authorization': 'token ' + token}
    answer =  {"question": 32, "duration": 5.5, "answers": "5/2", "skipped": False, 
               "comment": "I am not sure about the answer."}
    answer_post = requests.post(url=base_url + "custom-answer/", 
                                headers=headers,
                                json=answer)
    print(answer_post.json())
     ``` 
     
     This request should get a status 201 Created and print:
     ```python
     {'id': 118, 'user_profile': 6, 'created_on': '2020-04-16T20:54:39.944256Z', 'question': 32, 'duration': '5.50', 
   'answers': '5/2', 'correct': False, 'skipped': False, 'comment': 'I am not sure about the answer.'}
     ```
    
* **Notes:**

    This is not the only request that can create answers. 
