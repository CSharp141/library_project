from django.urls import include, path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('', lambda request: redirect('login/')),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('homePage/', views.user_HomePage, name='homePage'),
    path('catalogue/', views.book_list, name='catalogue'),
    path('catalogue/<int:book_id>/loan/', views.loan_book, name='loan_book'),
    path('booksOnLoan/', views.current_books_on_loan, name='booksOnLoan'),
    path('processReturns/', views.processReturns, name = 'processReturns'),
    path('issueLateFee/<int:loan_id>/', views.issueLateFee, name='issueLateFee'),
    path('userLateFees/', views.userLateFees, name='userLateFees'),
    path('mark-late-fee-paid/<int:late_fee_id>/', views.LateFeePaid, name='LateFeePaid'),
    path('add-new-book/', views.addNewBook, name='addNewBook'),
    path('edit-book/<int:book_id>/', views.editBook, name='editBook'),
    path('delete-book/<int:book_id>/', views.deleteBook, name='deleteBook'),
    path( 'manageUsers/', views.adminManageUsers, name='adminManageUsers'),
    path('editUser/<int:user_id>/', views.editUser, name='editUser'),
    path('deleteUser/<int:user_id>/', views.deleteUser, name='deleteUser'),

]

