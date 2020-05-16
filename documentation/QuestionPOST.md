**Create questions**
----
  This is a simple for creating questions. 
  
* **URL**

  custom-question/

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
            "subtopic": 13,
            "dependencies": "Brüche addieren",
            "dependencies_id": "1;3;8",
            "question": "$\\\\frac{3}{7} + \\\\frac{12}{7}$",
            "correctAnswers": "$\\\\frac{15}{7}}$",
            "appendix": "mL",
            "hint": "Addiere die beiden Zähler.",
            "imageSrc": "http://...",
            "validation_type": "singleFraction",
            "set_difficulty": 2
     }
     ```
    
    The fields 'question' and 'correctAnswers' are strictly required. The fields 'subtopic', 'subtopic_id'
    'dependencies', 'dependencies_id', appendix', 'hint' and 'imageSrc' are optional but must not be left blank. The 
    subtopic has to be specified by using one of the possible fields. The 
    field 'validation_type' is optional, must not be left blank and defaults to 'standardValidation.' Other valid values 
    for this field are 'standardValidation', 'singleFraction' and 'multipleString'. The topic is deduced from the 
    subtopic.
    
    
* **Success Response:**

  * **Code:** 201 Created <br />
    **Content:** 
    ```json
    {
        "id": 81,
        "created_on": "2020-04-17T18:25:44.169382Z",
        "topic": 22,
        "subtopic": 46,
        "dependencies": [1, 3, 8, 9],
        "question": "$\\\\frac{3}{7} + \\\\frac{12}{7}$",
        "correctAnswers": "$\\\\frac{15}{7}}$",
        "appendix": "",
        "hint": "",
        "imageSrc": "",
        "user_profile": 1,
        "validation_type": "singleFraction",
        "set_difficulty": 2
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
        "dependencies": [
            "This field may not be blank."
        ],
        "appendix": [
            "This field may not be blank."
        ]
    }
    ```

* **Sample Call:**

    ```python
    import requests
    base_url = 'http://127.0.0.1:8000/api/'
    token = '3e8eXXXXXXXXXXXXXXXXXXXXXXXXXXX3481'
    headers =  {'Authorization': 'token ' + token}
    question = {
            "topic": 12,
            "subtopic": 13,
            "question": "$\\\\frac{3}{7} + \\\\frac{12}{7}$",
            "correctAnswers": "$\\\\frac{15}{7}}$",
            "validation_type": "standardValidation"
            }
    question_post = requests.post(url=base_url + "custom-question/",
                                  headers=headers,
                                  json=question)
    print(question_post.json())
     ``` 
     
     This request should get a status 201 Created and print:
     ```python
      {
          'id': 82, 
          'created_on': '2020-04-17T18:56:11.262467Z', 
          'topic': 22, 
          'subtopic': 47, 
          'dependencies': [1, 3, 8, 9], 
          'question': '$\\\\frac{3}{7} + \\\\frac{12}{7}$', 
          'correctAnswers': '$\\\\frac{15}{7}}$', 
          'appendix': '', 
          'hint': '', 
          'imageSrc': '', 'user_profile': 6, 
          'validation_type': 'singleFraction'
      }
     ```
    
* **Notes:**

