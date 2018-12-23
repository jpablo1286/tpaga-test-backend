from django.shortcuts import render
import requests
import datetime
import json
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from miniapp.models import item
from miniapp.serializers import ItemSerializer
from miniapp.models import order
from miniapp.serializers import OrderSerializer
from miniapp.models import purchasedItem
from miniapp.serializers import PurchasedItemSerializer
from miniapp.serializers import PurchasedItemCreateSerializer
from miniapp.models import Keys
from miniapp.serializers import KeysSerializer


class CreateKey(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        data = JSONParser().parse(request)
        serializer = KeysSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        message = {'error': 'Los campos suministrados no son validos'}
        return Response(message,status=400)

class ListItems(APIView):

    def get(self, request):
        items = item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

class CreateItems(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = ItemSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        message = {'error': 'Los campos suministrados no son validos'}
        return Response(message,status=400)

class ListOrders(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        orders = order.objects.all()
        serializer = ItemSerializer(orders, many=True)
        return Response(serializer.data)

class InfoOrder(APIView):
    def get(self, request, id):
        try:
            myorder = order.objects.get(id=id)
        except order.DoesNotExist:
            message = {'error': 'La orden no existe'}
            return Response(message,status=404)
        serializer = OrderSerializer(myorder)
        return Response(serializer.data)
class CreateOrder(APIView):
    def post(self, request):
        data = JSONParser().parse(request)
        serializer = OrderSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        message = {'error': 'Los campos suministrados no son validos'}
        return Response(message,status=400)

class CheckOutOrder(APIView):

    def post(self, request, id):
        try:
            myorder = order.objects.get(id=id)
        except order.DoesNotExist:
            message = {'error': 'La orden no existe'}
            return Response(message,status=404)
        serializer = OrderSerializer(myorder)
        if serializer.data['status'] != "new":
            message = {'error': 'La orden ya ha sido procesada'}
            return Response(message,status=400)
        key = Keys.objects.first()
        url = 'https://stag.wallet.tpaga.co/merchants/api/v1/payment_requests/create'
        auth = "Basic %s"%(key.key)
        expDate = datetime.datetime.utcnow() + timedelta(days=1)
        expDateForm = expDate.strftime('%Y-%m-%dT%H:%M:%S.%f-05:00')[:-3]
        headers = {"Authorization": auth, "Cache-Control":"no-cache", "Content-Type":"application/json"}
        data = {
        "cost":serializer.data['cost'],
        "purchase_details_url":"https://www.juanrivera.org/",
        "voucher_url": "https://www.juanrivera.org/",
        "idempotency_token":serializer.data['iToken'],
        "order_id":serializer.data['id'],
        "terminal_id":"web_app",
        "purchase_description":"Compra en miniapp store",
        "user_ip_address": request.META.get('REMOTE_ADDR'),
        "expires_at": expDateForm
        }
        myResult=requests.post(url, json=data, headers=headers)
        myJsonResult=json.loads(myResult.text)
        if 'error_code' in myJsonResult:
            return Response(myJsonResult,status=400)
        updatedSerializer = OrderSerializer(myorder, data=serializer.data)
        if updatedSerializer.is_valid():
            updatedSerializer.save(token= myJsonResult['token'],tpagaPaymentUrl=myJsonResult['tpaga_payment_url'],status=myJsonResult['status'],expiresAt=myJsonResult['expires_at'])
            return Response(updatedSerializer.data)
        message = {'error': 'Error al procesar'}
        return Response(message,status=400)

class CreatePurchasedItem(APIView):
    def post(self, request):
        data = JSONParser().parse(request)
        serializer = PurchasedItemCreateSerializer(data=data)
        if serializer.is_valid():
            myOrder = order.objects.get(id=data['orderId'])
            myOrder.cost = myOrder.cost + int(data['cost'])
            myOrder.save()
            serializer.save()
            return Response(serializer.data)
        message = {'error': 'Los campos suministrados no son validos'}
        return Response(message,status=400)

class DeletePurchasedItem(APIView):
    def delete(self, request, itemId):
        try:
            myPurchasedItem = purchasedItem.objects.get(id=itemId)
        except purchasedItem.DoesNotExist:
            message = {'error': 'El item no existe'}
            return Response(message,status=404)
        serializer = PurchasedItemCreateSerializer(myPurchasedItem)
        myOrder = order.objects.get(id=serializer.data['orderId'])
        myOrder.cost = myOrder.cost - int(serializer.data['cost'])
        myOrder.save()
        myPurchasedItem.delete()
        message = {'info': 'Item eliminado con exito'}
        return Response(message,status=200)

class ListPurchasedItemsByOrderId(APIView):
    def get(self, request, orderId):
        try:
            #myPurchasedItems = purchasedItem.objects.get(orderId=orderId)
            myPurchasedItems=purchasedItem.objects.filter(orderId=orderId)
        except purchasedItem.DoesNotExist:
            message = {'error': 'La orden no existe'}
            return Response(message,status=404)
        serializer = PurchasedItemSerializer(myPurchasedItems,many=True)
        return Response(serializer.data)

class AdminView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Solo Admin!'}
        return Response(content)
