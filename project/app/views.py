from django.db import connection
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .models import User


def index(request):
    return render(request, "index.html")


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # SQL injection vulnerability!! vulnerability number 1
        query = f"SELECT * FROM app_user WHERE username='{username}' AND password='{password}'"
        with connection.cursor() as cursor:
            cursor.execute(query)
            user = cursor.fetchone()

        if user:
            request.session["user"] = (
                username  # No session expiry, no secure flags. Issue 2
            )
            # correct way to do it:
            # request.session.set_expiry(1800)
            # request.session.modified = True
            # additional measures in settings.py at ../project/settings.py, line 125 onwards
            return redirect("dashboard")
        else:
            return HttpResponse("Login Failed")

    return render(request, "login.html")

    # uncomment this line for flaw 3 and flaw 1
    # try:
    #    db_user = User.objects.get(username=username)
    # except User.DoesNotExist:
    #    return HttpResponse("Login Failed")

    # if db_user.check_password(password):  # secure hash check
    #    request.session["user"] = db_user.username
    #    request.session.set_expiry(1800)  # secure session timeout
    #    return redirect("dashboard")

    # return HttpResponse("Login Failed")


def dashboard(request):
    if "user" not in request.session:
        return redirect("login")

    current_user = request.session["user"]

    # ❌ Vulnerability: expose all user information to any logged-in user
    all_users = User.objects.all()

    return render(
        request,
        "dashboard.html",
        {
            "user": current_user,
            "users": all_users,
        },
    )


# No access control, anybody can see the admin panel
# Issue 4
def admin_panel(request):
    return HttpResponse("Admin panel")
    # safe way to do it:
    # if 'user' not in request.session:
    # return redirect('login')
    # username = request.session['user']
    # try:
    # user = User.objects.get(username=username)
    # except User.DoesNotExist:
    # return HttpResponse("User not found", status=403)

    # if user.role != 'admin':
    # return HttpResponse("Forbidden", status=403)
    # return HttpResponse("Admin Panel")


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        full_name = request.POST.get("full_name")
        birth_date = request.POST.get("birth_date")
        email = request.POST.get("email")

        if User.objects.filter(username=username).exists():
            return HttpResponse("Username already taken")

        if User.objects.filter(email=email).exists():
            return HttpResponse("Email already in use")

        user = User(
            username=username,
            full_name=full_name,
            birth_date=birth_date,
            email=email,
        )
        user.set_password(password)
        user.save()

        return redirect("login")

    return render(request, "register.html")

    return render(request, "register.html")


def users_public(request):
    from .models import User

    users = User.objects.all()
    return render(request, "users_public.html", {"users": users})
