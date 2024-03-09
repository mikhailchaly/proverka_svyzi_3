from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView

from shop.models import Basket
from shop.serializers import BasketSerializer


class OrderView(APIView):
    def get(self, request):
        orders = Basket.objects.all()
        serializer = BasketSerializer(orders, many=True)
        return Response({'oreders': serializer.data})

    def post(self, request):
        order = request.data.get('orders')
        serializer = BasketSerializer(data=order)
        if serializer.is_valid(raise_exception=True):
            order_saved = serializer.save()
        return Response({"success": "Order ' {} ' created successfully".format(order_saved.title)})

class OrderListView(ListModelMixin, GenericAPIView):
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)