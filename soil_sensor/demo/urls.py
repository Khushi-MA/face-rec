from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',views.home, name='home'),
    path('register/',views.add_customer,name="register"),
    path('login/',views.login_view,name="login_view"),
    path('logout/',views.logout_view,name="logout_view"),
    path('customer_profile/',views.customer_profile,name='customer_profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
  

    # admin works and operations
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('view_customers',views.view_customers,name="view_customers"),
    path('customers/update/<int:customer_id>/', views.update_customer, name='update_customer'),
    path('delete_user/<int:id>',views.delete_user,name="delete_user"),

    # Adding Deveices and Modifying Devices
    path('register_device/', views.register_device, name='register_device'),
    path('manage_devices/<int:user_id>/', views.manage_devices, name='manage_devices'),
    path('delete_device/<int:device_id>/', views.delete_device, name='delete_device'),

    # User device data and operations
    path('users/', views.user_list, name='admin_users'),
    path('user/<int:user_id>/devices/', views.user_devices, name='user_devices'),
    path('view_device_data/<str:device_name>/', views.view_device_data, name='view_device_data'),
    path('device_data/<str:device_name>/', views.display_sensor_data, name='display_sensor_data'),

    # Crop and Diseases and Fertilizers
    path('all_crops/', views.all_crops, name='all_crops'),
    path('crops/add-crop/', views.add_crop, name='add_crop'),
    path('crop/update/<int:crop_id>/', views.update_crop, name='update_crop'),
    path('crops/delete-crop/<int:crop_id>/', views.delete_crop, name='delete_crop'),

    path('crops/add-disease/<int:crop_id>/', views.add_disease, name='add_disease'),
    path('crops/delete-disease/<int:disease_id>/', views.delete_disease, name='delete_disease'),

    path('crops/add-pest/<int:crop_id>/', views.add_pest, name='add_pest'),
    path('crops/delete-pest/<int:pest_id>/', views.delete_pest, name='delete_pest'),

    path('crops/add-fertilizers/<int:crop_id>/', views.add_fertilizer_requirement, name='add_fertilizer_requirement'),
    path('admin_logout',views.admin_logout,name="admin_logout"),
   
    # User works and operations
    path('crops/', views.user_crops, name='user_crops'),
    path('crop/<int:crop_id>/', views.single_crop, name='single_crop'),

    path('add_plot/', views.add_plot, name='add_plot'),
    path('view_plots/', views.view_plots, name='view_plots'),
    path('delete_plot/<int:plot_id>/', views.delete_plot, name='delete_plot'),

    # Devices and Sensor data and motor control
    path('fetch_latest_data/', views.fetch_latest_data, name='fetch_latest_data'),
    path('user_device_data/<str:device_name>/', views.user_device_data, name='user_device_data'),
    path('history/',views.history, name="history"),
    path('led_control/<str:device_name>/', views.led_control_page, name='led_control_page'),
    path('api/update_led_status/', views.control_led, name='control_led'),
    path('api/update_device_status/', views.update_device_status, name='update_device_status'),
    
    path('contact', views.contact,name='contact'),
    path('about/', views.aboutus,name='about'),

    # API endpoints
    path('api/receive_data/',views.receive_data, name='receive_data'),
    path('api/get_motor_status/', views.get_motor_status, name='get_motor_status'), 

    path('predict-soil-health/<int:device_id>/', views.soil_health_prediction, name='soil_health_prediction'),
    path('soil_health/', views.soil_health, name='soil_health'),
    path('signup/', views.signup, name='signup'),

    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('reset_password/<str:email>/', views.reset_password, name='reset_password'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)