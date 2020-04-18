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
user_profile = {'email': 'email@email.com', 'name': 'Name', 'password': 'PW'}
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




"""Question"""

print("\n" + 30 * "*" + " Subtopic " + 30 * "*" + "\n")

# Question POST
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
print("\n" + 10 * "*" + "\n")

# Question GET
question_get = requests.get(url=base_url + "custom-question/", 
                            headers=headers, 
                            params={"number": 2}
                            )
print(question_get.json())



"""Answer"""

print("\n" + 30 * "*" + " Answer " + 30 * "*" + "\n")

# Answer POST
answer =  {"question": 32, "duration": 5.5, "answers": "5/2", "skipped": False, 
           "comment": "I am not sure about the answer."}
answer_post = requests.post(url=base_url + "custom-answer/", 
                            headers=headers,
                            json=answer)
print(answer_post.json())
print("\n" + 10 * "*" + "\n")

# Answer GET
answer_get = requests.get(url=base_url + "custom-answer/", 
                          headers=headers,
                          params={'number': 1})
print(answer_get.json())



"""Test"""

print("\n" + 30 * "*" + " Test " + 30 * "*" + "\n")

# Test POST
test =  {
            "questions": "31;32;33;34",
            "title": "Brüche subtrahieren",
            "html": "<h1> Brüche subtrahieren </h1>"
        }
test_post = requests.post(url=base_url + "custom-test/",
                          headers=headers,
                          json=test
                          )
print(test_post.json())
print("\n" + 10 * "*" + "\n")

test_get = requests.get(url=base_url + "custom-test/",
                          headers=headers,
                          params={'number': 1}
                          )
print(test_get.json())



"""CompletedTest"""

print("\n" + 30 * "*" + " CompletedTest " + 30 * "*" + "\n")

# CompletedTest POST
completed_test = {
    "answers": 
                [{
                        "question": 31,
                        "duration": "21.00",
                        "answers": "1/3",
                        "skipped": False
                },
                {
                        "question": 32,
                        "duration": "24.00",
                        "answers": "1/2",
                        "skipped": False
                }],
    "state": "First question answered",
    "duration": "12.00"
}
completed_test_post = requests.post(url=base_url + "custom-completed-test/",
                                    headers=headers,
                                    json=completed_test
                                    )
print(completed_test_post.json())
print("\n" + 10 * "*" + "\n")

completed_test_get = requests.get(url=base_url + "custom-completed-test/",
                                    headers=headers
                                    )
print(completed_test_get.json())


"""TheoryPage"""

print("\n" + 30 * "*" + " TheoryPage " + 30 * "*" + "\n")

# TheoryPage POST
theory_page = {
        "subtopic": "Folgen",
        "title": "Folgen",
        "html": "<h1> Folgen </h1>",
        "test": "Brüche subtrahieren"
}
theory_page_post = requests.post(url=base_url + "custom-theory-page/", 
                                 headers=headers,
                                 json=theory_page)
print(theory_page_post.json())
print("\n" + 10 * "*" + "\n")

theory_page_get = requests.get(url=base_url + "custom-theory-page/", 
                                 headers=headers)
print(theory_page_get.json())



"""RecommendedTheoryPage"""

print("\n" + 30 * "*" + " RecommendedTheoryPage " + 30 * "*" + "\n")

# RecommendedTheoryPage GET 
recommended_theory_page_get = requests.get(url=base_url + "recommended-theory-page/", 
                               headers=headers)
print(recommended_theory_page_get.json())



"""RecommendedTest"""

print("\n" + 30 * "*" + " RecommendedTest " + 30 * "*" + "\n")

# RecommendedTest GET
recommended_test_get = requests.get(url=base_url + "recommended-test/",
                                    headers=headers,
                                    params={'number': 1}
                                    )
print(recommended_test_get.json())
