**Get user profiles**
----
  This view handles getting user profiles.

* **URL**

  profile <br>
  profile/id

* **Method:**

  `Get` 
  
*  **URL Params**

    There are no URL parameters. 

* **Data Params**

    There is no Body to be provided. 
    
* **Success Response:**
  
  * **Code:** 200 Ok <br />
    **Content:** `[{ "id": 1, "email": "email@email.com", "name": "Roman"}]`
 
* **Error Response:**

    If an non-existing id is given in the URL, then the following response is given: 
    
  * **Code:** 404 Not Found <br />
    **Content:** `{"detail": "Not found."}`

* **Sample Call:**
    ```python
    import requests
    base_url = 'http://127.0.0.1:8000/api/'
    user_profile_get = requests.get(url=base_url + "profile")
    print(user_profile_get.json())
    ```
    
    This should print:
    ```python
    [{'id': 1, 'email': 'email1@email.com', 'name': 'Name1'}, ... ,  
    {'id': 6, 'email': 'email6@email.com', 'name': 'Name6'}]
    ```
    
* **Notes:**

  One has to specify the id in the url by adding /id/ if a certain user profile should be retrieved.
