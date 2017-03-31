from django.db import models
from django.contrib.auth.models import User

class Quiz(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(null=True)
    deadline = models.DateTimeField()

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name="questions")
    question = models.TextField()
    answer_description = models.TextField(null=True)

    def __str__(self):
        return self.question

class Option(models.Model):
    question = models.ForeignKey(Question, related_name="options")
    text = models.TextField()
    correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class QuestionAnswer(models.Model):
    question = models.ForeignKey(Question, related_name="answers")
    choice = models.ForeignKey(Option)
    user = models.ForeignKey(User)
