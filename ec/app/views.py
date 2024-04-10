from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import logout
from django.views import View
from . models import *
# import razorpay
from django.db.models import Count,Q
from . forms import *
from django.conf import settings
from django.http import request,JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.
@login_required
def home(request):
    totalitem=0
    wishlist=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishlist=len(Wishlist.objects.filter(user=request.user))
    return render(request,'app/home.html',locals())
#######################################
@login_required
def about(request):
    totalitem=0
    wishlist=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishlist=len(Wishlist.objects.filter(user=request.user))
    return render(request,'app/about.html',locals())
#######################################
@login_required
def contact(request):
    totalitem=0
    wishlist=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishlist=len(Wishlist.objects.filter(user=request.user))
    return render(request,'app/contact.html',locals())
#######################################
@method_decorator(login_required,name='dispatch')
class categoryview(View):
    def get(self,request,val):
        totalitem=0
        wishlist=0
        if request.user.is_authenticated:
            wishlist=len(Wishlist.objects.filter(user=request.user))
            totalitem=len(Cart.objects.filter(user=request.user))
        product=Product.objects.filter(category=val)
        title=Product.objects.filter(category=val).values('title')
        return render(request,'app/category.html',locals())
#######################################
@method_decorator(login_required,name='dispatch')
class  categorytitle(View):
    def get(self,request,val):
        product=Product.objects.filter(title=val)
        title=Product.objects.filter(category=product[0].category).values('title')
        totalitem=0
        wishlist=0
        if request.user.is_authenticated:
            wishlist=len(Wishlist.objects.filter(user=request.user))
            totalitem=len(Cart.objects.filter(user=request.user))
        return render(request,'app/category.html',locals())   
#######################################
@login_required
def show_wishlist(request):
    user = request.user
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len (Wishlist.objects.filter(user=request.user))
    product = Wishlist.objects.filter(user=user)
    return render(request, "app/wishlist.html", locals())

