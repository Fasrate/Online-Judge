from django import db
from django.shortcuts import redirect, render
from .models import Problem,Solution,TestCase
from django.core.files import File
import subprocess,os,sys
from django.contrib.auth.decorators import login_required
import time

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
        db=Solution(probid=probid,verdict=verdict)
        db.save()

    return redirect('leaderboard')


def check(request,probid):
    os.chdir('Test')
    input=TestCase.objects.get(probid=probid).input
    output=TestCase.objects.get(probid=probid).output
    code=request.POST.get('code')

    fcode=open('Code.c', 'w') 
    fcode.write(code)
    fcode.close()
    
    finput=open('Input.txt', 'w')
    finput.write(input)
    finput.close()
   
    # creates image from dockerfile
    docker_build_command = 'docker build -t myapp -f  dockerfile .'
    subprocess.run(docker_build_command, shell=True, timeout=60)

    # runs a container for above created image 

    ans=""
    try:
        start_time = time.time()
        s = subprocess.run(['docker', 'run', '--name', 'dockercontainer', 'myapp'], check=True, timeout=60)
        

        # copy output file from docker container to outside
        docker_cp_command = 'docker cp dockercontainer:/myapp/Useroutput.txt Useroutput.txt'
        result = subprocess.run(docker_cp_command, shell=True, timeout=10)


        fuseroutput = open('Useroutput.txt', 'r', encoding='utf-8')
        useroutput = fuseroutput.read()
        fuseroutput.close()


        fcode.close()
        finput.close()


        
        print(output)
        print(useroutput)
        print(s)
        if(s.returncode==0):
            ans= "TLE"
        elif(useroutput.strip()!=output.strip()):
            ans="WA"
        else:
            ans="AC"
    
    except Exception as e:
        print("woops!")
        ans= "CE"
    
    finally:
        subprocess.run(["docker", "rm", 'dockercontainer'], check=True)
        os.chdir('..')
    
        return ans
  

    
        
 