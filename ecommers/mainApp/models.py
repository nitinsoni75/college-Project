
from django.db import models
import datetime

from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin

from .managers import CustomerUserManager

# Create your models here.


CAT_CHOISES = ( ("Electronics",'Electroincs'),

               ("Vegitables",'Vegitables'),
               
               ("Womens Clouthes",'Women Clouthes'),

               ("Mens Clouthes",'Mens Clouthes'),

               ("Toys",'Toys')

)

CAT_TYPE_CHOISES = (

                ("/Piece",'/Piece'),
                ("/kg",'/kg'),
                ("/Packet",'/Packet'),

)



class User(AbstractBaseUser,PermissionsMixin):

    name = models.CharField(max_length=100)
    email = models.EmailField(_('email address'),unique = True)
    phone = models.CharField(max_length=10)
    status=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_active =models.BooleanField(default=True)
    country = models.CharField(max_length=20, null=True, blank=True)
    state=models.CharField(default= None,max_length=20,null=True, blank=True)
    city=models.CharField(max_length=20,default=None,null=True, blank=True)
    landmark = models.CharField(max_length=30, null=True, default=None, blank=True)
    road = models.CharField(max_length=50, null=True, default=None, blank=True)
    place=models.CharField(max_length=50, blank=True,null=True,default=None)
    pin=models.IntegerField(null=True,default=None, blank=True)


    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['name','phone']

    objects = CustomerUserManager()




# for product

class Product(models.Model):

    product_name = models.CharField(max_length=50)
    product_title = models.TextField(max_length=300)
    category = models.CharField(choices=CAT_CHOISES,max_length=20)

    quantity_type = models.CharField(choices=CAT_TYPE_CHOISES,max_length=20)
    price = models.BigIntegerField()
    offer = models.IntegerField()

    pro_images = models.ImageField(upload_to='pro_images',max_length = 500)

    total = models.IntegerField()
    avaliable = models.IntegerField()

    def __str__(self):

        return self.product_name

    

# for ordering details

class Order(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()
    total_price = models.FloatField()
    order_date = models.DateField(default=datetime.date.today())
    order_time = models.TimeField(default=datetime.datetime.now())
    status = models.BooleanField(default=False)
    order_address = models.TextField(max_length=100) 
    def __str__(self):

        p = str(self.user)+" | "+str(self.product)

        return p
