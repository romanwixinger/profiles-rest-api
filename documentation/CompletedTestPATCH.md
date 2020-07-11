**Update a completed test**
----
  This is a simple view for updating completed tests, namely altering the fields and adding new answers.
  
* **URL**

  custom-completed-test/{id}

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
          "answers": 
      [
      {
              "question": 430,
              "duration": "24.00",
              "answers": "1/2",
              "skipped": false
      }],
          "state": "Second question answered",
          "duration": "13.00"
      }

    ```
    
    All fields are not required, but may not be left blank. The answers have to be given in the form specified in the 
    POST method of Answer. The fields 'state', 'duration' and 'comment' are optional and may not be blank. 
    
* **Success Response:**

  * **Code:** 200 Created <br />
    
* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** `{ detail : "Authentication credentials were not provided." }`

  OR
    
  If one of the conditions on the data mentioned above is not fulfilled, a response similar to the following is send. 
  * **Code:** 400 Bad Request <br />
    **Content:** `{"non_field_errors": [ "Invalid answers given."]}`
                 
  OR
    
  * **Code:** 404 Bad Request <br />
    **Content:** `{"id": "The completed test with this id does not exist or does not belong to this user."}`

    
* **Sample Call:**

   ```python
   import requests
   base_url = 'http://127.0.0.1:8000/api/'
   token = '3e8eXXXXXXXXXXXXXXXXXXXXXXXXXXX3481'
   headers =  {'Authorization': 'token ' + token}
 
   completed_test_patch = completed_test = {
       "answers": 
                   [{
                           "question": 410,
                           "duration": "21.00",
                           "answers": "1/3",
                           "skipped": False
                   }],
       "state": "New questions answered."
   }
   completed_test_patch = requests.patch(url=base_url + "custom-completed-test/124/",
                                       headers=headers,
                                       json=completed_test_patch
                                       )
   print("Status code: ", completed_test_patch.status_code)
  ``` 
     
  This request should get a status 200 OK.
    
* **Notes:**

