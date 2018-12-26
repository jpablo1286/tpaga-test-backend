"""
Author: Juan Pablo Rivera Velasco
Version: 1.0
Correo: jpablo.localhost@gmail.com

Se definene las vista (acciones) para el mini comercio
"""
from django.shortcuts import render
import requests
import datetime
import json
import hashlib
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

#Clase que permite a el administrador crear llavas para integrar con el gateway de pago (tpaga)
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
#Clases que definien las acciones sobre los items disponibles en el mini comercio
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

class DeleteItem(APIView):
    permission_classes = (IsAuthenticated,)
    def delete(self, request, itemId):
        try:
            myItem = item.objects.get(id=itemId)
        except item.DoesNotExist:
            message = {'error': 'El item no existe'}
            return Response(message,status=404)
        myItem.delete()
        message = {'info': 'Item eliminado con exito'}
        return Response(message,status=200)
# Clases que definen las acciones disponibles para las ordenes, aqui se ejecutan las acciones
# que permiten integrar el mini comercion con el gateway de pagos tpaga
class ListOrders(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        orders = order.objects.all()
        serializer = OrderSerializer(orders, many=True)
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
        mydate=datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f-05:00')[:-3]
        if serializer.is_valid():
            serializer.save(iToken=hashlib.md5(mydate.encode('utf-8')).hexdigest())
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
        orderUrl = "https://192.168.1.172:4200/orderconfirm/%s"%(serializer.data['id'])
        expDate = datetime.datetime.utcnow() + timedelta(days=1)
        expDateForm = expDate.strftime('%Y-%m-%dT%H:%M:%S.%f-05:00')[:-3]
        headers = {"Authorization": auth, "Cache-Control":"no-cache", "Content-Type":"application/json"}
        data = {
        "cost":serializer.data['cost'],
        "purchase_details_url":orderUrl,
        "voucher_url": orderUrl,
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
            message = {'orderId': id, 'status': myJsonResult['status'],'payment_url': myJsonResult['tpaga_payment_url']}
            return Response(message)
        message = {'error': 'Error al procesar'}
        return Response(message,status=400)

class ConfirmOrder(APIView):

    def post(self, request, id):
        try:
            myorder = order.objects.get(id=id)
        except order.DoesNotExist:
            message = {'error': 'La orden no existe'}
            return Response(message,status=404)
        serializer = OrderSerializer(myorder)
        if serializer.data['status'] != "created" and serializer.data['status'] != "delivered":
            message = {'error': 'La orden necesita ser procesada antes de ser confirmada'}
            return Response(message,status=400)
        key = Keys.objects.first()
        url = 'https://stag.wallet.tpaga.co/merchants/api/v1/payment_requests/'+serializer.data['token']+'/info'
        auth = "Basic %s"%(key.key)
        headers = {"Authorization": auth, "Cache-Control":"no-cache", "Content-Type":"application/json"}
        data = {}
        myResult=requests.get(url, json=data, headers=headers)
        myJsonResult=json.loads(myResult.text)
        if 'error_code' in myJsonResult:
            return Response(myJsonResult,status=400)
        updatedSerializer = OrderSerializer(myorder, data=serializer.data)
        if updatedSerializer.is_valid():
            updatedSerializer.save(status=myJsonResult['status'])
            message = {'orderId': id, 'status': myJsonResult['status'], 'payment_url': serializer.data['tpagaPaymentUrl']}
            return Response(message)
        message = {'error': 'Error al confirmar'}
        return Response(message,status=400)

class RefundOrder(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, id):
        try:
            myorder = order.objects.get(id=id)
        except order.DoesNotExist:
            message = {'error': 'La orden no existe'}
            return Response(message,status=404)
        serializer = OrderSerializer(myorder)
        if serializer.data['status'] != "delivered":
            message = {'error': 'La orden solo puedes ser reembolsada una vez sea confirmada'}
            return Response(message,status=400)
        key = Keys.objects.first()
        url = 'https://stag.wallet.tpaga.co/merchants/api/v1/payment_requests/refund'
        auth = "Basic %s"%(key.key)
        headers = {"Authorization": auth, "Cache-Control":"no-cache", "Content-Type":"application/json"}
        data = {'payment_request_token':serializer.data['token']}
        myResult=requests.post(url, json=data, headers=headers)
        myJsonResult=json.loads(myResult.text)
        if 'error_code' in myJsonResult:
            return Response(myJsonResult,status=400)
        updatedSerializer = OrderSerializer(myorder, data=serializer.data)
        if updatedSerializer.is_valid():
            updatedSerializer.save(status=myJsonResult['status'])
            message = {'orderId': id, 'status': myJsonResult['status']}
            return Response(message)
        message = {'error': 'Error al reenbolsar '}
        return Response(message,status=400)
#Se ejecutan las acciones que permiten agregar o remover items de la orden de comprar/carrito de compras
class CreatePurchasedItem(APIView):
    def post(self, request):
        data = JSONParser().parse(request)
        serializer = PurchasedItemCreateSerializer(data=data)
        if serializer.is_valid():
            myOrder = order.objects.get(id=data['orderId'])
            if myOrder.status != "new":
                message = {'error': 'La orden no puede ser modificada despues de ser procesada'}
                return Response(message,status=400)
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
        if myOrder.status != "new":
            message = {'error': 'La orden no puede ser modificada despues de ser procesada'}
            return Response(message,status=400)
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
