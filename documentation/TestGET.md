**Retrieve tests**
----
  This is a simple for getting tests. 
  
* **URL**

  custom-test

* **Method:**

  `GET` 
  
*  **URL Params**

    **Optional:** <br>
                  
    Specify the index of the first test to be retrieved: <br>
    `start=[integer]`
                    
    Specify the maximum number of tests to be retrieved:  <br>
    `number=[integer]`
         
    Specify the test by its id: <br>
    `id=[integer]`
    
    Specify the test by its id: <br>
    `title=[string]`
    
    Specify the creation type of the test. Options are 'standard' and 'personal': <br>
    `creation_type=[string]`
    
    Set the parameter to 'random' to shuffle the tests randomly. Otherwise, the tests are 
    ordered by their id. <br> 
    `mode = [string]`
  
* **Data Params**

    An authorization header has to be provided. The key is 'token' 
    and the value should be a string of the form "token 3e8XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX3481". 
    
* **Success Response:**

  * **Code:** 200 OK <br />
    **Content:** 
    ```json
    [{
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
     }]
    ```
  OR
  
  If for example an non-existing id is given as a query-parameter, then the following response is send: 
  
  * **Code:** 204 No Content <br />
  
* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** `{ detail : "Authentication credentials were not provided." }`

    
* **Sample Call:**

   ```python
   import requests
   base_url = 'http://127.0.0.1:8000/api/'
   token = '3e8eXXXXXXXXXXXXXXXXXXXXXXXXXXX3481'
   headers =  {'Authorization': 'token ' + token}
   test_get = requests.get(url=base_url + "custom-test",
                             headers=headers,
                             params={'number': 1}
                             )
   print(test_get.json())
  ``` 
     
  This request should get a status 200 OK and print:
  ```python
  [
      {
          'id': 8, 
          'user_profile': 1, 
          'questions': [31, 32, 33, 34, 35], 
          'title': 'Brüche addieren', 
          'html': '<h1> Brüche addieren </h1>', 
          'created_on': '2020-04-13T21:41:48.048939Z'
      }
  ]
  ```
    
* **Notes:**

    This View does not send the actual questions but just their ids. This might be changed in the future. 
    
