**Retrieve recommended theory pages**
----
  This is a request for retrieving the recommended theory pages of a user. 
  
* **URL**

  recommended-theory-page

* **Method:**

  `GET' 
  
*  **URL Params**

   **Optional:** <br>
                   
    Specify the index of the first recommended theory page to be retrieved: <br>
    `start=[integer]`
                      
    Specify the maximum number of recommended theory pages to be retrieved:  <br>
    `number=[integer]`
    
    Set the parameter to 'random' to shuffle the recommended theory pages randomly. Otherwise, the theory pages are 
    ordered by their id. <br> 
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
            "id": 17,
            "user_profile": 1,
            "created_on": "2020-04-18T14:43:18.309431Z",
            "updated_on": "2020-04-18T14:43:18.309431Z",
            "topic": 12,
            "subtopic": 13,
            "title": "Folgen",
            "html": "<h1> Folgen </h1>",
            "test": 10
        }
    ]
    ```
    
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
    recommended_theory_page_get = requests.get(url=base_url + "recommended-theory-page", 
                                     headers=headers)
    print(recommended_theory_page_get.json())
     ``` 
     
    This request should get a status 200 OK and print
    ```python
    [
        {
            "id": 17,
            "user_profile": 1,
            "created_on": "2020-04-18T14:43:18.309431Z",
            "updated_on": "2020-04-18T14:43:18.309431Z",
            "topic": 12,
            "subtopic": 13,
            "title": "Folgen",
            "html": "<h1> Folgen </h1>",
            "test": 10
        }
    ]
   ```
    
* **Notes:**

   The theory pages are recommended based on the test results. 
