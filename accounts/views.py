from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate


def home(request):
	    return render(request, 'home.html', {})

def team_signup(request):

	    return render(request, 'team_signup.html', {})

def login(request):
	    return render(request, 'login.html', {})

