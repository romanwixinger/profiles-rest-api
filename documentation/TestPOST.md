**Create tests**
----
  This is a simple for creating tests. 
  
* **URL**

  custom-test

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
            "questions": "31;32;33;34",
            "title": "Brüche subtrahieren",
            "html": "<h1> Brüche subtrahieren </h1>"
     }
    ```
    
    The field 'questions' and "title" are strictly required and may not be blank. The field 'html' is optional but 
    must not be left blank. In the field 'questions', the ids of the questions have to be separated by semicolons as 
    delimiters.  In the field 'html', the length of the string should not exceed 8191 characters. 
    
* **Success Response:**

  * **Code:** 201 Created <br />
    **Content:** 
    ```json
    {
            "id": 10,
            "user_profile": 1,
            "questions": [
                31,
                32,
                33,
                34
            ],
            "title": "Brüche subtrahieren",
            "html": "<h1> Brüche subtrahieren </h1>",
            "created_on": "2020-04-17T19:39:31.271382Z"
        }
    ```
 
* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** `{ detail : "Authentication credentials were not provided." }`

  OR
    
  If one of the conditions on the data mentioned above is not fulfilled, a response similar to the following is send. 
  * **Code:** 400 Bad Request <br />
    **Content:** 
    ```json
    {
        "questions": [
            "This field is required."
        ],
        "title": [
            "This field is required."
        ]
    }
    ```
    
* **Sample Call:**

   ```python
   import requests
   base_url = 'http://127.0.0.1:8000/api/'
   token = '3e8eXXXXXXXXXXXXXXXXXXXXXXXXXXX3481'
   headers =  {'Authorization': 'token ' + token}
   test =  {
         "questions": "31;32;33;34",
         "title": "Brüche subtrahieren",
         "html": "<h1> Brüche subtrahieren </h1>"
    }
   test_post = requests.post(url=base_url + "custom-test",
                          headers=headers,
                          json=test)
  print(test_post.json())
  ``` 
     
  This request should get a status 201 Created and print:
  ```python
  {
      'id': 13, 
      'user_profile': 6, 
      'questions': [31, 32, 33, 34], 
      'title': 'Brüche subtrahieren', 
      'html': '<h1> Brüche subtrahieren </h1>', 
      'created_on': '2020-04-17T19:50:11.711909Z'
  }
  ```
    
* **Notes:**

    This is not the only request that can create answers. 
