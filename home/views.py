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
   
    print("yo")
    # creates image from dockerfile
    docker_build_command = 'docker build -t myapp -f  dockerfile .'
    subprocess.run(docker_build_command, shell=True)

    # runs a container for above created image 

    
    try:
        docker_run_command = f'docker run --name dockercontainer myapp'
        subprocess.run(docker_run_command, capture_output=True,text =True)

        # copy output file from docker container to outside
        docker_cp_command = 'docker cp dockercontainer:/myapp/Useroutput.txt Useroutput.txt'
        subprocess.run(docker_cp_command, shell=True, check=True)

        fuseroutput = open('Useroutput.txt', 'r', encoding='utf-8')
        useroutput = fuseroutput.read()
        fuseroutput.close()


        fcode.close()
        finput.close()



        # if(s.returncode!=0):
        #     return "CE"
        print(output)
        print(useroutput)

        if(useroutput.strip()!=output.strip()):
            return "WA"
        

        return "AC"
    
    except subprocess.CalledProcessError as e:

        return "CE"
    
  
    # Not able to handle TLE case

    
        
 