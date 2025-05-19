from django.shortcuts import render, redirect, resolve_url
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .models import User, Item, Order, OrderItem, Payment, Product
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.db.models import Sum, Count, Avg, F, ExpressionWrapper, DecimalField, Q, Case, When, Value, FloatField, CharField, DurationField, Subquery, OuterRef
from django.db.models.functions import TruncDate
import json
from datetime import datetime, timedelta
from django.http import HttpResponse, JsonResponse
import csv
from django.contrib.auth import get_user_model
import psutil
import os
from decimal import Decimal
import random
from django.db import transaction
from sklearn.svm import SVR
import numpy as np
import csv
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product
from datetime import datetime

# Create your views here.

def check_admin(user):
    return user.role == User.Role.ADMIN and (user.is_staff or user.is_superuser)

def check_manager(user):
    return user.role == User.Role.MANAGER

def check_analyst(user):
    return user.role == User.Role.ANALYST

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists!')
            return redirect('register')

        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            role=role
        )
        login(request, user)
        messages.success(request, 'Registration successful!')
        return redirect('dashboard')
    
    return render(request, 'members/register.html')

def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]  
        password = request.POST["password"]
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)

            if user.role=='admin':
                return redirect('admin_dashboard')
            elif user.role=='manager':
                return redirect('manager_dashboard')
            elif user.role=='analyst':
                return redirect('analyst_dashboard')    
            else:
                return redirect('default_dashboard')
        else:
            context = {'error_messages':'Invalid username or password.'}
            return render(request,'members/login.html', context)
    
    return render(request, 'members/login.html')

@login_required
def dashboard(request):
    user = request.user
    # Prioritize superuser check for admin dashboard
    if user.is_superuser:
        # Ensure role consistency, although superuser status grants access
        if user.role != User.Role.ADMIN:
            print(f"Warning: Superuser {user.username} has role {user.role}, expected ADMIN.")
            # Optionally update the role here if desired:
            # user.role = User.Role.ADMIN
            # user.save()
        return redirect('admin_dashboard')

    # If not superuser, check roles for other dashboards
    if user.role == User.Role.MANAGER:
        return redirect('manager_dashboard')
    elif user.role == User.Role.ANALYST:
        return redirect('analyst_dashboard')
    else:
        # Neither superuser nor a recognized role (Manager/Analyst)
        # Log them out instead of redirecting to login to break loops
        messages.error(request, 'Access denied. Invalid role or permissions. Logging out.')
        return redirect('logout')

# Admin Views
def is_admin(user):
    return user.is_authenticated and user.is_superuser

# @login_required(login_url='login')
# @user_passes_test(is_admin, login_url='dashboard')
def admin_dashboard(request):
    User = get_user_model()
    now = timezone.now()
    month_ago = now - timedelta(days=30)
    
    # Get user statistics
    total_users = User.objects.count()
    new_users = User.objects.filter(date_joined__gte=month_ago).count()
    active_users = User.objects.filter(last_login__gte=month_ago).count()
    
    # System metrics
    cpu_usage = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    # Recent activity (example - modify based on your activity tracking model)
    recent_activity = [
        {
            'user': 'admin',
            'action': 'System backup',
            'timestamp': now - timedelta(hours=2),
            'status': 'success'
        },
        {
            'user': 'manager1',
            'action': 'Updated inventory',
            'timestamp': now - timedelta(hours=3),
            'status': 'success'
        }
    ]
    
    # System alerts (example)
    system_alerts = []
    if memory.percent > 80:
        system_alerts.append({
            'type': 'warning',
            'title': 'High Memory Usage',
            'message': f'Memory usage is at {memory.percent}%',
            'timestamp': now
        })
    if disk.percent > 80:
        system_alerts.append({
            'type': 'warning',
            'title': 'Storage Space Low',
            'message': f'Disk usage is at {disk.percent}%',
            'timestamp': now
        })

    context = {
        'stats': {
            'total_users': total_users,
            'new_users': new_users,
            'active_users': active_users,
            'active_percentage': round((active_users / total_users * 100) if total_users > 0 else 0, 1),
            'system_load': cpu_usage,
            'uptime': '7 days',  # You can get actual uptime if needed
            'pending_actions': len(system_alerts),
            'critical_alerts': len([a for a in system_alerts if a['type'] == 'danger'])
        },
        'recent_activity': recent_activity,
        'system_status': {
            'last_backup': now - timedelta(days=1),
            'storage_usage': disk.percent,
            'memory_usage': memory.percent,
            'cpu_usage': cpu_usage
        },
        'system_alerts': system_alerts
    }
    
    return render(request, 'members/admin/admin_dashboard.html', context)

@login_required
@user_passes_test(is_admin, login_url='dashboard')
def manage_users(request):
    # Check if user is authenticated and is admin
    if not request.user.is_authenticated:
        return redirect('login')
    
    if not is_admin(request.user):
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('dashboard')

    User = get_user_model()
    search_query = request.GET.get('search', '')
    
    # Get all users with filters
    users = User.objects.all().order_by('-date_joined')
    
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(role__icontains=search_query)
        )
    
    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(users, 10)  # Show 10 users per page
    
    try:
        users_page = paginator.page(page)
    except PageNotAnInteger:
        users_page = paginator.page(1)
    except EmptyPage:
        users_page = paginator.page(paginator.num_pages)
    
    # Handle POST requests for user management
    if request.method == 'POST':
        action = request.POST.get('action')
        user_id = request.POST.get('user_id')
        
        if user_id:
            target_user = User.objects.get(id=user_id)
            
            if action == 'deactivate':
                target_user.is_active = False
                target_user.save()
                messages.success(request, f'User {target_user.username} has been deactivated.')
            
            elif action == 'activate':
                target_user.is_active = True
                target_user.save()
                messages.success(request, f'User {target_user.username} has been activated.')
            
            elif action == 'delete':
                username = target_user.username
                target_user.delete()
                messages.success(request, f'User {username} has been deleted.')
            
            elif action == 'change_role':
                new_role = request.POST.get('role')
                target_user.role = new_role
                target_user.save()
                messages.success(request, f'Role updated for user {target_user.username}.')
    
    context = {
        'users': users_page,
        'search_query': search_query,
        'total_users': User.objects.count(),
        'active_users': User.objects.filter(is_active=True).count(),
        'roles': User.Role.choices
    }
    
    return render(request, 'members/admin/manage_users.html', context)

@login_required
@user_passes_test(is_admin, login_url='dashboard')
def view_user_logs(request):
    User = get_user_model()
    # Get all users for the filter dropdown
    users = User.objects.all()
    
    # Example placeholder logs data
    # In a real implementation, you would fetch this from a UserLog model
    now = timezone.now()
    example_logs = [
        {
            'timestamp': now - timedelta(hours=1),
            'user': 'admin',
            'ip_address': '192.168.1.1',
            'action': 'Login',
            'details': 'Successful login',
            'status': 'success'
        },
        {
            'timestamp': now - timedelta(hours=2),
            'user': 'manager1',
            'ip_address': '192.168.1.2',
            'action': 'Create',
            'details': 'Created new product: Laptop',
            'status': 'success'
        },
        {
            'timestamp': now - timedelta(hours=3),
            'user': 'analyst1',
            'ip_address': '192.168.1.3',
            'action': 'View',
            'details': 'Viewed sales report',
            'status': 'success'
        },
        {
            'timestamp': now - timedelta(hours=4),
            'user': 'manager1',
            'ip_address': '192.168.1.2',
            'action': 'Update',
            'details': 'Updated product: Desktop',
            'status': 'warning'
        },
        {
            'timestamp': now - timedelta(hours=5),
            'user': 'admin',
            'ip_address': '192.168.1.1',
            'action': 'Delete',
            'details': 'Deleted user: test_user',
            'status': 'error'
        }
    ]
    
    context = {
        'users': users,
        'logs': example_logs
    }
    
    return render(request, 'members/admin/user_logs.html', context)

@login_required
@user_passes_test(is_admin, login_url='dashboard')
def system_settings(request):
    return render(request, 'members/admin/system_settings.html')

@login_required
@user_passes_test(is_admin, login_url='dashboard')
def system_logs(request):
    return render(request, 'members/admin/system_logs.html')

