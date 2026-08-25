from django.shortcuts import render
from . models import Contact

# Create your views here.

def home(request):
    return render(request,"smartfit_app/html/index.html")

def about(request):
        return render(request,"smartfit_app/html/about.html")

def contact(request):
    if request.method=="GET":
        return render(request,"smartfit_app/html/contact.html")
    if request.method=="POST":
        name = request.POST["name"]
        email=request.POST["email"]
        phone = request.POST["phone"]
        query = request.POST["query"]
        print("name=",name," email=",email,"phone=",phone," query=",query)
        contact_obj = Contact(name=name,email=email,phone=phone,query=query)
        contact_obj.save()
        return render(request,"smartfit_app/html/index.html")  





