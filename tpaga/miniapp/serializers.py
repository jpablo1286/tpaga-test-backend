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
    itemId = ItemSerializer()
    class Meta:
        model = purchasedItem
        fields = ('id','orderId','itemId','quantity','cost')