@login_required
@user_passes_test(is_admin, login_url='dashboard')
def admin_reports(request):
    try:
        # Get system metrics
        cpu_usage = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        boot_time = psutil.boot_time()
        uptime = timezone.now().timestamp() - boot_time
        uptime_days = int(uptime / (24 * 3600))
        uptime_hours = int((uptime % (24 * 3600)) / 3600)
        
        # Sample performance data (last 24 hours)
        now = timezone.now()
        hours = 24
        time_labels = [(now - timedelta(hours=i)).strftime('%H:00') for i in range(hours-1, -1, -1)]
        
        # Generate sample performance data
        # In a production environment, you would get this from your monitoring system
        performance_data = {
            'labels': json.dumps(time_labels),
            'cpu': json.dumps([round(random.uniform(20, 80), 1) for _ in range(hours)]),
            'memory': json.dumps([round(random.uniform(40, 90), 1) for _ in range(hours)])
        }
        
        # Sample activity logs
        activity_logs = [
            {
                'timestamp': (now - timedelta(minutes=5)).strftime('%Y-%m-%d %H:%M:%S'),
                'event': 'System Backup',
                'component': 'Backup Service',
                'status': 'success',
                'details': 'Daily backup completed successfully'
            },
            {
                'timestamp': (now - timedelta(minutes=15)).strftime('%Y-%m-%d %H:%M:%S'),
                'event': 'High CPU Usage',
                'component': 'System Monitor',
                'status': 'warning',
                'details': 'CPU usage exceeded 80%'
            },
            {
                'timestamp': (now - timedelta(minutes=30)).strftime('%Y-%m-%d %H:%M:%S'),
                'event': 'Failed Login Attempt',
                'component': 'Authentication',
                'status': 'danger',
                'details': 'Multiple failed login attempts detected'
            }
        ]
        
        context = {
            'system_metrics': {
                'cpu_usage': cpu_usage,
                'memory_usage': memory.percent,
                'storage_usage': disk.percent,
                'uptime': f"{uptime_days}d {uptime_hours}h",
                'network_usage': 45  # Example static value
            },
            'performance_data': performance_data,
            'activity_logs': activity_logs
        }
        
        return render(request, 'members/admin/reports.html', context)
    
    except Exception as e:
        print(f"Error in admin_reports view: {str(e)}")
        import traceback
        print(traceback.format_exc())
        
        # Return empty data structure
        context = {
            'system_metrics': {
                'cpu_usage': 0,
                'memory_usage': 0,
                'storage_usage': 0,
                'uptime': '0d 0h',
                'network_usage': 0
            },
            'performance_data': {
                'labels': json.dumps([]),
                'cpu': json.dumps([]),
                'memory': json.dumps([])
            },
            'activity_logs': []
        }
        return render(request, 'members/admin/reports.html', context)

@login_required
@user_passes_test(is_admin, login_url='dashboard')
def admin_analytics(request):
    return render(request, 'members/admin/analytics.html')

# Manager Views
@login_required
@user_passes_test(check_manager)
def manager_dashboard(request):
    # Calculate total distinct product names
    total_products = Product.objects.values('product_name').distinct().count()

    # Count pending orders
    pending_orders = Order.objects.filter(status=Order.Status.PENDING).count()

    # Count low stock items (current_stock < 5)
    low_stock_items = Product.objects.filter(current_stock__lt=5).count()

    context = {
        'total_products': total_products,
        'pending_orders': pending_orders,
        'low_stock_items': low_stock_items,
        'recent_activities': [
            {'action': 'Stock Update', 'item': 'Laptop', 'time': '2 hours ago'},
            {'action': 'New Order', 'item': 'Desktop', 'time': '3 hours ago'},
            {'action': 'Restock Alert', 'item': 'Mouse', 'time': '5 hours ago'},
        ]
    }
    return render(request, 'members/manager/manager_dashboard.html', context)

@login_required
@user_passes_test(check_manager)
def view_inventory(request):
    # Get all items from the database
    items = Product.objects.all().order_by('product_name')

    # Get distinct categories for the filter
    categories = Product.objects.values_list('category', flat=True).distinct()

    # Apply category filter
    category_filter = request.GET.get('category')
    if category_filter:
        items = items.filter(category=category_filter)

    # Apply search filter
    search_query = request.GET.get('search')
    if search_query:
        items = items.filter(product_name__icontains=search_query)

    # Calculate totals by category using Django aggregation
    category_totals = Product.objects.values('category').annotate(
        total=Sum('current_stock'),
        total_items=Count('id'),
        low_stock=Count('id', filter=Q(current_stock__lte=F('reorder_level'))),
        out_of_stock=Count('id', filter=Q(current_stock=0))
    ).order_by('category')

    # Convert to dictionary format with additional data
    category_data = {}
    for cat in category_totals:
        category_data[cat['category']] = {
            'total_stock': cat['total'] or 0,
            'total_items': cat['total_items'],
            'low_stock': cat['low_stock'],
            'out_of_stock': cat['out_of_stock'],
            'status': 'Out of Stock' if cat['total'] == 0 else 'Low Stock' if cat['total'] <= 10 else 'In Stock'
        }

    # Add pagination
    paginator = Paginator(items, 10)  # Show 10 items per page
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    context = {
        'items': items,
        'categories': categories,  # Pass categories to the template
        'category_totals': category_data,
        'total_stock': sum(cat['total_stock'] for cat in category_data.values()),
        'total_categories': len(category_data),
        'low_stock_categories': sum(1 for cat in category_data.values() if cat['low_stock'] > 0),
        'out_of_stock_categories': sum(1 for cat in category_data.values() if cat['out_of_stock'] > 0),
        'selected_category': category_filter,
        'search_query': search_query
    }

    return render(request, 'members/manager/inventory.html', context)

@login_required
@user_passes_test(check_manager)
def add_item(request):
    if request.method == 'POST':
        try:
            # Get the form data
            product_name = request.POST.get('product_name')
            category = request.POST.get('category')
            current_stock = int(request.POST.get('quantity'))
            unit_price = float(request.POST.get('price'))
            reorder_level = int(request.POST.get('reorder_level'))
            description = request.POST.get('description', '')
            supplier = request.POST.get('supplier', '')
            sku = request.POST.get('sku', '')
            active = request.POST.get('active') == 'on'
            
            # Create the Product instance with only the fields that exist in the model
            item = Product(
                product_name=product_name,
                category=category,
                current_stock=current_stock,
                unit_price=unit_price,
                reorder_level=reorder_level,
                status='In Stock',
                last_updated=datetime.now(),
                supplier=supplier,
                sku=sku,
                active=active,
                created_by=request.user
            )
            
            # Handle image upload if present
            if 'product_image' in request.FILES:
                item.product_image = request.FILES['product_image']
                
            # Calculate value (price * quantity)
            item.value = item.unit_price * item.current_stock
            item.save()
            
            messages.success(request, 'Item added successfully!')
            return redirect('view_inventory')
        except Exception as e:
            messages.error(request, f'Error adding item: {str(e)}')
    
    return render(request, 'members/manager/add_item.html')

