from django.contrib import admin
from django.conf.urls import url
from django.conf.urls import include
from quiz_app import views

urlpatterns = [
    # url(r'^', include('quiz_competition.urls')),
    url(r'^start_quiz/(?P<id>[A-Za-z_0-9\-]+)', views.start_quiz, name='start_quiz'),
    url(r'^start_quiz/', views.start_quiz, name='start_quiz'),
    url(r'^quiz_details/', views.quiz_details, name='quiz_details'),
    url(r'^signup/', views.signup, name='signup'),
    url(r'^signin/', views.signin, name='signin'),
    url('admin/', admin.site.urls),
    url(r'^', views.signin),
]
