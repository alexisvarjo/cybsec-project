from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User
from django.db import connection

def index(request):
    return render(request, 'index.html')

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # SQL injection vulnerability!! vulnerability number 1
        query = f"SELECT * FROM app_user WHERE username='{username}' AND password='{password}'"
        # Correct way to do it:
        # query = "SELECT * FROM app_user WHERE username=? AND password=?"
        with connection.cursor() as cursor:
            cursor.execute(query)
            #cursor.execute(query, (username, password))
            user = cursor.fetchone()

        if user:
            request.session['user'] = username  # No session expiry, no secure flags. Issue 2
            #correct way to do it:
            #request.session.set_expiry(1800)
            #request.session.modified = True
            #additional measures in settings.py at ../project/settings.py, line 125 onwards
            return redirect('dashboard')
        else:
            return HttpResponse("Login Failed")

        #Best way to do the login is to use django login, authenticate instead of writing own logic

    return render(request, 'login.html')

def dashboard(request):
    if 'user' not in request.session:
        return redirect('login')
    user = request.session.get('user', '')
    #issue 5
    #XSS as user session variable could include a script.
    #correct way to do it:
    #return render(request, 'dashboard.html', {'user': user}) where django handles the escape of any javascript etc.
    #see also templates/dashboard.html    
    return HttpResponse(f"Welcome {user}! <br> <a href='/admin'>Admin Panel</a>") 

# No access control, anybody can see the admin panel
# Issue 4
def admin_panel(request):
    return HttpResponse("Admin panel")
    #safe way to do it:
    #if 'user' not in request.session:
    # return redirect('login')
    #username = request.session['user']
    # try:
    #user = User.objects.get(username=username)
    #except User.DoesNotExist:
    # return HttpResponse("User not found", status=403)
    #if user.role != 'admin':
        #return HttpResponse("Forbidden", status=403)
    #return HttpResponse("Admin Panel")
