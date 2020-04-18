**Retrieve answers**
----
  This request is for retrieving answers of the logged in user.
  
* **URL**

  custom-answer/

* **Method:**

  `GET` 
  
*  **URL Params**

   **Optional:** <br>
            
   Specify the index of the first answer to be retrieved: <br>
   `start=[integer]`
              
   Specify the maximum number of answers to be retrieved:  <br>
   `number=[integer]`
   
   Specify the question of the answer by its id: <br>
   `question_id=[integer]`
              
   Specify the topic of the answer by its id: <br>
   `topic_id=[integer]`
              
   Specify the subtopic of the answer by its id: <br>
   `subtopic_id=[integer]`
  
  
* **Data Params**

    An authorization header has to be provided. The key is 'token' 
    and the value should be a string of the form "token 3e8XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX3481". 
    
    No body has to be provided. 
    
* **Success Response:**

  * **Code:** 200 OK <br />
    **Content:** `{"id": 107, "user_profile": 1, "created_on": "2020-04-16T20:24:12.371529Z", "question": 32, 
    "duration": "12.50", "answers": "5/2", "correct": false, "skipped": false, 
    "comment": "I am not sure about the answer."}`
    
 OR
 
  *  **Code:** 204 No Content <br />
 
* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** `{ detail : "Authentication credentials were not provided." }`

* **Sample Call:**

    ```python
    import requests
    base_url = 'http://127.0.0.1:8000/api/'
    token = '3e8eXXXXXXXXXXXXXXXXXXXXXXXXXXX3481'
    headers =  {'Authorization': 'token ' + token}
    answer_get = requests.get(url=base_url + "custom-answer/", 
                              headers=headers,
                              params={'number': 1})
    print(answer_get.json())
     ``` 
     
     This request should get a status 200 OK and print:
     ```python
     [{'id': 107, 'user_profile': 1, 'created_on': '2020-04-16T20:24:12.371529Z', 'question': 32, 'duration': '12.50', 
     'answers': '5/2', 'correct': False, 'skipped': False, 'comment': 'I am not sure about the answer.'}]
     ```
    
* **Notes:**

    It is not possible to retrieve answers given by other users.  
