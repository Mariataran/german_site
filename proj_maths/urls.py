"""proj_maths URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('terms-list', views.terms_list),
    path('add-term', views.add_term),
    path('send-term', views.send_term),
    path('stats', views.show_stats),
    path('add-list', views.add_list),
    path('send-list', views.send_list),
    path('verb-add', views.verb_add),
    path('choose-verb', views.choose_verb),
    path('show-verbs', views.show_verbs),
    path('show-lists', views.show_lists),
    path('show-one-list', views.show_one_list),
    path('test-list', views.test_list),
    path('test-result', views.test_result)
]