@login_required
@user_passes_test(check_manager)
def create_order(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                order = Order.objects.create(
                    customer_name=request.POST.get('customer_name'),
                    total_amount=Decimal(request.POST.get('total_amount', '0')),
                    created_by=request.user,
                    status='pending'
                )
                items_data = json.loads(request.POST.get('items', '[]'))
                for item_data in items_data:
                    product = Product.objects.get(id=item_data['item_id'])
                    quantity = int(item_data['quantity'])
                    OrderItem.objects.create(
                        order=order,
                        product=product,  # Use Product instead of Item
                        quantity=quantity,
                        price_at_time_of_order=product.unit_price
                    )
                    product.current_stock -= quantity
                    if product.current_stock <= 0:
                        product.status = 'Out of Stock'
                    elif product.current_stock <= product.reorder_level:
                        product.status = 'Reordered'
                    product.save()
            messages.success(request, 'Order created successfully!')
            return redirect('view_order', order_id=order.id)
        except Product.DoesNotExist:
            messages.error(request, 'One or more products not found.')
        except ValueError as e:
            messages.error(request, f'Invalid data provided: {str(e)}')
        except Exception as e:
            messages.error(request, f'Error creating order: {str(e)}')
        return redirect('manage_orders')

    products = Product.objects.filter(active=True, current_stock__gt=0).order_by('category', 'product_name')
    categories = products.values_list('category', flat=True).distinct()
    context = {
        'items': products,
        'categories': categories,
        'items_json': json.dumps([{
            'id': product.id,
            'name': product.product_name,
            'price': float(product.unit_price),
            'available_quantity': product.current_stock,
            'category': product.category
        } for product in products])
    }
    return render(request, 'members/manager/create_order.html', context)

@login_required
@user_passes_test(check_manager)
def view_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        order_items = order.items.all()  # Fetch related OrderItem objects
        context = {
            'order': order,
            'order_items': order_items
        }
        return render(request, 'members/manager/view_order.html', context)
    except Order.DoesNotExist:
        messages.error(request, 'Order not found.')
        return redirect('manage_orders')

@login_required
@user_passes_test(check_manager)
def process_order(request, order_id):
    if request.method == 'POST':
        try:
            order = Order.objects.get(id=order_id)
            if order.status == 'pending' and order.payment_status == 'paid':  # Ensure payment is completed
                order.status = 'completed'
                order.processed_by = request.user
                order.save()
                messages.success(request, 'Order processed successfully!')
            elif order.payment_status != 'paid':
                messages.warning(request, 'Order cannot be processed - payment is not completed.')
            else:
                messages.warning(request, 'Order cannot be processed - invalid status.')
        except Order.DoesNotExist:
            messages.error(request, 'Order not found.')
    return redirect('manage_orders')

@login_required
@user_passes_test(check_manager)
def cancel_order(request, order_id):
    if request.method == 'POST':
        try:
            order = Order.objects.get(id=order_id)
            if order.status == 'pending':
                order.status = 'cancelled'
                order.save()
                messages.success(request, 'Order cancelled successfully!')
            else:
                messages.warning(request, 'Order cannot be cancelled - invalid status.')
        except Order.DoesNotExist:
            messages.error(request, 'Order not found.')
    return redirect('manage_orders')

@login_required
@user_passes_test(check_manager)
def manage_orders(request):
    order_list = Order.objects.all().order_by('-order_date')
    paginator = Paginator(order_list, 10)  # Show 10 orders per page
    
    page = request.GET.get('page')
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)
    
    context = {
        'orders': orders
    }
    return render(request, 'members/manager/orders.html', context)

@login_required
@user_passes_test(check_manager)
def order_history(request):
    orders = Order.objects.all()
    
    # Filter by date range
    date_range = request.GET.get('date_range')
    if date_range and date_range != 'all':
        days = int(date_range)
        cutoff_date = timezone.now() - timezone.timedelta(days=days)
        orders = orders.filter(order_date__gte=cutoff_date)
    
    # Filter by status
    status = request.GET.get('status')
    if status and status != 'all':
        orders = orders.filter(status=status)
    
    # Sort orders
    sort = request.GET.get('sort', 'date_desc')
    if sort == 'date_asc':
        orders = orders.order_by('order_date')
    elif sort == 'date_desc':
        orders = orders.order_by('-order_date')
    elif sort == 'amount_asc':
        orders = orders.order_by('total_amount')
    elif sort == 'amount_desc':
        orders = orders.order_by('-total_amount')
    
    # Pagination
    paginator = Paginator(orders, 10)  # Show 10 orders per page
    page = request.GET.get('page')
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)
    
    context = {
        'orders': orders,
        'current_filters': {
            'date_range': date_range or 'all',
            'status': status or 'all',
            'sort': sort
        }
    }
    return render(request, 'members/manager/order_history.html', context)

@login_required
@user_passes_test(check_manager)
def stock_reports(request):
    # Get filters from request
    category = request.GET.get('category', 'all')
    status = request.GET.get('status', 'all')
    sort = request.GET.get('sort', 'name')

    # Base queryset
    items = Item.objects.all()

    # Apply filters
    if category != 'all':
        items = items.filter(category=category)

    if status != 'all':
        if status == 'out':
            items = items.filter(quantity=0)
        elif status == 'low':
            items = items.filter(quantity__gt=0, quantity__lte=F('reorder_level'))
        elif status == 'normal':
            items = items.filter(quantity__gt=F('reorder_level'))
        elif status == 'excess':
            items = items.filter(quantity__gt=F('reorder_level') * 2)

    # Apply sorting
    if sort == 'name':
        items = items.order_by('product_name')
    elif sort == 'stock_asc':
        items = items.order_by('quantity')
    elif sort == 'stock_desc':
        items = items.order_by('-quantity')
    elif sort == 'reorder':
        items = items.order_by(
            (F('quantity') - F('reorder_level')).asc()
        )

    # Calculate stock value for each item
    items = items.annotate(
        stock_value=ExpressionWrapper(
            F('quantity') * F('price'),
            output_field=DecimalField()
        )
    )

    # Get category-wise stock levels for chart
    category_stats = Item.objects.values('category').annotate(
        total_stock=Sum('quantity'),
        total_value=Sum(F('quantity') * F('price'))
    ).order_by('category')
    
    # Convert category stats to dictionary format
    category_stats_dict = {
        stat['category']: {
            'total_stock': stat['total_stock'] or 0,
            'total_value': float(stat['total_value'] or 0)
        }
        for stat in category_stats
    }
    
    category_labels = [stat['category'] for stat in category_stats]
    category_stock = [stat['total_stock'] for stat in category_stats]
    category_values = [float(stat['total_value']) for stat in category_stats]

    # Get summary statistics
    total_items = Item.objects.count()
    total_categories = Item.objects.values('category').distinct().count()
    low_stock_count = Item.objects.filter(
        quantity__gt=0,
        quantity__lte=F('reorder_level')
    ).count()
    out_of_stock_count = Item.objects.filter(quantity=0).count()
    total_stock_value = sum(category_values)

    # Get unique categories for filter
    categories = Item.objects.values_list('category', flat=True).distinct()

    # Pagination
    paginator = Paginator(items, 10)  # Show 10 items per page
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    context = {
        'items': items,
        'total_items': total_items,
        'total_categories': total_categories,
        'low_stock_count': low_stock_count,
        'out_of_stock_count': out_of_stock_count,
        'total_stock_value': total_stock_value,
        'category_labels': json.dumps(category_labels),
        'category_stock': json.dumps(category_stock),
        'category_values': json.dumps(category_values),
        'categories': categories,
        'category_stats': category_stats_dict,
        'current_filters': {
            'category': category,
            'status': status,
            'sort': sort
        }
    }

    # Handle CSV export
    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="stock_report.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Product Name', 'Category', 'Current Stock', 'Reorder Level', 
                        'Unit Price', 'Value', 'Status', 'Last Updated'])
        
        for item in items:
            status = 'Out of Stock' if item.quantity == 0 else \
                    'Low Stock' if item.quantity <= item.reorder_level else 'In Stock'
            writer.writerow([
                item.product_name,
                item.category,
                item.quantity,
                item.reorder_level,
                item.price,
                item.stock_value,
                status,
                item.updated_at.strftime('%Y-%m-%d %H:%M')
            ])
        return response

    return render(request, 'members/manager/stock_reports.html', context)

