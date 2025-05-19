from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth.views import LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from . import views

class CustomLogoutView(SuccessMessageMixin, LogoutView):
    next_page = 'login'
    http_method_names = ['get', 'post', 'options'] # Allow GET requests
    
    def dispatch(self, request, *args, **kwargs):
        # Message is now handled in get() or by parent LogoutView for POST
        # if request.user.is_authenticated:
        #     messages.success(request, 'You have been successfully logged out.')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """Log out the user and redirect to login page."""
        # Add message here since parent dispatch might not be called for GET
        if request.user.is_authenticated:
            messages.success(request, 'You have been successfully logged out.') 
            logout(request)
        return redirect(self.next_page)

urlpatterns = [
    path('', views.landing, name='landing'),
    # Authentication URLs
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('upload_csv/', views.upload_csv, name='upload_csv'),

    # Role-specific Dashboards
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manager/dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('analyst/dashboard/', views.analyst_dashboard, name='analyst_dashboard'),

    # Admin URLs
    path('administrator/users/', views.manage_users, name='manage_users'),
    path('administrator/user-logs/', views.view_user_logs, name='user_logs'),
    path('administrator/system-settings/', views.system_settings, name='system_settings'),
    path('administrator/system-logs/', views.system_logs, name='system_logs'),
    path('administrator/reports/', views.admin_reports, name='admin_reports'),
    path('administrator/analytics/', views.admin_analytics, name='admin_analytics'),

    # Manager URLs
    path('manager/inventory/', views.view_inventory, name='view_inventory'),
    path('manager/add-item/', views.add_item, name='add_item'),
    path('manager/orders/', views.manage_orders, name='manage_orders'),
    path('manager/order/create/', views.create_order, name='create_order'),
    path('manager/order/<int:order_id>/', views.view_order, name='view_order'),
    path('manager/order/<int:order_id>/process/', views.process_order, name='process_order'),
    path('manager/order/<int:order_id>/cancel/', views.cancel_order, name='cancel_order'),
    path('manager/order-history/', views.order_history, name='order_history'),
    path('manager/stock-reports/', views.stock_reports, name='stock_reports'),
    path('manager/sales-reports/', views.sales_reports, name='sales_reports'),
    path('manager/edit-item/<int:item_id>/', views.edit_item, name='edit_item'),
    path('manager/reorder-item/', views.reorder_item, name='reorder_item'),
    path('manager/order/<int:order_id>/process_payment/', views.process_payment, name='process_payment'),

    # Analyst URLs
    path('analyst/forecasts/', views.view_forecasts, name='view_forecasts'),
    # path('analyst/forecast-details/<str:forecast_id>/', views.forecast_details, name='forecast_details'),
    path('analyst/generate-predictions/', views.generate_predictions, name='generate_predictions'),
    path('analyst/sales-trends/', views.sales_trends, name='sales_trends'),
    path('analyst/inventory-trends/', views.inventory_trends, name='inventory_trends'),
    path('analyst/analytics-reports/', views.analytics_reports, name='analytics_reports'),
    path('analyst/performance-metrics/', views.performance_metrics, name='performance_metrics'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

