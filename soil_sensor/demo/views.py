import json
import threading
from turtle import pd
import joblib
import openpyxl
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from datetime import datetime, time, timezone, timedelta
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from django.contrib import messages

from sklearn.discriminant_analysis import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from .models import Contact, Pest, SensorData, Device, NewUser, PasswordResetOTP
from .serializers import LEDControlSerializer, SensorDataSerializer
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import make_naive, localtime, now,timedelta
from rest_framework.response import Response
from demo.models import Crop, Device, Disease, FertilizerRequirement, LEDControl, NewUser, Plot, SensorData
from django.core.paginator import Paginator
from rest_framework import status
from io import BytesIO
import pytz
from django.views.decorators.csrf import csrf_exempt 
from django.utils import timezone
import time
from django.contrib.auth.models import User
from sqlalchemy import create_engine
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import google.generativeai as genai
from django.core.mail import send_mail
from django.conf import settings
import random
import string
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.urls import reverse_lazy

def add_customer(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        contact_no = request.POST.get('phone')
        password = request.POST.get('password')
        place = request.POST.get('place')
        passw = make_password(password)

        username = email if email else contact_no

        # Check for existing email or phone
        if NewUser.objects.filter(username=username).exists():
            error_message = "User already exists."
            return render(request, 'register.html', {'error_message': error_message})

        # Create new user
        user = NewUser.objects.create(
            username=username,
            full_name=full_name,
            email=email,
            contact_no=contact_no,
            password=passw,
            place=place,
        )

        # Send welcome email
        try:
            subject = 'Welcome to Soil Sensors'
            message = f'''Hello {full_name},

Thank you for registering with Soil Sensors!

Your account has been successfully created with the following details:
Email: {email}
Phone: {contact_no}

You can now login to your account and start monitoring your soil sensors.

Best regards,
Soil Sensors Team'''
            
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False
            )
            print(f"Welcome email sent to {email}")  # Debug print
        except Exception as e:
            print(f"Failed to send welcome email: {str(e)}")  # Debug print

        error_message = "User added successfully. Please login."
        return render(request, 'register.html', {'user_added': True, 'error_message': error_message})
    
    return render(request, 'register.html')



@login_required
def customer_profile(request):
    user = request.user  # Current logged-in user
    devices = Device.objects.filter(user=user)
    context = {
        'user': user,
        'devices': devices,
    }
    return render(request, "my-account.html", context)

def login_view(request):
    if request.method == 'POST':
        username_input = request.POST.get('username')  # could be email or phone
        password = request.POST.get('password')

        try:
            user_obj = NewUser.objects.get(email=username_input)
        except NewUser.DoesNotExist:
            try:
                user_obj = NewUser.objects.get(contact_no=username_input)
            except NewUser.DoesNotExist:
                user_obj = None

        if user_obj:
            user = authenticate(request, username=user_obj.username, password=password)
            if user:
                login(request, user)
                if user.is_superuser:
                    return redirect('/admin_dashboard/')
                return redirect('home')
        
        error_message = "Invalid email or phone number, or password. Please try again."
        return render(request, 'login.html', {'error_message': error_message})

    return render(request, 'login.html')



def logout_view(request):
    logout(request)
    return redirect("login_view")


# ==============================================================admin==============================================================

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import NewUser, Device, FertilizerRequirement, Disease, Crop, SensorData, LEDControl
from django.core.serializers import serialize
import json

@login_required(login_url="/")
def admin_dashboard(request):
    # Model counts
    total_users = NewUser.objects.filter(is_superuser=False).count()
    total_devices = Device.objects.count()
    total_fertilizers = FertilizerRequirement.objects.count()
    total_diseases = Disease.objects.count()
    total_crops = Crop.objects.count()

    # Fetch devices with LED control status
    devices = Device.objects.all().prefetch_related('led_controls')
    device_data = []
    for device in devices:
        # Get latest SensorData by device_name
        latest_sensor_data = SensorData.objects.filter(device_name=device.device_name).order_by('-timestamp').first()
        # Get latest LEDControl
        latest_led_control = device.led_controls.order_by('-start_time').first()
        # Debug logging
        print(f"Device: {device.device_name}")
        print(f"  SensorData: {latest_sensor_data}")
        print(f"  LEDControl: {latest_led_control}")
        device_data.append({
            'device_name': device.device_name,
            'latest_sensor_data': latest_sensor_data,
            'latest_led_control': latest_led_control
        })

    # Sensor data for charts (last 10 readings)
    sensor_data = SensorData.objects.order_by('-timestamp')[:10]
    sensor_data_json = serialize('json', sensor_data, fields=('timestamp', 'temperature', 'moisture'))
    # Debug logging
    print("Sensor data for charts:", sensor_data.count())
    print("Serialized sensor_data_json:", sensor_data_json)

    context = {
        'total_users': total_users,
        'total_devices': total_devices,
        'total_fertilizers': total_fertilizers,
        'total_diseases': total_diseases,
        'total_crops': total_crops,
        'devices': device_data,
        'sensor_data_json': sensor_data_json
    }
    return render(request, 'admin1/admin_dashboard.html', context)


@login_required(login_url="/admin_login")
def view_customers(request):
    customers = NewUser.objects.filter(is_superuser=False).prefetch_related('devices').order_by('-id')
    context = {
        'customers': customers
    }
    return render(request, 'admin1/view_customers.html', context)


