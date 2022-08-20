from fileinput import hook_compressed
from django.shortcuts import render,redirect
from django.http import HttpResponse,response
from .models import CustomUser,Fileupload
from .forms import usercreationform
from django.contrib.auth import authenticate,login,logout
from datetime import date
from django.http import FileResponse
import os


def home(request):
    return render(request,"home.html")

def SignUp(request):
    form = usercreationform
    if request.method == "POST":
        form = usercreationform(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.is_user = True
            f.save()
            return redirect(Login)
    return render(request, "signup.html", {"form": form})

def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password = password)
        if user and user.is_user == True:
            login(request, user)
            return redirect(Upload)
        else:
            return HttpResponse('Invalid login details')
    return render(request,"login.html")

def Userportal(request):
    if request.user.is_authenticated:
        #no of files
        files = Fileupload.objects.all()
        totalfiles = len(files)
        pdf = Fileupload.objects.filter(type=".pdf")
        csv = Fileupload.objects.filter(type=".csv")
        excel = Fileupload.objects.filter(type=".excel")
        txt = Fileupload.objects.filter(type=".txt")
        docx = Fileupload.objects.filter(type=".docx")
        users = []
        numbers = []
        for item in files:
            if item.user in users:
                pass
            else:
                users.append(item.user)
        length = len(users)
        for i in range(length):
            numbers.append(len(Fileupload.objects.filter(user=users[i])))
        userlist = dict(zip(users,numbers))
        return render(request,"userportel.html",{"pdf":len(pdf),"csv":len(csv),"excel":len(excel),"txt":len(txt),"docx":len(docx),"total":totalfiles,"userlist":userlist})
    return redirect(home)
def Upload(request,):
    files = Fileupload.objects.all()
    if request.user.is_authenticated:
        if request.method == "POST":
            file = request.FILES['file']
            if file:
                today = date.today()
                text = str(file)
                text1 = os.path.splitext(text)
                name = text1[0]
                type = text1[1]
                if type == ".pdf" or type == ".txt" or type == ".excel" or type == ".docx" or type ==".csv":
                    data = Fileupload(user=request.user, file=file, date=today, filename = name, type=type)
                    data.save()
                    return render(request, "fileupload.html", {"files": files})
                else:
                    error = "wrong file type"
                    fil = len(files)
                    return render(request, "fileupload.html", {"files": files,"error":error,"len":fil})
            return render(request, "fileupload.html", {"files": files})
        return render(request, "fileupload.html", {"files": files})
    return redirect(home)

def download(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        # user = request.user
        obj = Fileupload.objects.get(filename=name)
        response = FileResponse(open(obj.file.path, 'rb'))
        return response



def Logout(request):
    logout(request)
    return redirect(home)
