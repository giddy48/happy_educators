from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

def login_view(request):
    error = None

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            if user.is_superuser:
                return redirect('results')
            elif user.groups.filter(name='Teacher').exists():
                return redirect('teacher-dashboard')
            elif user.groups.filter(name='Student').exists():
                return redirect('results')
        else:
            error = "Invalid credentials"

    return render(request, 'accounts/login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('login')
from django.shortcuts import redirect

def dashboard_router(request):
    profile = request.user.profile

    if profile.role == 'admin':
        return redirect('admin_dashboard')
    elif profile.role == 'teacher':
        return redirect('teacher_dashboard')
    else:
        return redirect('student_dashboard')
from django.shortcuts import render

def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

def teacher_dashboard(request):
    return render(request, 'teacher_dashboard.html')

@login_required
def student_dashboard(request):
    return render(request, "academics/student_dashboard.html")