# Update customer details
def update_customer(request, customer_id):
    user = get_object_or_404(NewUser, id=customer_id)

    if request.method == 'POST':
        user.username = request.POST.get('username', user.username)
        user.email = request.POST.get('email', user.email)
        user.contact_no = request.POST.get('contact_no', user.contact_no)
        user.place = request.POST.get('place', user.place)
        user.location = request.POST.get('location', user.location)
        user.save()

        return redirect('view_customers') 

    return render(request, 'admin1/update_customer.html', {'user': user})

#delete customer
def delete_user(request,id):
    obj = NewUser.objects.get(id=id)
    obj.delete()
    return redirect('/view_customers')



@login_required(login_url="/admin_login")
def register_device(request):
    users = NewUser.objects.all()  # Fetch all users

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        device_name = request.POST.get('device_name')
        user = get_object_or_404(NewUser, id=user_id)

        # Check if the device name already exists for this user
        if Device.objects.filter(user=user, device_name=device_name).exists():
            error_message = "Device name already exists for this user"
            return render(request, 'admin1/device_register.html', {'error_message': error_message, 'users': users})

        # Create and associate device with the user
        Device.objects.create(user=user, device_name=device_name)
        success_message = "Device registered successfully!"
        return render(request, 'admin1/device_register.html', {'device_added': True, 'users': users, 'success_message': success_message})

    return render(request, 'admin1/device_register.html', {'users': users})




@login_required(login_url="/admin_login")
def manage_devices(request, user_id):
    user = get_object_or_404(NewUser, id=user_id)
    devices = user.devices.all()
    if request.method == "POST":
        device_id = request.POST.get("device_id")
        device = get_object_or_404(Device, id=device_id, user=user)
        # Update device name
        new_device_name = request.POST.get("device_name")
        if new_device_name:
            device.device_name = new_device_name
        # Update subscription days
        days = request.POST.get("subscription_days")
        if days and days.isdigit():
            device.subscription_end_date = now() + timedelta(days=int(days))
        # Update device status
        device.is_active = "device_status" in request.POST  # Checkbox is checked if present

        # Save all changes
        device.save()

        return redirect("manage_devices", user_id=user.id)

    return render(request, "admin1/manage_devices.html", {"user": user, "devices": devices})



@login_required(login_url="/admin_login")
def delete_device(request, device_id):
    device = get_object_or_404(Device, id=device_id)
    user_id = device.user.id  # Save user ID before deleting
    device.delete()
    return redirect('manage_devices', user_id=user_id)

# User List for Deveice Data
@login_required(login_url="/")
def user_list(request):
    users = NewUser.objects.filter(is_superuser=False)  # Fetch all users
    return render(request, "admin1/admin_user_list.html", {"users": users})


@login_required(login_url="/")
def user_devices(request, user_id):
    user = get_object_or_404(NewUser, id=user_id)
    devices = user.devices.all()  # Fetch all devices for the selected user
    return render(request, "admin1/user_devices.html", {"user": user, "devices": devices})



@login_required(login_url="/")
def view_device_data(request, device_name):
    latest_entry = SensorData.objects.filter(device_name=device_name).order_by('-timestamp').first()

    # Get current time and subtract 5 minutes
    five_minutes_ago = now() - timedelta(minutes=1)

    if latest_entry and latest_entry.timestamp >= five_minutes_ago:
        adjusted_timestamp = localtime(latest_entry.timestamp) + timedelta(hours=5, minutes=30)
        sensor_data = {
            'temperature': latest_entry.temperature,
            'sensor_id': latest_entry.sensor_id,
            'moisture': latest_entry.moisture,
            'timestamp': adjusted_timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'conductivity': latest_entry.conductivity,
            'pH': latest_entry.pH,
            'device_name': latest_entry.device_name,
            'led_status': latest_entry.led_status,
            'overall_moisture': latest_entry.overall_moisture,
            'status': latest_entry.status,
        }
    else:
        # If no data or data is older than 5 minutes, return "Offline"
        sensor_data = {
            'temperature': "Offline",
            'sensor_id': "Offline",
            'moisture': "Offline",
            'timestamp': "Offline",
            'conductivity': "Offline",
            'pH': "Offline",
            'device_name': device_name,
            'led_status': "Offline",
            'overall_moisture': "Offline",
            'status': "Offline",
        }

    return JsonResponse(sensor_data)  # Return JSON response


@login_required(login_url="/")
def display_sensor_data(request, device_name):
    return render(request, 'admin1/device_data.html', {'device_name': device_name})



def all_crops(request):
    crops = Crop.objects.all()
    return render(request, 'admin1/all_crops.html', {'crops': crops})


