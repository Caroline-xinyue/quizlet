"""models.py for the quiz system."""
from django.conf import settings
from django.db import models


class Quiz(models.Model):
    """Quiz model."""

    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through="QuizUser", blank=True)
    name = models.CharField(max_length=20, default="")
    diffLevels = (
        (0, "easy"),
        (1, "medium"),
        (2, "hard"),
    )
    subject = models.CharField(max_length=200, default="", blank=True)
    difficulty = models.IntegerField(choices=diffLevels, default=0, blank=True)

    def __str__(self):
        """To string method for the quiz model."""
        return self.name


class Question(models.Model):
    """Question model."""

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.CharField(max_length=500, default="")

    def __str__(self):
        """To string method for the question model."""
        return self.text


class Choice(models.Model):
    """Choice model."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    text = models.CharField(max_length=300, default="")
    pointTypes = (
        (0, 0),
        (1, 0.5),
        (2, 1)
    )
    point = models.IntegerField(choices=pointTypes, default=0)

    def __str__(self):
        """To string method for the choice model."""
        return self.text


class QuizUser(models.Model):
    """QuizUser model that specifies the ManyToMany relatinoship between Django User model and the Quiz model."""

    quiz = models.ForeignKey(Quiz)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    class Meta:
        """Set the combined foreign keys to be unique."""

        unique_together = ('user', 'quiz')
