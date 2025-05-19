from django.shortcuts import render, redirect, get_object_or_404
from .models import User  # Use the custom User model
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Incident  # Import the Incident model
from .models import Evidence  # Import the Evidence model
from .models import Suspect  # Import the Suspect model
from .models import JoinRequest  # Import the JoinRequest model
from .models import Message  # Import the Message model
from .models import Threat  # Import the Threat model
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import requests
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from .models import Report  # Import the Report model
import google.generativeai as genai  # Import the Gemini API library
import markdown  # Import the markdown library

# Configure Gemini API once
genai.configure(api_key="AIzaSyBSX0pzvlMY9aFb4tRoif78EUvYz63us8w")  # Replace with your actual API key
model = genai.GenerativeModel('gemini-1.5-flash')  # Specify the Gemini model

def signup_view(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(email=email).exists():
            messages.error(request, "User already exists, please login")
            return redirect('login')  # Redirect to login page if user exists

        try:
            # Create user with email as username
            user = User.objects.create_user(
                username=email,       # Using email as username here
                email=email,
                password=password,
                first_name=name,
                role='User'           # explicitly set role to User on signup
            )
            user.save()
            messages.success(request, "Registration successful. Please log in.")
            return redirect('login')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('signup')

    return render(request, 'signup.html')



def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # Check if the user exists with the provided email
        try:
            user = User.objects.get(email=email)  # Use the custom User model
            username = user.username  # Get the username associated with the email
        except User.DoesNotExist:
            messages.error(request, "Invalid credentials")
            return redirect('login')

        # Authenticate using the username
        user = authenticate(request, username=username, password=password)

        if user is not None:  # Explicitly check if user is authenticated
            login(request, user)
            if user.is_superuser:  # Redirect superuser to admin dashboard
                return redirect('admin_dashboard')
            return redirect('user_dashboard')  # Redirect regular users to the user dashboard
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')

    return render(request, 'login.html')

def home(request):
    return render(request, 'home.html')

@login_required
def user_dashboard(request):
    incidents = Incident.objects.filter(user=request.user).exclude(incident_id__isnull=True)  # Incidents created by the user
    joined_incidents = Incident.objects.filter(assessors=request.user).exclude(user=request.user)  # Incidents the user is assessing

    # Fetch join requests for the logged-in user
    pending_requests = JoinRequest.objects.filter(requested_by=request.user, status='Pending')
    accepted_requests = JoinRequest.objects.filter(requested_by=request.user, status='Accepted')
    rejected_requests = JoinRequest.objects.filter(requested_by=request.user, status='Declined')

    return render(request, 'user_dashboard.html', {
        'incidents': incidents,
        'joined_incidents': joined_incidents,
        'pending_requests': pending_requests,
        'accepted_requests': accepted_requests,
        'rejected_requests': rejected_requests
    })

@login_required
@user_passes_test(lambda u: u.is_superuser)
def custom_admin_dashboard(request):
    incidents = Incident.objects.all()  # Fetch all incidents
    reports = Report.objects.all()  # Fetch all reports
    messages_list = Message.objects.all()  # Fetch all messages
    users = User.objects.all()  # Fetch all users
    join_requests = JoinRequest.objects.all()  # Fetch all join requests

    return render(request, 'admin_dashboard.html', {
        'incidents': incidents,
        'reports': reports,
        'messages_list': messages_list,
        'users': users,
        'join_requests': join_requests
    })

@login_required
def add_incident(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        severity = request.POST['severity']
        location = request.POST.get('location', '')  # Get location input
        date_occurred = request.POST.get('date_occurred', None)  # Get date_occurred input

        try:
            incident = Incident.objects.create(
                user=request.user,
                title=title,
                description=description,
                severity=severity,
                location=location,
                date_occurred=date_occurred
            )
            incident.save()
            messages.success(request, "Incident added successfully.")
            return redirect('user_dashboard')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('add_incident')

    return render(request, 'add_incident.html')

@login_required
def update_status(request, incident_id):
    if request.method == 'POST':
        status = request.POST.get('status')
        incident = get_object_or_404(Incident, incident_id=incident_id, user=request.user)  # Use incident_id here

        if status in ['Open', 'In Progress', 'Resolved']:
            incident.status = status
            incident.save()
            messages.success(request, "Incident status updated successfully.")
        else:
            messages.error(request, "Invalid status selected.")

    return redirect('user_dashboard')

@login_required
def add_evidence(request, incident_id):
    incident = get_object_or_404(Incident, incident_id=incident_id, user=request.user)

    if request.method == 'POST' and request.FILES['evidence_file']:
        evidence_file = request.FILES['evidence_file']
        fs = FileSystemStorage(location=settings.MEDIA_ROOT / 'evidence/')  # Use / for path concatenation
        filename = fs.save(evidence_file.name, evidence_file)
        file_url = fs.url(filename)

        try:
            Evidence.objects.create(
                incident=incident,
                file=filename,
                uploaded_by=request.user
            )
            messages.success(request, "Evidence added successfully.")
            return redirect('user_dashboard')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('add_evidence', incident_id=incident_id)

    return render(request, 'add_evidence.html', {'incident': incident})

@login_required
def add_suspect(request, incident_id):
    incident = get_object_or_404(Incident, incident_id=incident_id, user=request.user)

    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        ip_address = request.POST.get('ip_address', '')
        risk_score = request.POST.get('risk_score', 0.0)
        notes = request.POST.get('notes', '')

        try:
            Suspect.objects.create(
                incident=incident,
                name=name,
                email=email,
                ip_address=ip_address,
                risk_score=risk_score,
                notes=notes
            )
            messages.success(request, "Suspect added successfully.")
            return redirect('user_dashboard')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('add_suspect', incident_id=incident_id)

    return render(request, 'add_suspect.html', {'incident': incident})

@login_required
def available_incidents(request):
    # Exclude incidents with pending join requests by the user
    pending_incidents = JoinRequest.objects.filter(requested_by=request.user, status='Pending').values_list('incident__incident_id', flat=True)
    # Include incidents with rejected join requests
    rejected_incidents = JoinRequest.objects.filter(requested_by=request.user, status='Declined').values_list('incident__incident_id', flat=True)
    # Fetch incidents excluding pending ones
    incidents = Incident.objects.exclude(incident_id__in=pending_incidents).exclude(assessors=request.user) | Incident.objects.filter(incident_id__in=rejected_incidents)
    admins = User.objects.filter(is_superuser=True)  # List of available admins
    return render(request, 'available_incidents.html', {'incidents': incidents, 'admins': admins})

@login_required
def send_join_request(request, incident_id):
    incident = get_object_or_404(Incident, incident_id=incident_id)
    admin_id = request.POST.get('admin_id')
    admin = get_object_or_404(User, id=admin_id, is_superuser=True)
    message = request.POST.get('message', '')

    try:
        JoinRequest.objects.create(
            incident=incident,
            requested_by=request.user,
            admin=admin,
            message=message
        )
        messages.success(request, "Request sent to join the incident.")
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")

    return redirect('available_incidents')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def handle_join_request(request, request_id):
    join_request = get_object_or_404(JoinRequest, request_id=request_id)
    action = request.POST.get('action')

    if action == 'accept':
        join_request.status = 'Accepted'
        join_request.incident.assessors.add(join_request.requested_by)
        join_request.save()
        messages.success(request, "Join request accepted.")
    elif action == 'decline':
        join_request.status = 'Declined'
        join_request.save()
        messages.success(request, "Join request declined.")
    else:
        messages.error(request, "Invalid action.")

    return redirect('admin_dashboard')

@login_required
def chat(request, incident_id):
    incident = get_object_or_404(Incident, incident_id=incident_id)
    if request.user not in incident.assessors.all() and request.user != incident.user:
        messages.error(request, "You are not authorized to view this chat.")
        return redirect('user_dashboard')

    messages_list = Message.objects.filter(incident=incident).order_by('timestamp')  # Fetch messages for the incident

    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Message.objects.create(
                incident=incident,
                sender=request.user,
                content=content
            )
            return redirect('chat', incident_id=incident_id)

    return render(request, 'chat.html', {'incident': incident, 'messages_list': messages_list})

def compute_confidence_score(incident):
    score = 0.0

    # Severity weight
    severity_weights = {
        'Critical': 30,
        'High': 20,
        'Medium': 10,
        'Low': 0,
    }
    score += severity_weights.get(incident.severity, 0)

    # Evidence count contribution
    evidence_count = incident.evidences.count()
    if evidence_count >= 5:
        score += 25  # Strong evidence base
    elif evidence_count >= 3:
        score += 20
    elif evidence_count >= 1:
        score += 10

    # Threat keyword weights
    threat_keywords = {
        'high_risk': ['ransomware', 'rootkit', 'zero-day', 'data exfiltration'],
        'medium_risk': ['malware', 'trojan', 'phishing', 'keylogger'],
        'low_risk': ['suspicious', 'unauthorized', 'probe', 'scan'],
    }

    description = incident.description.lower()
    for kw in threat_keywords['high_risk']:
        if kw in description:
            score += 25
            break

    for kw in threat_keywords['medium_risk']:
        if kw in description:
            score += 15
            break

    for kw in threat_keywords['low_risk']:
        if kw in description:
            score += 5
            break

    # Suspicious file extensions with weights
    file_weight_map = {
        '.exe': 15,
        '.js': 10,
        '.bat': 10,
        '.vbs': 10,
        '.dll': 15,
        '.ps1': 20,
    }

    for evidence in incident.evidences.all():
        file_name = evidence.file.name.lower()
        for ext, weight in file_weight_map.items():
            if file_name.endswith(ext):
                score += weight
                break  # Avoid overcounting multiple extensions

    # Suspect risk score influence
    for suspect in incident.suspects.all():
        score += min(suspect.risk_score * 20, 25)  # Cap individual suspect impact

    # Bonus for multiple high-risk suspects
    high_risk_suspects = sum(1 for s in incident.suspects.all() if s.risk_score > 75)
    if high_risk_suspects >= 2:
        score += 10

    # Cap score to 100
    return min(score, 100.0)

@login_required
def generate_threat(request, incident_id):
    incident = get_object_or_404(Incident, incident_id=incident_id)

    if request.method == 'POST':
        threat_type = request.POST.get('threat_type', '').strip()
        threat_level = request.POST.get('threat_level', '').strip()

        if not threat_type or not threat_level:
            messages.error(request, "Threat type and level are required.")
            return redirect('user_dashboard')

        confidence_score = compute_confidence_score(incident)

        Threat.objects.create(
            incident=incident,
            threat_type=threat_type,
            confidence_score=confidence_score,
            threat_level=threat_level
        )
        messages.success(request, "Threat generated successfully.")
        return redirect('user_dashboard')

    return render(request, 'generate_threat.html', {'incident': incident})

@login_required
def generate_report(request, incident_id):
    incident = get_object_or_404(Incident, incident_id=incident_id)

    if request.method == 'POST':
        report_type = request.POST.get('report_type', '').strip()

        if not report_type:
            messages.error(request, "Report type is required.")
            return redirect('user_dashboard')

        # Collect incident data
        evidences = [evidence.file.name for evidence in incident.evidences.all()]
        suspects = [{"name": suspect.name, "risk_score": suspect.risk_score} for suspect in incident.suspects.all()]
        messages_list = [{"sender": message.sender.username, "content": message.content, "timestamp": str(message.timestamp)} for message in incident.messages.all()]
        threats = [{"type": threat.threat_type, "score": threat.confidence_score, "timestamp": str(threat.detected_at)} for threat in incident.threats.all()]

        prompt = f"""
        Generate a {report_type} report for the following incident details:

        Incident Title: {incident.title}
        Incident ID: {incident.incident_id}
        Description: {incident.description}
        Severity: {incident.severity}
        Status: {incident.status}
        Date Occurred: {incident.date_occurred}
        Location: {incident.location}

        Evidences: {evidences}
        Suspects: {suspects}
        Messages: {messages_list}
        Threats: {threats}
        """

        try:
            # Use Gemini API to generate the report
            response = model.generate_content(prompt)
            report_content = response.text

            # Save the generated report in the media/reports subfolder
            file_name = f"report_{incident.incident_id}_{report_type}.txt"
            file_path = default_storage.save(f"reports/{file_name}", ContentFile(report_content))

            # Create a Report object
            Report.objects.create(
                incident=incident,
                generated_by=request.user,
                report_type=report_type,
                file_path=file_path
            )
            messages.success(request, "Report generated successfully.")
        except Exception as e:
            messages.error(request, f"Failed to generate report: {e}")

        return redirect('user_dashboard')

    return render(request, 'generate_report.html', {'incident': incident})

@login_required
def view_report(request, report_id):
    report = get_object_or_404(Report, report_id=report_id)

    # Read the content of the report file
    try:
        with open(report.file_path.path, 'r', encoding='utf-8') as file:
            report_content = file.read()

        # Convert Markdown content to HTML
        html_content = markdown.markdown(report_content)

        return render(request, 'view_report.html', {
            'report': report,
            'html_content': html_content
        })
    except FileNotFoundError:
        messages.error(request, "The report file could not be found.")
        return redirect('user_dashboard')

