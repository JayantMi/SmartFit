from django.shortcuts import render , redirect
from . models import Trainer, Member

from django.contrib import messages
from django.views.decorators.cache import never_cache

##memberLogout
def trainer_logout(request):
    request.session.flush()#to clear all the keys from session dict\
    messages.success(request,"Successfully Logged Out")
    return redirect("t_login")



def t_login(request):
    if request.method =="GET":
        return render(request,"smartfit_app/trainer/t_login.html")
    
    if request.method=="POST":
        m_email = request.POST["email"]
        m_password = request.POST["password"]
        data = Trainer.objects.filter(email=m_email)
        if len(data)>0:
            if m_password==data[0].password:
                request.session["role"]="trainer"
                request.session["trainer_email"]=m_email

                messages.success(request,"login successfuly")
                return redirect("trainer_home")
                
            else:
                messages.error(request,"password not match")
                return redirect("t_login")
        else:
            messages.error(request,"email not match")
            return redirect("t_login")
        
@never_cache
def trainer_home(request):
    key=request.session.keys()
    if "role" in key:
        if request.session["role"]=="trainer":
         trainer_email = request.session["trainer_email"]
         trainer_obj = Trainer.objects.get(email=trainer_email)
         assigned_members = trainer_obj.assigned_members.all()
         data = {
                    "trainer":trainer_obj,
                    "assigned_members": assigned_members,
                    "member_count": assigned_members.count()
                }
         return render(request,"smartfit_app/trainer/trainer_home.html",data)
    else:
            messages.error(request,"unorthorised access")
            return redirect("t_login")

@never_cache
def assigned_members(request):
    key=request.session.keys()
    if "role" not in key or request.session.get("role") != "trainer":
        messages.error(request, "Please login as a trainer to view assigned members")
        return redirect("t_login")

    trainer_email = request.session["trainer_email"]
    trainer_obj = Trainer.objects.get(email=trainer_email)
    members = trainer_obj.assigned_members.all()
    return render(request, "smartfit_app/trainer/assigned_members.html", {"trainer": trainer_obj, "members": members})


def t_edit_profile(request):
    trainer_email = request.session["trainer_email"]
    if request.method=="GET":
        trainer_obj = Trainer.objects.get(email=trainer_email)
        data = {
            "trainer":trainer_obj
        }
        return render(request,"smartfit_app/trainer/t_edit_profile.html",data)
    if request.method=="POST":
        name = request.POST["name"]
        phone = request.POST["phone"]
        city = request.POST["city"]
        profile_pic = request.FILES["profile_pic"]
        trainer_obj = Trainer.objects.get(email=trainer_email)
        trainer_obj.name=name
        trainer_obj.phone=phone
        trainer_obj.city=city
        trainer_obj.profile_pic=profile_pic
        trainer_obj.save()
        return redirect("trainer_edit_profile")
        

    