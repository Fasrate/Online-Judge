from django import db
from django.shortcuts import redirect, render
from .models import Problem,Solution,TestCase
from django.core.files import File
import subprocess,os,sys
from django.contrib.auth.decorators import login_required

def problemset(request):
    context={
        'problems':Problem.objects.all()
    }
    return render(request,'Problemset.html',context)

@login_required
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
        
        #  checker
        verdict=check(request,probid)
        language=request.POST.get('language')
        user=request.POST.get('user')
        db=Solution(probid=probid,verdict=verdict,user=request.user)
        db.save()

    return redirect('leaderboard')


def check(request,probid):
    os.chdir('Test')
    input=TestCase.objects.get(probid=1).input
    output=TestCase.objects.get(probid=1).output
    code=request.POST.get('code')

    fcode=open('Code.c', 'w') 
    fcode.write(code)
    
    foutput=open('Output.txt', 'w')
    foutput.write(output)
    finput=open('Input.txt', 'w')
    finput.write(input)
   
   # ref https://stackoverflow.com/questions/163542/how-do-i-pass-a-string-into-subprocess-popen-using-the-stdin-argument
   
    r,w=os.pipe()
    # string input goal is to convert it into bytes object 
    os.write(w,bytes(input,"utf-8"));
    os.close(w)

    subprocess.Popen(["gcc","Code.c"],shell=True)
    s=subprocess.run("a.exe", stdin=r,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=60,shell=True)
    

    useroutput=s.stdout.decode('utf-8');
    error=s.stderr.decode('utf-8');

    fcode.close()
    finput.close()
    foutput.close()

    os.chdir('..')

    if(s.returncode!=0):
        return "CE"

    if(useroutput!=output):
        return "WA"
    

    return "AC"
 