"""tests.py for the quiz system."""
from django.core.urlresolvers import reverse
from django.test import TestCase

from models import Quiz, Question, Choice, QuizUser
from django.contrib.auth.models import User

from forms import LoginForm, SignupForm, QuizForm, QuestionForm, ChoiceForm


class QuizModelTests(TestCase):
    """ModelTests for Quiz model."""

    def setUp(self):
        """Set up for testing the quiz model."""
        self.quiz = Quiz.objects.create(
            name="Database",
            subject="CS306",
            difficulty=1,
        )
        self.quiz.save()

    def test_quiz_creation(self):
        """Testing the __str__() method in quiz model."""
        self.assertEqual(self.quiz.__str__(), "Database")


class QuizViewTests(TestCase):
    """ViewTests for Quiz creation and deletion."""

    def setUp(self):
        """Set up for testing the quiz view."""
        self.user = User.objects.create_user(
            'dxu', 'dxu@cs.brynmawr.edu', 'yilun')
        self.user.is_superuser = True
        self.quiz = Quiz.objects.create(
            name="Database",
            subject="CS306",
            difficulty=1,
        )
        self.question = Question.objects.create(
            text="What is Django?",
            quiz=self.quiz
        )
        self.choice = Choice.objects.create(
            text="A great python framework",
            question=self.question,
            point=0,
        )
        self.user.save()
        self.quiz.save()
        self.question.save()
        self.choice.save()

    def test_create_quiz_login(self):
        """Testing the login required decorator for create_quiz method in view."""
        resp = self.client.get(reverse('create_quiz'), follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'login.html')

    def test_create_quiz(self):
        """Testing the create_quiz method in view. Check whether the exising quizzes are shown at bottom."""
        self.client.login(username='dxu', password='yilun')
        resp = self.client.get(reverse('create_quiz'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'createQuiz.html')
        self.assertIn(self.quiz, resp.context['lists'])

    def test_quiz_list_login(self):
        """Testing the login required decorator for quiz_list method in view."""
        resp = self.client.get(reverse('quiz_list'), follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'login.html')

    def test_quiz_list(self):
        """Testing the quiz_list method in view. Check whether the exising quizzes are shown."""
        self.client.login(username='dxu', password='yilun')
        resp = self.client.get(reverse('quiz_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'quizList.html')
        self.assertIn(self.quiz, resp.context['lists'])

    def test_quiz_form_valid(self):
        """Testing whether the quiz form is valid."""
        form_data = {'name': 'Database', 'subject': 'CS306', 'difficulty': 1}
        form = QuizForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_quiz_form_invalid(self):
        """Testing whether the quiz form is invalid."""
        form2_data = {'name': 'Database', 'subject': 'CS306', 'difficulty': 5}
        form2 = QuizForm(data=form2_data)
        self.assertFalse(form2.is_valid())

    def test_add_quiz(self):
        """Testing whether superuser can successfully add quizzes to the database."""
        self.client.login(username='dxu', password='yilun')
        resp = self.client.post(reverse('add_quiz'), {
                                'name': self.quiz.name, 'subject': self.quiz.subject, 'difficulty': self.quiz.difficulty}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'createQuiz.html')
        qz_exist = Quiz.objects.filter(name=self.quiz.name).exists()
        self.assertTrue(qz_exist)

    def test_delete_quiz(self):
        """Testing whether superuser can successfully delete quizzes from the database."""
        self.client.login(username='dxu', password='yilun')
        resp = self.client.post(
            reverse('delete_quiz'), {'delete': self.quiz.id}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'quizList.html')
        qz_exist = Quiz.objects.filter(name=self.quiz.name).exists()
        self.assertFalse(qz_exist)
        ques_exist = Question.objects.filter(text=self.question.text).exists()
        self.assertFalse(ques_exist)
        choi_exist = Choice.objects.filter(text=self.choice.text).exists()
        self.assertFalse(choi_exist)


class QuestionModelTests(TestCase):
    """ModelTests for Question model."""

    def setUp(self):
        """Set up for testing the question model."""
        self.user = User.objects.create_user(
            'dianna', 'dxu@cs.brynmawr.edu', 'yilun')
        self.quiz = Quiz.objects.create(
            name="Database",
            subject="CS306",
            difficulty=1,
        )
        self.question = Question.objects.create(
            text="What is Django?",
            quiz=self.quiz
        )
        self.user.save()
        self.quiz.save()
        self.question.save()

    def test_question_creation(self):
        """Testing the __str__() method in question model."""
        self.assertEqual(self.question.text, "What is Django?")
        self.assertEqual(self.question.__str__(), "What is Django?")


class QuestionViewTests(TestCase):
    """ViewTests for Question creation and deletion."""

    def setUp(self):
        """Set up for testing the question view."""
        self.user = User.objects.create_user(
            'dxu', 'dxu@cs.brynmawr.edu', 'yilun')
        self.user.is_superuser = True
        self.quiz = Quiz.objects.create(
            name="Database",
            subject="CS306",
            difficulty=1,
        )
        self.question = Question.objects.create(
            text='What is Django?',
            quiz=self.quiz,
        )
        self.user.save()
        self.quiz.save()
        self.question.save()

    def test_question_form(self):
        """Testing whether the question form is valid."""
        form_data = {'text': "What is Django?", 'quiz': self.quiz.id}
        form = QuestionForm(
            data=form_data)
        self.assertTrue(form.is_valid())

    def test_create_question(self):
        """Testing the create_question method in view. Check whether the exising questions are shown at bottom."""
        resp = self.client.get(
            reverse('create_question', kwargs={'quiz_id': self.quiz.id}), follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'login.html')

        self.client.login(username='dxu', password='yilun')
        resp = self.client.get(
            reverse('create_question', kwargs={'quiz_id': self.quiz.id}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'createQuestion.html')
        self.assertEqual(resp.context['quizID'], self.quiz.id)
        self.assertEqual(resp.context['quiz_name'], self.quiz)
        self.assertIn(self.question, resp.context['lists'])

    def test_question_list(self):
        """Testing the question_list method in view. Check whether the exising questions are shown."""
        resp = self.client.get(
            reverse('question_list', kwargs={'quiz_id': self.quiz.id}), follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'login.html')

        self.client.login(username='dxu', password='yilun')
        resp = self.client.get(
            reverse('question_list', kwargs={'quiz_id': self.quiz.id}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'questionList.html')
        self.assertEqual(resp.context['quizID'], self.quiz.id)
        self.assertIn(self.question, resp.context['lists'])

    def test_add_question(self):
        """Testing whether superuser can successfully add questions to the database."""
        self.client.login(username='dxu', password='yilun')
        resp = self.client.post(reverse('add_question', kwargs={'quiz_id': self.quiz.id}), {
                                'text': self.question.text, 'quiz': self.quiz.id}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'createQuestion.html')
        ques_exist = Question.objects.filter(text=self.question.text).exists()
        self.assertTrue(ques_exist)

    def test_delete_question(self):
        """Testing whether superuser can successfully delete questions from the database."""
        self.client.login(username='dxu', password='yilun')
        resp = self.client.post(
            reverse('delete_question', kwargs={'quiz_id': self.quiz.id}), {'delete': self.question.id}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'questionList.html')
        ques_exist = Question.objects.filter(text=self.question.text).exists()
        self.assertFalse(ques_exist)


class ChoiceModelTests(TestCase):
    """ModelTests for Choice model."""

    def setUp(self):
        """Set up for testing the choice model."""
        self.user = User.objects.create_user(
            'dianna', 'dxu@cs.brynmawr.edu', 'yilun')
        self.quiz = Quiz.objects.create(
            name="Database",
            subject="CS306",
            difficulty=1,
        )
        self.question = Question.objects.create(
            text="What is Django?",
            quiz=self.quiz
        )
        self.choice = Choice.objects.create(
            text="A great python framework",
            question=self.question,
            point=0,
        )
        self.user.save()
        self.quiz.save()
        self.question.save()
        self.choice.save()

    def test_choice_creation(self):
        """Testing the __str__() method in choice model."""
        self.assertEqual(self.choice.text, "A great python framework")
        self.assertEqual(self.choice.question, self.question)
        self.assertEqual(self.choice.point, 0)
        self.assertEqual(self.choice.__str__(), "A great python framework")


class ChoiceViewTests(TestCase):
    """ViewTests for Choice creation and deletion."""

    def setUp(self):
        """Set up for testing the question view."""
        self.user = User.objects.create_user(
            'dxu', 'dxu@cs.brynmawr.edu', 'yilun')
        self.user.is_superuser = True
        self.quiz = Quiz.objects.create(
            name="Database",
            subject="CS306",
            difficulty=1,
        )
        self.question = Question.objects.create(
            text='What is Django?',
            quiz=self.quiz,
        )
        self.choice = Choice.objects.create(
            text="A great python framework",
            question=self.question,
            point=0,
        )
        self.user.save()
        self.quiz.save()
        self.question.save()
        self.choice.save()

    def test_choice_form(self):
        """Testing whether the choice form is valid."""
        form_data = {'text': "A great python framework",
                     'point': 0, 'question': self.question.id}
        form = ChoiceForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_create_choice(self):
        """Testing the create_choice method in view. Check whether the exising choices are shown at bottom."""
        resp = self.client.get(
            reverse('create_choice', kwargs={'quiz_id': self.quiz.id, 'question_id': self.question.id}), follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'login.html')

        self.client.login(username='dxu', password='yilun')
        resp = self.client.get(
            reverse('create_choice', kwargs={'quiz_id': self.quiz.id, 'question_id': self.question.id}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'createChoice.html')
        self.assertEqual(resp.context['quizID'], self.quiz.id)
        self.assertEqual(resp.context['questionID'], self.question.id)
        self.assertEqual(resp.context['question_name'], self.question)
        self.assertIn(self.choice, resp.context['lists'])

    def test_choice_list(self):
        """Testing the choice_list method in view. Check whether the exising choices are shown."""
        resp = self.client.get(
            reverse('choice_list', kwargs={'quiz_id': self.quiz.id, 'question_id': self.question.id}), follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'login.html')

        self.client.login(username='dxu', password='yilun')
        resp = self.client.get(
            reverse('choice_list', kwargs={'quiz_id': self.quiz.id, 'question_id': self.question.id}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'choiceList.html')
        self.assertEqual(resp.context['quizID'], self.quiz.id)
        self.assertEqual(resp.context['questionID'], self.question.id)
        self.assertIn(self.choice, resp.context['lists'])

    def test_add_choice(self):
        """Testing whether superuser can successfully add choices to the database."""
        self.client.login(username='dxu', password='yilun')
        resp = self.client.post(reverse('add_choice', kwargs={'quiz_id': self.quiz.id, 'question_id': self.question.id}), {
                                'text': self.choice.text, 'point': self.choice.point, 'question': self.question.id}, follow=True)
        self.assertTemplateUsed(resp, 'createChoice.html')
        self.assertEqual(resp.status_code, 200)
        choi_exist = Choice.objects.filter(text=self.choice.text).exists()
        self.assertTrue(choi_exist)

    def test_delete_choice(self):
        """Testing whether superuser can successfully delete choices from the database."""
        self.client.login(username='dxu', password='yilun')
        resp = self.client.post(
            reverse('delete_choice', kwargs={'quiz_id': self.quiz.id, 'question_id': self.question.id}), {'delete': self.choice.id}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'choiceList.html')
        choi_exist = Choice.objects.filter(text=self.choice.text).exists()
        self.assertFalse(choi_exist)


class AdminViewTests(TestCase):
    """ViewTests for administration methods including signup, login and logout."""

    def setUp(self):
        """Set up for testing the administration methods in view."""
        self.user = User.objects.create_user(
            'dxu', 'dxu@cs.brynmawr.edu', 'yilun')
        self.user.is_superuser = True
        self.user.save()

    def test_login_form(self):
        """Testing whether the login form is valid."""
        form_data = {'username': 'dxu',
                     'password': 'yilun'}
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())

        form_data = {'username': 'dxu'}
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_userLogin(self):
        """Testing whether the login page is successfully displayed."""
        resp = self.client.get(reverse('login'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'login.html')
        self.assertEqual(resp.context['title'], 'Please Log In')

    def test_submitLogin_valid(self):
        """Testing whether user can successfully login."""
        resp = self.client.post(
            reverse('submitLogin'), {'username': 'dxu', 'password': 'yilun'}, follow=True)
        self.assertTemplateUsed(resp, 'homepage.html')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('_auth_user_id', self.client.session)
        self.assertEqual(
            int(self.client.session['_auth_user_id']), self.user.pk)

    def test_submitLogin_mismatch(self):
        """Testing whether the login successfully authenticate the user."""
        resp2 = self.client.post(
            reverse('submitLogin'), {'username': 'xzhang', 'password': 'lexie'})
        self.assertEqual(resp2.status_code, 200)
        self.assertTemplateUsed(resp2, 'login.html')
        self.assertEqual(
            resp2.context['error'], "Incorrect username or password")

    def test_submitLogin_invalid(self):
        """Testing whether the login successfully handle the invalid data."""
        resp2 = self.client.post(
            reverse('submitLogin'), {'username': 'xzhang'})
        self.assertEqual(resp2.status_code, 200)
        self.assertTemplateUsed(resp2, 'login.html')

    def test_submitLogout(self):
        """Testing whether user can successfully logout."""
        self.client.login(username='dxu', password='yilun')
        resp = self.client.post(
            reverse('submitLogout'), {'username': 'dxu', 'password': 'yilun'}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'main.html')
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_userSignup(self):
        """Testing whether the signup page is successfully displayed."""
        resp = self.client.get(reverse('signup'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'signup.html')
        self.assertEqual(resp.context['title'], 'Please Sign Up')

    def test_submitSignup_valid(self):
        """Testing whether user can successfully signup."""
        resp = self.client.post(reverse('submitSignup'), {
            'username': 'tluan', 'password1': 'erica', 'password2': 'erica'}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'login.html')

    def test_submitSignup_invalid(self):
        """Testing whether the signup form successfully handle the invalid data."""
        resp = self.client.post(
            reverse('submitSignup'), {'username': 'tluan', 'password1': 'erica'})
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'signup.html')
        user_exist = User.objects.filter(username=self.user.username).exists()
        self.assertTrue(user_exist)

    def test_homepage_login(self):
        """Testing the login required decorator for quiz_list method in view."""
        resp = self.client.get(reverse('homepage'), follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'login.html')

    def test_homepage(self):
        """Testing whether the username is passed into the template and whether homepage is successfully displayed."""
        self.client.login(username='dxu', password='yilun')
        resp = self.client.get(reverse('homepage'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'homepage.html')
        self.assertEqual(resp.context['name'], self.user.username)

    def test_main(self):
        """Testing whether the title is passed into the template and whether main page is successfully displayed."""
        resp = self.client.get(reverse('main'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'main.html')
        self.assertEqual(resp.context['title'], 'Welcome to the Quiz System')


class QuizSystemViewTests(TestCase):
    """ViewTests for quiz taking methods, including displaying quizzes, questions, save userchoices, and report pages."""

    def setUp(self):
        """Set up for testing the quiz taking methods in view."""
        self.user = User.objects.create_user(
            'dxu', 'dxu@cs.brynmawr.edu', 'yilun')
        self.user2 = User.objects.create_user(
            'tluan', 'tluan@cs.brynmawr.edu', 'erica')
        self.user3 = User.objects.create_user(
            'xzhang', 'xzhang@cs.brynmawr.edu', 'lexie')
        self.user2.is_superuser = True
        self.quiz = Quiz.objects.create(
            name="Database",
            subject="CS306",
            difficulty=1,
        )
        self.question = Question.objects.create(
            text="What is Django?",
            quiz=self.quiz
        )
        self.choice = Choice.objects.create(
            text="A great python framework",
            question=self.question,
            point=0,
        )
        self.choice2 = Choice.objects.create(
            text="A programming language",
            question=self.question,
            point=1,
        )
        self.choice3 = Choice.objects.create(
            text="A structured query language(SQL)",
            question=self.question,
            point=2,
        )
        self.user.save()
        self.user2.save()
        self.user3.save()
        self.quiz.save()
        self.question.save()
        self.choice.save()

    def test_quizzes(self):
        """Test whether the existing quizzes are displayed for the current user."""
        self.client.login(username='dxu', password='yilun')
        resp = self.client.get(reverse('quizzes'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'quizzes.html')
        self.assertIn(self.quiz, resp.context['quizzes'])

    def test_quizzes_taken(self):
        """Test whether the quizzes already taken are not displayed for the current user."""
        self.client.login(username='dxu', password='yilun')
        resp = self.client.post(reverse('save_userchoice', kwargs={
            'quiz_id': self.quiz.id}), {'userchoice': (self.choice2.id, self.choice3.id)}, follow=True)
        resp = self.client.get(reverse('quizzes'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'quizzes.html')
        self.assertNotIn(self.quiz, resp.context['quizzes'])

    def test_questions(self):
        """Test whether the existing questions are displayed for the current user."""
        self.client.login(username='dxu', password='yilun')
        resp = self.client.get(
            reverse('questions', kwargs={'quiz_id': self.quiz.id}), {'quiz_id': self.quiz.id})
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'questions.html')
        self.assertEqual(resp.context['title'], 'Quizzes')
        self.assertEqual(resp.context['quiz'], self.quiz)

    def test_questions_taken(self):
        """Test whether the invalidAttempt page is shown for the current user if the quiz has already been taken before."""
        self.client.login(username='dxu', password='yilun')
        resp = self.client.post(reverse('save_userchoice', kwargs={
            'quiz_id': self.quiz.id}), {'userchoice': (self.choice2.id, self.choice3.id)}, follow=True)
        resp = self.client.get(
            reverse('questions', kwargs={'quiz_id': self.quiz.id}), {'quiz_id': self.quiz.id}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'invalidAttempt.html')
        self.assertEqual(
            resp.context['message'], 'You have taken this quiz before!!!')

    def test_save_userchoice(self):
        """Test whether the choices selected by the users are successfully saved to the database."""
        self.client.login(username='dxu', password='yilun')
        resp = self.client.post(reverse('save_userchoice', kwargs={
            'quiz_id': self.quiz.id}), {'userchoice': (self.choice2.id, self.choice3.id)}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'report.html')
        userchoi_exist = Choice.objects.filter(users=self.user.id).exists()
        self.assertTrue(userchoi_exist)

    def test_questions_taken(self):
        """Test whether the invalidAttempt page is shown for the current user if the quiz has already been taken before."""
        self.client.login(username='dxu', password='yilun')
        resp = self.client.post(reverse('save_userchoice', kwargs={
            'quiz_id': self.quiz.id}), {'userchoice': (self.choice2.id, self.choice3.id)}, follow=True)
        resp = self.client.get(
            reverse('questions', kwargs={'quiz_id': self.quiz.id}), {'quiz_id': self.quiz.id}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'invalidAttempt.html')
        self.assertEqual(
            resp.context['message'], 'You have taken this quiz before!!!')

    def test_report_half(self):
        """Test that the scores calculation is partially correct and the correct informations are being passed to the template."""
        self.client.login(username='dxu', password='yilun')
        self.client.post(reverse('save_userchoice', kwargs={
            'quiz_id': self.quiz.id}), {'userchoice': (self.choice2.id, self.choice3.id)})
        resp = self.client.get(
            reverse('report', kwargs={'user_id': self.user.id, 'quiz_id': self.quiz.id}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'report.html')
        self.assertEqual(resp.context['score'], 0.5)
        self.assertEqual(resp.context['total'], 1)
        self.assertEqual(resp.context['quiz_name'], self.quiz.name)
        self.assertEqual(resp.context['user_name'], self.user.username)
        self.assertNotEqual(resp.context['user_name'], self.user2.username)

    def test_report_correct(self):
        """Test that the scores calculated is correct and correct informations are being passed to the template."""
        self.client.login(username='tluan', password='erica')
        self.client.post(reverse('save_userchoice', kwargs={
            'quiz_id': self.quiz.id}), {'userchoice': (self.choice3.id)})
        resp = self.client.get(
            reverse('report', kwargs={'user_id': self.user2.id, 'quiz_id': self.quiz.id}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['score'], 1)
        self.assertEqual(resp.context['total'], 1)

    def test_report_wrong(self):
        """Test that the scores calculated is wrong and correct informations are being passed to the template."""
        self.client.login(username='xzhang', password='lexie')
        self.client.post(reverse('save_userchoice', kwargs={
            'quiz_id': self.quiz.id}), {'userchoice': (self.choice.id, self.choice3.id)})
        resp = self.client.get(
            reverse('report', kwargs={'user_id': self.user3.id, 'quiz_id': self.quiz.id}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['score'], 0)
        self.assertEqual(resp.context['total'], 1)

    def test_my_report(self):
        """Test that the scores for the user are displayed if the user has attempted the quiz."""
        self.client.login(username='dxu', password='yilun')
        resp = self.client.post(reverse('save_userchoice', kwargs={
            'quiz_id': self.quiz.id}), {'userchoice': (self.choice2.id, self.choice3.id)})
        resp = self.client.get(reverse('my_report'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'myreport.html')
        self.assertEqual(
            zip([self.quiz.name], [0.5], [1]), resp.context['reports'])

    def test_users_report(self):
        """Test that the scores are not displayed if the user hasn't attempted the quiz."""
        self.client.login(username='tluan', password='erica')
        resp = self.client.get(reverse('users_report'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'usersreport.html')
        self.assertNotEqual(
            zip([self.quiz.name], [self.user2.username], [0.5], [1]), resp.context['reports'])

    def test_users_report_taken(self):
        """Test that the scores are displayed if the user has attempted the quiz."""
        self.client.login(username='tluan', password='erica')
        resp = self.client.post(reverse('save_userchoice', kwargs={
            'quiz_id': self.quiz.id}), {'userchoice': (self.choice2.id, self.choice3.id)})
        resp = self.client.get(reverse('users_report'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'usersreport.html')
        self.assertEqual(
            zip([self.quiz.name], [self.user2.username], [0.5], [1]), resp.context['reports'])

    def test_users_report_invalid(self):
        """Test that non-superusers cannot access the usersreport page and invalidAttempt is displayed."""
        self.client.login(username='dxu', password='yilun')
        resp = self.client.post(reverse('save_userchoice', kwargs={
            'quiz_id': self.quiz.id}), {'userchoice': (self.choice2.id, self.choice3.id)})
        resp = self.client.get(reverse('users_report'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'invalidAttempt.html')
