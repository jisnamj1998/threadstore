from django.shortcuts import render,redirect

from store.forms import SignUpForm,SignInForm

from django.views.generic import View

from django.contrib.auth.models import User

from django.contrib.auth import authenticate,login,logout

from store.models import Product,Size,Basket,BasketItem,Order

# Create your views here.

class RegistrationView(View):

    def get(self,request,*args,**kwargs):

        form_instance=SignUpForm()

        return render(request,"register.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=SignUpForm(request.POST)

        if form_instance.is_valid():

            form_instance.save()

            # data=form_instance.cleaned_data

            # User.objects.create_user(**data)

            print("registration successful")

            return redirect("signin")
        
        return render(request,"register.html",{"form":form_instance})
    
class LoginView(View):

    def get(self,request,*args,**kwargs):

        form_instance=SignInForm()

        return render(request,"login.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=SignInForm(request.POST)

        if form_instance.is_valid():

            data=form_instance.cleaned_data

            uname=data.get("username")

            pwd=data.get("password")

            user_object=authenticate(request,username=uname,password=pwd)

            print(user_object)

            if user_object:

                login(request,user_object)

                print("logined successfully")

                return redirect("index")
            
        print("login failed")

        return render(request,"login.html",{"form":form_instance})    
    

class IndexView(View):

    def get(self,request,*args,**kwargs):

        qs=Product.objects.all()

        return render(request,"index.html",{"data":qs})   


class ProductDetailView(View):

    def get(self,request,*args,**kwargs):

        # to get id from url
        id=kwargs.get("pk")

        qs=Product.objects.get(id=id)

        return render(request,"product_detail.html",{"data":qs})
    
class AddToCartView(View):

    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        product_obj=Product.objects.get(id=id)

        size_name=request.POST.get("size")

        size_obj=Size.objects.get(name=size_name)

        qty=request.POST.get("qty")

        #basket_obj=Basket.objects.get(owner=request.user)

        basket_obj=request.user.cart

        basket_item_obj=BasketItem.objects.filter(basket_object=basket_obj,product_object=product_obj,size_object=size_obj,is_order_placed=False)

        if basket_item_obj:

            basket_item_obj[0].quantity+=int(qty)

            basket_item_obj[0].save()

        else:



            BasketItem.objects.create(

                basket_object=basket_obj,
                size_object=size_obj,
                product_object=product_obj,
                quantity=qty
             )
        print("product added to cart")
        

        return redirect("index")    
    
class CartSummaryView(View):

    def get(self,request,*args,**kwargs):

        qs=request.user.cart.cartitems.filter(is_order_placed=False).order_by("-created_date")

        return render(request,"cart_list.html",{"data":qs}) 


class CartDestroyView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        BasketItem.objects.get(id=id).delete()

        return redirect("cart-summary")
    
class LogoutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect("signin")
    
class CartQuanityUpdateView(View):

    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        basket_item_obj=BasketItem.objects.get(id=id)

        action=request.POST.get("action")

        if action=="increment":

            basket_item_obj.quantity+=1

        else:

            basket_item_obj.quantity-=1

        basket_item_obj.save()        

        print(action)

        return redirect("cart-summary")  


class PlaceOrderView(View):

    def get(self,request,*args,**kwargs):

        return render(request,"place_order.html")
    
    def post(self,request,*args,**kwargs):

        email=request.POST.get("email")

        phone=request.POST.get("phone")

        address=request.POST.get("address")

        pin=request.POST.get("pin")

        payment_mode=request.POST.get("payment_mode")

        cart_item_objects=request.user.cart.cartitems.filter(is_order_placed=False)
        
        user_obj=request.user

        if payment_mode=="cod":

            order_obj=Order.objects.create(
                   user_object=user_obj,
                   delivery_address=address,
                   phone=phone,
                   pin=pin,
                   email=email,
                   payment_mode=payment_mode

            )

            for bi in cart_item_objects:

                order_obj.basket_item_objects.add(bi)

                bi.is_order_placed=True
                
                bi.save()

            order_obj.save()    

        return redirect("index")
    
class OrderSummaryView(View):

    def get(self,request,*args,**kwargs):

        qs=Order.objects.filter(user_object=request.user).order_by("-created_date")    

        return render(request,"order_summary.html",{"data":qs})
    





    

                













            
                
                    
