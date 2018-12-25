"""
Author: Juan Pablo Rivera Velasco
Version: 1.0
Correo: jpablo.localhost@gmail.com

Se escribe los modelos a partir del diseño de base de datos, se especifican tipos de datos y relaciones entre tablas.
"""
from django.db import models

class Keys(models.Model):
    id = models.AutoField(primary_key=True)
    key = models.CharField(max_length=250)
class item(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    imgUrl = models.CharField(max_length=250)
    description = models.CharField(max_length=500)
    price = models.IntegerField()
class order(models.Model):
    id = models.AutoField(primary_key=True)
    iToken = models.CharField(null=True,max_length=500)
    expiresAt = models.CharField(null=True,max_length=250)
    token = models.CharField(null=True,max_length=500)
    tpagaPaymentUrl = models.CharField(null=True,max_length=250)
    status = models.CharField(max_length=80)
    customerEmail = models.CharField(max_length=250)
    cost = models.IntegerField()

class purchasedItem(models.Model):
    id = models.AutoField(primary_key=True)
    orderId = models.ForeignKey(order,on_delete=models.CASCADE)
    itemId = models.ForeignKey(item,null=True,on_delete=models.SET_NULL,related_name='items', related_query_name="item")
    quantity = models.IntegerField()
    cost = models.IntegerField()