@login_required
@user_passes_test(check_manager)
def sales_reports(request):
    # Get date range from request
    date_range = request.GET.get('date_range', 'month')
    
    # Initialize dates
    end_date = timezone.now()
    
    if date_range == 'custom':
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')
        if start_date_str and end_date_str:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
                # Set end_date to end of day
                end_date = end_date.replace(hour=23, minute=59, second=59)
            except ValueError:
                # If date parsing fails, default to month
                date_range = 'month'
                start_date = end_date - timedelta(days=30)
        else:
            # If custom dates not provided, default to month
            date_range = 'month'
            start_date = end_date - timedelta(days=30)
    elif date_range == 'today':
        start_date = end_date.replace(hour=0, minute=0, second=0)
    elif date_range == 'week':
        start_date = end_date - timedelta(days=7)
    elif date_range == 'month':
        start_date = end_date - timedelta(days=30)
    elif date_range == 'quarter':
        start_date = end_date - timedelta(days=90)
    else:  # year
        start_date = end_date - timedelta(days=365)

    # Get orders for the selected period
    orders = Order.objects.filter(
        order_date__gte=start_date,
        order_date__lte=end_date,
        status='completed'
    )

    # Calculate summary statistics
    total_sales = orders.aggregate(total=Sum('total_amount'))['total'] or 0
    total_orders = orders.count()
    avg_order_value = total_sales / total_orders if total_orders > 0 else 0

    # Calculate items sold using OrderItem model
    items_sold = OrderItem.objects.filter(
        order__in=orders
    ).aggregate(
        total=Sum('quantity')
    )['total'] or 0

    # Get previous period data for comparison
    prev_start_date = start_date - (end_date - start_date)
    prev_orders = Order.objects.filter(
        order_date__gte=prev_start_date,
        order_date__lt=start_date,
        status='completed'
    )
    prev_total_sales = prev_orders.aggregate(total=Sum('total_amount'))['total'] or 0
    prev_total_orders = prev_orders.count()
    prev_items_sold = OrderItem.objects.filter(
        order__in=prev_orders
    ).aggregate(
        total=Sum('quantity')
    )['total'] or 0

    # Calculate percentage changes
    sales_change = ((total_sales - prev_total_sales) / prev_total_sales * 100) if prev_total_sales > 0 else 0
    orders_change = ((total_orders - prev_total_orders) / prev_total_orders * 100) if prev_total_orders > 0 else 0
    items_change = ((items_sold - prev_items_sold) / prev_items_sold * 100) if prev_items_sold > 0 else 0

    # Get sales trend data for chart
    daily_sales = orders.annotate(
        date=TruncDate('order_date')
    ).values('date').annotate(
        total=Sum('total_amount')
    ).order_by('date')

    # If no sales data, provide sample data for visualization
    if not daily_sales:
        # Create sample data for the last 7 days
        sample_dates = []
        sample_values = []
        for i in range(7, 0, -1):
            sample_date = (timezone.now() - timedelta(days=i)).date()
            sample_dates.append(sample_date.strftime('%Y-%m-%d'))
            sample_values.append(float(i * 1000))  # Sample increasing values
        
        chart_labels = sample_dates
        chart_data = sample_values
        print("Using sample sales trend data")
    else:
        chart_labels = [sale['date'].strftime('%Y-%m-%d') for sale in daily_sales]
        chart_data = [float(sale['total']) for sale in daily_sales]

    # Get top selling products using OrderItem model
    revenue_expression = ExpressionWrapper(
        F('quantity') * F('price_at_time_of_order'),
        output_field=DecimalField()
    )
    
    top_products = OrderItem.objects.filter(
        order__in=orders
    ).values(
        'product__product_name'
    ).annotate(
        name=F('product__product_name'),
        units_sold=Sum('quantity'),
        revenue=Sum(revenue_expression)
    ).order_by('-units_sold')[:5]

    # Get sales by category
    category_sales = OrderItem.objects.filter(
        order__order_date__gte=start_date,
        order__order_date__lte=end_date,
        order__status='completed'
    ).values(
        'product__category'
    ).annotate(
        total=Sum('quantity'),
        revenue=Sum(revenue_expression)
    ).order_by('-total')

    # If no category data, provide sample data
    if not category_sales:
        # Sample categories and values
        sample_categories = ['Electronics', 'Clothing', 'Food', 'Other']
        sample_quantities = [25, 15, 10, 5]
        sample_revenues = [2500, 1500, 500, 250]
        
        # Create a list of dictionaries for the template
        category_data_for_template = []
        for i in range(len(sample_categories)):
            category_data_for_template.append({
                'category': sample_categories[i],
                'units': sample_quantities[i],
                'revenue': sample_revenues[i]
            })
        
        category_labels = json.dumps(sample_categories)
        category_quantities = json.dumps(sample_quantities)
        category_revenues = json.dumps(sample_revenues)
        print("Using sample category data")
    else:
        # Create a list of dictionaries for the template
        category_data_for_template = []
        for sale in category_sales:
            category_data_for_template.append({
                'category': sale['product__category'],
                'units': sale['total'],
                'revenue': float(sale['revenue'])
            })
        
        category_labels = json.dumps([sale['product__category'] for sale in category_sales])
        category_quantities = json.dumps([sale['total'] for sale in category_sales])
        category_revenues = json.dumps([float(sale['revenue']) for sale in category_sales])

    # Get detailed sales with pagination
    detailed_sales = Order.objects.all().order_by('-order_date')
    paginator = Paginator(detailed_sales, 10)
    page = request.GET.get('page')
    try:
        detailed_sales = paginator.page(page)
    except PageNotAnInteger:
        detailed_sales = paginator.page(1)
    except EmptyPage:
        detailed_sales = paginator.page(paginator.num_pages)

    context = {
        'total_sales': total_sales,
        'total_orders': total_orders,
        'avg_order_value': avg_order_value,
        'items_sold': items_sold,
        'sales_change': sales_change,
        'orders_change': orders_change,
        'items_change': items_change,
        'avg_value_change': ((avg_order_value - (prev_total_sales/prev_total_orders if prev_total_orders > 0 else 0)) / (prev_total_sales/prev_total_orders if prev_total_orders > 0 else 1) * 100),
        'chart_labels': json.dumps(chart_labels),
        'chart_data': json.dumps(chart_data),
        'top_products': top_products,
        'category_labels': category_labels,
        'category_data': category_quantities,
        'category_revenue': category_revenues,
        'category_data_for_template': category_data_for_template,
        'detailed_sales': detailed_sales,
        'selected_date_range': date_range,
        'start_date': start_date,
        'end_date': end_date
    }

    # Handle CSV export
    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="sales_report_{date_range}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Date', 'Order ID', 'Customer', 'Items', 'Total', 'Status'])
        
        for order in Order.objects.filter(order_date__gte=start_date, order_date__lte=end_date).order_by('-order_date'):
            writer.writerow([
                order.order_date.strftime('%Y-%m-%d'),
                order.id,
                order.customer_name,
                order.items.count(),
                order.total_amount,
                order.status
            ])
        return response

    return render(request, 'members/manager/sales_reports.html', context)

# Analyst Views
@login_required
@user_passes_test(check_analyst)
def analyst_dashboard(request):
    context = {
        'total_predictions': 150,  # Replace with actual count
        'accuracy_rate': 92.5,  # Replace with actual percentage
        'recent_forecasts': [
            {'product': 'Laptop', 'prediction': '500 units', 'accuracy': '95%'},
            {'product': 'Desktop', 'prediction': '300 units', 'accuracy': '90%'},
            {'product': 'Mouse', 'prediction': '1000 units', 'accuracy': '88%'},
        ]
    }
    return render(request, 'members/analyst/analyst_dashboard.html', context)

