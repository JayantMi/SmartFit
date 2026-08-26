from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.cache import never_cache

from .models import (
    Member,
    Feedback,
    WorkoutProgram,
    Membership_Plan,
    UPI,
    Payment,
)


import os
from dotenv import load_dotenv
import cohere

load_dotenv()


def member_required(request):
    if "role" not in request.session:
        return False

    if request.session["role"] != "member":
        return False

    if "member_email" not in request.session:
        return False

    return True




def member_logout(request):
    request.session.flush()
    messages.success(request, "Logged out successfully")
    return redirect("member_login")




def registration(request):

    if request.method == "GET":
        return render(request, "smartfit_app/member/registration.html")

    if request.method == "POST":

        try:
            email = request.POST["email"]

            if Member.objects.filter(email=email).exists():
                messages.error(request, "Email already registered")
                return redirect("registration")

            Member.objects.create(
                name=request.POST["name"],
                email=email,
                password=request.POST["password"],
                phone=request.POST["phone"],
                gender=request.POST["gender"],
                city=request.POST["city"],
                profile_pic=request.FILES["profile_pic"],
                address=request.POST["address"],
            )

            messages.success(request, "Registration successful")
            return redirect("member_login")

        except:
            messages.error(request, "Something went wrong")
            return redirect("registration")




def member_login(request):

    if request.method == "GET":
        return render(request, "smartfit_app/member/member_login.html")

    if request.method == "POST":

        email = request.POST["email"]
        password = request.POST["password"]

        data = Member.objects.filter(email=email)

        if data.exists():

            user = data.first()

            if user.password == password:

                request.session["role"] = "member"
                request.session["member_email"] = email

                messages.success(request, "Login successful")
                return redirect("member_home")

            else:
                messages.error(request, "Wrong password")
                return redirect("member_login")

        else:
            messages.error(request, "Email not found")
            return redirect("member_login")



@never_cache
def member_home(request):

    if not member_required(request):
        return redirect("member_login")

    member = Member.objects.get(
        email=request.session["member_email"]
    )

    return render(
        request,
        "smartfit_app/member/member_home.html",
        {
            "member": member,
            "assigned_trainer": member.assigned_trainer
        }
    )




@never_cache
def edit_profile(request):

    if not member_required(request):
        return redirect("member_login")

    member = Member.objects.get(
        email=request.session["member_email"]
    )

    if request.method == "GET":
        return render(
            request,
            "smartfit_app/member/edit_profile.html",
            {"member": member}
        )

    if request.method == "POST":

        member.name = request.POST["name"]
        member.phone = request.POST["phone"]
        member.address = request.POST["address"]

        if "profile_pic" in request.FILES:
            member.profile_pic = request.FILES["profile_pic"]

        member.save()

        messages.success(request, "Profile updated")
        return redirect("member_edit_profile")




@never_cache
def feedback(request):

    if not member_required(request):
        return redirect("member_login")

    if request.method == "GET":
        return render(request, "smartfit_app/member/feedback.html")

    if request.method == "POST":

        member = Member.objects.get(
            email=request.session["member_email"]
        )

        Feedback.objects.create(
            member=member,
            rating=request.POST["rating"],
            comments=request.POST["message"]
        )

        messages.success(request, "Feedback submitted")
        return redirect("feedback")




def view_workout(request):

    programs = WorkoutProgram.objects.all()

    return render(
        request,
        "smartfit_app/member/view_workout.html",
        {"workout_program": programs}
    )




@never_cache
def view_membership(request):

    if not member_required(request):
        return redirect("member_login")

    plans = Membership_Plan.objects.all()

    return render(
        request,
        "smartfit_app/member/view_membership.html",
        {"membership_plan": plans}
    )




@never_cache
def purchase_plan(request, id):

    if not member_required(request):
        return redirect("member_login")

    plan = Membership_Plan.objects.get(id=id)

    upi = UPI.objects.first()

    upi_link = f"upi://pay?pa={upi.upi_id}&am={plan.price}"

    return render(
        request,
        "smartfit_app/member/purchase_plan.html",
        {
            "plans": plan,
            "upi_link": upi_link
        }
    )




@never_cache
def purchase(request):

    if not member_required(request):
        return redirect("member_login")

    if request.method == "POST":

        member = Member.objects.get(
            email=request.session["member_email"]
        )

        if Payment.objects.filter(member=member).exists():
            messages.error(request, "You already purchased a plan")
            return redirect("member_home")

        plan = Membership_Plan.objects.get(
            id=request.POST["plan_id"]
        )

        Payment.objects.create(
            member=member,
            plan=plan,
            transaction_id=request.POST["transaction_id"],
            status="Pending"
        )

        messages.success(request, "Payment submitted")
        return redirect("member_home")




