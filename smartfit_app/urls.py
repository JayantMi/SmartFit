from django.urls import path
from . import views , member_views , trainer_views

urlpatterns = [
    path("",views.home,name="home"),
    path("about/",views.about,name="about"),
    path("contact/",views.contact,name="contact"),
    path("registration/",member_views.registration,name="registration"),
    path("member_login/",member_views.member_login,name="member_login"),
    path("member_home/",member_views.member_home,name="member_home"),
    path("t_login/",trainer_views.t_login,name="t_login"),
    path("feedback/",member_views.feedback,name="feedback"),
    path("trainer_home/",trainer_views.trainer_home,name="trainer_home"),
    path("member_logout/",member_views.member_logout,name="member_logout"),
    path("trainer_logout/",trainer_views.trainer_logout,name="trainer_logout"),
    path("member_edit_profile/",member_views.edit_profile,name="member_edit_profile"),
    path("trainer_edit_profile/",trainer_views.t_edit_profile,name="trainer_edit_profile"),
    path("view_workout/",member_views.view_workout,name="view_workout"),
    path("view_membership/",member_views.view_membership,name="view_membership"),
    path("purchase_plan/<int:id>",member_views.purchase_plan,name="purchase_plan"),
    path("purchase/",member_views.purchase,name="purchase"),
    path("view_purchase_plan/",member_views.view_purchase_plan,name="view_purchase_plan"),
    path("fitness_goal_planner/",member_views.fitness_goal_planner,name="fitness_goal_planner"),
    path("request_personal_trainer/",member_views.request_personal_trainer,name="request_personal_trainer"),
    path("view_assigned_trainer/",member_views.view_assigned_trainer,name="view_assigned_trainer"),
    path("ai_response/",member_views.ai_response,name="ai_response"),
    path("assigned_members/",trainer_views.assigned_members,name="assigned_members"),
    path("reset_password/",member_views.reset_password,name="reset_password"),


]