@login_required
@user_passes_test(check_analyst)
def view_forecasts(request):
    # Get filter parameters
    time_range = request.GET.get('time_range', '30')
    category = request.GET.get('category', 'all')
    accuracy_filter = request.GET.get('accuracy', 'all')
    
    # Calculate date range
    end_date = timezone.now()
    if time_range != 'all':
        start_date = end_date - timedelta(days=int(time_range))
    else:
        start_date = end_date - timedelta(days=365)  # Default to last year for "all"

    # Get all predictions from session data
    all_predictions = []
    if 'predictions' in request.session:
        all_predictions = request.session['predictions']

    # Define our standard categories
    standard_categories = ['Electronics', 'Clothing', 'Food', 'Accessories']

    # If no predictions exist, create sample data
    if not all_predictions:
        # Generate sample predictions for the last 7 days
        categories = standard_categories
        products = {
            'Electronics': ['Laptop', 'Smartphone', 'Tablet'],
            'Clothing': ['T-Shirt', 'Jeans', 'Jacket'],
            'Food': ['Snacks', 'Beverages', 'Canned Goods'],
            'Accessories': ['Watch', 'Bag', 'Belt']
        }

        for i in range(7):
            date = (end_date - timedelta(days=i)).strftime('%Y-%m-%d')
            category = random.choice(categories)
            product = random.choice(products[category])
            forecasted = random.randint(50, 200)
            actual = forecasted + random.randint(-20, 20)
            accuracy = round((1 - abs(actual - forecasted) / forecasted) * 100, 1)
            variance = round(abs(actual - forecasted) / forecasted * 100, 1)

            all_predictions.append({
                'date': date,
                'category': category,
                'product': product,
                'forecasted': str(forecasted),
                'actual': str(actual),
                'accuracy': str(accuracy),
                'variance': str(variance),
                'id': f"pred_{i}"
            })

        # Store sample predictions in session
        request.session['predictions'] = all_predictions

    # Filter predictions based on criteria
    filtered_predictions = []
    for pred in all_predictions:
        pred_date = datetime.strptime(pred['date'], '%Y-%m-%d').date()
        pred_category = pred.get('category', 'All Categories')

        if pred_date >= start_date.date() and pred_date <= end_date.date():
            if category == 'all' or category == pred_category:
                filtered_predictions.append(pred)

    # Calculate accuracy metrics
    total_forecasts = len(filtered_predictions)
    if total_forecasts > 0:
        accuracies = [float(pred.get('accuracy', 0)) for pred in filtered_predictions]
        average_accuracy = round(sum(accuracies) / len(accuracies), 1)
        
        # Calculate category-wise accuracy
        category_accuracies = {}
        for pred in filtered_predictions:
            cat = pred.get('category', 'Unknown')
            if cat not in category_accuracies:
                category_accuracies[cat] = []
            category_accuracies[cat].append(float(pred.get('accuracy', 0)))
        
        most_accurate_category = max(
            category_accuracies.items(),
            key=lambda x: sum(x[1]) / len(x[1])
        )[0] if category_accuracies else "N/A"
        
        category_accuracy = round(
            sum(category_accuracies[most_accurate_category]) /
            len(category_accuracies[most_accurate_category]),
            1
        ) if most_accurate_category != "N/A" else 0
    else:
        average_accuracy = 0
        most_accurate_category = "N/A"
        category_accuracy = 0
    
    # Prepare accuracy trend data
    dates = []
    accuracies = []
    for pred in sorted(filtered_predictions, key=lambda x: x['date']):
        dates.append(pred['date'])
        accuracies.append(float(pred.get('accuracy', 0)))  # Use .get() with default value

    accuracy_trend_data = {
        "dates": dates,
        "accuracies": accuracies
    }

    # Ensure categories are extracted safely
    categories = list(set(pred.get('category', 'Unknown') for pred in all_predictions))  # Use .get() with default value

    # Get all unique categories from the Product model and predictions
    # This ensures we show all actual categories in the database
    db_categories = set(Product.objects.values_list('category', flat=True).distinct())
    prediction_categories = set(pred.get('category', 'Unknown') for pred in all_predictions)
    
    # Also include our standard categories to ensure they're always available
    all_categories = sorted(db_categories.union(prediction_categories).union(set(standard_categories)))

    # Print categories for debugging
    print("Available categories:", all_categories)

    context = {
        'time_range': time_range,
        'category': category,
        'accuracy': accuracy_filter,
        'total_forecasts': total_forecasts,
        'average_accuracy': average_accuracy,
        'most_accurate_category': most_accurate_category,
        'category_accuracy': category_accuracy,
        'accuracy_trend_data': json.dumps(accuracy_trend_data),
        'forecasts': filtered_predictions,
        'categories': all_categories  # Use the enhanced list of categories
    }
    return render(request, 'members/analyst/forecasts.html', context)

@login_required
@user_passes_test(check_analyst)
def analytics_reports(request):
    try:
        # Calculate date ranges
        end_date = timezone.now()
        start_date = end_date - timedelta(days=30)
        prev_start_date = start_date - timedelta(days=30)

        # 1. Sales Growth
        current_period_sales = OrderItem.objects.filter(
            order__order_date__gte=start_date,
            order__order_date__lte=end_date,
            order__status='completed'
        ).aggregate(
            total=Sum(F('quantity') * F('price_at_time_of_order'))
        )['total'] or 0

        previous_period_sales = OrderItem.objects.filter(
            order__order_date__gte=prev_start_date,
            order__order_date__lt=start_date,
            order__status='completed'
        ).aggregate(
            total=Sum(F('quantity') * F('price_at_time_of_order'))
        )['total'] or 0

        sales_growth = ((current_period_sales - previous_period_sales) / previous_period_sales * 100) if previous_period_sales > 0 else 0

        # 2. Inventory Turnover
        # Calculate COGS (Cost of Goods Sold)
        cogs = OrderItem.objects.filter(
            order__order_date__gte=start_date,
            order__order_date__lte=end_date,
            order__status='completed'
        ).aggregate(
            total=Sum(F('quantity') * F('price_at_time_of_order'))
        )['total'] or 0

        # Calculate average inventory value
        current_inventory = Item.objects.aggregate(
            total=Sum(F('quantity') * F('price'))
        )['total'] or 1

        previous_inventory = current_inventory  # Simplified for demonstration
        avg_inventory = (current_inventory + previous_inventory) / 2 if (current_inventory + previous_inventory) > 0 else 1

        inventory_turnover = (cogs / avg_inventory) if avg_inventory > 0 else 0

        # 3. Forecast Accuracy
        predictions = request.session.get('predictions', [])
        if predictions:
            accuracies = [float(pred.get('accuracy', 0)) for pred in predictions if pred.get('accuracy')]
            forecast_accuracy = sum(accuracies) / len(accuracies) if accuracies else 0
        else:
            forecast_accuracy = 0

        # 4. Order Fulfillment Time
        fulfilled_orders = Order.objects.filter(
            status='completed',
            order_date__gte=start_date
        ).annotate(
            fulfillment_time=ExpressionWrapper(
                F('updated_at') - F('order_date'),
                output_field=DurationField()
            )
        )
        
        avg_fulfillment_days = fulfilled_orders.aggregate(
            avg_time=Avg('fulfillment_time')
        )['avg_time']
        
        fulfillment_time = avg_fulfillment_days.days if avg_fulfillment_days else 0

        # Prepare context with KPI data
        context = {
            'kpi_data': {
                'sales_growth': round(sales_growth, 1),
                'inventory_turnover': round(inventory_turnover, 2),
                'forecast_accuracy': round(forecast_accuracy, 1),
                'fulfillment_time': round(fulfillment_time, 1)
            },
            'trend_analysis': {
                'top_category': {
                    'name': 'Electronics',  # Example value
                    'growth': 15.5
                },
                'fastest_product': {
                    'name': 'Laptop',  # Example value
                    'growth': 25.0
                },
                'seasonal_impact': {
                    'current_season': 'Summer'
                }
            }
        }
        
        return render(request, 'members/analyst/analytics_reports.html', context)
    
    except Exception as e:
        print(f"Error in analytics_reports view: {str(e)}")
        import traceback
        print(traceback.format_exc())
        
        # Return default context with zeros
        context = {
            'kpi_data': {
                'sales_growth': 0,
                'inventory_turnover': 0,
                'forecast_accuracy': 0,
                'fulfillment_time': 0
            },
            'trend_analysis': {
                'top_category': {
                    'name': 'N/A',
                    'growth': 0
                },
                'fastest_product': {
                    'name': 'N/A',
                    'growth': 0
                },
                'seasonal_impact': {
                    'current_season': 'Unknown'
                }
            }
        }
        return render(request, 'members/analyst/analytics_reports.html', context)


