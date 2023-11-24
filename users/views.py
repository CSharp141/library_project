from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import signUpForm, LoginForm
from django.contrib import messages
from django.contrib.auth.models import Group

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
                
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def success(request):
    return render(request, 'registerSuccess.html')