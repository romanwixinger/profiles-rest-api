# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 20:23:16 2020

@author: roman

Intention: Sample calls
"""

import requests


base_url = 'http://127.0.0.1:8000/api/'


"""User profile"""

print("\n" + 30 * "*" + " User profile " + 30 * "*" + "\n")

# User profile POST
user_profile = {'email': 'email@email.com','name': 'Name', 'password': 'PW'}
user_profile_post = requests.post(url=base_url + "profile/", json=user_profile)
print(user_profile_post.json())
print("\n" + 10 * "*" + "\n")

# User profile GET
user_profile_get = requests.get(url=base_url + "profile/")
print(user_profile_get.json())
print("\n" + 10 * "*" + "\n")

# User profile GET for single user profile
user_id = "1"
user_profile_get = requests.get(url=base_url + "profile/" + user_id)
print(user_profile_get.json())




"""Login"""

print("\n" + 30 * "*" + " Login " + 30 * "*" + "\n")

# Create token with POST
credentials =  {'username': 'email@email.com', 'password': 'PW'}
login_post = requests.post(url=base_url + "login/", json=credentials)
print(login_post.json())



"""Topic"""

print("\n" + 30 * "*" + " Topic " + 30 * "*" + "\n")

# Topic POST
topic = {'name': 'Division of fractions'}
token = '3e8e8c442748d5c05e34079f24b4b105f63d3481'
headers =  {'Authorization': 'token ' + token}
topic_post = requests.post(url=base_url + "custom-topic/", 
                           json=topic, 
                           headers=headers)
print(topic_post.json())
print("\n" + 10 * "*" + "\n")

# Topic GET
topic_get = requests.get(url=base_url + "custom-topic/", headers=headers)
print(topic_get.json())



"""Subtopic"""

print("\n" + 30 * "*" + " Subtopic " + 30 * "*" + "\n")

# Subtopic POST
subtopic = {"name": "Brüche addieren", "html": "<h1> Brüche addieren </h1>", 
            "topic": 1}
subtopic_post = requests.post(url=base_url + "custom-subtopic/", 
                              headers=headers,
                              json=subtopic)
print(subtopic_post.json())
print("\n" + 10 * "*" + "\n")

# Subtopic GET
subtopic_get = requests.get(url=base_url + "custom-subtopic/", 
                            headers=headers, 
                            params={'topic_id': 12}
                            )
print(subtopic_get.json())



"""Answer"""

print("\n" + 30 * "*" + " Answer " + 30 * "*" + "\n")
answer =  {"question": 32, "duration": 5.5, "answers": "5/2", "skipped": False, 
           "comment": "I am not sure about the answer."}
answer_post = requests.post(url=base_url + "custom-answer/", 
                            headers=headers,
                            json=answer)
print(answer_post.json())






