from django.forms import modelformset_factory
from django.shortcuts import render, redirect


def main(request):
    quizzes = Quiz.objects.all()
    return render(request, 'main.html', {"quizzes": quizzes})


def userLogin(request):
    return render(request, 'login.html', {'title': 'Welcome to the Quiz System'})


def userSignup(request):
    return render(request, 'signup.html', {'title': 'Please Sign up'})


def submitLogin(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect('/my/')
        else:
            return HttpResponse("The password is valid, but the account has been disabled!")
    else:
        return HttpResponse("The username and password were incorrect")


def submitLogout(request):
    logout(request)
    return HttpResponseRedirect('/')


def submitSignup(request):
    firstName = request.POST['firstname']
    lastName = request.POST['lastname']
    userName = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']

    user = User.objects.create_user(userName, email, password)
    user.last_name = lastName
    user.first_name = firstName
    user.save()
    return HttpResponseRedirect('/login')


def homepage(request):
    return render(request, 'homepage.html')


def quizzes(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quizzes.html', {'quizzes': quizzes})


def questions(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    questions = quiz.question_set.all()
    choices = []
    for question in questions:
        # questionID = question.id
        q_choice = question.choice_set.all()
        for choice in q_choice:
            choices.append(choice)

    return render(request, 'questions.html', {
        'questions': questions,
        'choices': choices,
        'title': 'Quizzes',
    })


def create_quiz(request):
    if request.method = "POST":
        quizzes = MusicianForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/create_quiz/')
    return render(request, 'createQuiz.html', context={'quizzes': quizzes})


def add(request):
    new_quiz = Quiz.objects.create(name=request.POST['save'])
    new_quiz.save()
    return HttpResponseRedirect('/create_quiz/')


def delete(request):
    delete_quiz = Quiz.objects.get(pk=request.POST['delete'])
    delete_quiz.delete()
    return HttpResponseRedirect('/quiz_list/')


def quiz_list(request):
    quizzes = Quiz.objects.order_by('name')
    return render(request, 'quizList.html', {'quizzes': quizzes})


def report(request):
    return render(request, 'report.html', {})


def solution(request):
    return render(request, 'solution.html', {})
