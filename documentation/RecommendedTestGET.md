**Retrieve recommended tests**
----
  This is a request for getting the recommended tests.
  
* **URL**

  recommended-test/

* **Method:**

  `GET` 
  
*  **URL Params**
  
    **Optional:** <br>
                  
    Specify the index of the first recommended test to be retrieved: <br>
    `start=[integer]`
                    
    Specify the maximum number of recommended tests to be retrieved:  <br>
    `number=[integer]`
    
    Set the parameter to 'random' to shuffle the recommended tests randomly. Otherwise the tests are ordered by 
     their id. <br> 
    `mode = [string]`
         
  
* **Data Params**

    An authorization header has to be provided. The key is 'token' 
    and the value should be a string of the form "token 3e8XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX3481". 
    
* **Success Response:**

  * **Code:** 200 OK <br />
    **Content:** 
    ```json
    [
        {
            "id": 8,
            "user_profile": 1,
            "questions": [
                31,
                32,
                33,
                34,
                35
            ],
            "title": "Brüche addieren",
            "html": "<h1> Brüche addieren </h1>",
            "created_on": "2020-04-13T21:41:48.048939Z"
        }
    ]
    ```
  OR 
  
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
   recommended_test_get = requests.get(url=base_url + "recommended-test/",
                             headers=headers,
                             params={'number': 1}
                             )
   print(recommended_test_get.json())
  ``` 
     
  This request should get a status 200 OK and print:
  ```python
  [
    {
        "id": 8,
        "user_profile": 1,
        "questions": [
            31,
            32,
            33,
            34,
            35
        ],
        "title": "Brüche addieren",
        "html": "<h1> Brüche addieren </h1>",
        "created_on": "2020-04-13T21:41:48.048939Z"
    }
  ]
  ```
    
* **Notes:**

  The tests are recommended based on the results of other tests.     
