"""views.py for the quiz system."""
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core.urlresolvers import reverse

from models import Quiz, Question, Choice, QuizUser
from django.contrib.auth.models import User

from forms import LoginForm, SignupForm, QuizForm, QuestionForm, ChoiceForm


def main(request):
    """Render the main welcoming page."""
    return render(request, 'main.html', {'title': 'Welcome to the Quiz System'})


def userLogin(request):
    """Render the login page."""
    form = LoginForm()
    return render(request, 'login.html', {'title': 'Please Log In', 'form': LoginForm})


def userSignup(request):
    """Render the signup page."""
    form = SignupForm()
    return render(request, 'signup.html', {'title': 'Please Sign Up', 'form': SignupForm})


def submitLogin(request):
    """Call Django login methods to log in the user."""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/my/')
                else:
                    return render(request, 'login.html', {'form': form, 'error': "Disabled account"})
            else:
                return render(request, 'login.html', {'form': form, 'error': "Incorrect username or password"})
        else:
            return render(request, 'login.html', {'form': form})
    else:
        return render(request, 'invalidAttempt.html', {'message': 'Form resubmission!'})


@login_required(login_url='/login/')
def submitLogout(request):
    """Call Django logout method to logout the user."""
    logout(request)
    return HttpResponseRedirect('/')


def submitSignup(request):
    """Sign up the user."""
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect('/login/')
        else:
            return render(request, 'signup.html', {'form': form})
    else:
        return render(request, 'invalidAttempt.html', {'message': 'Form resubmission!'})


@login_required(login_url='/login/')
def homepage(request):
    """Pass in the current logged-in user's name and render homepage.html."""
    user = request.user
    name = user.username
    return render(request, 'homepage.html', {'name': name})


@login_required(login_url='/login/')
def quizzes(request):
    """Pass in the quizzes list of untaken quizzes and render quizzes.html."""
    quizzes = Quiz.objects.exclude(users=request.user)
    return render(request, 'quizzes.html', {'quizzes': quizzes})


@login_required(login_url='/login/')
def questions(request, quiz_id):
    """Check whether the quiz has taken by the user before and display the quiz questions."""
    if request.user.quiz_set.filter(id=quiz_id).exists():
        return render(request, 'invalidAttempt.html', {'message': 'You have taken this quiz before!!!'})
    else:
        quiz = get_object_or_404(Quiz, id=quiz_id)
        return render(request, 'questions.html', {
            'title': 'Quizzes',
            'quiz': quiz,
        })


@login_required(login_url='/login/')
def save_userchoice(request, quiz_id):
    """Check whether the quiz has taken by the user before and save the user answers(userchoice)."""
    if request.method == 'POST':
        if request.user.quiz_set.filter(id=quiz_id).exists():
            return render(request, 'invalidAttempt.html', {'message': 'You have taken this quiz before!!!'})
        else:
            if 'userchoice' in request.POST and request.POST['userchoice'].isdigit():
                quiz = get_object_or_404(Quiz, id=quiz_id)
                quizuser = QuizUser.objects.create(
                    quiz=quiz, user=request.user)
                quizuser.save()
                selections = request.POST.getlist('userchoice')
                for selection in selections:
                    choice = get_object_or_404(Choice, id=selection)
                    choice.users.add(request.user)
                    choice.save()
                return HttpResponseRedirect(reverse('report', kwargs={'user_id': request.user.id, 'quiz_id': quiz_id}))
            else:
                return render(request, 'invalidAttempt.html', {'message': 'Invalid Input!'})
    else:
        return render(request, 'invalidAttempt.html', {'message': 'Form resubmission!'})


@login_required(login_url='/login/')
def my_report(request):
    """Display the scoreboard for the current user."""
    quizzes = Quiz.objects.filter(users=request.user)
    quiznames = []
    scores = []
    totals = []
    for quiz in quizzes:
        quiznames.append(quiz.name)
        point = score(request.user.id, quiz.id).get('score')
        scores.append(point)
        total = score(request.user.id, quiz.id).get('total')
        totals.append(total)
    return render(request, 'myreport.html', {'reports': zip(quiznames, scores, totals)})


