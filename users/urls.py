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
]

#urlpatterns += [
#    path('accounts/', include('django.contrib.auth.urls')),
#]