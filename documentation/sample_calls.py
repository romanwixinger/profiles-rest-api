# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 20:23:16 2020

@author: roman

Intention: Sample calls
"""

import requests


base_url = 'http://127.0.0.1:8000/api/'
email = 'Schueler1@email.com'
name = 'Schueler 1'
password = 'Schueler 1'


"""User profile"""

print("\n" + 30 * "*" + " User profile " + 30 * "*" + "\n")

# User profile POST
user_profile = {'email': email, 'name': name, 'password': password}
user_profile_post = requests.post(url=base_url + "profile", json=user_profile)

if user_profile_post.status_code == 201: 
    print(user_profile_post.json())
    user_id = user_profile_post.json()['id']
else: 
    user_profile_get = requests.get(url=base_url + "profile", params={'search': email})
    print(user_profile_get.json())
    user_id = [user for user in user_profile_get.json()][0]['id']
    
print("Status code: ", user_profile_post.status_code)
print(user_profile_post.json())
print("\n" + 10 * "*" + "\n")


# User profile GET
user_profile_get = requests.get(url=base_url + "profile")

print("Status code: ", user_profile_get.status_code)
print(user_profile_get.json())
print("\n" + 10 * "*" + "\n")


# User profile GET for single user profile
user_profile_get = requests.get(url=base_url + "profile/" + str(user_id))

print("Status code: ", user_profile_get.status_code)
print(user_profile_get.json())


"""Login"""

print("\n" + 30 * "*" + " Login " + 30 * "*" + "\n")

# Create token with POST
credentials =  {'username': 'Schueler2@email.com', 'password': 'Schueler 2'}
login_post = requests.post(url=base_url + "login", json=credentials)
token = login_post.json()['token']
print("Status code: ", login_post.status_code)
print(login_post.json())



"""Topic"""

print("\n" + 30 * "*" + " Topic " + 30 * "*" + "\n")

# Topic POST
topic = {'name': 'Division of fractions'}
headers =  {'Authorization': 'token ' + token}
topic_post = requests.post(url=base_url + "custom-topic", 
                           json=topic, 
                           headers=headers)
topic_id = topic_post.json()['id']

print("Status code: ", topic_post.status_code)
print(topic_post.json())
print("\n" + 10 * "*" + "\n")


# Topic GET
topic_get = requests.get(url=base_url + "custom-topic", 
                         headers=headers, 
                         params = {'number': 1})
print("Status code: ", topic_get.status_code)
print(topic_get.json())



"""Subtopic"""

print("\n" + 30 * "*" + " Subtopic " + 30 * "*" + "\n")

# Subtopic POST
subtopic = {"name": "Brüche addieren", "html": "<h1> Brüche addieren </h1>", 
            "topic": 'Division of fractions'}
subtopic_post = requests.post(url=base_url + "custom-subtopic", 
                              headers=headers,
                              json=subtopic)
subtopic_id = subtopic_post.json()['id']
print("Status code: ", subtopic_post.status_code)
print(subtopic_post.json())
print("\n" + 10 * "*" + "\n")


# Subtopic GET
subtopic_get = requests.get(url=base_url + "custom-subtopic", 
                            headers=headers, 
                            params={'topic_id': topic_id, 'number': 1}
                            )
print("Status code: ", subtopic_get.status_code)
print(subtopic_get.json())



"""Question"""

print("\n" + 30 * "*" + " Question " + 30 * "*" + "\n")

# Question POST
question = {
        "subtopic_id": subtopic_id,
        "question": "$\\\\frac{3}{7} + \\\\frac{2}{7}$",
        "correctAnswers": "$\\\\frac{4}{7}}$",
        "validation_type": "standardValidation",
        "dependencies_id": "13;14",
        "set_difficulty": 2
    }
question_post = requests.post(url=base_url + "custom-question",
                              headers=headers,
                              json=question)
question_id = question_post.json()['id']

print("Status code: ", question_post.status_code)
print(question_post.json())
print("\n" + 10 * "*" + "\n")


# Question GET
question_get = requests.get(url=base_url + "custom-question", 
                            headers=headers, 
                            params={"number": 1, "question_id": 687}
                            )
print("Status code: ", question_get.status_code)
print(question_get.json())



"""Answer"""

print("\n" + 30 * "*" + " Answer " + 30 * "*" + "\n")

# Answer POST
answer =  {"question": question_id, "duration": 5.5, "answers": "5/2", "skipped": False, 
           "comment": "I am not sure about the answer."}
answer_post = requests.post(url=base_url + "custom-answer", 
                            headers=headers,
                            json=answer)
print("Status code: ", answer_post.status_code)
print(answer_post.json())
print("\n" + 10 * "*" + "\n")

# Answer GET
answer_get = requests.get(url=base_url + "custom-answer", 
                          headers=headers,
                          params={'number': 1})
print("Status code: ", answer_get.status_code)
print(answer_get.json())
print("\n" + 10 * "*" + "\n")

# Answer PATCH
answer = {"duration": 20, "answers": "new answer"}
answer_patch = requests.patch(url=base_url + "custom-answer/7352",
                            headers=headers,
                            json=answer)
print("Status code: ", answer_patch.status_code)

"""Test"""

print("\n" + 30 * "*" + " Test " + 30 * "*" + "\n")

# Test POST
test =  {
            "questions": str(question_id),
            "title": "Brüche addieren",
            "html": "<h1> Brüche addieren </h1>"
        }
test_post = requests.post(url=base_url + "custom-test",
                          headers=headers,
                          json=test
                          )
print("Status code: ", test_post.status_code)
print(test_post.json())
print("\n" + 10 * "*" + "\n")

test_get = requests.get(url=base_url + "custom-test",
                          headers=headers,
                          params={'number': 1}
                          )
print("Status code: ", test_get.status_code)
print(test_get.json())



"""CompletedTest"""

print("\n" + 30 * "*" + " CompletedTest " + 30 * "*" + "\n")

# CompletedTest POST
completed_test = {
    "answers": 
                [{
                        "question": 852,
                        "duration": 21.00,
                        "answers": "1/3",
                        "skipped": False
                },
                {
                        "question": 853,
                        "duration": 24.00,
                        "answers": "1/2",
                        "skipped": False
                }],
    "state": "First question answered",
    "duration": "12.00",
    "test": 470
}
completed_test_post = requests.post(url=base_url + "custom-completed-test",
                                    headers=headers,
                                    json=completed_test
                                    )
print("Status code: ", completed_test_post.status_code)
print(completed_test_post.json())
print("\n" + 10 * "*" + "\n")


# CompletedTest GET
completed_test_get = requests.get(url=base_url + "custom-completed-test",
                                    headers=headers,
                                    params = {'number': 1})

print("Status code: ", completed_test_get.status_code)
print(completed_test_get.json())


# CompletedTest Patch
completed_test_patch = completed_test = {
    "answers": 
                [{
                        "question": 687,
                        "duration": "21.00",
                        "answers": "1/3",
                        "skipped": False
                }],
    "state": "New questions answered."
}
completed_test_patch = requests.patch(url=base_url + "custom-completed-test/167",
                                    headers=headers,
                                    json=completed_test_patch
                                    )
print("Status code: ", completed_test_patch.status_code)

"""TheoryPage"""

print("\n" + 30 * "*" + " TheoryPage " + 30 * "*" + "\n")

# TheoryPage POST
theory_page = {
        "subtopic": "Anteile",
        "title": "Folgen",
        "html": "<h1> Folgen </h1>",
        "test_id": 470
}
theory_page_post = requests.post(url=base_url + "custom-theory-page", 
                                 headers=headers,
                                 json=theory_page)
print("Status code: ", theory_page_post.status_code)
print(theory_page_post.json())
print("\n" + 10 * "*" + "\n")

theory_page_get = requests.get(url=base_url + "custom-theory-page", 
                                 headers=headers,
                                 params = {'number': 1})
print("Status code: ", theory_page_get.status_code)
print(theory_page_get.json())



"""RecommendedTheoryPage"""

print("\n" + 30 * "*" + " RecommendedTheoryPage " + 30 * "*" + "\n")

# RecommendedTheoryPage GET 
recommended_theory_page_get = requests.get(url=base_url + "recommended-theory-page", 
                               headers=headers)
print("Status code: ", recommended_theory_page_get.status_code)
print(recommended_theory_page_get.json())



"""RecommendedTest"""

print("\n" + 30 * "*" + " RecommendedTest " + 30 * "*" + "\n")

# RecommendedTest GET
recommended_test_get = requests.get(url=base_url + "recommended-test",
                                    headers=headers,
                                    params={'number': 1}
                                    )
print("Status code: ", recommended_test_get.status_code)
print(recommended_test_get.json())
print("\n" + 10 * "*" + "\n")

# RecommendedTest POST
recommended_test_post = requests.post(url=base_url + "recommended-test",
                                    headers=headers,
                                    params={'number': 5, 'length': 1}
                                    )
print("Status code: ", recommended_test_post.status_code)
print(recommended_test_post.json())
print("\n" + 10 * "*" + "\n")



"""RecommendedTest"""

print("\n" + 30 * "*" + " RecommendedSubtopic " + 30 * "*" + "\n")

# RecommendedSubtopic GET
recommended_subtopic_get = requests.get(url=base_url + "recommended-subtopic",
                                    headers=headers,
                                    params={'number': 1}
                                    )
print("Status code: ", recommended_subtopic_get.status_code)
print(recommended_subtopic_get.json())
print("\n" + 10 * "*" + "\n")






