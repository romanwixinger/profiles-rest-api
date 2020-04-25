**Create completed test**
----
  This is a simple for creating completed tests.
  
* **URL**

  custom-completed-test/

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
         "answers": 
     [{
             "question": 31,
             "duration": "21.00",
             "answers": "1/3",
             "skipped": false
     },
     {
             "question": 32,
             "duration": "24.00",
             "answers": "1/2",
             "skipped": false
     }],
         "state": "First question answered",
         "duration": "12.00",
         "comment": "This questions are easy!"
     }
    ```
    
    Here 'answers' is not required, may be an empty list but must not be blank. This will be a useful feature when HTTP PATCH is released. 
    The answers have to be given in the form specified in the POST method of Answer. Both fields 'state' and 'duration' 
    are required and may not be blank. The field 'comment' is optional but may not be blank. 
 
    
* **Success Response:**

  * **Code:** 201 Created <br />
    **Content:** 
    ```json
    {
        "id": 26,
        "user_profile": 1,
        "answers": [
            127,
            128
        ],
        "state": "First question answered",
        "created_on": "2020-04-17T20:37:28.593765Z",
        "updated_on": "2020-04-17T20:37:28.593765Z",
        "duration": "12.00",
        "comment": "",
        "recommendedSubtopics": [
            13
        ]
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
        "state": [
            "This field may not be blank."
        ],
        "duration": [
            "This field may not be null."
        ]
    }
    ```
    
    OR
    
    * **Code:** 400 Bad Request <br />
        **Content:** `{"answers": "The question to one of the answers does not exist."}`

    
* **Sample Call:**

   ```python
   import requests
   base_url = 'http://127.0.0.1:8000/api/'
   token = '3e8eXXXXXXXXXXXXXXXXXXXXXXXXXXX3481'
   headers =  {'Authorization': 'token ' + token}
   completed_test = {
      "answers": 
                [{
                        "question": 31,
                        "duration": "21.00",
                        "answers": "1/3",
                        "skipped": False
                },
                {
                        "question": 32,
                        "duration": "24.00",
                        "answers": "1/2",
                        "skipped": False
                }],
      "state": "First question answered",
      "duration": "12.00"
      }
  completed_test_post = requests.post(url=base_url + "custom-completed-test/",
                                    headers=headers,
                                    json=completed_test
                                    )
  print(completed_test_post.json())
  ``` 
     
  This request should get a status 201 Created and print:
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
