from django.contrib import admin
from django.urls import path,include
from Users import views as Users_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    #admin
    path('admin/', admin.site.urls),

    # problemset page
    path('', include('home.urls'), name='problemset'),

    #register page
    path('register/',Users_views.register,name='register'),

    #login
    path('login/',auth_views.LoginView.as_view(template_name='login.html'),name='login'),

     #logout
    path('logout/',auth_views.LogoutView.as_view(template_name='logout.html'),name='logout'),
]
