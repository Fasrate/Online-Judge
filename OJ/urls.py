from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    #admin
    path('admin/', admin.site.urls),

    # problemset page
    path('', include('home.urls'), name='problemset'),

]
