from django.contrib import admin
from .models import Car, Category, SuperCategory, Booking, Review, Favorite, Coupon


class CategoryInline(admin.TabularInline):
    model = Category
    extra = 1


@admin.register(SuperCategory)
class SuperCategoryAdmin(admin.ModelAdmin):
    list_display = ('superCategory_name', 'created_at')
    search_fields = ('superCategory_name',)
    inlines = [CategoryInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'superCategory_name', 'created_at')
    list_filter = ('superCategory_name',)
    search_fields = ('category_name',)


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('car_name', 'car_category', 'car_hourRate', 'car_deliveryRate', 'car_capacity', 'car_quantity', 'is_featured')
    list_filter = ('car_category', 'car_category__superCategory_name', 'is_featured')
    search_fields = ('car_name',)
    list_editable = ('car_hourRate', 'car_deliveryRate', 'car_quantity', 'is_featured')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_number', 'car', 'customer_name', 'status', 'total_cost', 'created_at')
    list_filter = ('status', 'created_at', 'include_driver')
    search_fields = ('booking_number', 'customer_name', 'customer_email')
    readonly_fields = ('booking_number', 'created_at', 'updated_at')
    list_editable = ('status',)
    fieldsets = (
        ('Booking Info', {
            'fields': ('booking_number', 'status', 'user', 'car', 'coupon')
        }),
        ('Customer Info', {
            'fields': ('customer_name', 'customer_email', 'customer_mobile', 'customer_address')
        }),
        ('Rental Details', {
            'fields': ('rental_hours', 'car_quantity', 'include_driver', 'delivery_date', 'delivery_time')
        }),
        ('Price Snapshot', {
            'fields': ('hourly_rate', 'driver_rate', 'delivery_rate')
        }),
        ('Cost Breakdown', {
            'fields': ('subtotal', 'driver_cost', 'delivery_cost', 'discount_amount', 'total_cost')
        }),
        ('Admin', {
            'fields': ('admin_notes', 'created_at', 'updated_at')
        }),
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'car', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'car__car_name', 'comment')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'car', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'car__car_name')


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_type', 'discount_value', 'is_active', 'current_uses', 'max_uses', 'valid_until')
    list_filter = ('discount_type', 'is_active')
    search_fields = ('code', 'description')
    list_editable = ('is_active',)
