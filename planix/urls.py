"""
URL configuration for planix project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core.views import dashboard, create_project
from core.views.analysis_views import generate_analysis, view_analysis, history_analysis


urlpatterns = [
    path('admin/', admin.site.urls),

    # ✅ Add this line to enable login/logout pages
    path('accounts/', include('django.contrib.auth.urls')),

    path('', dashboard, name='dashboard'),
    path('project/create/', create_project, name='create_project'),
    path('project/<int:project_id>/analyze/', generate_analysis, name='generate_analysis'),
    path('analysis/<int:analysis_id>/', view_analysis, name='view_analysis'),
    path("project/<int:project_id>/analysis/history/", history_analysis, name="analysis_history"),

]

