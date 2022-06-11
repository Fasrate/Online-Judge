from . import views 
from django.http import HttpResponse
from django.urls import path

urlpatterns = [

    # problemset page
    path('',views.problemset, name='problemset'),

    # individual problem
    path('problem/<int:probid>/',views.problem, name='problem'),

    # leaderboard
    path('leaderboard/',views.leaderboard, name='leaderboard'),

    #submit 
    path('submit/<int:probid>/',views.submit,name='submit')

]
