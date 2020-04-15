**Create and retrieve topics**
----
  This is a simple for for creating and retrieving topics. 
* **URL**

  custom-topic/

* **Method:**

  `GET` | `POST` 
  
*  **URL Params**

   For `GET` the following query-parameters exist: 

   **Optional:** <br>
   
    Specify the index of the first topic to be retrieved: <br>
    `start=[integer]` 
       
    Specify the maximum number of topics to be retrieved:  <br>
    `number=[integer]` 

* **Data Params**

    The body should be a JSON object with the key 'name'. <br> An authorization header has to be provided. The key is 'token' 
    and the value should be a string of the form "token 3e8XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX3481". 
    
* **Success Response:**

  * **Code:** 201 Created <br />
    **Content:** `{'id': 20, 'user_profile': 6, 'name': 'Division of fractions'}`
    
  * **Code:** 200 OK <br />
    **Content:** `[{"id": 1, "user_profile": 1, "name": "Rechenoperationen"}, ... , {"id": 6, "user_profile": 1, 
                 "name": "Brüche"}]`
  
  * **Code:** 204 No Content <br />
 
* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** `{ detail : "Authentication credentials were not provided." }`

  OR

  * **Code:** 400 Bad Request <br />
    **Content:** `{"name": ["This field may not be blank."]}`

* **Sample Call:**

    ```python
    import requests
    base_url = 'http://127.0.0.1:8000/api/'
    topic = {'name': 'Division of fractions'}
    token = '3e8eXXXXXXXXXXXXXXXXXXXXXXXXXXX3481'
    headers =  {'Authorization': 'token ' + token}
    topic_post = requests.post(url=base_url + "custom-topic/", 
                               json=topic, 
                               headers=headers)
     ``` 
     
     This request should get a status 201 Created and print:
     ```python
     {'id': 20, 'user_profile': 6, 'name': 'Division of fractions'}
     ```
    
* **Notes:**

    This is not the only request that can create topics, there are others that create topics on-the-fly.
