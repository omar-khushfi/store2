from django.contrib import admin
from . models import *
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.auth.models import Group
# Register your models here.
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Cart)
admin.site.register(Payment)
admin.site.register(OrderPlaced)
admin.site.register(Wishlist)
admin.site.unregister(Group)
class ProductModelAdmin(admin.ModelAdmin):
    list_display=['id','title','discounted_price','category','prodapp_image'] 

class CustomerModelAdmin(admin.ModelAdmin):
    list_display=['id','user','locality','city','state','zipcode']   


class CartModelAdmin(admin.ModelAdmin):
    list_display=['id','user','product','quantity']   
    def products (self, obj):
       link = reverse("admin: app_product_change", args=[obj.product.pk]) 
       return format_html('<a href="{}">{}</a>', link, obj.product.title)

class PaymentModelAdmin(admin.ModelAdmin):
    list_display=['id','user','amount',' razorpay_order_id','razorpay_payment_status','razorpay_payment_id','paid'] 



class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display=['id','user','customer','product','quantity','ordered_data','status','payment'] 
    def customers (self, obj):
        link=reverse('admin: app_customer_change', args=[obj.customer.pk]) 
        return format_html('<a href="{}">{}</a>',link, obj.customer.name)




class WishlistModelAdmin (admin. ModelAdmin):
    list_display= ['id', 'user', 'product']
    def products (self, obj):
       link= reverse("admin: app_product_change", args=[obj.product.pk])
       return format_html('<a href="{}">{}</a>', link, obj.product.title)