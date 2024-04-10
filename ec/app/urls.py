from django.contrib import admin
from django.contrib.auth import views as auth_view
from django.contrib.auth.views import LogoutView
from django.urls import path,include
from . import views
from .views import *
from . forms import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',views.home),
    path('about/',views.about,name="about"),
    path('contact/',views.contact,name="contact"),
    path('category/<slug:val>',views.categoryview.as_view(),name="category"),
    path('category-title/<val>',views.categorytitle.as_view(),name="category-title"),
    path('product-detail/<int:pk>',views.ProductDetail.as_view(),name="product-detail"),
    path('pluswishlist/', views.plus_wishlist),
    path('minuswishlist/', views.minus_wishlist),
    path('profile/',views.ProfileView.as_view(),name='profile'),
    path('address/',views.address,name='address'),
    path('pluscart/',views.plus_cart),
    path('minuscart/',views.minus_cart),
    path('removecart/',views.remove_cart),
    path('orders/',views.orders,name="orders"),
    path('registerion/',views.custeomerregisterionview.as_view(),name="custeomerregisterionform"),
    path('accounts/login/',auth_view.LoginView.as_view(template_name='app/login.html',authentication_form=LoginForm),name="login"),
    path('updateaddress/<int:pk>',views.updateAddress.as_view(),name="updateAddress"),
    path('passwordchange/',auth_view.PasswordChangeView.as_view(template_name='app/changepassword.html',form_class=MyPasawordChangeForm,success_url='/passwordchangedone'),name='passwordchange'),
    path('passwordchangedone/',auth_view.PasswordChangeDoneView.as_view(template_name='app/passwordchangeDone.html'),name='passwordchangedone'),
    path('custom-logout/', views.custom_logout, name='custom_logout'),
    path('add-to-cart/',views.add_to_cart,name='add-to-cart'),
    path('cart/',views.show_cart,name='showcart'),
    path('checkout/',views.checkout.as_view(),name='checkout'),
    path('search/',views.search,name="search"),
    path("wishlist/",views.show_wishlist,name="wishlist"),
    path('password-reset/',auth_view.PasswordResetView.as_view(template_name='app/password_reset.html',form_class=MyPasswordResetForm),name="password_reset"),
    path('password-reset/done/',auth_view.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'),name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/',auth_view.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html',form_class=MySetPasswordForm),name="password_reset_confirm"),
    path('password-reset-complete/',auth_view.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'),name="password_reset_complete"),
    
    
   ]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


admin.site.site_header = "Neel Dairy"
admin.site.site_title = "Neel Dairy"
admin.site.site_index_title = "Welcome to Neel Dairy Shop"