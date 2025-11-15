from django.db import connection
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .models import User

# FLAW 1: SQL injection in login
#   True  = vulnerable
#   False = fixed
FLAW_1_SQL_INJECTION_LOGIN = True

# FLAW 2: insecure session handling
#   True  = vulnerable
#   False = fixed
FLAW_2_INSECURE_SESSION = True

# FLAW 4: no access control on admin panel
#   True  = vulnerable
#   False = fixed
FLAW_4_NO_ADMIN_ACCESS_CONTROL = True


def index(request):
    return render(request, "index.html")


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # flaw 1: SQL injection
        if FLAW_1_SQL_INJECTION_LOGIN:
            query = (
                f"SELECT * FROM app_user "
                f"WHERE username='{username}' AND password='{password}'"
            )
            with connection.cursor() as cursor:
                cursor.execute(query)
                row = cursor.fetchone()
            user_ok = row is not None
        else:
            try:
                db_user = User.objects.get(username=username)
            except User.DoesNotExist:
                user_ok = False
            else:
                user_ok = db_user.check_password(password)

        if user_ok:
            # FLAW 2: session handling
            request.session["user"] = username

            if not FLAW_2_INSECURE_SESSION:
                request.session.set_expiry(1800)  # 30 min

            return redirect("dashboard")
        else:
            return HttpResponse("Login Failed")

    return render(request, "login.html")


def dashboard(request):
    if "user" not in request.session:
        return redirect("login")

    current_user = request.session["user"]

    # XSS Vulnerability: expose all user info to any logged-in user
    all_users = User.objects.all()

    return render(
        request,
        "dashboard.html",
        {
            "user": current_user,
            "users": all_users,
        },
    )


def admin_panel(request):
    # FLAW 4: lack of access control in the admin panel
    if FLAW_4_NO_ADMIN_ACCESS_CONTROL:
        users = User.objects.all()
        return render(
            request,
            "admin.html",
            {"user": request.session.get("user", "Guest"), "users": users},
        )

    # Fixed version
    if "user" not in request.session:
        return redirect("login")

    username = request.session["user"]

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse("User not found", status=403)

    if user.role != "admin":
        return HttpResponse("Forbidden", status=403)

    users = User.objects.all()
    return render(request, "admin.html", {"user": user.username, "users": users})


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        full_name = request.POST.get("full_name")
        birth_date = request.POST.get("birth_date")
        email = request.POST.get("email")

        # Prevent duplicates
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

        # Flaw 3 is handled inside set_password/check_password
        user.set_password(password)
        user.save()

        return redirect("login")

    return render(request, "register.html")


def users_public(request):
    users = User.objects.all()
    return render(request, "users_public.html", {"users": users})
