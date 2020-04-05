from django.db import models
from django.conf import settings

from profiles_api.question.question_model import Question

import re


class Answer(models.Model):
    """Answer"""
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    created_on = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    duration = models.DecimalField(max_digits=8, decimal_places=2, blank=True) # in seconds
    answers = models.CharField(max_length=1024, blank=True)

    # Fields set after correction
    correct = models.BooleanField(blank=True)
    skipped = models.BooleanField(blank=True)
    comment = models.CharField(max_length=1024, blank=True)

    def __str__(self):
        """Return the model as a string"""
        return self.answers

    def performCorrection(self):
        """Corrects the answer"""
        validation = self.question.validation

        if self.skipped is not None and self.skipped:
            return
        if self.answers is None or self.answers == '':
            self.correct = False
            return

        # Standard validation
        if validation is None or validation == '':
            self.correct = self.answers == self.question.correctAnswers
            return

        # Multiple strings
        if validation == 'multipleStrings':
            answerList = self.answers.split(';')
            correctAnswerList = self.question.correctAnswers.split(';')
            wrongAnswerList = []
            for i in range(len(answerList)):
                if answerList[i] != correctAnswerList[i]:
                    wrongAnswerList.append(str(i+1))
            if len(wrongAnswerList) == 0:
                self.correct = True
            elif len(wrongAnswerList) == 1:
                self.correct = False
                separator = ', '
                self.comment = str("Das Antwortfeld " + separator.join(wrongAnswerList) + " ist noch nicht korrekt ausgefüllt.")
            else:
                self.correct = False
                separator = ', '
                self.comment = "Die Antwortfelder " + separator.join(wrongAnswerList) + " sind noch nicht korrekt ausgefüllt."

        # Single fractions
        if validation == 'singleFraction':
            answerFloat = 1
            correctAnswerFloat = 1

            # Convert decimal or int to float
            if not bool(re.search('/', self.answers)) and not bool(re.search(':', self.answers)):
                answerFloat = float(self.answers)
            # Convert fraction to float
            else:
                try:
                    p = re.compile(r'\d+').findall(self.answers)
                    nominator = int(p[0])
                    denominator = int(p[1])
                    answerFloat = float(nominator/denominator)
                    print(answerFloat)
                except:
                    self.comment = "Die Frage konnte nicht korrigiert werden."
                    return
            if not bool(re.search('frac', self.question.correctAnswers)) and not bool(re.search('/', self.answers)):
                correctAnswerFloat = float(self.question.correctAnswers)
            # Convert fraction to float
            else:
                try:
                    p = re.compile(r'\d+').findall(self.question.correctAnswers)
                    nominator = int(p[0])
                    denominator = int(p[1])
                    correctAnswerFloat = float(nominator/denominator)
                    print(answerFloat)
                except:
                    self.comment = "Die Frage konnte nicht korrigiert werden."
                    return

            self.correct = abs(answerFloat - correctAnswerFloat) <= 1e-3
            return
        else:
            return
