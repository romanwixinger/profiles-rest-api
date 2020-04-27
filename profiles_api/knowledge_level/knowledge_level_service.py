import numpy as np
import scipy.special
from scipy.stats import binom, norm
from scipy.optimize import minimize

from profiles_api.answer.answer_service import AnswerService


class KnowledgeLevelService:
    """Class for knowledge level estimation"""

    @classmethod
    def knowledge_level(cls, user_id: int, subtopic_id: int):
        """Get the knowledge level of a user in a specific subtopic"""

        data = cls.__get_knowledge_data(user_id=user_id, subtopic_id=subtopic_id)
        level = cls.__knowledge_level_estimation(data)

        return level

    @classmethod
    def __get_knowledge_data(cls, user_id: int, subtopic_id: int) -> np.array:
        """Get the data necessary for the estimation of the knowledge level"""

        query_params_dict = {'user_id': user_id,
                             'subtopic_id': subtopic_id}
        answers = AnswerService.get_answers(query_params_dict)

        correct = 0
        incorrect = 0
        for answer in answers:
            if answer.correct:
                correct += 1
            else:
                incorrect += 1

        data = np.array([[3], [correct], [incorrect]])

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
    def __log_likelihood(cls, data: np.array, mu: float, sigma: float):
        """
        Negative of the natural logarithm of the likelihood that the data occurs given the
        parameters mu, sigma and delta.

        """

        levels = data[0,:]              # Difficulty level that occur in the data
        correct = data[1,:]             # Number of correctly answered questions
        incorrect = data[2,:]           # Number of incorrectly answered questions
        log_prob = 0

        for i, level in enumerate(levels):

            k = correct[i]
            n = correct[i] + incorrect[i]
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
