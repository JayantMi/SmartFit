from django.db import models
from django.utils import timezone 

# Create your models here.

class Contact(models.Model):
    name = models.CharField(max_length=50,default="")
    email = models.CharField(max_length=100,default="")
    phone = models.CharField(max_length=13,default="")
    query = models.TextField(default="")

class Member(models.Model):
    name = models.CharField(max_length=50,default="")
    email = models.CharField(max_length=100,default="")
    password = models.CharField(max_length=50,default="")
    phone = models.CharField(max_length=13,default="")
    gender = models.CharField(max_length=7,default="")
    city = models.CharField(max_length=30,default="")
    profile_pic = models.ImageField(upload_to="member/profile/")
    address = models.TextField()
    trainer_request = models.BooleanField(default=False)
    request_status = models.CharField(
        max_length=20,
        choices=[('none','None'), ('pending','Pending'), ('assigned','Assigned')],
        default='none'
    )
    assigned_trainer = models.ForeignKey(
        'Trainer',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='assigned_members'
    )

    def save(self, *args, **kwargs):
        if self.assigned_trainer:
            self.trainer_request = True
            self.request_status = 'assigned'
        elif self.trainer_request:
            self.request_status = 'pending'
        else:
            self.request_status = 'none'
        super().save(*args, **kwargs)
    def __str__(self):
        return self.name


class Trainer(models.Model):
    name = models.CharField(max_length=50,default="")
    email = models.CharField(max_length=100,default="")
    password = models.CharField(max_length=50,default="")
    phone = models.CharField(max_length=13,default="")
    gender = models.CharField(max_length=7,default="")
    city = models.CharField(max_length=30,default="")
    profile_pic = models.ImageField(upload_to="trainer/profile/")
    def __str__(self):
        return self.name


class Feedback(models.Model):
    member = models.ForeignKey(Member,on_delete=models.CASCADE)
    rating=models.IntegerField()
    comments = models.TextField()
    submitted_on = models.DateField(default=timezone.now)
    

class WorkoutProgram(models.Model):
    program_name = models.CharField(max_length=100)
    category = models.CharField(max_length=100) 
    duration_weeks = models.IntegerField()
    session_time = models.IntegerField(help_text="Workout duration in minutes")
    description = models.TextField()
    def __str__(self):
        return self.program_name


class Membership_Plan(models.Model):
    plan_name = models.CharField(max_length=100)
    duration = models.IntegerField()
    price = models.IntegerField()
    discription = models.TextField()  
    def __str__(self):
        return self.plan_name  

class UPI(models.Model):
    upi_id = models.CharField(max_length=40)

class Payment(models.Model):
    member = models.ForeignKey(Member,on_delete=models.CASCADE)  
    plan = models.ForeignKey(Membership_Plan,on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100, default="")    
    status = models.CharField(max_length=20, default="false") 
    def __str__(self):
        return self.member.name 

