from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin', _('Admin')
        MANAGER = 'manager', _('Inventory Manager')
        ANALYST = 'analyst', _('Analyst')

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.MANAGER,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    



class Product(models.Model):
    STATUS_CHOICES = [
        ('In Stock', 'In Stock'),
        ('Out of Stock', 'Out of Stock'),
        ('Reordered', 'Reordered'),
    ]

    product_name = models.CharField(max_length=100, verbose_name="Product Name")
    category = models.CharField(max_length=50)
    
    current_stock = models.PositiveIntegerField()
    reorder_level = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    value = models.DecimalField(max_digits=12, decimal_places=2)

    supplier = models.CharField(max_length=200, blank=True, null=True)
    sku = models.CharField(max_length=50, unique=True, blank=True, null=True)
    product_image = models.ImageField(upload_to='products/', blank=True, null=True)
    active = models.BooleanField(default=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='In Stock')

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    last_updated = models.DateTimeField()

    def __str__(self):
        return self.product_name  # Fixed from self.name to self.product_name

    def save(self, *args, **kwargs):
        self.value = self.unit_price * self.current_stock
        super().save(*args, **kwargs)
    
    
    @property
    def stock_status(self):
        if self.quantity <= 0:
            return 'Out of Stock'
        elif self.quantity <= self.reorder_level:
            return 'Low Stock'
        return 'In Stock'


class Item(models.Model):
    class Category(models.TextChoices):
        ELECTRONICS = 'Electronics', _('Electronics')
        CLOTHING = 'Clothing', _('Clothing')
        FOOD = 'Food', _('Food Items')
        OTHER = 'Other', _('Other')

    product_name = models.CharField(max_length=200)
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.OTHER
    )
    description = models.TextField(blank=True)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    reorder_level = models.PositiveIntegerField()
    supplier = models.CharField(max_length=200, blank=True)
    sku = models.CharField(max_length=50, unique=True, blank=True, null=True)
    product_image = models.ImageField(upload_to='products/', blank=True, null=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.product_name

    @property
    def stock_status(self):
        if self.quantity <= 0:
            return 'Out of Stock'
        elif self.quantity <= self.reorder_level:
            return 'Low Stock'
        return 'In Stock'
    


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', _('Pending')
        PROCESSING = 'processing', _('Processing')
        COMPLETED = 'completed', _('Completed')
        CANCELLED = 'cancelled', _('Cancelled')

    customer_name = models.CharField(max_length=200)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    payment_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', _('Pending')),
            ('paid', _('Paid')),
            ('failed', _('Failed')),
        ],
        default='pending'
    )
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='processed_orders')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_orders')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)  # Allow null and blank
    quantity = models.IntegerField()
    price_at_time_of_order = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.product_name if self.product else 'Unknown Product'} - {self.quantity} units"

class Payment(models.Model):
    class PaymentMethod(models.TextChoices):
        CASH = 'cash', _('Cash')
        CARD = 'card', _('Credit/Debit Card')
        UPI = 'upi', _('UPI')
        NETBANKING = 'netbanking', _('Net Banking')

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices)
    transaction_id = models.CharField(max_length=100, unique=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('success', _('Success')),
            ('failed', _('Failed')),
            ('pending', _('Pending')),
        ],
        default='pending'
    )
    card_number = models.CharField(max_length=16, null=True, blank=True)
    upi_id = models.CharField(max_length=50, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Payment for Order #{self.order.id} - {self.amount}"

    def save(self, *args, **kwargs):
        if not self.transaction_id:
            import uuid
            self.transaction_id = str(uuid.uuid4())
        super().save(*args, **kwargs)

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

class Forecast(models.Model):
    category = models.CharField(max_length=100)
    forecast_date = models.DateField()
    predicted_value = models.FloatField()
    actual_value = models.FloatField(null=True, blank=True)
    confidence_level = models.FloatField(null=True, blank=True)
