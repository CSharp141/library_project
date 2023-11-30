from datetime import datetime
from django.dispatch import receiver
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import NewBookForm, UserEditForm, signUpForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.signals import user_logged_out
from .models import Books, LateFee, Loan
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test


# Create your views here.
def user_signup(request):
    if request.method == 'POST':
        form = signUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='Student')
            user.groups.add(group)
            messages.success(request, 'Registration successful. Please log in with your new credentials.')

            # Redirect to the login page
            return redirect('login')
    else:
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
                return redirect('homePage')   
                
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required(login_url='login')
def user_HomePage(request):
    user = request.user
    user_group = user.groups.first()
    return render(request, 'homePage.html', {'user_group': user_group, 'user': user})

def user_logout(request):
    logout(request)
    return redirect('login')


@receiver(user_logged_out)
def on_user_logged_out(sender, request, **kwargs):
    messages.add_message(request, messages.INFO, 'Logged out.')

@login_required(login_url='login')
def book_list(request):
    books = Books.objects.all()
    user = request.user
    user_group = user.groups.first()
    
    search_query = request.GET.get('q')
    if search_query:
        books = books.filter(title__icontains=search_query)


    paginator = Paginator(books, 10)  # Show 10 books per page
    page = request.GET.get('page')

    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        books = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver last page of results.
        books = paginator.page(paginator.num_pages)
    return render(request, 'catalogue.html', {'books': books, 'user_group': user_group})

@login_required(login_url='login')
def loan_book(request, book_id):
    book = get_object_or_404(Books, pk=book_id)
    

    if request.method == 'POST':
        # Create a new loan transaction
        loan = Loan.objects.create(book=book, user=request.user)
        
        # Update the availability status of the book
        book.is_available = False
        book.save()
        messages.success(request, 'Loan Succuessful')
        return redirect('catalogue')

    return render(request, 'loan_book.html', {'book': book})

@login_required(login_url='login')
def current_books_on_loan(request):
    # Filter loans for the current user and books that are not returned
    current_user_loans = Loan.objects.filter(user=request.user, is_returned=False)
    user = request.user
    user_group = user.groups.first()
    return render(request, 'booksOnLoan.html', {'current_loans': current_user_loans, 'user_group': user_group})

@user_passes_test(lambda u: u.groups.filter(name='Staff').exists())
def processReturns(request):
    users_with_loans = User.objects.filter(loan__is_returned=False).distinct()
    user = request.user
    user_group = user.groups.first()
    # Create a list to hold the loan details for each user
    loansList = []

    search_username = request.GET.get('search_username')
    if search_username:
        users_with_loans = users_with_loans.filter(username__icontains=search_username)

    
    for user in users_with_loans:
        # Retrieve loan details for each user
        user_loans = Loan.objects.filter(user=user, is_returned=False)
        
        for loan in user_loans:
            loansList.append({
                'user__username': user.username,
                'book__title': loan.book.title,
                'loan_date': loan.loan_date,
                'return_date': loan.return_date,
                'loan_id': loan.id,
            })

    if request.method == 'POST':
        loan_id = request.POST.get('loan_id')
        loan = Loan.objects.get(id=loan_id)
        
        # Process the return
        loan.is_returned = True
        loan.return_date = datetime.now()
        loan.save()

        # Update the book to available
        book = loan.book
        book.is_available = True
        book.save()

        return redirect('processReturns')

    return render(request, 'processReturns.html', {'loans': loansList, 'user_group': user_group})

@user_passes_test(lambda u: u.groups.filter(name='Staff').exists())
def issueLateFee(request, loan_id):
    # Get the loan object or return a 404 if not found
    loan = get_object_or_404(Loan, id=loan_id)

    # Check if the loan is late
    days_late = (datetime.now().date() - loan.loan_date).days

    # Check if a late fee already exists for the loan
    existing_late_fee = LateFee.objects.filter(loan=loan).first()

    if existing_late_fee:
        messages.warning(request, 'A late fee has already been issued')
        return redirect('processReturns')


    if days_late > 7:
        # Create a late fee for the loan
        late_fee_amount = 5
        late_fee = LateFee.objects.create(loan=loan, amount=late_fee_amount)
        late_fee.save()
    else:
        messages.warning(request, 'This loan is not yet late.')


    return redirect('processReturns')

