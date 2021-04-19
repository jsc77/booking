from django.db import models
from django.contrib.auth.models import User
from django import forms
from datetime import datetime
from django.contrib.auth.models import User

class Student(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/Student/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    def __str__(self):
        return f"{self.user}"

Q1 = (
    ('要介護4～5','要介護4～5'),
    ('要介護3','要介護３'),
    ('要介護1～2','要介護1～2'),
    ('いいえ','いいえ')
)
Q2 = (
    ('一人暮らし','一人暮らし'),
    ('夫婦','夫婦'),
    ('若い家族いる（仕事あり）','若い家族いる（仕事あり）'),
    ('若い家族いる（仕事なし）','若い家族いる（仕事なし）')
)

class Question(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE, default=1)
    question1 = models.CharField(choices=Q1, max_length=100, default=1)
    question2 = models.CharField(choices=Q2, max_length=100, default=1)
    date = models.DateTimeField(default=datetime.now, blank=True)


class Book(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateField(max_length=50)
    time = models.TimeField(max_length=50)
    facility = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.user}様の{self.date}/{self.time}の予約"
    class Meta:
        ordering = ['date','time']

# Create your models here.
CATEGORY_CHOICES = (
    ('C','車椅子'),
    ('W','歩行器'),
    ('M','マットレス')

)
LABEL_CHOICES = (
    ('新製品','新製品'),
    ('人気','人気'),
)

BOOT_CHOICES = (
    ('warning', 'warning'),
    ('danger', 'danger'),
)

class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    discount_price = models.IntegerField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=10)
    label = models.CharField(choices=LABEL_CHOICES, max_length=10)
    boot = models.CharField(choices=BOOT_CHOICES, max_length=10)
    slug = models.SlugField()
    description = models.TextField()
    quantity = models.IntegerField(default=1)
    image = models.ImageField(null=True, blank=True, upload_to="image/")


    # def get_absolute_url(self):
    #     return reverse('product', kwargs={
    #         'slug': self.slug,
    #     })
    
    # def get_add_to_cart_url(self):
    #     return reverse("add-to-cart", kwargs={
    #         'slug': self.slug,
    #     })

    # def get_remove_from_cart_url(self):
    #     return reverse("remove-from-cart", kwargs={
    #         'slug': self.slug,
    #     })

class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.item.title} - {self.quantity}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    # billing_address = models.ForeignKey('BillingAddress', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total =0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total
