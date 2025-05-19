from django.urls import path
from .views import signup_view, home, login_view, user_dashboard, custom_admin_dashboard, add_incident, update_status, add_evidence, add_suspect, available_incidents, send_join_request, handle_join_request, chat, generate_threat, generate_report, view_report
from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('user_dashboard')

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('', home, name='home'),
    path('admin_dashboard/', custom_admin_dashboard, name='admin_dashboard'),
    path('logout/', logout_view, name='logout'),
    path('add-incident/', add_incident, name='add_incident'),
    path('update-status/<int:incident_id>/', update_status, name='update_status'),
    path('add-evidence/<int:incident_id>/', add_evidence, name='add_evidence'),
    path('user-dashboard/', user_dashboard, name='user_dashboard'),  # Add this line
    path('add-suspect/<int:incident_id>/', add_suspect, name='add_suspect'),
    path('available-incidents/', available_incidents, name='available_incidents'),
    path('send-join-request/<int:incident_id>/', send_join_request, name='send_join_request'),
    path('handle-join-request/<int:request_id>/', handle_join_request, name='handle_join_request'),
    path('chat/<int:incident_id>/', chat, name='chat'),
    path('generate-threat/<int:incident_id>/', generate_threat, name='generate_threat'),
    path('generate-report/<int:incident_id>/', generate_report, name='generate_report'),
    path('view-report/<int:report_id>/', view_report, name='view_report'),
]