@login_required
@user_passes_test(check_analyst)
def generate_predictions(request):
    if request.method == 'POST':
        try:
            prediction_type = request.POST.get('prediction_type')
            time_range = request.POST.get('time_range')
            category = request.POST.get('category')
            confidence_level = Decimal(request.POST.get('confidence_level', '95%').strip('%')) / 100
            consider_seasonal = request.POST.get('consider_seasonal') == 'on'

            # Use Product data from the database
            products = Product.objects.all()
            if category != 'All Categories':
                products = products.filter(category=category)
            total_quantity = products.aggregate(total_qty=Sum('current_stock'))['total_qty'] or 0
            total_revenue = products.aggregate(
                total_rev=Sum(ExpressionWrapper(F('current_stock') * F('unit_price'), output_field=DecimalField()))
            )['total_rev'] or Decimal('0.00')

            days = {'Next Week': 7, 'Next Month': 30, 'Next Quarter': 90}.get(time_range, 7)
            predictions = []
            start_date = timezone.now().date()
            for i in range(days):
                future_date = start_date + timedelta(days=i)
                # For demand forecast, add a gradual growth factor; for revenue, add a random variation
                if prediction_type == 'Demand Forecast':
                    growth = Decimal('1.0') + (Decimal(i) * Decimal('0.02'))  # 2% growth per day
                    multiplier = confidence_level * growth
                elif prediction_type == 'Revenue Forecast':
                    fluctuation = Decimal(random.uniform(0.95, 1.05))
                    multiplier = confidence_level * fluctuation
                else:
                    multiplier = confidence_level
                if consider_seasonal:
                    if future_date.weekday() in [5, 6]:
                        multiplier *= Decimal('1.2')
                    elif future_date.weekday() == 0:
                        multiplier *= Decimal('0.9')
                predicted_qty = Decimal(total_quantity) * multiplier
                predicted_rev = Decimal(total_revenue) * multiplier
                predictions.append({
                    'date': future_date.strftime('%Y-%m-%d'),
                    'predicted_quantity': str(predicted_qty.quantize(Decimal('0.01'))),
                    'predicted_revenue': str(predicted_rev.quantize(Decimal('0.01')))
                })
            request.session['predictions'] = predictions
            messages.success(request, 'Predictions generated successfully!')
        except Exception as e:
            messages.error(request, f'Error generating predictions: {str(e)}')
    categories = Product.objects.values_list('category', flat=True).distinct()
    context = {
        'categories': categories,
        'predictions': request.session.get('predictions', []),
        'predictions_json': json.dumps(request.session.get('predictions', [])),
        'prediction_type': request.POST.get('prediction_type', 'Demand Forecast')
    }
    return render(request, 'members/analyst/predictions.html', context)

