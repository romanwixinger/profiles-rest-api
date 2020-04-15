**Create token**
----
  Create a Authorization token by providing the credentials. 

* **URL**

  login/

* **Method:**
  
  `POST`
  
*  **URL Params**

   There are no URL parameters. 

* **Data Params**

  The body should contain a JSON object with the keys 'username' and 'password'. The value corresponding to the key 
  'username' has to be the email. 

* **Success Response:**
  
  <_What should the status code be on success and is there any returned data? This is useful when people need to to know what their callbacks should expect!_>

  * **Code:** 200 OK <br />
    **Content:** `{"token": "0f7XXXXXXXXXXXXXXXXXXXXXXXXXXXXX6e"}`
 
* **Error Response:**

  If an invalid email is given, then the following response is given: 
  * **Code:** 400 Bad Request <br />
    **Content:** `{{"username": ["This field is required." ],"password": ["This field is required."]}`

  OR
  
  If a wrong password is provided, then the following response is given. 

  * **Code:** 400 Bad Request <br />
    **Content:** `{"non_field_errors": [ "Unable to log in with provided credentials."]}`

* **Sample Call:**
    
    ```python
    import requests
    base_url = 'http://127.0.0.1:8000/api/'
    credentials =  {'username': 'email@email.com', 'password': 'PW'}
    login_post = requests.post(url=base_url + "login/", json=credentials)
    print(login_post.json())
    ```
    
    This should print
    
    ```python
    {'token': '3e8XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX3481'}
    ```
  
* **Notes:**

    The token can afterwards be put in the header with key 'Authorization' and value 
    'token 3e8XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX3481' for authorization. 