class custeomerregisterionview(View):
    def get(self, request):
        form = CusteomerRegisterionForm()
        totalitem=0
        wishlist=0
        if request.user.is_authenticated:
            wishlist=len(Wishlist.objects.filter(user=request.user))
            totalitem=len(Cart.objects.filter(user=request.user))
        return render(request, 'app/custeomerregisterionform.html', locals())
    def post(self, request):
        form = CusteomerRegisterionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Congratulations! User Register successfully")
          
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request, 'app/custeomerregisterionform.html', locals())
#######################################
@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        form=CustomerProfileForm()
        totalitem=0
        wishlist=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishlist=len(Wishlist.objects.filter(user=request.user))
        return render(request,'app/profile.html',locals())
    def post(self,request):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            user=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            mobile=form.cleaned_data['mobile']
            zipcode=form.cleaned_data['zipcode']
            state=form.cleaned_data['state']
            reg=Customer(user=user,name=name,locality=locality,mobile=mobile,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,"Congratulations! User Register successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request,'app/profile.html',locals()) 
#######################################
@login_required
def address(request):
    totalitem=0
    wishlist=0
    if request.user.is_authenticated:
        wishlist=len(Wishlist.objects.filter(user=request.user))
        totalitem=len(Cart.objects.filter(user=request.user))
    add=Customer.objects.filter(user=request.user)
    return render(request,'app/address.html',locals())
#######################################
@method_decorator(login_required,name='dispatch')
class updateAddress(View):
    def get(self,request,pk):
        add=Customer.objects.get(pk=pk)
        form=CustomerProfileForm(instance=add)
        totalitem=0
        wishlist=0
        if request.user.is_authenticated:
            wishlist=len(Wishlist.objects.filter(user=request.user))  
            totalitem=len(Cart.objects.filter(user=request.user))
        return render(request,'app/updateaddress.html',locals())
    def post(self,request,pk):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            add=Customer.objects.get(pk=pk)
            add.name=form.cleaned_data['name']
            add.locality=form.cleaned_data['locality']
            add.city=form.cleaned_data['city']
            add.mobile=form.cleaned_data['mobile']
            add.zipcode=form.cleaned_data['zipcode']
            add.state=form.cleaned_data['state']
            add.save()
            messages.success(request,"Congratulations! User Register successfully")
        
        else:
            messages.warning(request,"Invalid Input Data")
        return redirect("address")

def custom_logout(request):
    logout(request)
    return redirect('login') 
@login_required
def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
   
    return redirect("/cart")
@login_required
def show_cart(request):
    user=request.user
    cart=Cart.objects.filter(user=user)
    amount=0
    for p in cart:
        value=p.quantity*p.product.discounted_price
        amount=amount+value
    totalamount=amount+40
    wishlist=0
    totalitem=0
    if request.user.is_authenticated:
        wishlist=len(Wishlist.objects.filter(user=request.user))
        totalitem=len(Cart.objects.filter(user=request.user))
    return render(request,'app/addtocart.html',locals())


@method_decorator(login_required,name='dispatch')   
class checkout(View):
    def get(self,request):
        wishlist=0
        totalitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishlist=len(Wishlist.objects.filter(user=request.user))
        user=request.user
        add=Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        famount=0
        for p in cart_items:
            value=p.quantity * p.product.discounted_price
            famount=famount+value
        totalamount=famount+40 
        # razoramount= int(totalamount * 100)
        # client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        # data={ "amount":razoramount,"currency":"INR","receipt":"order_recptid_12"}
        # payment_response=client.order.create(data=data)
        # print(payment_response)
        return render(request,'app/checkout.html',locals())


@login_required
def orders (request):
    totalitem=0
    wishlist=0
    if request.user.is_authenticated:
        wishlist=len(Wishlist.objects.filter(user=request.user))
        totalitem=len(Cart.objects.filter(user=request.user))
    order_placed=OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',locals())



def plus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        # print(prod_id)
        carts = Cart.objects.get(Q(product=prod_id)&Q( user=request.user))
        c=carts
        c.quantity+=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
           value = p.quantity * p.product.discounted_price
           amount = amount + value
        totalamount = amount + 40
        data={
                'quantity':c.quantity,
                'amount': amount,
                'totalamount': totalamount}
        
        return JsonResponse(data)




def minus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        carts = Cart.objects.get(Q(product=prod_id)&Q( user=request.user))
        c=carts
        c.quantity-=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data={
            'quantity':c.quantity,
            'amount': amount,
            'totalamount': totalamount}
        return JsonResponse(data)




def remove_cart(request):
    if request.method == 'GET':
            prod_id=request.GET['prod_id']
            carts = Cart.objects.get(Q(product=prod_id)&Q( user=request.user))
            c=carts
            c.delete()
            user = request.user
            cart = Cart.objects.filter(user=user)
            amount = 0
            for p in cart:
                value = p.quantity * p.product.discounted_price
                amount = amount + value
            totalamount = amount + 40
            data={
            'amount': amount,
            'totalamount': totalamount}
            return JsonResponse(data)



def plus_wishlist(request):
    if request.method == 'GET':
        print(request.GET)
        prod_id=1
        product=Product.objects.get(id=prod_id)
        user=request.user
        Wishlist(user=user,product=product).save()
        data={
        'message': 'Wishlist Added Successfully',
         
        }
        return JsonResponse(data)
    
def  minus_wishlist(request):
    if request.method == 'GET':
        prod_id=1
        print(request.GET)
        product=Product.objects.get(id=prod_id)
        user=request.user
        Wishlist.objects.filter(user=user, product=product).delete()
        data={
        'message': 'Wishlist Remove Successfully',
         
        }
        return JsonResponse(data)
@method_decorator(login_required,name='dispatch')
class ProductDetail(View):   
    def get(self,request,pk):
        product=Product.objects.get(pk=pk)
        wishlist=None
        ser= Wishlist.objects.all()
        for wi in ser:
            if wi.product==product and wi.user==request.user:
                wishlist=wi
                break
        totalitem=0
        wishlist=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishlist=len(Wishlist.objects.filter(user=request.user))
        return render(request,'app/productdetail.html',locals())

@login_required
def search(request):
    query = request.GET['search']
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    product = Product.objects.filter(Q(title__icontains=query))
    return render(request, "app/search.html", locals())