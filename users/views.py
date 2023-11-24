from django.dispatch import receiver
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout 
from .forms import signUpForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.signals import user_logged_out
from .models import Books

# Create your views here.
def user_signup(request):
    if request.method == 'POST':
        print("Form submitted - POST request")
        form = signUpForm(request.POST)
        print(form)
        if form.is_valid():
            print("Form is valid - Saving data")
            user = form.save()
            print("Data saved successfully")
            group = Group.objects.get(name='Student')
            user.groups.add(group)
            messages.success(request, 'Registration successful. Please log in with your new credentials.')

            # Redirect to the login page
            return redirect('login')
        else:
            print("Form is not valid - Check form data")
    else:
        print("No form submitted - Displaying empty form")
        form = signUpForm()

    return render(request, 'signup.html', {'form': form})

# login page
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                print("logic success")
                messages.success(request, 'Login successful.')
                return redirect('homePage')   
                
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required(login_url='login')
def user_HomePage(request):
    return render(request, 'homePage.html')

def user_logout(request):
    logout(request)
    return redirect('login')


@receiver(user_logged_out)
def on_user_logged_out(sender, request, **kwargs):
    messages.add_message(request, messages.INFO, 'Logged out.')

@login_required(login_url='login')
def book_list(request):
    books = Books.objects.all()
    return render(request, 'catalogue.html', {'books': books})