from . import views 
from django.contrib.auth import views as auth_views
from django.http import HttpResponse
from django.urls import path
from Users import views as user_views

urlpatterns = [

    # problemset page
    path('',views.problemset, name='problemset'),

    # individual problem
    path('problem/<int:probid>/',views.problem, name='problem'),

    # leaderboard
    path('leaderboard/',views.leaderboard, name='leaderboard'),

    #submit 
    path('submit/<int:probid>/',views.submit,name='submit'),

    #register
    path('register/', user_views.register, name='register'),
    
    #login
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),

    #logout
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),

]
