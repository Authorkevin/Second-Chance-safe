from django.contrib import admin
from .models import Order, OrderItem, Category, Item

admin.site.register(Item)
admin.site.register(Category)

class OrderItemInline(admin.TabularInline):  # To display OrderItems within Order admin
    model = OrderItem
    extra = 1  # How many empty forms to display

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'total_price', 'created_at', 'order_status']  # Display these fields in the list view
    list_filter = ['user', 'created_at', 'order_status']  # Add filters for these fields
    inlines = [OrderItemInline] # display order items
    search_fields = ['order_number', 'user__username']  # Enable search
    # Add a new field
    list_editable = ['order_status']
    fieldsets = (
        ('Order Details', {
            'fields': ('order_number','user', 'total_price', 'created_at', 'shipping_address', 'order_status')
        }),
    )
    readonly_fields = ('order_number', 'created_at', 'total_price')  # These fields are not editable
    
    # Add order status
    ORDER_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

