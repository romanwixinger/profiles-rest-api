**Create user profile**
----
  This view handles creating user profiles.

* **URL**

  profile

* **Method:**

  `POST` 
  
*  **URL Params**

    There are no URL parameters. 

* **Data Params**

  The body should be a JSON object with the keys 'email', 'name' and password'. The values should be non-empty strings. 

* **Success Response:**
  
  * **Code:** 201 Created <br />
    **Content:** `{ "id": 1, "email": "email@email.ch", "name": "Name"}`
 
* **Error Response:**

  * **Code:** 400 Bad Request <br />
    **Content:** `{"email": [ "Enter a valid email address."]}`

  OR
  
  * **Code:** 400 Bad Request <br />
      **Content:** `{"email": ["user profile with this email already exists."]}`
  
  OR
  

  * **Code:** 400 Bad Request <br />
    **Content:** `{"name": [ "This field may not be blank." ],"password": [ "This field may not be blank."]}`

* **Sample Call:**
    ```python
    import requests
    base_url = 'http://127.0.0.1:8000/api/'
    user_profile = {'email': 'email@email.com','name': 'Name', 'password': 'PW'}
    user_profile_post = requests.post(url=base_url + "profile", json=user_profile)
    print(user_profile_post.json())
    ```
    
    This should print:
    ```python
    {'id': 1, 'email': 'email@email.com', 'name': 'Name'}
    ```
    
* **Notes:**

  The http method `PUT' works in a similar manner. One has to specify the id in the url by adding /id. 
