# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 20:23:16 2020

@author: roman

Intention: Sample calls
"""

import requests


base_url = 'http://127.0.0.1:8000/api/'


"""User profile"""

# User profile POST
user_profile = {'email': 'email@email.com','name': 'Name', 'password': 'PW'}
user_profile_post = requests.post(url=base_url + "profile/", json=user_profile)
print(user_profile_post.json())

# User profile GET
user_profile_get = requests.get(url=base_url + "profile/")
print(user_profile_get.json())


# User profile GET for single user profile
user_id = "1"
user_profile_get = requests.get(url=base_url + "profile/" + user_id)
print(user_profile_get.json())