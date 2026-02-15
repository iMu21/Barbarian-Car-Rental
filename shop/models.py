import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


class SuperCategory(models.Model):
    superCategory_name = models.CharField(max_length=30, default="")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name_plural = "Super Categories"

    def __str__(self):
        return self.superCategory_name


class Category(models.Model):
    category_name = models.CharField(max_length=30, default="")
    superCategory_name = models.ForeignKey(
        'SuperCategory',
        on_delete=models.SET_DEFAULT,
        default=""
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category_name


class Car(models.Model):
    car_name = models.CharField(max_length=50, default="")
    car_category = models.ForeignKey(
        'Category',
        on_delete=models.SET_DEFAULT,
        default=""
    )
    car_driverRate = models.IntegerField(default=0)
    car_hourRate = models.IntegerField(default=0)
    car_deliveryRate = models.IntegerField(default=0)
    car_capacity = models.IntegerField(default=0)
    car_quantity = models.IntegerField(default=0)
    car_image = models.ImageField(upload_to='shop/images', default="")
    is_featured = models.BooleanField(default=False)
    featured_tagline = models.CharField(max_length=100, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.car_name

    def average_rating(self):
        reviews = self.review_set.all()
        if not reviews.exists():
            return 0
        return round(reviews.aggregate(models.Avg('rating'))['rating__avg'], 1)

    def review_count(self):
        return self.review_set.count()


class Coupon(models.Model):
    DISCOUNT_TYPE_CHOICES = [
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    ]

    code = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=200, blank=True, default="")
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES, default='percentage')
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    max_discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    min_order_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    max_uses = models.IntegerField(default=0)
    current_uses = models.IntegerField(default=0)
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} ({self.get_discount_type_display()})"

    @property
    def is_valid(self):
        now = timezone.now()
        if not self.is_active:
            return False
        if now < self.valid_from or now > self.valid_until:
            return False
        if self.max_uses > 0 and self.current_uses >= self.max_uses:
            return False
        return True

    def calculate_discount(self, order_total):
        if not self.is_valid:
            return 0
        if order_total < self.min_order_amount:
            return 0
        if self.discount_type == 'percentage':
            discount = order_total * self.discount_value / 100
            if self.max_discount:
                discount = min(discount, self.max_discount)
        else:
            discount = min(self.discount_value, order_total)
        return round(discount, 2)


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    booking_number = models.CharField(max_length=20, unique=True, editable=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='bookings')
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)

    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_mobile = models.CharField(max_length=20)
    customer_address = models.CharField(max_length=200)

    rental_hours = models.IntegerField(validators=[MinValueValidator(1)])
    car_quantity = models.IntegerField(validators=[MinValueValidator(1)])
    include_driver = models.BooleanField(default=False)
    delivery_date = models.DateField()
    delivery_time = models.TimeField()

    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    driver_rate = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_rate = models.DecimalField(max_digits=10, decimal_places=2)

    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    driver_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    delivery_cost = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)

    admin_notes = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.booking_number} — {self.car.car_name}"

    def save(self, *args, **kwargs):
        if not self.booking_number:
            self.booking_number = f"BCR-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='review_set')
    booking = models.OneToOneField(Booking, on_delete=models.SET_NULL, null=True, blank=True)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(max_length=1000, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'car')

    def __str__(self):
        return f"{self.user.username} — {self.car.car_name} ({self.rating}/5)"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='favorites')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'car')

    def __str__(self):
        return f"{self.user.username} — {self.car.car_name}"