@never_cache
def view_purchase_plan(request):

    if not member_required(request):
        return redirect("member_login")

    member = Member.objects.get(
        email=request.session["member_email"]
    )

    payment = Payment.objects.filter(member=member).first()

    if not payment:
        return render(
            request,
            "smartfit_app/member/view_purchase_plan.html",
            {
                "payments": None,
                "message": "You have not purchased any plan yet."
            }
        )

    return render(
        request,
        "smartfit_app/member/view_purchase_plan.html",
        {"payments": payment}
    )


@never_cache
def request_personal_trainer(request):

    if not member_required(request):
        return redirect("member_login")

    member = Member.objects.get(
        email=request.session["member_email"]
    )

    if request.method == "GET":
        return render(
            request,
            "smartfit_app/member/request_personal_trainer.html",
            {"member": member}
        )

    if request.method == "POST":

        member.trainer_request = True
        member.request_status = "pending"
        member.save()

        messages.success(request, "Trainer request sent")
        return redirect("member_home")




@never_cache
def view_assigned_trainer(request):

    if not member_required(request):
        return redirect("member_login")

    member = Member.objects.get(
        email=request.session["member_email"]
    )

    return render(
        request,
        "smartfit_app/member/view_assigned_trainer.html",
        {
            "member": member,
            "assigned_trainer": member.assigned_trainer
        }
    )




@never_cache
def reset_password(request):

    if not member_required(request):
        return redirect("member_login")

    if request.method == "GET":
        return render(
            request,
            "smartfit_app/member/reset_password.html"
        )

    if request.method == "POST":

        member = Member.objects.get(
            email=request.session["member_email"]
        )

        old = request.POST["old_password"]
        new = request.POST["confirm_password"]

        if member.password == old:

            member.password = new
            member.save()

            messages.success(request, "Password updated")

        else:
            messages.error(request, "Old password wrong")

        return redirect("reset_password")




@never_cache
def fitness_goal_planner(request):

    if not member_required(request):
        return redirect("member_login")

    if request.method == "GET":
        return render(request,"smartfit_app/member/fitness_goal_planner.html")

    if request.method == "POST":

        goal = request.POST["fitness_goal"]
        weight = request.POST["current_weight"]
        age = request.POST["age"]
        activity = request.POST["activity_level"]
        workout = request.POST["weekly_workouts"]
        diet = request.POST["dietary_preference"]
        calorie = request.POST["calorie_target"]
        note = request.POST["extra_notes"]

        prompt = f"""
Create advanced professional fitness report in HTML.

User Details:
Goal: {goal}
Weight: {weight} kg
Age: {age}
Activity: {activity}
Workout Days: {workout}
Diet Type: {diet}
Calories: {calorie}
Extra Notes: {note}

Give output in this format:

<h2>1. Goal Analysis</h2>

<h2>2. Weekly Workout Plan</h2>
Day wise table

<h2>3. Nutrition Plan</h2>
Meal table

<h2>4. Protein / Carb / Fat Chart</h2>

<h2>5. Important Tips</h2>

Use colorful HTML tables and bullet points.
"""

        try:
            client = cohere.Client(os.getenv("COHERE_API_KEY"))

            response = client.chat(
                model="command-a-03-2025",
                message=prompt
            )

            answer = response.text

        except Exception as e:

            print("AI Error:", e)

            answer = f"""
            <h2>Your Goal : {goal}</h2>

            <table border='1' cellpadding='10'>
            <tr><th>Nutrient</th><th>Target</th></tr>
            <tr><td>Protein</td><td>{int(float(weight)*2)} gm</td></tr>
            <tr><td>Carbs</td><td>{int(float(weight)*4)} gm</td></tr>
            <tr><td>Fats</td><td>{int(float(weight)*0.8)} gm</td></tr>
            </table>

            <h3>Workout Split</h3>
            <ul>
            <li>Monday - Chest</li>
            <li>Tuesday - Back</li>
            <li>Wednesday - Legs</li>
            <li>Thursday - Shoulder</li>
            <li>Friday - Arms</li>
            </ul>
            """

        return render(
            request,
            "smartfit_app/member/ai_response.html",
            {
                "answer": answer,
                "page_title": "Your SmartFit Result",
                "page_subtitle": "Your personalized AI fitness result is ready.",
                "back_url": "/fitness_goal_planner/"
            }
        )


def ai_response(request):

    return render(
        request,
        "smartfit_app/member/ai_response.html"
    )