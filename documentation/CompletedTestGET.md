**Retrieve completed test**
----
  This is a simple for retrieving completed tests. 
  
* **URL**

  custom-completed-test

* **Method:**

  `GET` 
  
*  **URL Params**

    **Optional:** <br>
                    
    Specify the id of the completed test: <br>
    `id=[integer]`
    
    Specify the index of the first completed tests to be retrieved: <br>
    `start=[integer]`
                  
    Specify the maximum number of completed tests to be retrieved:  <br>
    `number=[integer]`
    
    Set the parameter to 'random' to shuffle the completed tests randomly. <br> 
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
            "id": 25,
            "user_profile": 1,
            "answers": [
                107,
                108,
                109
            ],
            "state": "started",
            "created_on": "2020-04-17T20:28:57.908528Z",
            "updated_on": "2020-04-17T20:28:57.908528Z",
            "duration": "105.00",
            "comment": "I did not answer all questions.",
            "recommendedSubtopics": []
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
   completed_test_get = requests.get(url=base_url + "custom-completed-test",
                                      headers=headers
                                      )
   print(completed_test_get.json())
  ``` 
     
  This request should get a status 200 OK and print:
  ```python
  {
      'id': 31, 
      'user_profile': 6, 
      'answers': [132, 133], 
      'state': 'First question answered', 
      'created_on': '2020-04-17T21:10:08.800956Z', 
      'updated_on': '2020-04-17T21:10:08.800956Z', 
      'duration': '12.00', 
      'comment': '', 
      'recommendedSubtopics': [13]
  }
  ```
    
* **Notes:**

    This request is intended to be used with a corresponding HTTP PATCH request. However, this method is not 
    released yet.
