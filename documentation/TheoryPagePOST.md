**POST theory pages**
----
  This is a request for creating theory pages. 
  
* **URL**

  custom-theory-page

* **Method:**

  `POST' 
  
*  **URL Params**

   There are no query-parameters.
        
 
* **Data Params**

    An authorization header has to be provided. The key is 'token' 
    and the value should be a string of the form "token 3e8XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX3481". 
    
    The body should be a JSON object of the following form: <br>
    ```json
    {
        "subtopic_id": 24,
        "title": "Folgen",
        "html": "<h1> Folgen </h1>",
        "test_id": 11
    }
    ```
    
    OR
    
    ```json
    {
        "subtopic": "Folgen",
        "title": "Folgen",
        "html": "<h1> Folgen </h1>",
        "test": "Brüche subtrahieren"
    }
    ```
    
    At least one of the fields 'subtopic' or 'subtopic_id' has to be filled. Note that 'subtopic' will set the subtopic 
    to the first subtopic that has the given name. The same goes for the fields 'test' and 'test_id'. The field 'title' 
    is required and may not be blank. The field 'html' is not required but may not be left blank too. 
   
    
    
* **Success Response:**

  * **Code:** 201 Created <br />
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
 
* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** `{ detail : "Authentication credentials were not provided." }`

  OR

  * **Code:** 400 Bad Request <br />
    **Content:** `
    ```json
    {
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
    theory_page = {
        "subtopic": "Folgen",
        "title": "Folgen",
        "html": "<h1> Folgen </h1>",
        "test": "Brüche subtrahieren"
    }
    theory_page_post = requests.post(url=base_url + "custom-theory-page", 
                                 headers=headers,
                                 json=theory_page)
    print(theory_page_post.json())
     ``` 
     
    This request should get a status 200 OK and print
    ```python
    {
       'id': 13, 
       'user_profile': 6, 
       'created_on': '2020-04-17T22:47:38.025198Z', 
       'updated_on': '2020-04-17T22:47:38.025198Z', 
       'topic': 15, 'subtopic': 24, 'title': 
       'Folgen', 
       'html': '<h1> Folgen </h1>', 
       'test': 10
    }     
    ```
    
* **Notes:**

   
