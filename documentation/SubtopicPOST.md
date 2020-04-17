**Create subtopics**
----
  This is a simple for for creating subtopics. 
  
* **URL**

  custom-subtopic/

* **Method:**

  `POST` 
  
*  **URL Params**

    There are no query-parameters.
  
* **Data Params**

    An authorization header has to be provided. The key is 'token' 
    and the value should be a string of the form "token 3e8XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX3481". 
    
    The body should be a JSON object of the following form: <br>
    ```json
    {
        "name": "Brüche addieren", 
        "html": "<h1> Brüche addieren </h1>",
        "topic": 1
   }
    ```
    All the fields are required but 'html' can have an empty string as value.
    
    
* **Success Response:**

  * **Code:** 201 Created <br />
    **Content:** `{"id": 44, "user_profile": 1, "name": "Brüche subtrahieren", "html": "<h1> Brüche subtrahieren </h1>",
     "topic": 22}`
    
  OR  
  
  * **Code:** 200 OK <br />
    **Content:** `[{ "id": 13, "user_profile": 1, "name": "Brüche addieren", "html": "", "topic": 12}]`
                  
  OR                
                  
  * **Code:** 204 No Content <br />
 
* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** `{ detail : "Authentication credentials were not provided." }`

  OR

  * **Code:** 400 Bad Request <br />
    **Content:** 
    ```json
    { 
        "name": ["This field is required."], 
        "html": ["This field is required."], 
        "topic": ["This field is required."] 
    }
    ```

* **Sample Call:**

    ```python
    import requests
    base_url = 'http://127.0.0.1:8000/api/'
    token = '3e8eXXXXXXXXXXXXXXXXXXXXXXXXXXX3481'
    headers =  {'Authorization': 'token ' + token}
    subtopic = {"name": "Brüche addieren", "html": "<h1> Brüche addieren </h1>", 
                "topic": 1}
    subtopic_post = requests.post(url=base_url + "custom-subtopic/", 
                                  headers=headers,
                                  json=subtopic)
     ``` 
     
     This request should get a status 201 Created and print:
     ```python
     {'id': 45, 'user_profile': 6, 'name': 'Brüche addieren', 'html': '<h1> Brüche addieren </h1>', 'topic': 23}
     ```
    
* **Notes:**

    This is not the only request that can create subtopics, there are others that create subtopics on-the-fly.
