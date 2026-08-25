from django.contrib import admin

# Register your models here.
from . models import Member , Contact , Trainer , Feedback , WorkoutProgram , Membership_Plan , UPI , Payment

class ContactAdmin(admin.ModelAdmin):
    list_display=["name","email","phone","query",]


class FeedbackAdmin(admin.ModelAdmin):
    list_display=["member","rating","comments"]
    list_filter=["rating"]

class MemberAdmin(admin.ModelAdmin):
    list_display=["name","email","city","trainer_request","request_status","assigned_trainer"]
    search_fields=["city"]
    list_filter=["trainer_request","request_status","city"]

class TrainerAdmin(admin.ModelAdmin):
    list_display=["name","email","city","profile_pic"] 
    search_fields=["city"]   

class WorkoutProgramAdmin(admin.ModelAdmin):
    list_display=["program_name","category","duration_weeks","session_time","description"]

class UPIAdmin(admin.ModelAdmin):
    list_display=["upi_id"]       
class PaymentAdmin(admin.ModelAdmin):
    list_display=["member","plan","transaction_id","status"]            


admin.site.register(Contact,ContactAdmin)
admin.site.register(Feedback,FeedbackAdmin)
admin.site.register(Member,MemberAdmin)
admin.site.register(Trainer,TrainerAdmin)
admin.site.register(WorkoutProgram,WorkoutProgramAdmin)
admin.site.register(Membership_Plan)
admin.site.register(UPI,UPIAdmin)
admin.site.register(Payment,PaymentAdmin)


##Customization of Admin Panel

admin.site.site_header="SmartFit Admin DashBoard"
admin.site.site_title="Fitness for healty life"

admin.site.index_title="Fitness Portal"