def add_crop(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        scientific_name = request.POST.get('scientific_name')
        crop_type = request.POST.get('crop_type')
        general_information = request.POST.get('general_information')
        growth_duration = request.POST.get('growth_duration')
        temperature = request.POST.get('temperature')
        rainfall = request.POST.get('rainfall')
        sowing_temperature = request.POST.get('sowing_temperature')
        harvesting_temperature = request.POST.get('harvesting_temperature')
        season = request.POST.get('season')
        soil = request.POST.get('soil')
        land_preparation = request.POST.get('land_preparation')
        seed_rate = request.POST.get('seed_rate')
        seed_treatment = request.POST.get('seed_treatment')
        insecticide_name = request.POST.get('insecticide_name')
        quantity = request.POST.get('quantity')
        time_of_sowing = request.POST.get('time_of_sowing')
        spacing = request.POST.get('spacing')
        method_of_sowing = request.POST.get('method_of_sowing')
        sowing_depth = request.POST.get('sowing_depth')
        weed_control = request.POST.get('weed_control')
        irrigation = request.POST.get('irrigation')
        ph_level = request.POST.get('ph_level')
        harvesting_time = request.POST.get('harvesting_time')
        yield_per_hectare = request.POST.get('yield_per_hectare')
        post_harvest_handling = request.POST.get('post_harvest_handling')
        image = request.FILES.get('image')

        crop = Crop.objects.create(
            name=name,
            scientific_name=scientific_name,
            crop_type=crop_type,
            general_information=general_information,
            growth_duration=growth_duration,
            temperature=temperature,
            rainfall=rainfall,
            sowing_temperature=sowing_temperature,
            harvesting_temperature=harvesting_temperature,
            season=season,
            soil=soil,
            land_preparation=land_preparation,
            seed_rate=seed_rate,
            seed_treatment=seed_treatment,
            insecticide_name=insecticide_name,
            quantity=quantity,
            time_of_sowing=time_of_sowing,
            spacing=spacing,
            method_of_sowing=method_of_sowing,
            sowing_depth=sowing_depth,
            weed_control=weed_control,
            irrigation=irrigation,
            ph_level=ph_level,
            harvesting_time=harvesting_time,
            yield_per_hectare=yield_per_hectare,
            post_harvest_handling=post_harvest_handling,
            image=image
        )
        return redirect('all_crops')

    return render(request, 'admin1/add_crop.html')


def update_crop(request, crop_id):
    crop = get_object_or_404(Crop, id=crop_id)
    if request.method == 'POST':
        crop.name = request.POST.get('name')
        crop.scientific_name = request.POST.get('scientific_name')
        crop.crop_type = request.POST.get('crop_type')
        crop.general_information = request.POST.get('general_information')
        crop.growth_duration = request.POST.get('growth_duration')
        crop.temperature = request.POST.get('temperature')
        crop.rainfall = request.POST.get('rainfall')
        crop.sowing_temperature = request.POST.get('sowing_temperature')
        crop.harvesting_temperature = request.POST.get('harvesting_temperature')
        crop.season = request.POST.get('season')
        crop.soil = request.POST.get('soil')
        crop.land_preparation = request.POST.get('land_preparation')
        crop.seed_rate = request.POST.get('seed_rate')
        crop.seed_treatment = request.POST.get('seed_treatment')
        crop.insecticide_name = request.POST.get('insecticide_name')
        crop.quantity = request.POST.get('quantity')
        crop.time_of_sowing = request.POST.get('time_of_sowing')
        crop.spacing = request.POST.get('spacing')
        crop.method_of_sowing = request.POST.get('method_of_sowing')
        crop.sowing_depth = request.POST.get('sowing_depth')
        crop.weed_control = request.POST.get('weed_control')
        crop.irrigation = request.POST.get('irrigation')
        crop.ph_level = request.POST.get('ph_level')
        crop.harvesting_time = request.POST.get('harvesting_time')
        crop.yield_per_hectare = request.POST.get('yield_per_hectare')
        crop.post_harvest_handling = request.POST.get('post_harvest_handling')
        if request.FILES.get('image'):
            crop.image = request.FILES.get('image')

        crop.save()
        return redirect('all_crops')

    return render(request, 'admin1/update_crop.html', {'crop': crop})



def delete_crop(request, crop_id):
    crop = get_object_or_404(Crop, id=crop_id)
    crop.delete()
    return redirect('all_crops')

def add_disease(request, crop_id):
    crop = get_object_or_404(Crop, id=crop_id)
    if request.method == "POST":
        name = request.POST['name']
        image = request.FILES.get('image')
        description = request.POST['description']
        control_methods = request.POST['control_methods']

        Disease.objects.create(
            crop=crop, 
            name=name,
            description=description,
            control_methods=control_methods, 
            image=image
            )
        return redirect('all_crops')
    
    return render(request, 'admin1/add_disease.html', {'crop': crop})


def delete_disease(request, disease_id):
    disease = get_object_or_404(Disease, id=disease_id)
    disease.delete()
    return redirect('all_crops')



def add_pest(request, crop_id):
    crop = get_object_or_404(Crop, id=crop_id)
    if request.method == "POST":
        name = request.POST['name']
        image = request.FILES.get('image')
        description = request.POST['description']
        control_methods = request.POST['control_methods']

        Pest.objects.create(
            crop=crop, 
            name=name,
            description=description,
            control_methods=control_methods, 
            image=image
            )
        return redirect('all_crops')
    
    return render(request, 'admin1/add_pest.html', {'crop': crop})


def delete_pest(request, pest_id):
    pest = get_object_or_404(Pest, id=pest_id)
    pest.delete()
    return redirect('all_crops')



def add_fertilizer_requirement(request, crop_id):
    fert_crops = get_object_or_404(Crop, id=crop_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        value = request.POST.get('value')
        FertilizerRequirement.objects.create(
            crop=fert_crops, 
            name=name, 
            value=value
            )
        print(fert_crops)
        return redirect('all_crops')
    return render(request, 'admin1/add_fertilizer_requirement.html', {'fert_crops': fert_crops})



def admin_logout(request):
    logout(request)
    return redirect('login_view')




# ========================admin end================================================================

# =========================customer start================================================================



def home(request):
    user=request.user
    crops = Crop.objects.all()
    context ={
    'crops': crops,
    }
    return render(request,'home.html',context)




def add_plot(request):
    user = request.user  # Get the logged-in user
    devices = Device.objects.filter(user=user)  # Get all devices for this user
    crops = Crop.objects.all()  # Get all crops for the dropdown

    if request.method == "POST":
        plot_name = request.POST.get("plot_name")
        plot_number = request.POST.get("plot_number")
        device_id = request.POST.get("device")
        crop_id = request.POST.get("crop")  # Get crop ID from dropdown

        # Check if the device exists and belongs to the user
        device = Device.objects.filter(id=device_id, user=user).first()
        if not device:
            error_message = "Selected device not found or does not belong to you."
            return render(request, "add_plot.html", {
                "error_message": error_message,
                "devices": devices,
                "crops": crops
            })

       # Get crop from database
        crop = Crop.objects.filter(id=crop_id).first()
        if not crop:
            error_message = "Selected crop not found."
            return render(request, "add_plot.html", {
                "error_message": error_message,
                "devices": devices,
                "crops": crops
            })

        # Save crop.name (string) into crop_name field of Plot model
        Plot.objects.create(
            user=user,
            plot_name=plot_name,
            plot_number=plot_number,
            device=device,
            crop_name=crop.name  # ✅ this is the key line
        )

        return redirect("view_plots")  # Redirect to plots page after successful addition

    return render(request, "add_plot.html", {"devices": devices, "crops": crops})

def delete_plot(request, plot_id):
    plot = get_object_or_404(Plot, id=plot_id)
    plot.delete()
    return redirect("view_plots")

@login_required(login_url="/")
def view_plots(request):
    user = request.user
    plots = Plot.objects.filter(user=user)

    for plot in plots:
        # Check if the device has an active subscription
        if plot.device.subscription_end_date and plot.device.subscription_end_date >= now():
            plot.device.is_active = True  # Subscription is still valid
        else:
            plot.device.is_active = False  # Subscription expired
        motor_status = LEDControl.objects.filter(device=plot.device).order_by('-start_time').first()
        plot.device.motor_status = motor_status.relay_status if motor_status else "OFF"
   
    return render(request, "view_plots.html", {"plots": plots})


def fetch_latest_data(request):
    device_name = request.GET.get('device_name')  # Pass device_name from frontend
    sensor_id = request.GET.get('sensor_id', 1)   # Optional, default to 1
    if not device_name:
        return JsonResponse({'error': 'Device name is required'}, status=400)

    # Optional: Check if this device belongs to the user
    if not Device.objects.filter(user=request.user, device_name=device_name).exists():
        return JsonResponse({'error': 'Unauthorized or invalid device'}, status=403)

    latest_entry = SensorData.objects.filter(device_name=device_name, sensor_id=sensor_id).order_by('-timestamp').first()

    if latest_entry:
        adjusted_latest_entry_timestamp = latest_entry.timestamp + timedelta(hours=5, minutes=30)
        user_last_logged_in_time = request.user.last_login

        if latest_entry.timestamp > user_last_logged_in_time:
            data = {
                'latest_entry': {
                    'temperature': latest_entry.temperature,
                    'sensor_id': latest_entry.sensor_id,
                    'moisture': latest_entry.moisture,
                    'timestamp': adjusted_latest_entry_timestamp,
                    'conductivity': latest_entry.conductivity,
                    'pH': latest_entry.pH,
                    'device_name': latest_entry.device_name,
                    'led_status': latest_entry.led_status,
                    'overall_moisture': latest_entry.overall_moisture,
                    'status': latest_entry.status,
                }
            }
            return JsonResponse(data)
        else:
            return JsonResponse({'error': 'No new data available'}, status=404)
    else:
        return JsonResponse({'error': 'No data available'}, status=404)



@login_required(login_url="/")
def user_device_data(request, device_name):
    user = request.user

    # Check if the user has access to this device
    if not Device.objects.filter(user=user, device_name=device_name).exists():
        return JsonResponse({'error': 'Unauthorized access'}, status=403)

    # Fetch the latest sensor data for the selected device
    data = SensorData.objects.filter(device_name=device_name).order_by('-timestamp')[:10]
    latest_entry = SensorData.objects.filter(device_name=device_name).order_by('-timestamp').first()
    motor_status = LEDControl.objects.filter(device__device_name=device_name).order_by('-start_time').first()


    context = {
        'data': data,
        'latest_entry': latest_entry,
        'motor_status': motor_status,
        'device_name': device_name,

    }
    return render(request, 'data1.html', context)


from django.shortcuts import render

""" @login_required(login_url="/login_view")
def soil_health(request):
    return render(request, 'soil_health.html') """
    
import json
from django.shortcuts import render
from sqlalchemy import create_engine
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

import google.generativeai as genai
# configure Gemini once
genai.configure(api_key="YOUR_API_KEY")  # Replace with your API key
model = genai.GenerativeModel('gemini-1.5-flash')

import numpy as np

""" def soil_health(request):
    # Connect and fetch
    engine = create_engine("mysql+pymysql://root:root%1234@localhost:3306/greeniot", pool_pre_ping=True)
    try:
        df = pd.read_sql("SELECT * FROM demo_sensordata;", engine)
        if df.empty:
            # Provide fallback data if no sensor data is available
            temp_data = {
                "labels": [],
                "actual": [],
                "forecast": []
            }
            moisture_data = {
                "labels": [],
                "actual": [],
                "forecast": []
            }
            diagnosis = "No sensor data available"
            return render(request, 'soil_health.html', {
                "diagnosis": diagnosis,
                "temp_data": json.dumps(temp_data),
                "moisture_data": json.dumps(moisture_data)
            })

        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)
        df.sort_index(inplace=True)

        # Sensor filtering and interpolation
        sensor_df = df[df['sensor_id'] == 1]
        if sensor_df.empty:
            temp_data = {
                "labels": [],
                "actual": [],
                "forecast": []
            }
            moisture_data = {
                "labels": [],
                "actual": [],
                "forecast": []
            }
            diagnosis = "No sensor data for sensor_id=1"
            return render(request, 'soil_health.html', {
                "diagnosis": diagnosis,
                "temp_data": json.dumps(temp_data),
                "moisture_data": json.dumps(moisture_data)
            })

        # --- LSTM Temperature Forecasting ---
        from sklearn.preprocessing import MinMaxScaler
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import LSTM, Dense
        from tensorflow.keras.optimizers import Adam

        temp_series = sensor_df['temperature'].resample('h').mean().interpolate()
        temp_values = temp_series.values.reshape(-1, 1)

        scaler = MinMaxScaler(feature_range=(0, 1))
        temp_scaled = scaler.fit_transform(temp_values)

        def create_dataset(data, time_step=24):
            X, y = [], []
            for i in range(len(data) - time_step - 1):
                X.append(data[i:(i + time_step), 0])
                y.append(data[i + time_step, 0])
            return np.array(X), np.array(y)

        time_step = 24
        X, y = create_dataset(temp_scaled, time_step)
        if len(X) < 10:
            # Not enough data for LSTM, fallback to ARIMA or empty
            temp_data = {
                "labels": temp_series.index.strftime('%Y-%m-%d %H:%M').tolist(),
                "actual": temp_series.round(2).tolist(),
                "forecast": []
            }
        else:
            X = X.reshape(X.shape[0], X.shape[1], 1)
            train_size = int(len(X) * 0.8)
            X_train, X_test = X[:train_size], X[train_size:]
            y_train, y_test = y[:train_size], y[train_size:]

            # Build and train LSTM model (for demo, retrain every time)
            model = Sequential()
            model.add(LSTM(units=50, return_sequences=False, input_shape=(time_step, 1)))
            model.add(Dense(units=1))
            model.compile(optimizer=Adam(learning_rate=0.001), loss='mean_squared_error')
            model.fit(X_train, y_train, epochs=10, batch_size=32, verbose=0)

            # Forecast next 24 steps
            last_input = temp_scaled[-time_step:].reshape(1, time_step, 1)
            forecast_scaled = []
            for _ in range(24):
                next_pred = model.predict(last_input, verbose=0)[0][0]
                forecast_scaled.append(next_pred)
                last_input = np.append(last_input[:, 1:, :], [[[next_pred]]], axis=1)
            forecast = scaler.inverse_transform(np.array(forecast_scaled).reshape(-1, 1)).flatten().round(2).tolist()

            # Prepare labels for forecast
            last_time = temp_series.index[-1]
            forecast_index = pd.date_range(start=last_time, periods=25, freq='h')[1:]
            temp_data = {
                "labels": temp_series.index.strftime('%Y-%m-%d %H:%M').tolist() + forecast_index.strftime('%Y-%m-%d %H:%M').tolist(),
                "actual": temp_series.round(2).tolist(),
                "forecast": forecast
            }

        # --- Moisture (still ARIMA, or you can adapt LSTM similarly) ---
        moisture_series = sensor_df['moisture'].resample('h').mean().interpolate()
        moisture_model = ARIMA(moisture_series, order=(1, 1, 1)).fit()
        moisture_forecast = moisture_model.forecast(steps=24)
        last_time = moisture_series.index[-1]
        forecast_index = pd.date_range(start=last_time, periods=25, freq='h')[1:]
        moisture_data = {
            "labels": moisture_series.index.strftime('%Y-%m-%d %H:%M').tolist() + forecast_index.strftime('%Y-%m-%d %H:%M').tolist(),
            "actual": moisture_series.round(2).tolist(),
            "forecast": moisture_forecast.round(2).tolist()
        }
        
        latest_data = df.iloc[-1]
        prompt = f\"""Analyze the following soil information and provide a single word diagnosis of the possible soil health (healthy, unhealthy, or moderate):
        Temperature: {latest_data['temperature']}
        Moisture: {latest_data['moisture']}
        Conductivity: {latest_data['conductivity']}
        PH Value: {latest_data['pH']}
        Soil Moisture: {latest_data['overall_moisture']}
        \"""
        try:
            response = model.generate_content(prompt)
            diagnosis = response.text
            
            return render(request, 'soil_health.html', {
                "diagnosis": diagnosis,
                "temp_data": json.dumps(temp_data),
                "moisture_data": json.dumps(moisture_data)
            })
        except Exception as e:
            return render(request, 'soil_health.html', {
                "diagnosis": "Failed to generate diagnosis",
                "temp_data": json.dumps(temp_data),
                "moisture_data": json.dumps(moisture_data)
            })
    except Exception as e:
        # Fallback for DB connection or pandas errors
        temp_data = {
            "labels": [],
            "actual": [],
            "forecast": []
        }
        moisture_data = {
            "labels": [],
            "actual": [],
            "forecast": []
        }
        return render(request, 'soil_health.html', {
            "diagnosis": f"Database connection error: {str(e)}",
            "temp_data": json.dumps(temp_data),
            "moisture_data": json.dumps(moisture_data)
        }) """
        
def soil_health(request):
    # Connect and fetch
    engine = create_engine("mysql+pymysql://root:root@localhost:3306/greeniot")
    df = pd.read_sql("SELECT * FROM demo_sensordata;", engine)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)
    df.sort_index(inplace=True)

    # Sensor filtering and interpolation
    sensor_df = df[df['sensor_id'] == 1]
    temp_series = sensor_df['temperature'].resample('h').mean().interpolate()
    moisture_series = sensor_df['moisture'].resample('h').mean().interpolate()

    # ARIMA forecast (24 steps ahead)
    temp_model = ARIMA(temp_series, order=(1, 1, 1)).fit()
    temp_forecast = temp_model.forecast(steps=24)

    moisture_model = ARIMA(moisture_series, order=(1, 1, 1)).fit()
    moisture_forecast = moisture_model.forecast(steps=24)

    # Build forecast labels
    last_time = temp_series.index[-1]
    forecast_index = pd.date_range(start=last_time, periods=25, freq='h')[1:]

    # Prepare JSON-safe output
    temp_data = {
        "labels": temp_series.index.strftime('%Y-%m-%d %H:%M').tolist() + forecast_index.strftime('%Y-%m-%d %H:%M').tolist(),
        "actual": temp_series.round(2).tolist(),
        "forecast": temp_forecast.round(2).tolist()
    }

    moisture_data = {
        "labels": moisture_series.index.strftime('%Y-%m-%d %H:%M').tolist() + forecast_index.strftime('%Y-%m-%d %H:%M').tolist(),
        "actual": moisture_series.round(2).tolist(),
        "forecast": moisture_forecast.round(2).tolist()
    }
    
    latest_data = df.iloc[-1]  # Gets the last row of the DataFrame
    prompt = f"""Analyze the following soil information and provide a single word diagnosis of the possible soil health (healthy, unhealthy, or moderate):
    Temperature: {latest_data['temperature']}
    Moisture: {latest_data['moisture']}
    Conductivity: {latest_data['conductivity']}
    PH Value: {latest_data['pH']}
    Soil Moisture: {latest_data['overall_moisture']}
    """
    try:
        response = model.generate_content(prompt)
        diagnosis = response.text
        
        return render(request, 'soil_health.html', {
            "diagnosis": diagnosis,
            "temp_data": json.dumps(temp_data),
            "moisture_data": json.dumps(moisture_data)
        })
    except Exception as e:
        return render(request, 'soil_health.html', {
            "diagnosis": "Failed to generate diagnosis",
            "temp_data": json.dumps(temp_data),
            "moisture_data": json.dumps(moisture_data)
        })
    
@login_required(login_url="/login_view")
def history(request):
    # Get parameters from request
    from_date = request.GET.get('from-date')
    to_date = request.GET.get('to-date')
    device_name = request.GET.get('device-name')
    export = request.GET.get('export')
    page = request.GET.get('page', 1)  # Get current page, default to 1

    # Get the logged-in user's devices
    user_devices = Device.objects.filter(user=request.user)

    if not user_devices.exists():
        return render(request, 'history_data.html', {
            'filtered_data': [],
            'page_obj': None,
            'from_date': from_date,
            'to_date': to_date,
            'device_name': device_name,
            'user_devices': user_devices,
            'error': "No devices linked to this account."
        })

    # If no device is selected, use the first available device
    selected_device = None
    if device_name:
        selected_device = user_devices.filter(device_name=device_name).first()
    else:
        selected_device = user_devices.first()

    if not selected_device:
        return render(request, 'history_data.html', {
            'filtered_data': [],
            'page_obj': None,
            'from_date': from_date,
            'to_date': to_date,
            'device_name': device_name,
            'user_devices': user_devices,
            'error': "Selected device not found."
        })

    # Initialize filtered data
    filtered_data = SensorData.objects.filter(device_name=selected_device.device_name).order_by('-timestamp')

    # Filter by date range
    if from_date and to_date:
        try:
            from_date_obj = datetime.strptime(from_date, '%Y-%m-%dT%H:%M')
            to_date_obj = datetime.strptime(to_date, '%Y-%m-%dT%H:%M') + timedelta(days=1) - timedelta(seconds=1)
            filtered_data = filtered_data.filter(timestamp__range=[from_date_obj, to_date_obj])
        except ValueError:
            pass

    # Get the latest motor status (relay_status) from LEDControl for this device
    latest_led_control = LEDControl.objects.filter(device=selected_device).order_by('-start_time').first()
    motor_status = latest_led_control.relay_status if latest_led_control else "N/A"

    # Check for export request
    if export == 'excel':
        return export_to_excel(filtered_data, motor_status)

    # Paginate the filtered data (100 records per page)
    paginator = Paginator(filtered_data, 25)
    page_obj = paginator.get_page(page)
    
    context = {
        'filtered_data': page_obj,
        'page_obj': page_obj,
        'from_date': from_date,
        'to_date': to_date,
        'device_name': selected_device.device_name,
        'user_devices': user_devices,  # List of user's devices for dropdown
        'motor_status': motor_status,


    }

    return render(request, 'history_data.html', context)


def export_to_excel(filtered_data, motor_status):
    # Create an Excel file
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Sensor Data'

    # Define headers
    headers = [
        'ID', 'Device Name', 'Soil Temperature', 'Soil Moisture', 'Conductivity',
        'PH Value', 'Motor Status', 'Overall Moisture', 'Timestamp'
    ]
    worksheet.append(headers)

    # Write data
    for data in filtered_data:
        # Convert timezone-aware datetime to naive
        timestamp = data.get_localized_timestamp()
        if timestamp and timestamp.tzinfo:
            timestamp = make_naive(timestamp)

        worksheet.append([
            data.id, data.device_name, data.temperature, data.moisture,
            data.conductivity, data.pH, motor_status, data.overall_moisture, timestamp
        ])

    # Save to BytesIO
    buffer = BytesIO()
    workbook.save(buffer)
    buffer.seek(0)

    # Create HTTP response
    response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=sensor_data.xlsx'
    return response


def user_crops(request):
    query = request.GET.get('text', '')  # Get search query from request
    if query:
        crops = Crop.objects.filter(name__icontains=query)  # Filter crops by name
    else:
        crops = Crop.objects.all()

    last_five_crops = Crop.objects.order_by('-id')[:5]

    return render(request, 'user_crops.html', {
        'crops': crops,
        'last_five_crops': last_five_crops,
        'query': query,
    })



def single_crop(request, crop_id):
    crop = get_object_or_404(Crop, id=crop_id)
    diseases = Disease.objects.filter(crop=crop)  # Fetch related diseases
    pests = Pest.objects.filter(crop=crop)
    fertilizers = FertilizerRequirement.objects.filter(crop=crop)
      # Fetch related fertilizers

    context = {
        'crop': crop,
        'diseases': diseases,
        'pests': pests,
        'fertilizers': fertilizers,
    }
    return render(request, 'single_crop.html', context)


# ============================================================MOTOR STATUS==========================================================
@api_view(['POST'])
def update_device_status(request):
    try:
        data = request.data
        device_name = data.get('device_name')
        if not device_name:
            return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure the device_name matches the device in the database
        device = Device.objects.filter(device_name=device_name).first()
        if not device:
            return Response({"error": "Device not found"}, status=status.HTTP_404_NOT_FOUND)

        # Update existing entries or create new one
        updated_count = LEDControl.objects.filter(device=device).update(
            user=device.user
        )
        if updated_count == 0:
            LEDControl.objects.create(
                device=device,
                user=device.user
            )

        return Response({"message": "Device status updated successfully"}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@login_required(login_url="/")
def led_control_page(request, device_name):
    user = request.user
    device = Device.objects.filter(user=user, device_name=device_name).first()

    if not device:
        return render(request, 'led_control.html', {"error": "No device found for this user."})

    latest_entry = SensorData.objects.filter(device_name=device.device_name).order_by('-timestamp').first()
    motor_status = LEDControl.objects.filter(device=device).order_by('-start_time').first()

    if motor_status and motor_status.end_time and motor_status.end_time <= timezone.now():
        motor_status.relay_status = "OFF"
        motor_status.save()

    return render(request, 'led_control.html', {
        'device_name': device.device_name,
        'latest_entry': latest_entry,
        'motor_status': motor_status,
        'end_time': motor_status.end_time if motor_status else None,

    })

@csrf_exempt
def control_led(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            device_name = data.get('device_name')
            relay_status = data.get('relay_status')
            timer_duration = int(data.get('timer_duration', 0))

            if not device_name:
                return JsonResponse({"error": "Device name is required"}, status=400)

            device = Device.objects.filter(device_name=device_name).first()
            if not device:
                return JsonResponse({"error": "Invalid device name"}, status=400)

            led_entry = LEDControl.objects.create(
                user=device.user,
                device=device,
                relay_status=relay_status,
                timer_duration=timer_duration
            )

            if relay_status == "ON" and timer_duration > 0:
                threading.Thread(target=auto_turn_off_led, args=(device, timer_duration), daemon=True).start()

            return JsonResponse({
                "message": f"LED turned {relay_status}",
                "relay_status": relay_status,
                "end_time": led_entry.end_time.isoformat() if led_entry.end_time else None
            }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=405)

def auto_turn_off_led(device, delay):
    time.sleep(delay)
    latest_entry = LEDControl.objects.filter(device=device).order_by('-start_time').first()
    if latest_entry and latest_entry.relay_status == "ON":
        latest_entry.relay_status = "OFF"
        latest_entry.end_time = timezone.now()
        latest_entry.save()

  
            

@csrf_exempt 
@api_view(['POST'])
def receive_data(request):
    if request.method == 'POST':
        serializer = SensorDataSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            timestamp = data.get('timestamp')
            if timestamp:
                if timezone.is_naive(timestamp):
                    timestamp = timezone.make_aware(timestamp, timezone.get_current_timezone())
                timestamp = timestamp.astimezone(pytz.UTC)
                data['timestamp'] = timestamp
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# ======================================API FOR Send Data==============================


    


@api_view(['GET'])
def get_motor_status(request):
    try:
        latest_entry = LEDControl.objects.order_by('-start_time').first()
        if latest_entry:
            motor_status_serializer = LEDControlSerializer(latest_entry)
            return Response(motor_status_serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "No data found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

def contact(request):
    user = request.user
    if user.is_authenticated:
        if request.method == "POST":
            name = request.POST.get("name")
            email = request.POST.get("email")
            message = request.POST.get("message")
            if name and email and message:
                Contact.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    name=name,
                    email=email,
                    message=message
                )
                return JsonResponse({"success": True, "message": "Your message has been sent successfully!"})
            else:
                return JsonResponse({"success": False, "message": "All fields are required!"})
        return render(request, 'contact.html')
    else:
        if request.method == "POST":
            name = request.POST.get("name")
            email = request.POST.get("email")
            message = request.POST.get("message")
            if name and email and message:
                Contact.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    name=name,
                    email=email,
                    message=message
                )
                return JsonResponse({"success": True, "message": "Your message has been sent successfully!"})
            else:
                return JsonResponse({"success": False, "message": "All fields are required!"})
        return render(request, 'contact.html')

def aboutus(request):
    return render(request,'about_us.html')

# =========================Soil Health Assessment Start==============================================================

# Helper function to calculate a synthetic Soil Health Index for training
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils.timezone import now
from .models import Device, SensorData
from django.views.decorators.csrf import csrf_exempt
import json

# Simple soil health predictor function (for demo — you can replace this logic)
def predict_soil_health(sensor_data):
    if sensor_data.temperature > 35 or sensor_data.moisture < 20 or sensor_data.pH < 5.5 or sensor_data.pH > 8:
        return "Poor"
    elif 20 <= sensor_data.moisture <= 60 and 6 <= sensor_data.pH <= 7.5:
        return "Optimal"
    else:
        return "Moderate"

# View to get latest sensor data and predict soil health
@csrf_exempt
def soil_health_prediction(request, device_id):
    device = get_object_or_404(Device, id=device_id)
    sensor_data = SensorData.objects.filter(device_name=device.device_name).order_by('-timestamp').first()

    if not sensor_data:
        return JsonResponse({'error': 'No sensor data found for this device'}, status=404)

    prediction = predict_soil_health(sensor_data)

    response_data = {
        'device_name': sensor_data.device_name,
        'timestamp': sensor_data.get_localized_timestamp(),
        'temperature': sensor_data.temperature,
        'moisture': sensor_data.moisture,
        'pH': sensor_data.pH,
        'overall_moisture': sensor_data.overall_moisture,
        'status': sensor_data.status,
        'predicted_soil_health': prediction,
    }

    return JsonResponse(response_data, status=200)




# =========================Soil Health Assessment End==============================================================

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        full_name = data.get('full_name')
        email = data.get('email')
        contact_no = data.get('phone')
        password = data.get('password')
        place = data.get('place')
        
        # Check if user already exists
        if NewUser.objects.filter(email=email).exists() or NewUser.objects.filter(contact_no=contact_no).exists():
            return JsonResponse({'error': 'User with this email or phone number already exists'}, status=400)
        
        # Create new user
        user = NewUser.objects.create_user(
            username=email,  # Using email as username
            email=email,
            password=password,
            full_name=full_name,
            contact_no=contact_no,
            place=place
        )
        
        # Send welcome email
        subject = 'Welcome to Soil Sensors!'
        message = f'''
        Dear {full_name},

        Welcome to Soil Sensors! We're excited to have you join our community of smart agriculture enthusiasts.

        Your account has been successfully created with the following details:
        - Full Name: {full_name}
        - Email: {email}
        - Phone: {contact_no}
        - Location: {place}

        Getting Started:
        1. Log in to your account using your email and password
        2. Add your soil sensors to your account
        3. Monitor your soil health data in real-time
        4. Receive alerts and recommendations for optimal crop growth

        If you have any questions or need assistance, please don't hesitate to contact our support team.

        Best regards,
        The Soil Sensors Team
        '''
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]
        
        try:
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            print(f"Welcome email sent successfully to {email}")
        except Exception as e:
            print(f"Failed to send welcome email: {str(e)}")
        
        return JsonResponse({
            'message': 'User created successfully',
            'user_id': user.id,
            'email': user.email
        }, status=201)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        # Handle form submission
        if 'remove_photo' in request.POST:
            # Clear the profile photo
            request.user.profile_photo.delete()  # Deletes the file from storage
            request.user.profile_photo = None    # Clears the field
            request.user.save()
            messages.success(request, 'Profile photo removed successfully.')
        else:
            user = request.user
            user.full_name = request.POST.get('full_name', user.full_name)
            user.email = request.POST.get('email', user.email)
            user.contact_no = request.POST.get('contact_no', user.contact_no)
            user.place = request.POST.get('place', user.place)
        
        # Handle profile photo upload
        if 'profile_photo' in request.FILES:
            user.profile_photo = request.FILES['profile_photo']
        
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('customer_profile')
    
    return render(request, 'edit_profile.html', {'user': request.user})

from django.core.mail import send_mail
from django.contrib.auth import get_user_model
User = get_user_model()

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "User with this email does not exist.")
            return redirect("forgot_password")

        if "otp" not in request.session:  # Generate OTP only if not already set
            otp = random.randint(100000, 999999)  # Generate 6-digit OTP
            request.session["otp"] = str(otp)  # Store OTP in session
            request.session["user_email"] = email  # Store user email
            request.session.set_expiry(300)  # Expire session in 5 minutes

            try:
                send_mail(
                    "Your OTP Code",
                    f"Your OTP for password reset is: {otp}",
                    settings.EMAIL_HOST_USER,  # Use the configured email
                    [email],
                    fail_silently=False,
                )
                messages.success(request, "OTP has been sent to your email.")
            except Exception as e:
                messages.error(request, f"Failed to send email: {str(e)}")
                return redirect("forgot_password")

        return redirect("verify_otp")

    return render(request, "forgot_password.html")

def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        session_otp = request.session.get("otp")
        user_email = request.session.get("user_email")

        if not session_otp or not user_email:
            messages.error(request, "Session expired. Try again.")
            return redirect("forgot_password")

        if str(entered_otp) == str(session_otp):  
            request.session["otp_verified"] = True  
            del request.session["otp"]  
            return redirect("reset_password", email=user_email)  # ✅ Pass email argument
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, "verify_otp.html")

def reset_password(request,email):
    if not request.session.get("otp_verified"):
        messages.error(request, "OTP verification required.")
        return redirect("verify_otp")  # Ensure user can't bypass OTP

    if request.method == "POST":
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password == confirm_password:
            user_email = request.session.get("user_email")
            if not user_email:
                messages.error(request, "Session expired. Try again.")
                return redirect("forgot_password")

            user = User.objects.get(email=user_email)
            user.set_password(new_password)
            user.save()
            
            messages.success(request, "Password reset successful. Please log in.")
            return redirect("login_view")  # Redirect to login page
        else:
            messages.error(request, "Passwords do not match.")

    return render(request, "reset_password.html")
