"""forms.py for the quiz system."""
from django import forms
from django.forms import ModelForm
from models import Quiz, Question, Choice, QuizUser
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm


class LoginForm(forms.Form):
    """Login form."""

    username = forms.CharField(label='Username', max_length=30, widget=forms.TextInput(
        attrs={'placeholder': 'Your Username'}))
    password = forms.CharField(label='Password', min_length=5, max_length=100, widget=forms.PasswordInput(
        attrs={'placeholder': 'Your Password'}))


class SignupForm(UserCreationForm):
    """Signup form."""

    password1 = forms.CharField(label='Password', min_length=5, max_length=100, widget=forms.PasswordInput(
        attrs={'placeholder': 'Your Password'}))

    class Meta:
        """Specifies the model used, fields used and widgets."""

        model = User
        fields = ('first_name', 'last_name', 'username', 'email',)
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Your First name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Your Last name'}),
            'username': forms.TextInput(attrs={'placeholder': 'Your Username'}),
            'email': forms.TextInput(attrs={'placeholder': 'Your Email Address'}),
        }

    def save(self, commit=True):
        """Method that overrides the save method in UserCreationForm."""
        user = super(SignupForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            return user


class QuizForm(ModelForm):
    """Quiz form."""

    class Meta:
        """Specifies the model used, fields used and widgets."""

        model = Quiz
        fields = ('name', 'subject', 'difficulty',)
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Quiz Name'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Subject Of This Quiz'}),
        }


class QuestionForm(ModelForm):
    """Question form."""

    class Meta:
        """Specifies the model used, fields used and widgets."""

        model = Question
        fields = ('text', 'quiz',)
        widgets = {
            'text': forms.TextInput(attrs={'placeholder': 'Your Question Text'}),
            'quiz': forms.HiddenInput(),
        }


class ChoiceForm(ModelForm):
    """Choice form."""

    class Meta:
        """Specifies the model used, fields used and widgets."""

        model = Choice
        fields = ('text', 'point', 'question', 'users',)
        widgets = {
            'text': forms.TextInput(attrs={'placeholder': 'Your Choice Text'}),
            'question': forms.HiddenInput(),
            'users': forms.HiddenInput(),
        }
