**Retrieve questions**
----
  This is a simple for getting questions. 
  
* **URL**

  custom-question/

* **Method:**

  `GET` 
  
*  **URL Params**

    **Optional:** <br>
                
    Specify the index of the first question to be retrieved: <br>
    `start=[integer]`
                  
    Specify the maximum number of questions to be retrieved:  <br>
    `number=[integer]`
       
    Specify the topic of the question by its name: <br>
    `topic=[string]`
                  
    Specify the topic of the question by its id: <br>
    `topic_id=[integer]`
                  
    Specify the subtopic of the question by its name: <br>
    `subtopic=[string]`
                      
    Specify the subtopic of the question by its id: <br>
    `subtopic_id=[integer]`
    
    Specify the difficulty of the question. Allowed difficulties are in [1,2,3,4,5]: <br>
    `difficulty=[integer]`
    
    Set the parameter to 'random' to shuffle the questions randomly. <br> 
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
              "id": 31,
              "created_on": "2020-04-13T21:22:30.321628Z",
              "topic": 12,
              "subtopic": 13,
              "dependencies": [],
              "question": "$\\\\frac{2}{7} + \\\\frac{13}{7}$",
              "correctAnswers": "$\\\\frac{15}{7}}$",
              "appendix": "",
              "hint": "",
              "imageSrc": "",
              "user_profile": 1,
              "validation_type": "standardValidation",
              "set_difficulty": 2
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
    question_get = requests.get(url=base_url + "custom-question/", 
                            headers=headers, 
                            params={"number": 1}
                            )
    print(question_get.json())
     ``` 
     
     This request should get a status 200 OK and print:
     ```python
      [
          {   
              'id': 31, 
              'created_on': '2020-04-13T21:22:30.321628Z', 
              'topic': 12, 'subtopic': 13, 
              'dependencies': [], 
              'question': '$\\\\frac{2}{7} + \\\\frac{13}{7}$', 
              'correctAnswers': '$\\\\frac{15}{7}}$', 
              'appendix': '', 
              'hint': '', 'imageSrc': '', 
              'user_profile': 1, 
              'validation_type': 'standardValidation',
              'set_difficulty': 2
            }
     ]
     ```
    
* **Notes:**

