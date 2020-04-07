import re

from profiles_api.answer.answer_model import Answer


def perform_correction(answer: Answer):
    """Corrects the answer"""
    validation = answer.question.validation

    if answer.skipped is not None and answer.skipped:
        answer.correct = False
        return
    if answer.answers is None or answer.answers == '':
        answer.correct = False
        return

    # Standard validation
    if validation is None or validation == '':
        answer.correct = answer.answers == answer.question.correctAnswers
        return

    # Multiple strings
    if validation == 'multipleStrings':
        answer_list = answer.answers.split(';')
        correct_answer_list = answer.question.correctAnswers.split(';')
        wrong_answer_list = []
        for i in range(len(answer_list)):
            if answer_list[i] != correct_answer_list[i]:
                wrong_answer_list.append(str(i+1))
        if len(wrong_answer_list) == 0:
            answer.correct = True
        elif len(wrong_answer_list) == 1:
            answer.correct = False
            separator = ', '
            answer.comment = str("Das Antwortfeld " + separator.join(wrong_answer_list) + " ist noch nicht korrekt ausgefüllt.")
        else:
            answer.correct = False
            separator = ', '
            answer.comment = "Die Antwortfelder " + separator.join(wrong_answer_list) + " sind noch nicht korrekt ausgefüllt."

    # Single fractions
    if validation == 'singleFraction':
        answerFloat = 1
        correctAnswerFloat = 1

        # Convert decimal or int to float
        if not bool(re.search('/', answer.answers)) and not bool(re.search(':', answer.answers)):
            answerFloat = float(answer.answers)
        # Convert fraction to float
        else:
            try:
                p = re.compile(r'\d+').findall(answer.answers)
                nominator = int(p[0])
                denominator = int(p[1])
                answerFloat = float(nominator/denominator)
                print(answerFloat)
            except:
                self.comment = "Die Frage konnte nicht korrigiert werden."
                return
        if not bool(re.search('frac', answer.question.correctAnswers)) and not bool(re.search('/', answer.answers)):
            correctAnswerFloat = float(answer.question.correctAnswers)
        # Convert fraction to float
        else:
            try:
                p = re.compile(r'\d+').findall(answer.question.correctAnswers)
                nominator = int(p[0])
                denominator = int(p[1])
                correctAnswerFloat = float(nominator/denominator)
                print(answerFloat)
            except:
                answer.comment = "Die Frage konnte nicht korrigiert werden."
                return

        answer.correct = abs(answerFloat - correctAnswerFloat) <= 1e-3
        return
    else:
        return