@login_required(login_url='login')
def userLateFees(request):
    # Retrieve all late fees for the current user
    is_staff = Group.objects.get(name='Staff') in request.user.groups.all()
    lateFeeList = LateFee.objects.all()
    user = request.user
    user_group = user.groups.first()
    if is_staff:
        # If the user is in the "Staff" group, retrieve all late fees in the system
        
        return render(request, 'userLateFees.html', {'lateFeeList': lateFeeList, 'user_group': user_group})
    else:
        # If the user is not in the "Staff" group, retrieve only their late fees
        user_late_fees = []

        for late_fee in lateFeeList:
            if late_fee.loan.user == request.user:
                user_late_fees.append(late_fee)
        lateFeeList = user_late_fees

        return render(request, 'userLateFees.html', {'lateFeeList': lateFeeList, 'user_group': user_group})
    
@user_passes_test(lambda u: u.groups.filter(name='Staff').exists())
def LateFeePaid(request, late_fee_id):
    late_fee = get_object_or_404(LateFee, id=late_fee_id)

    # Mark the late fee as paid
    late_fee.paid = True
    late_fee.save()

    return redirect('userLateFees')

@user_passes_test(lambda u: u.groups.filter(name='Librarian').exists())
def addNewBook(request):
    user = request.user
    user_group = user.groups.first()
    if request.method == 'POST':
        form = NewBookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('catalogue')  # Redirect to the book list or any other page
    else:
        form = NewBookForm()

    return render(request, 'addNewBook.html', {'form': form, 'user_group': user_group})

@user_passes_test(lambda u: u.groups.filter(name='Librarian').exists())
def editBook(request, book_id):
    user = request.user
    user_group = user.groups.first()
    book = get_object_or_404(Books, id=book_id)

    if request.method == 'POST':
        form = NewBookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('catalogue')  # Redirect to the book list or any other page
    else:
        form = NewBookForm(instance=book)

    return render(request, 'editBook.html', {'form': form, 'book': book, 'user_group': user_group})

@user_passes_test(lambda u: u.groups.filter(name='Librarian').exists())
def deleteBook(request, book_id):
    book = get_object_or_404(Books, id=book_id)
    user = request.user
    user_group = user.groups.first()

    if request.method == 'POST':
        book.delete()
        return redirect('catalogue')  # Redirect to the book list or any other page

    return render(request, 'deleteBook.html', {'book': book, 'user_group': user_group})

@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def adminManageUsers(request):
    users = User.objects.all()
    user = request.user
    user_group = user.groups.first()

    return render(request, 'adminUserControl.html', {'users': users, 'user_group': user_group})

@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def editUser(request, user_id):
    user = get_object_or_404(User, id=user_id)
    currentUser = request.user
    user_group = currentUser.groups.first()

    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            # Save user data
            user = form.save()

            # Clear existing groups and add the selected ones
            user.groups.clear()
            user.groups.add(*form.cleaned_data['groups'])

            return redirect('adminManageUsers')
    else:
        form = UserEditForm(instance=user)

    return render(request, 'editUser.html', {'form': form, 'user': user, 'user_group': user_group, 'currentUser': currentUser})

@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def deleteUser(request, user_id):
    user = get_object_or_404(User, id=user_id)
    currentUser = request.user
    user_group = currentUser.groups.first()

    if request.method == 'POST':
        # Handle user deletion
        user.delete()
        return redirect('adminManageUsers')

    return render(request, 'deleteUser.html', {'user': user, 'user_group': user_group})