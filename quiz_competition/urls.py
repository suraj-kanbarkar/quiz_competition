"""quiz_competition URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
]
