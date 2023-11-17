from django.shortcuts import render, redirect
from .forms import signUpForm
from django.contrib import messages

# Create your views here.
def user_signup(request):
    if request.method == 'POST':
        form = signUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_page')  # Redirect to a success page
    else:
        form = signUpForm()

    return render(request, 'signup.html', {'form': form})

# login page
def user_login(request):
    return render(request, 'login.html')


def success(request):
    return render(request, 'registerSuccess.html')