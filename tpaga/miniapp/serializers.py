"""
Author: Juan Pablo Rivera Velasco
Version: 1.0
Correo: jpablo.localhost@gmail.com

Se definen los serializadores que permiten interactuar con los modelos, y la representación de los mismos
"""
from rest_framework import serializers
#Importamos los modelos
from miniapp.models import Keys
from miniapp.models import item
from miniapp.models import order
from miniapp.models import purchasedItem

class KeysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keys
        fields = ('id','key')

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = item
        fields = ('id','name','imgUrl','description','price')

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = order
        fields = ('id','iToken','expiresAt','token','tpagaPaymentUrl','status','customerEmail','cost')

class PurchasedItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = purchasedItem
        fields = ('id','orderId','itemId','quantity','cost')

class PurchasedItemSerializer(serializers.ModelSerializer):
    itemId = ItemSerializer() # Se representa el campo itemId como objeto item
    class Meta:
        model = purchasedItem
        fields = ('id','orderId','itemId','quantity','cost')
