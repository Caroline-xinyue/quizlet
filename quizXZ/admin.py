"""admin.py for the quiz system."""
from django.contrib import admin

# Register your models here.
from .models import Quiz, Question, Choice, QuizUser


class ChoiceInline(admin.StackedInline):
    """Display the Choice model inline in the admin page."""

    model = Choice


class QuizUserInline(admin.TabularInline):
    """Display the QuizUser model inline in the admin page."""

    model = QuizUser


class QuestionAdmin(admin.ModelAdmin):
    """Display the Choices inline in the Question admin."""

    inlines = [ChoiceInline, ]


class QuizAdmin(admin.ModelAdmin):
    """Display the QuizUser inline in the Quiz admin."""

    inlines = [QuizUserInline, ]


admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
