**Retrieve subtopics**
----
  This is a request for retrieving subtopics. 
  
* **URL**

  custom-subtopic/

* **Method:**

  `GET' 
  
*  **URL Params**

     **Optional:** <br>
     
      Specify the index of the first topic to be retrieved: <br>
      `start=[integer]`
       
      Specify the maximum number of topics to be retrieved:  <br>
      `number=[integer]`
       
      Specify the topic of the subtopic by its name: <br>
      `topic=[string]`
       
      Specify the topic of the subtopic by its id: <br>
      `topic_id=[integer]`

      Set the parameter to 'random' to shuffle the subtopics randomly. Otherwise, the subtopics are 
      ordered by their id. <br> 
      `mode = [string]`
  
* **Data Params**

    An authorization header has to be provided. The key is 'token' 
    and the value should be a string of the form "token 3e8XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX3481". 
    
    The body should be a JSON object of the following form: <br>
    `{"name": "Brüche addieren", "html": "<h1> Brüche addieren </h1>", "topic": 1}` <br>
    All the fields are required but 'html' can have an empty string as value.
    
    
* **Success Response:**

  * **Code:** 201 Created <br />
    **Content:** `{"id": 44, "user_profile": 1, "name": "Brüche subtrahieren", "html": "<h1> Brüche subtrahieren </h1>",
     "topic": 22}`
     
  OR
    
  * **Code:** 200 OK <br />
    **Content:** `[{ "id": 13, "user_profile": 1, "name": "Brüche addieren", "html": "", "topic": 12}]`
                  
  OR
                  
  * **Code:** 204 No Content <br />
 
* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** `{ detail : "Authentication credentials were not provided." }`

  OR

  * **Code:** 400 Bad Request <br />
    **Content:** `{ 
                      "name": ["This field is required."], 
                      "html": ["This field is required."], 
                      "topic": ["This field is required."] 
                  }`

* **Sample Call:**

    ```python
    import requests
    base_url = 'http://127.0.0.1:8000/api/'
    token = '3e8eXXXXXXXXXXXXXXXXXXXXXXXXXXX3481'
    headers =  {'Authorization': 'token ' + token}
    subtopic_get = requests.get(url=base_url + "custom-subtopic/", 
                            headers=headers, 
                            params={'topic_id': 12}
                            )
    print(subtopic_get.json())
     ``` 
     
     This request should get a status 200 OK and print
     ```python
      [{'id': 13, 'user_profile': 1, 'name': 'Brüche addieren', 'html': '', 'topic': 12}]     
     ```
     if a subtopic with a topic with id 1 exists. Otherwise, one gets a status 204 No Content. 
    
* **Notes:**

   
