**Retrieve recommended subtopics**
----
  This is a request for retrieving recommended subtopics. 
  
* **URL**

  recommended-subtopic/

* **Method:**

  `GET' 
  
*  **URL Params**

     **Optional:** <br>
     
      Specify the maximum number of topics to be retrieved:  <br>
      `number=[integer]`
  
* **Data Params**

    An authorization header has to be provided. The key is 'token' 
    and the value should be a string of the form "token 3e8XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX3481". 
    
* **Success Response:**
    
  * **Code:** 200 OK <br />
    **Content:** `[{ "id": 13, "user_profile": 1, "name": "Brüche addieren", "html": "", "topic": 12}]`
                  
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
    recommended_subtopic_get = requests.get(url=base_url + "recommended-subtopic/",
                                    headers=headers,
                                    params={'number': 1}
                                    )
    print(recommended_subtopic_get.json())
    ``` 
     
    This request should get a status 200 OK and print
    ```python
    [{'id': 13, 'user_profile': 1, 'name': 'Brüche addieren', 'html': '', 'topic': 12}]     
    ```
    if at least one subtopic exists. Otherwise, one gets a status 204 No Content. 
    
* **Notes:**

   
