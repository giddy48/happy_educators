from django.contrib import admin
from django.urls import path, include
from academics import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('academics/', include('academics.urls')),

    # AUTH
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # DASHBOARD
    path('dashboard/', views.dashboard_home, name='dashboard'),

    # APP ROUTES
    path('', include('academics.urls')),
]


