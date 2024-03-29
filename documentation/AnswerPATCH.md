**Update answers**
----
  This is a simple for partially updating answers. 
  
* **URL**

  custom-answer/<pk>

* **Method:**

  `PATCH` 
  
*  **URL Params**

    There are no query-parameters. 
  
* **Data Params**

    An authorization header has to be provided. The key is 'token' 
    and the value should be a string of the form "token 3e8XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX3481". 
    
    The body should be a JSON object of the following form: <br>
    
    ```json
    {
        "duration": 12.5, 
        "answers": "5/2", 
        "correct": true,
        "skipped": false, 
        "comment": "I am not sure about the answer."
    }
    ```
    
    All fields are optional, but must not be left blank. 
    
* **Success Response:**

  * **Code:** 201 Created <br />
    **Content:** 
    ```json
    {
         "id": 107,
         "user_profile": 1, 
         "created_on": "2020-04-16T20:24:12.371529Z", 
         "question": 32, 
         "duration": "12.50", 
         "answers": "5/2", 
          "correct": false, 
         "skipped": false, 
         "comment": "I am not sure about the answer.",
     }
    ```
 
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
    answer =  {"duration": 20, "answers": "new answer"}
    answer_patch = requests.post(url=base_url + "custom-answer/6400", 
                                headers=headers,
                                json=answer)
    print(answer_patch.json())
     ``` 
     
     This request should get a status 200 OK.

    
* **Notes:**

    This is not the only request that can create answers. If the answer already exists, it is left unchanged. For 
    updating answers, one can use 
    [PATCH](https://github.com/romanwixinger/profiles-rest-api/blob/master/documentation/CompletedTestPATCH.md). 
