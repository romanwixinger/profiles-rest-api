import numpy as np
import scipy.special
from scipy.stats import binom, norm
from scipy.optimize import minimize

from profiles_api.answer.answer_service import AnswerService


class KnowledgeLevelService:
    """Class for knowledge level estimation"""

    @classmethod
    def knowledge_level_list(cls, user_id: int, subtopic_id_list: [int]) -> dict:
        """Get the knowledge level of a user for a list of subtopics"""

        level_dict = {}

        for subtopic_id in subtopic_id_list:
            level = cls.knowledge_level(user_id=user_id, subtopic_id=subtopic_id)
            level_dict[subtopic_id] = level

        return level_dict

    @classmethod
    def knowledge_level(cls, user_id: int, subtopic_id: int):
        """Get the knowledge level of a user in a specific subtopic. The knowledge level takes values between 1 to 5
        where 5 is the best level. If the user did not give any answers in this subtopic, the level is 0."""

        data = cls.__get_knowledge_data(user_id=user_id, subtopic_id=subtopic_id)
        if data == {}:
            return 0

        level = cls.__knowledge_level_estimation(data)
        return level

    @classmethod
    def __get_knowledge_data(cls, user_id: int, subtopic_id: int) -> np.array:
        """Get the data necessary for the estimation of the knowledge level"""

        query_params_dict = {'user_id': user_id,
                             'subtopic_id': subtopic_id}
        answers = AnswerService.search_answers(query_params_dict)

        # Gather necessary information about the answers
        question_id_list = [answer.question.id for answer in answers]
        if len(question_id_list) == 0:
            empty_dict = {}
            return empty_dict

        difficulty_list = AnswerService.difficulty_list(question_id_list=question_id_list)
        correctness_list = [answer.correct for answer in answers]

        # Initialise data dict
        data = {}
        for difficulty in np.unique(np.array(difficulty_list)):
            data[difficulty] = {'correct': 0, 'incorrect': 0, 'total': 0, 'ratio': 0.0}

        # Fill information in the dict
        for difficulty, correct in zip(difficulty_list, correctness_list):
            data[difficulty]['total'] += 1
            if correct:
                data[difficulty]['correct'] += 1
            else:
                data[difficulty]['incorrect'] += 1

        for difficulty in difficulty_list:
            data[difficulty]['ratio'] = data[difficulty]['correct'] / (data[difficulty]['correct'] + data[difficulty]['incorrect'])

        return data

    @classmethod
    def __knowledge_level_estimation(cls, data: np.array) -> float:
        """Returns the estimated knowledge level"""

        sigma = 1           # Standard deviation that corresponds to the Q-function
        min_mu = 0          # Minimally allowed value of mu
        max_mu = 6          # Maximally allowed value of mu
        start_mu = 3        # Initial guess for the optimisation of mu
        min_level = 1       # Minimally allowed level
        max_level = 5       # Maximally allowed level
        correct_goal = 0.7  # Desired part of correct answers

        cost_function = lambda mu: cls.__log_likelihood(data=data, mu=mu, sigma=sigma)

        results = minimize(cost_function, x0=np.array([start_mu]), bounds=[(min_mu, max_mu)], options={'disp': False})

        level = results['x'] - norm.ppf(q=correct_goal, scale=sigma)
        level = min(max_level, max(min_level, level + 0.5))

        return int(level)

    @classmethod
    def __log_likelihood(cls, data: dict, mu: float, sigma: float):
        """
        Negative of the natural logarithm of the likelihood that the data occurs given the
        parameters mu, sigma and delta.

        """

        log_prob = 0

        for level in data.keys():

            k = data[level]['correct']
            n = data[level]['total']
            if n == 0:
                continue

            p = cls.__q_function(x=level, mu=mu, sigma=sigma)
            p = max(1e-3, p)
            p = min(1-1e-3, p)

            log_prob += np.log(binom.pmf(k, n, p)) if binom.pmf(k, n, p) != 0 else 0

        return -log_prob

    @classmethod
    def __q_function(cls, x: float, mu: float, sigma: float) -> float:
        """
        Q-function that models the probability of answering the question correctly.
        It is the complementary cumulative distribution function of a Gaussian
        distribution.
        x:      difficulty level
        mu:     position of the peak of the corresponding gaussian distribution
        sigma:  standard deviation of the corresponding gaussian distribution
        """

        erf_argument = (x-mu)/(np.sqrt(2)*sigma)

        return (1 - scipy.special.erf(erf_argument))/2
