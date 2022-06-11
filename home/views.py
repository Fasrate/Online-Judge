from django import db
from django.shortcuts import redirect, render
from .models import Problem,Solution,TestCase

def problemset(request):
    context={
        'problems':Problem.objects.all()
    }
    return render(request,'Problemset.html',context)

def problem(request,probid):
    context={
        'currproblem':Problem.objects.get(probid=probid)
    }
    return render(request,'Problems.html',context)

def leaderboard(request):

    context={
        'solutions':Solution.objects.all().order_by('-submittedat')[0:10]
    }

    return render(request,'Leaderboard.html',context)

def submit(request,probid):
    
    if(request.method=='POST'):
        code=request.POST.get('code')
        language=request.POST.get('language')

        db=Solution(probid=probid,verdict='AC')
        db.save()

    return redirect('leaderboard')
   