@login_required(login_url='/login/')
def users_report(request):
    """Display the scoreboard to the superuser."""
    if request.user.is_superuser:
        quiznames = []
        usernames = []
        scores = []
        totals = []
        quizzes = Quiz.objects.order_by('name')
        quizzes = quizzes.exclude(users__id=None)
        for quiz in quizzes:
            for user in quiz.users.all():
                quiznames.append(quiz.name)
                usernames.append(user.username)
                point = score(user.id, quiz.id).get('score')
                scores.append(point)
                total = score(user.id, quiz.id).get('total')
                totals.append(total)
        return render(request, 'usersreport.html', {'reports': zip(quiznames, usernames, scores, totals)})
    else:
        return render(request, 'invalidAttempt.html', {'message': 'You are not a super user!'})


@login_required(login_url='/login/')
def report(request, user_id, quiz_id):
    """Render report.html to display the report page for the quiz."""
    point = score(user_id, quiz_id).get('score')
    total = score(user_id, quiz_id).get('total')
    user = get_object_or_404(User, id=user_id)
    quiz = get_object_or_404(Quiz, id=quiz_id)
    return render(request, 'report.html', {'score': point, 'total': total, 'quiz_name': quiz.name, 'user_name': user.username})


def score(user_id, quiz_id):
    """Pass in the user_id and quiz_id and calculate user's score for the particular quiz."""
    user = get_object_or_404(User, id=user_id)
    choices = user.choice_set.all()
    point = 0
    total = 0
    quiz = get_object_or_404(Quiz, id=quiz_id)
    for question in quiz.question_set.all():
        question_point = 0
        question_total = 0
        numCorrect = 0
        numPartial = 0
        numWrong = 0
        selections = choices.filter(question=question.id)
        for selection in selections:
            if selection.point == 0:
                numWrong = numWrong + 1
            elif selection.point == 1:
                numPartial = numPartial + 1
            elif selection.point == 2:
                numCorrect = numCorrect + 1
        for choice in question.choice_set.all():
            if choice.point == 2:
                question_total = question_total + 1

        if numWrong > 0:
            question_point = 0
        else:
            question_point = numCorrect
            if numPartial > 0:
                for i in range(0, numPartial):
                    question_point = question_point * 0.5
        point = point + question_point
        total = total + question_total
    return {'score': point, 'total': total}


@login_required(login_url='/login/')
def create_quiz(request):
    """For superuser to create new quizzes."""
    if(request.user.is_superuser):
        form = QuizForm()
        quizzes = Quiz.objects.order_by('name')
        return render(request, 'createQuiz.html', {'form': form, 'lists': quizzes})
    else:
        return render(request, 'invalidAttempt.html', {'message': 'You are not a super user!'})


@login_required(login_url='/login/')
def create_question(request, quiz_id):
    """For superuser to create new questions."""
    if(request.user.is_superuser):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        form = QuestionForm(initial={'quiz': quiz})
        questions = Question.objects.order_by('text')
        return render(request, 'createQuestion.html', {'form': form, 'quizID': int(quiz_id), 'quiz_name': quiz, 'lists': questions})
    else:
        return render(request, 'invalidAttempt.html', {'message': 'You are not a super user!'})


@login_required(login_url='/login/')
def create_choice(request, quiz_id, question_id):
    """For superuser to create new choices."""
    if(request.user.is_superuser):
        question = get_object_or_404(Question, id=question_id)
        form = ChoiceForm(initial={'question': question})
        choices = Choice.objects.order_by('text')
        return render(request, 'createChoice.html', {'form': form, 'quizID': int(quiz_id), 'questionID': int(question_id), 'question_name': question, 'lists': choices})
    else:
        return render(request, 'invalidAttempt.html', {'message': 'You are not a super user!'})


