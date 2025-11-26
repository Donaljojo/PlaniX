from django.contrib import admin
from django.urls import path
from core.views.dashboard_views import dashboard
from core.views.project_views import create_project
from core.views.analysis_views import generate_analysis, view_analysis, history_analysis

urlpatterns = [
    path("admin/", admin.site.urls),

    # Project actions
    path("project/create/", create_project, name="create_project"),
    path("project/<int:project_id>/analysis/", generate_analysis, name="generate_analysis"),
    path("analysis/<int:analysis_id>/", view_analysis, name="view_analysis"),
    path("project/<int:project_id>/analysis/history/", history_analysis, name="analysis_history"),

    # Dashboard last (so it doesn't override other routes)
    path("", dashboard, name="dashboard"),
]



