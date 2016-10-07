"""urls.py for the quiz system."""
from django.conf.urls import include, url
from django.contrib import admin
from quizXZ import views

urlpatterns = [
    url(r'^/?$', views.main, name='main'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', views.userLogin, name='login'),
    url(r'^signup/$', views.userSignup, name='signup'),
    url(r'^submitLogin/$', views.submitLogin, name='submitLogin'),
    url(r'^submitSignup/$', views.submitSignup, name='submitSignup'),
    url(r'^submitLogout/$', views.submitLogout, name='submitLogout'),
    url(r'^my/$', views.homepage, name='homepage'),
    url(r'^create_quiz/$', views.create_quiz, name='create_quiz'),
    url(r'^quiz_list/', views.quiz_list, name='quiz_list'),
    url(r'^(?P<quiz_id>\d+)/create_question/$',
        views.create_question, name='create_question'),
    url(r'^(?P<quiz_id>\d+)/question_list/$',
        views.question_list, name='question_list'),
    url(r'^(?P<quiz_id>\d+)/(?P<question_id>\d+)/create_choice/$',
        views.create_choice, name='create_choice'),
    url(r'^(?P<quiz_id>\d+)/(?P<question_id>\d+)/choice_list/$',
        views.choice_list, name='choice_list'),
    url(r'^add_quiz/$', views.add_quiz, name='add_quiz'),
    url(r'^(?P<quiz_id>\d+)/add_question/$',
        views.add_question, name='add_question'),
    url(r'^(?P<quiz_id>\d+)/(?P<question_id>\d+)/add_choice/$',
        views.add_choice, name='add_choice'),
    url(r'^delete_quiz/$', views.delete_quiz, name='delete_quiz'),
    url(r'^(?P<quiz_id>\d+)/delete_question/$',
        views.delete_question, name='delete_question'),
    url(r'^(?P<quiz_id>\d+)/(?P<question_id>\d+)/delete_choice/$',
        views.delete_choice, name='delete_choice'),

    url(r'^quizzes/$', views.quizzes, name='quizzes'),
    url(r'^(?P<quiz_id>\d+)/questions/$', views.questions, name='questions'),
    url(r'^(?P<quiz_id>\d+)/save_userchoice/$',
        views.save_userchoice, name='save_userchoice'),
    url(r'^users/report/$', views.users_report, name='users_report'),
    url(r'^my/report/$', views.my_report, name='my_report'),
    url(r'^(?P<user_id>\d+)/(?P<quiz_id>\d+)/report/$', views.report, name='report'),
]
