**Retrieve theory pages**
----
  This is a request for retrieving theory pages. 
  
* **URL**

  custom-theory-page/

* **Method:**

  `GET' 
  
*  **URL Params**

   **Optional:** <br>
                   
    Specify the id of the theory page: <br>
    `id=[integer]`
    
    Specify the title of the theory page: <br>
    `title=[string]`
    
    Set the parameter to 'random' to shuffle the theory pages randomly. Otherwise, the theory pages are 
    ordered by their id. <br> 
    `mode = [string]`
        
* **Data Params**

    An authorization header has to be provided. The key is 'token' 
    and the value should be a string of the form "token 3e8XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX3481". 
   
    
* **Success Response:**

  * **Code:** 200 OK <br />
    **Content:** 
    ```json
    {
        "id": 8,
        "user_profile": 1,
        "created_on": "2020-04-17T22:26:33.743303Z",
        "updated_on": "2020-04-17T22:26:33.743303Z",
        "topic": 15,
        "subtopic": 24,
        "title": "Folgen",
        "html": "<h1> Folgen </h1>",
        "test": 10
    }
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
    theory_page_get = requests.get(url=base_url + "custom-theory-page/", 
                                     headers=headers)
    print(theory_page_get.json())
     ``` 
     
    This request should get a status 200 OK and print
    ```python
    [
      {
          'id': 4, 
          'user_profile': 1, 
          'created_on': '2020-04-17T21:41:03.465351Z', 
          'updated_on': '2020-04-17T21:41:03.466348Z', 
          'topic': 14, 
          'subtopic': 24, 
          'title': 'Folgen und ihre Folgen', 
          'html': '<h1> Folgen </h1>', 'test': 11}, 
          {'id': 5, 
          'user_profile': 1, 
          'created_on': '2020-04-17T22:07:48.453170Z', 
          'updated_on': '2020-04-17T22:07:48.453170Z', 
          'topic': 14, 'subtopic': 24, 
          'title': 'Folgen', 
          'html': '<h1> Folgen </h1>', 
          'test': 11}
   ]
   ```
    
* **Notes:**

   
