**Create recommended tests**
----
  This is a request for creating a test that is personalised. 
  
* **URL**

  recommended-test

* **Method:**

  `GET` 
  
*  **URL Params**
  
    **Optional:** <br>
                    
    Specify the maximum number of recommended subtopics to be tested:  <br>
    `number=[integer]`
    
    Specify the maximum number of questions per subtopic to be tested:  <br>
    `length=[integer]`
         
  
* **Data Params**

    An authorization header has to be provided. The key is 'token' 
    and the value should be a string of the form "token 3e8XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX3481". 
    The questions are selected by the REST API and are not sent in the request's body. 
    
* **Success Response:**

  * **Code:** 201 Created <br />
    **Content:** 
    ```json
    {
        "id": 74,
        "user_profile": 1,
        "questions": [
            41,
            42,
            66,
            67
        ],
        "title": "Persönliche Übungen",
        "html": "",
        "created_on": "2020-05-03T08:08:20.387275Z"
    }
    ```
  
* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** `{ detail : "Authentication credentials were not provided." }`

    
* **Sample Call:**

   ```python
   import requests
   base_url = 'http://127.0.0.1:8000/api/'
   token = '3e8eXXXXXXXXXXXXXXXXXXXXXXXXXXX3481'
   headers =  {'Authorization': 'token ' + token}
   recommended_test_post = requests.post(url=base_url + "recommended-test",
                             headers=headers,
                             params={'number': 3, 'length': 2}
                             )
   print(recommended_test_post.json())
  ``` 
     
  This request should get a status 201 Created and print:
  ```python
  {
      "id": 92,
      "user_profile": 1,
      "questions": [
          41,
          42,
          43,
          44,
          66,
          67
      ],
      "title": "Persönliche Übungen",
      "html": "",
      "created_on": "2020-05-03T08:19:36.067806Z"
  }
  

  ```
    
* **Notes:**

  The tests are recommended based on the results of other tests.     