@login_required(login_url='/login/')
@require_http_methods(["POST"])
def add_quiz(request):
    """Add the new quiz that superuser created to the database."""
    form = QuizForm(request.POST)
    if form.is_valid():
        new_quiz = form.save()
        new_quiz.save()
        return HttpResponseRedirect('/create_quiz/')
    else:
        return render(request, 'invalidAttempt.html', {'message': 'Invalid input!'})


@login_required(login_url='/login/')
@require_http_methods(["POST"])
def delete_quiz(request):
    """Delete the quiz that superuser created."""
    if 'delete' in request.POST and request.POST['delete'].isdigit():
        delete_quiz = get_object_or_404(Quiz, pk=request.POST['delete'])
        delete_quiz.delete()
        return HttpResponseRedirect('/quiz_list/')
    else:
        return render(request, 'invalidAttempt.html', {'message': 'Invalid input!'})


@login_required(login_url='/login/')
@require_http_methods(["POST"])
def add_question(request, quiz_id):
    """Add the new question that superuser created to the database."""
    form = QuestionForm(request.POST)
    if form.is_valid():
        new_ques = form.save()
        new_ques.save()
        return HttpResponseRedirect(reverse('create_question', kwargs={'quiz_id': quiz_id}))
    else:
        return render(request, 'invalidAttempt.html', {'message': 'Invalid input!'})


@login_required(login_url='/login/')
@require_http_methods(["POST"])
def delete_question(request, quiz_id):
    """Delete the question that superuser created."""
    if 'delete' in request.POST and request.POST['delete'].isdigit():
        delete_question = get_object_or_404(
            Question, pk=request.POST['delete'])
        delete_question.delete()
        return HttpResponseRedirect(reverse('question_list', kwargs={'quiz_id': quiz_id}))
    else:
        return render(request, 'invalidAttempt.html', {'message': 'Invalid input!'})


@login_required(login_url='/login/')
@require_http_methods(["POST"])
def add_choice(request, quiz_id, question_id):
    """Add the new choice that superuser created to the database."""
    if(request.user.is_superuser):
        if request.method == 'POST':
            form = ChoiceForm(request.POST)
            if form.is_valid():
                new_choice = form.save()
                new_choice.save()
                return HttpResponseRedirect(reverse('create_choice', kwargs={'question_id': question_id, 'quiz_id': quiz_id}))
            else:
                return render(request, 'invalidAttempt.html', {'message': 'Invalid input!'})
    else:
        return render(request, 'invalidAttempt.html', {'message': 'You are not a super user!'})


@login_required(login_url='/login/')
@require_http_methods(["POST"])
def delete_choice(request, quiz_id, question_id):
    """Delete the choice that superuser created."""
    if 'delete' in request.POST and request.POST['delete'].isdigit():
        delete_choice = get_object_or_404(Choice, pk=request.POST['delete'])
        delete_choice.delete()
        return HttpResponseRedirect(reverse('choice_list', kwargs={'question_id': question_id, 'quiz_id': quiz_id}))
    else:
        return render(request, 'invalidAttempt.html', {'message': 'Invalid input!'})


@login_required(login_url='/login/')
def quiz_list(request):
    """Display the list of quizzes in the database."""
    if(request.user.is_superuser):
        quizzes = Quiz.objects.order_by('name')
        return render(request, 'quizList.html', {'lists': quizzes})
    else:
        return render(request, 'invalidAttempt.html', {'message': 'You are not a super user!'})


@login_required(login_url='/login/')
def question_list(request, quiz_id):
    """Display the list of questions in the database."""
    if(request.user.is_superuser):
        questions = Question.objects.order_by('text')
        return render(request, 'questionList.html', {'quizID': int(quiz_id), 'lists': questions})
    else:
        return render(request, 'invalidAttempt.html', {'message': 'You are not a super user!'})


@login_required(login_url='/login/')
def choice_list(request, quiz_id, question_id):
    """Display the list of choices in the database."""
    if(request.user.is_superuser):
        choices = Choice.objects.order_by('text')
        return render(request, 'choiceList.html', {'quizID': int(quiz_id), 'questionID': int(question_id), 'lists': choices})
    else:
        return render(request, 'invalidAttempt.html', {'message': 'You are not a super user!'})
