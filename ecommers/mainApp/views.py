from unicodedata import category
from django.http import HttpResponse
from django.shortcuts import render,redirect

from mainApp.models import Product,User,Order

from django.views import View

from mainApp.validations import mobileNumber_validate,email_validation,check_name

from django.contrib import messages

from django.contrib.auth import authenticate
from django.contrib.auth import login as loginUser

from django.core.paginator import Paginator




import datetime

# Create your views here.

def index(request):

    return render(request,'index.html')






# home 


class Home(View):

    category_data = Product.objects.filter(category="/Pies")

    data = Product.objects.all()

    category_data = Product.objects.raw('SELECT * FROM mainApp_product group by "category"')


    def get(self, request):

         if request.user.is_authenticated:

             itemIN_cart = request.session.get('cart')
            
             category = request.GET.get('category')
            
             if category:
                
                 category_wise = Product.objects.filter(category = 'category')
                
                 for i in self.category_data:
                     print(i.category)
                    
                 return render(request,'home.html',{'cart':itemIN_cart,'category_data':self.category_data,'data':category_wise})
            
             else:
                
                 return render(request,'home.html',{'cart':itemIN_cart,'category_data':self.category_data,'data':self.data})
            
         else:
            
             return HttpResponse(f''' <center style="color:red"> <h1>Yor are not authenticated....</h1><br><h4><a herf="/login"> Login First !<h4></center>''')
    
    
 
    def post(self,request):
        
        
        
         cart = request.session.get("cart")
        
         if request.method == "POST":
            
             product_id = request.POST.get('pid')
            
             if cart is not None:
                 if product_id in cart :
                      product_value = cart[product_id]
                    
                      cart[product_id] = product_value+1
                     
                     
                     
                 else:
                     
                      cart[product_id] = 1
             else:
                
                 cart = {}
                
                 cart[product_id] = 1  # by default first time 1 quantity insert with prouduct id
            
         request.session['cart'] = cart 
        
         return self.get(request)
                     
            
                
                
                
                
# froms 


def form(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            sname = request.POST.get("sname")
            email = request.POST.get("email")
            mobile = request.POST.get("mobile")
            password1 = request.POST.get("password1")
            password2 = request.POST.get("password2")
            if sname and email and mobile and password1 and password2:
                if password1 == password2:
                    if mobileNumber_validate(mobile):
                        if email_validation(email):
                            if check_name(sname):
                                check_usnique_mail = User.objects.filter(email=email)
                                if not check_usnique_mail:
                                    User.objects.create_user(email, password1, sname, mobile)
                                    messages.error(request, "Accounts has been created!")
                                else:
                                    messages.error(request, "Ragister with another email id!")

                            else:
                                messages.error(request, "name should be alphabatical form!")
                        else:
                            messages.error(request, "enter a vailed Email Id!")
                    else:
                        messages.error(request, "Mobile number should be 10 digit and digit form!")
                else:
                    messages.error(request, "password does not matched!")
            else:
                messages.error(request, "fill required field!")
        return render(request, 'index.html')
    else:
        return redirect("/home")


# login



def login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            email = request.POST.get('email')
            password = request.POST.get('pass')
            print(email,password,"<this is user name and password")
            if email and password:
                if email_validation(email):
                    authenticated_user = authenticate(email=email, password=password)
                    if authenticated_user:
                        loginUser(request, authenticated_user)
                        return redirect("/home")
                    else:
                        messages.error(request, 'invailed creadientials!')
                else:
                    messages.error(request, "enter a valiled email!")
            else:
                messages.error(request, "fill required all fields!")
        return render(request, 'login.html')
    else:
        return redirect("/home")
    

# log out




def logout(request):
    request.session.clear()
    return redirect('/login')




# cart

def cart(request):
    if request.user.is_authenticated:
        error = False
        try:
            data = request.session.get('cart')
            data = (data.keys())
            list(data)
            data = Product.objects.filter(id__in=data).order_by("-id")
            print(data)
        except:
            error=("You Have Not any item in cart!")
  
        return render(request, 'cart.html', {'data': data,"error":error})
    else:
        return HttpResponse(f'''<center style="color:red"><h1>You'r not authinticated..<br><h4><a href="/login">Login First!''')



# order



def order(request, pid):
    if request.user.is_authenticated:
        user_data = User.objects.filter(email=request.user)
        data = Product.objects.filter(id=pid)
        cat_data = Product.objects.filter(category=data[0].category)
        cat_data=Paginator(cat_data,2)
        page_number=request.GET.get('page')
        page_obj=cat_data.get_page(page_number)

        print(request.POST.get('update'))
        if request.method == "POST" and request.POST.get("update")=="Update Address":
            country = request.POST.get("country")
            state = request.POST.get("state")
            city = request.POST.get("city")
            landmark = request.POST.get("landmark")
            road = request.POST.get("road")
            place = request.POST.get("place")
            pin = request.POST.get("pin")
            # print(cuntry,state,city,landmark,road,place,pin,"<----address data")
            if User.objects.filter(email=request.user).update(country=country, state=state,city=city,
                                                landmark=landmark,road=road, place=place, pin=pin):
                print('update succrssfuly....')
        elif request.method=="POST" and request.POST.get('confirm')=="Confirm Order":
            ord_address=request.POST.get("order_address")
            print(ord_address,'<--this is order address')
            quantity=request.POST.get('quantity')
            product_obj=Product.objects.get(id=pid)
            print(product_obj,"<---product object")
            date=datetime.date.today()
            try:
                if int(quantity)>=1 and data[0].avaliable >= int(quantity):
                    try:
                        Product.objects.filter(id=pid).update(avaliable=data[0].avaliable - int(quantity))

                        total_price = int(data[0].price) * int(quantity)
                        print(data[0].price)
                        print(total_price,'<-Total prize')
                        a=Order.objects.create(user=request.user, product=product_obj,
                                                 quantity=quantity, price=data[0].price,
                                                 total_price=total_price,order_address=ord_address)
                        if a:
                            get_cart_value = request.session.get('cart')
                            try:
                                del(get_cart_value[str(pid)])
                                # print(get_cart_value, "<- before this is order cart")

                                request.session['cart']=get_cart_value
                                # print(get_cart_value,"<-after this is order cart")
                                messages.success(request,'Order successful.....!')
                            except:
                                
                                messages.success(request, 'Order successful.....!')
                    except:
                        print("Somthing went wrong during Order!")


                else:
                    messages.error(request, "Product not available as your quantity!")
            except:
                messages.error(request,"Add product quantity as you want to order!")

        return render(request, 'all_order.html', {'data': data,"user_data":user_data,'page_obj':page_obj})
    else:
        return HttpResponse(f'''<center style="color:red"><h1>You are not authinticated..<br><h1><a href="/login">Login First!</a>''')








# my order


def myorder(request):
    if request.user.is_authenticated:
        user=request.user
        try:
            user_order=Order.objects.select_related('product').filter(user=user).order_by('-id')
            print(user_order)
        except Exception as e:
            print(e)
            raise("Something went wrong!")
        return render(request,"myorder.html",{'user_order':user_order})
    else:


        return HttpResponse(
            f'''<center style="color:red"><h1>You'r not authinticated..<br><h4><a href="/login">Login First!''')

# delete cart



def delete_cart(request,pid):
    if pid is not None:
        cart=request.session.get("cart")
        print(cart,"<before")
        del cart[str(pid)]
        request.session['cart']=cart
    return redirect('/cart')