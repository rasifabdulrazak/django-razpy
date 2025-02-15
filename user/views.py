import json

import razorpay
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import views

from .models import Order
from .serializers import OrderSerializer,FileSerializer
from django.conf import settings


@api_view(['POST'])
def start_payment(request):
    # request.data is coming from frontend
    amount = request.data['amount']
    name = request.data['name']

    # setup razorpay client this is the client to whome user is paying money that's you
    client = razorpay.Client(auth=(settings.RAZORPAY_API, settings.SECRET_KEY_RAZORPAY))

    # create razorpay order
    # the amount will come in 'paise' that means if we pass 50 amount will become
    # 0.5 rupees that means 50 paise so we have to convert it in rupees. So, we will 
    # mumtiply it by 100 so it will be 50 rupees.
    payment = client.order.create({"amount": int(amount) * 100, 
                                   "currency": "INR", 
                                   "payment_capture": "1"})

    # we are saving an order with isPaid=False because we've just initialized the order
    # we haven't received the money we will handle the payment succes in next 
    # function
    order = Order.objects.create(order_product=name, 
                                 order_amount=amount, 
                                 order_payment_id=payment['id'])

    serializer = OrderSerializer(order)

    """order response will be 
    {'id': 17, 
    'order_date': '23 January 2021 03:28 PM', 
    'order_product': '**product name from frontend**', 
    'order_amount': '**product amount from frontend**', 
    'order_payment_id': 'order_G3NhfSWWh5UfjQ', # it will be unique everytime
    'isPaid': False}"""

    data = {
        "payment": payment,
        "order": serializer.data
    }
    return Response(data)


@api_view(['POST'])
def handle_payment_success(request):
    # request.data is coming from frontend
    res = json.loads(request.data["response"])

    """res will be:
    {'razorpay_payment_id': 'pay_G3NivgSZLx7I9e', 
    'razorpay_order_id': 'order_G3NhfSWWh5UfjQ', 
    'razorpay_signature': '76b2accbefde6cd2392b5fbf098ebcbd4cb4ef8b78d62aa5cce553b2014993c0'}
    this will come from frontend which we will use to validate and confirm the payment
    """

    ord_id = ""
    raz_pay_id = ""
    raz_signature = ""

    # res.keys() will give us list of keys in res
    for key in res.keys():
        if key == 'razorpay_order_id':
            ord_id = res[key]
        elif key == 'razorpay_payment_id':
            raz_pay_id = res[key]
        elif key == 'razorpay_signature':
            raz_signature = res[key]

    # get order by payment_id which we've created earlier with isPaid=False
    order = Order.objects.get(order_payment_id=ord_id)

    # we will pass this whole data in razorpay client to verify the payment
    data = {
        'razorpay_order_id': ord_id,
        'razorpay_payment_id': raz_pay_id,
        'razorpay_signature': raz_signature
    }

    client = razorpay.Client(auth=(settings.RAZORPAY_API, settings.SECRET_KEY_RAZORPAY))

    # checking if the transaction is valid or not by passing above data dictionary in 
    # razorpay client if it is "valid" then check will return None
    check = client.utility.verify_payment_signature(data)

    if check is not None:
        print("Redirect to error url or error page")
        return Response({'error': 'Something went wrong'})

    # if payment is successful that means check is None then we will turn isPaid=True
    order.isPaid = True
    order.save()

    res_data = {
        'message': 'payment successfully received!'
    }

    return Response(res_data)



from django.http import HttpResponse
import time
from .models import Order,TestModL
from asgiref.sync import sync_to_async
import asyncio



def get_movies():
    print("getting movies ....")
    time.sleep(2)
    qs = Order.objects.all()
    print(qs)
    print("all movies fetched")


def get_theatres():
    print("getting theatres ...")
    time.sleep(5)
    qs = TestModL.objects.all()
    print(qs)
    print("all theatres fetched")


@sync_to_async
def get_movies_async():
    print("getting movies ....")
    time.sleep(2)
    qs = Order.objects.all()
    print(qs)
    print("all movies fetched")


@sync_to_async
def get_theatres_async():
    print("getting theatres ...")
    time.sleep(5)
    qs = TestModL.objects.all()
    print(qs)
    print("all theatres fetched")


@api_view(['GET'])
def sync_view(request):
    start_time = time.time()
    get_movies()
    get_theatres()
    total = time.time()-start_time
    return HttpResponse(f"time taken {total}")


@api_view(['GET'])
async def async_view(request):
    start_time = time.time()
    # approach 1 
    # movie_task = asyncio.ensure_future(get_movies_async())
    # theatre_task = asyncio.ensure_future(get_theatres_async())
    # await asyncio.wait([movie_task, theatre_task])
    # approach 2 using gather
    await asyncio.gather(get_movies_async(), get_theatres_async())
    total = time.time()-start_time
    return HttpResponse(f"time taken async {total}")

import pandas as pd

class Upload(views.APIView):
    serializer_class = FileSerializer

    def post(self,request,*args,**kwargs):
        rf = request.FILES.get('file')
        csv = pd.read_excel(rf,sheet_name=None)
        print(csv.keys())
        print(csv['TENANT DETAILS'])
        tenant_data = csv['TENANT DETAILS']
        for i in tenant_data:
            print(i)
        return Response({'done':'ok'})