@login_required
@user_passes_test(check_analyst)
def sales_trends(request):
    # Get date range from request or default to last 30 days
    days = int(request.GET.get('days', 30))
    end_date = timezone.now()
    start_date = end_date - timedelta(days=days)
    
    try:
        # Get sales data grouped by date
        daily_sales = OrderItem.objects.filter(
            order__order_date__gte=start_date,
            order__order_date__lte=end_date,
            order__status='completed'
        ).annotate(
            date=TruncDate('order__order_date')
        ).values('date').annotate(
            total_quantity=Sum('quantity'),
            total_revenue=Sum(F('quantity') * F('price_at_time_of_order'))
        ).order_by('date')

        # Get sales data grouped by category
        category_sales = OrderItem.objects.filter(
            order__order_date__gte=start_date,
            order__order_date__lte=end_date,
            order__status='completed'
        ).values(
            'product__category'
        ).annotate(
            total_quantity=Sum('quantity'),
            total_revenue=Sum(F('quantity') * F('price_at_time_of_order'))
        ).order_by('-total_revenue')

        # Calculate total revenue and quantity directly from OrderItem
        totals = OrderItem.objects.filter(
            order__order_date__gte=start_date,
            order__order_date__lte=end_date,
            order__status='completed'
        ).aggregate(
            total_revenue=Sum(F('quantity') * F('price_at_time_of_order')),
            total_quantity=Sum('quantity')
        )

        total_revenue = float(totals['total_revenue'] or 0)
        total_quantity = int(totals['total_quantity'] or 0)
        
        # Calculate daily averages
        days_count = (end_date.date() - start_date.date()).days + 1
        avg_daily_revenue = total_revenue / days_count if days_count > 0 else 0
        avg_daily_quantity = total_quantity / days_count if days_count > 0 else 0

        # Prepare data for charts
        dates = [entry['date'].strftime('%Y-%m-%d') for entry in daily_sales]
        quantities = [float(entry['total_quantity']) for entry in daily_sales]
        revenues = [float(entry['total_revenue']) for entry in daily_sales]

        categories = [entry['product__category'] for entry in category_sales]
        category_quantities = [float(entry['total_quantity']) for entry in category_sales]
        category_revenues = [float(entry['total_revenue']) for entry in category_sales]

        # Calculate growth rates
        if len(revenues) >= 2:
            revenue_growth = ((revenues[-1] - revenues[0]) / revenues[0] * 100) if revenues[0] != 0 else 0
            quantity_growth = ((quantities[-1] - quantities[0]) / quantities[0] * 100) if quantities[0] != 0 else 0
        else:
            revenue_growth = 0
            quantity_growth = 0

        context = {
            'sales_trend_data': json.dumps({
                'dates': dates,
                'quantities': quantities,
                'revenues': revenues
            }),
            'category_data': json.dumps({
                'categories': categories or ['No Data'],
                'quantities': category_quantities or [0],
                'revenues': category_revenues or [0]
            }),
            'summary': {
                'total_revenue': total_revenue,
                'total_quantity': total_quantity,
                'avg_daily_revenue': avg_daily_revenue,
                'avg_daily_quantity': avg_daily_quantity,
                'revenue_growth': revenue_growth,
                'quantity_growth': quantity_growth
            },
            'selected_days': days
        }
        
        return render(request, 'members/analyst/sales_trends.html', context)
    
    except Exception as e:
        print(f"Error in sales_trends view: {str(e)}")
        import traceback
        print(traceback.format_exc())
        
        context = {
            'sales_trend_data': json.dumps({
                'dates': [(end_date - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(days-1, -1, -1)],
                'quantities': [0] * days,
                'revenues': [0] * days
            }),
            'category_data': json.dumps({
                'categories': ['No Data'],
                'quantities': [0],
                'revenues': [0]
            }),
            'summary': {
                'total_revenue': 0,
                'total_quantity': 0,
                'avg_daily_revenue': 0,
                'avg_daily_quantity': 0,
                'revenue_growth': 0,
                'quantity_growth': 0
            },
            'selected_days': days
        }
        
        return render(request, 'members/analyst/sales_trends.html', context)

@login_required
@user_passes_test(check_analyst)
def inventory_trends(request):
    # Get filter parameters
    period = request.GET.get('period', 'monthly')
    date_range = request.GET.get('range', '30')
    category = request.GET.get('category', 'all')
    
    # Calculate date range
    end_date = timezone.now()
    days = int(date_range)
    start_date = end_date - timedelta(days=days)
    
    try:
        # Base queryset
        items = Item.objects.all()
        if category != 'all':
            items = items.filter(category=category)

        # Calculate current inventory stats with proper annotations
        current_stats = items.aggregate(
            total_value=Sum(F('quantity') * F('price')),
            total_items=Sum('quantity'),
            low_stock_count=Count('id', filter=Q(quantity__lte=F('reorder_level'))),
            avg_stock=Avg('quantity')
        )

        # Calculate stock turnover rate for the selected period
        # 1. Cost of Goods Sold (COGS) during the period
        cogs_order_items = OrderItem.objects.filter(
            order__order_date__gte=start_date,
            order__order_date__lte=end_date,
            order__status='completed'
        )
        if category != 'all':
            cogs_order_items = cogs_order_items.filter(product__category=category)  # Changed from item__category

        cogs = cogs_order_items.aggregate(
            total_cogs=Sum(F('quantity') * F('price_at_time_of_order'))
        )['total_cogs'] or 0

        # 2. Average Inventory Value during the period
        # This is a simplified approach. A more accurate method might track daily values.
        # For now, let's use the current value as an approximation for the average.
        avg_inventory_value = current_stats['total_value'] or 0

        # Calculate Turnover (COGS / Average Inventory Value)
        # Avoid division by zero
        stock_turnover = (cogs / avg_inventory_value) if avg_inventory_value > 0 else 0

        # Get daily inventory levels for trend chart (Consider using InventorySnapshot if available)
        # Simplified: Using OrderItem data might not reflect actual inventory level changes precisely
        # A dedicated InventorySnapshot model recording daily levels would be better.
        inventory_trend_base = Item.objects.all() # Start with all items
        if category != 'all':
            inventory_trend_base = inventory_trend_base.filter(category=category)

        # --- Placeholder for more accurate trend data calculation ---
        # Example: If you had an InventorySnapshot model with date and quantity
        # snapshots = InventorySnapshot.objects.filter(
        #     date__gte=start_date, date__lte=end_date
        # )
        # if category != 'all':
        #     snapshots = snapshots.filter(item__category=category)
        # daily_levels = snapshots.values('date').annotate(
        #     stock_level=Sum('quantity')
        # ).order_by('date')
        # --- End Placeholder ---

        # Using simplified OrderItem data for trend (less accurate)
        inventory_trend_items = OrderItem.objects.filter(
            order__order_date__gte=start_date,
            order__order_date__lte=end_date
        )
        if category != 'all':
            inventory_trend_items = inventory_trend_items.filter(product__category=category)  # Changed from item__category

        inventory_trend = inventory_trend_items.annotate(
            date=TruncDate('order__order_date')
        ).values('date').annotate(
            stock_level=Avg('quantity')  # Changed from Avg('item__quantity')
        ).order_by('date')

        # Prepare trend data
        dates = []
        stock_levels = []
        
        current_date = start_date
        while current_date <= end_date:
            dates.append(current_date.strftime('%Y-%m-%d'))
            level = next(
                (entry['stock_level'] for entry in inventory_trend if entry['date'] == current_date.date()),
                None
            )
            stock_levels.append(float(level) if level is not None else 0)
            current_date += timedelta(days=1)

        # Calculate stock status distribution
        stock_distribution = {
            'Out of Stock': items.filter(quantity=0).count(),
            'Low Stock': items.filter(quantity__gt=0, quantity__lte=F('reorder_level')).count(),
            'Optimal': items.filter(
                quantity__gt=F('reorder_level'),
                quantity__lte=F('reorder_level') * 2
            ).count(),
            'Excess': items.filter(quantity__gt=F('reorder_level') * 2).count()
        }

        # Get detailed inventory data
        detailed_inventory = items.annotate(
            stock_value=F('quantity') * F('price'),
            # Placeholder for turnover_rate per item - needs sales data for the item
            turnover_rate=Value(0, output_field=FloatField()), # Example placeholder
            # total_sales=Subquery(...) # Requires linking item sales
            # turnover_rate=Case(
            #     When(quantity__gt=0, then=F('total_sales') / F('quantity')),
            #     default=0,
            #     output_field=FloatField()
            # ),
            status=Case(
                When(quantity=0, then=Value('Out of Stock')),
                When(quantity__lte=F('reorder_level'), then=Value('Low Stock')),
                When(quantity__lte=F('reorder_level') * 2, then=Value('Optimal')),
                default=Value('Excess'),
                output_field=CharField()
            )
        ).values(
            'product_name', 'category', 'quantity', 'reorder_level',
            'stock_value', 'turnover_rate', 'status'
        )

        context = {
            'selected_filters': {
                'period': period,
                'range': date_range,
                'category': category
            },
            'metrics': {
                'total_value': float(current_stats['total_value'] or 0),
                'stock_turnover': stock_turnover,
                'low_stock_items': current_stats['low_stock_count'] or 0,
                'avg_stock_level': float(current_stats['avg_stock'] or 0)
            },

            
            'trend_data': json.dumps({
                'dates': dates,
                'stock_levels': stock_levels
            }),
            'distribution_data': json.dumps({
                'labels': list(stock_distribution.keys()),
                'values': list(stock_distribution.values())
            }),

            # 'trend_data': json.dumps(trend_data),  # trend_data = {"dates": [...], "stock_levels": [...]}
            # 'distribution_data': json.dumps(distribution_data),

            'detailed_inventory': detailed_inventory
        }
        
        return render(request, 'members/analyst/inventory_trends.html', context)
    
    except Exception as e:
        print(f"Error in inventory_trends view: {str(e)}")
        import traceback
        print(traceback.format_exc())
        
        # Return empty data structure with zeros
        context = {
            'selected_filters': {
                'period': period,
                'range': date_range,
                'category': category
            },
            'metrics': {
                'total_value': 0,
                'stock_turnover': 0,
                'low_stock_items': 0,
                'avg_stock_level': 0
            },
            'trend_data': json.dumps({
                'dates': [],
                'stock_levels': []
            }),
            'distribution_data': json.dumps({
                'labels': ['Out of Stock', 'Low Stock', 'Optimal', 'Excess'],
                'values': [0, 0, 0, 0]
            }),
            'detailed_inventory': []
        }
        
        return render(request, 'members/analyst/inventory_trends.html', context)

@login_required
@user_passes_test(check_analyst)
def performance_metrics(request):
    try:
        # Get filter parameters
        period = request.GET.get('period', 'weekly')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        compare_with = request.GET.get('compare_with', 'previous')

        # Set default date range if not provided
        if not end_date:
            end_date = timezone.now()
        else:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')

        if not start_date:
            if period == 'weekly':
                start_date = end_date - timedelta(days=7)
            elif period == 'monthly':
                start_date = end_date - timedelta(days=30)
            elif period == 'quarterly':
                start_date = end_date - timedelta(days=90)
            else:
                start_date = end_date - timedelta(days=7)
        else:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')

        # Calculate previous period
        period_length = (end_date - start_date).days
        prev_end_date = start_date
        prev_start_date = prev_end_date - timedelta(days=period_length)

        # 1. Sales Performance
        current_sales = OrderItem.objects.filter(
            order__order_date__gte=start_date,
            order__order_date__lte=end_date,
            order__status='completed'
        ).aggregate(
            total=Sum(F('quantity') * F('price_at_time_of_order'))
        )['total'] or 0

        previous_sales = OrderItem.objects.filter(
            order__order_date__gte=prev_start_date,
            order__order_date__lte=prev_end_date,
            order__status='completed'
        ).aggregate(
            total=Sum(F('quantity') * F('price_at_time_of_order'))
        )['total'] or 0

        sales_change = ((current_sales - previous_sales) / previous_sales * 100) if previous_sales > 0 else 0

        # 2. Order Fulfillment Rate
        total_orders = Order.objects.filter(
            order_date__gte=start_date,
            order_date__lte=end_date
        ).count()

        fulfilled_orders = Order.objects.filter(
            order_date__gte=start_date,
            order_date__lte=end_date,
            status='completed'
        ).count()

        fulfillment_rate = (fulfilled_orders / total_orders * 100) if total_orders > 0 else 0

        # 3. Inventory Turnover
        cogs = OrderItem.objects.filter(
            order__order_date__gte=start_date,
            order__order_date__lte=end_date,
            order__status='completed'
        ).aggregate(
            total=Sum(F('quantity') * F('price_at_time_of_order'))
        )['total'] or 0

        avg_inventory = Item.objects.aggregate(
            total=Sum(F('quantity') * F('price'))
        )['total'] or 1

        inventory_turnover = cogs / avg_inventory if avg_inventory > 0 else 0

        # 4. Forecast Accuracy
        predictions = request.session.get('predictions', [])
        if predictions:
            accuracies = [float(pred.get('accuracy', 0)) for pred in predictions if pred.get('accuracy')]
            forecast_accuracy = sum(accuracies) / len(accuracies) if accuracies else 0
        else:
            forecast_accuracy = 0

        # Get trend data for chart
        trend_data = OrderItem.objects.filter(
            order__order_date__gte=start_date,
            order__order_date__lte=end_date
        ).annotate(
            date=TruncDate('order__order_date')
        ).values('date').annotate(
            sales=Sum(F('quantity') * F('price_at_time_of_order')),
            orders=Count('order', distinct=True),
            turnover=Sum('quantity')
        ).order_by('date')

        # Prepare data for charts
        dates = []
        sales_data = []
        orders_data = []
        turnover_data = []

        # Fill in data for each day in the range
        current_date = start_date
        while current_date <= end_date:
            dates.append(current_date.strftime('%Y-%m-%d'))
            
            # Find data for this date
            day_data = next(
                (item for item in trend_data if item['date'].strftime('%Y-%m-%d') == current_date.strftime('%Y-%m-%d')),
                None
            )
            
            if day_data:
                sales_data.append(float(day_data['sales'] or 0))
                orders_data.append(int(day_data['orders'] or 0))
                turnover_data.append(int(day_data['turnover'] or 0))
            else:
                sales_data.append(0)
                orders_data.append(0)
                turnover_data.append(0)
            
            current_date += timedelta(days=1)

        # Get category performance data
        category_performance = OrderItem.objects.filter(
            order__order_date__gte=start_date,
            order__order_date__lte=end_date
        ).values(
            'product__category'
        ).annotate(
            sales=Sum(F('quantity') * F('price_at_time_of_order')),
            orders=Count('order', distinct=True)
        ).order_by('-sales')

        # Prepare category data
        category_data = []
        for cat in category_performance:
            if cat['product__category']:  # Ensure category is not None
                category_data.append({
                    'category': cat['product__category'],
                    'sales': float(cat['sales'] or 0),
                    'orders': int(cat['orders'] or 0)
                })

        # Prepare detailed metrics
        detailed_metrics = [
            {
                'metric': 'Total Sales',
                'current_value': f"${current_sales:,.2f}",
                'previous_value': f"${previous_sales:,.2f}",
                'change': f"{sales_change:,.1f}%",
                'status': 'up' if sales_change > 0 else 'down'
            },
            {
                'metric': 'Order Fulfillment Rate',
                'current_value': f"{fulfillment_rate:.1f}%",
                'previous_value': 'N/A',
                'change': 'N/A',
                'status': 'neutral'
            },
            {
                'metric': 'Inventory Turnover',
                'current_value': f"{inventory_turnover:.2f}x",
                'previous_value': 'N/A',
                'change': 'N/A',
                'status': 'neutral'
            },
            {
                'metric': 'Forecast Accuracy',
                'current_value': f"{forecast_accuracy:.1f}%",
                'previous_value': 'N/A',
                'change': 'N/A',
                'status': 'neutral'
            }
        ]

        context = {
            'metrics': {
                'sales_performance': f"${current_sales:,.2f}",
                'order_fulfillment': f"{fulfillment_rate:.1f}%",
                'inventory_turnover': f"{inventory_turnover:.1f}x",
                'forecast_accuracy': f"{forecast_accuracy:.1f}%"
            },
            'changes': {
                'sales_vs': f"{sales_change:,.1f}",
                'fulfillment_vs': '0.0',
                'turnover_vs': '0.0',
                'accuracy_vs': '0.0'
            },
            'chart_data': {
                'dates': json.dumps(dates),
                'sales': json.dumps(sales_data),
                'orders': json.dumps(orders_data),
                'turnover': json.dumps(turnover_data)
            },
            'category_performance': json.dumps(category_data),
            'detailed_metrics': detailed_metrics,
            'selected_filters': {
                'period': period,
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'compare_with': compare_with
            }
        }
        
        return render(request, 'members/analyst/performance_metrics.html', context)

    except Exception as e:
        print(f"Error in performance_metrics view: {str(e)}")
        import traceback
        print(traceback.format_exc())
        
        # Return default context with zeros
        context = {
            'metrics': {
                'sales_performance': '$0.00',
                'order_fulfillment': '0.0%',
                'inventory_turnover': '0.0x',
                'forecast_accuracy': '0.0%'
            },
            'changes': {
                'sales_vs': '0.0',
                'fulfillment_vs': '0.0',
                'turnover_vs': '0.0',
                'accuracy_vs': '0.0'
            },
            'chart_data': {
                'dates': json.dumps([]),
                'sales': json.dumps([]),
                'orders': json.dumps([]),
                'turnover': json.dumps([])
            },
            'category_performance': json.dumps([]),
            'detailed_metrics': [],
            'selected_filters': {
                'period': 'weekly',
                'start_date': '',
                'end_date': '',
                'compare_with': 'previous'
            }
        }
        return render(request, 'members/analyst/performance_metrics.html', context)

@login_required
def edit_item(request, item_id):
    try:
        item = Item.objects.get(id=item_id)
        if request.method == 'GET':
            # Return item details as JSON for AJAX request
            return JsonResponse({
                'product_name': item.product_name,
                'category': item.category,
                'description': item.description,
                'quantity': item.quantity,
                'price': item.price,
                'reorder_level': item.reorder_level,
                'supplier': item.supplier,
                'sku': item.sku,
                'active': item.active,
                'product_image': item.product_image.url if item.product_image else None,
            })
        elif request.method == 'POST':
            # Update item with new data
            item.product_name = request.POST.get('product_name')
            item.category = request.POST.get('category')
            item.description = request.POST.get('description')
            item.quantity = request.POST.get('quantity')

            item.price = request.POST.get('price')
            item.reorder_level = request.POST.get('reorder_level')
            item.supplier = request.POST.get('supplier')
            item.sku = request.POST.get('sku')
            item.active = request.POST.get('active') == 'on'
            
            if 'product_image' in request.FILES:
                item.product_image = request.FILES['product_image']
                                   
            item.save()
            messages.success(request, 'Item updated successfully')
            return redirect('inventory')
    except Item.DoesNotExist:
        messages.error(request, 'Item not found')
        return redirect('inventory')
    except Exception as e:
        messages.error(request, f'Error updatingitem: {str(e)}')
        return redirect('inventory')

@login_required
def reorder_item(request):
    if request.method == 'POST':
        try:
            item_id = request.POST.get('item_id')
            quantity = int(request.POST.get('quantity'))
            
            product = Product.objects.get(id=item_id)  # Changed from Item to Product
            product.current_stock += quantity  # Changed from item.quantity to product.current_stock
            product.save()
            
            # Create a record in the Order model
            order = Order.objects.create(
                created_by=request.user,
                total_amount=product.unit_price * quantity,  # Changed from item.price to product.unit_price
                status='Completed'
            )
            
            # Create OrderItem
            OrderItem.objects.create(
                order=order,
                product=product,  # Changed from item to product
                quantity=quantity,
                price_at_time_of_order=product.unit_price  # Changed from item.price to product.unit_price
            )
            
            messages.success(request, f'Successfully reordered {quantity} units of {product.product_name}')  # Changed from item.product_name to product.product_name
        
        except Product.DoesNotExist:  # Changed from Item.DoesNotExist to Product.DoesNotExist
            messages.error(request, 'Item not found')
        except ValueError:
            messages.error(request, 'Invalid quantity')
        except Exception as e:
            messages.error(request, f'Error processing reorder: {str(e)}')
    
    return redirect('view_inventory')

def landing(request):
    return render(request, 'members/landing.html')

@login_required
@user_passes_test(check_manager)
def process_payment(request, order_id):
    if request.method == 'POST':
        try:
            order = Order.objects.get(id=order_id)
            
            if order.payment_status == 'paid':
                messages.warning(request, 'This order has already been paid.')
                return redirect('view_order', order_id=order_id)
            
            payment_method = request.POST.get('payment_method')
            transaction_id = request.POST.get('transaction_id')
            
            # Create payment record
            payment = Payment(
                order=order,
                amount=order.total_amount,
                payment_method=payment_method,
                transaction_id=transaction_id,
                created_by=request.user,
                status='success'  # For demo, in production this would depend on payment gateway response
            )
            
            # Save the payment
            payment.save()
            
            # Update order status to completed and payment status to paid
            order.status = 'completed'  # Change status to completed
            order.payment_status = 'paid'
            order.save()
            
            messages.success(request, f'Payment of Rs{order.total_amount} processed successfully! Transaction ID: {transaction_id}')
            
        except Order.DoesNotExist:
            messages.error(request, 'Order not found.')
        except Exception as e:
            messages.error(request, f'Error processing payment: {str(e)}')
    
    return redirect('view_order', order_id=order_id)

def upload_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']

        # ✅ Fix extension check
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a valid CSV (.csv) file.')
            return redirect('upload_csv')

        try:
            # Read CSV file
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file)

            # Skip header
            next(reader)

            for row in reader:
                try:
                    product_name = row[0]
                    category = row[1]
                    current_stock = int(row[2])
                    reorder_level = int(row[3])
                    unit_price = float(row[4])
                    status = row[5] if row[5] else 'In Stock'

                    product = Product(
                        product_name=product_name,
                        category=category,
                        current_stock=current_stock,
                        reorder_level=reorder_level,
                        unit_price=unit_price,
                        status=status,
                        last_updated=datetime.now()
                    )
                    product.save()
                except Exception as e:
                    messages.error(request, f"Row error: {row} | {e}")

            messages.success(request, 'CSV data uploaded successfully.')
        except Exception as e:
            messages.error(request, f"Failed to process CSV file: {e}")

        return redirect('upload_csv')

    return render(request, 'members/upload_csv.html')
