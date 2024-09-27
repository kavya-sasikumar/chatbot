from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, permissions, filters
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from chatbot.pagination import CustomPagination
import requests
from transformers import pipeline

# from chatbot.pagination import CustomPagination
from django.contrib.auth.models import User
from .models import *
from .serializers import *

fashion_advisor=pipeline("text-generation", model="gpt2")
"""View to create a user"""
@api_view(['POST',])
@permission_classes((permissions.AllowAny,))
def user_create(request):
    if request.method == 'POST':
        serializer = UserCreateSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = "Successfully Registered New User"
        else:
            data = serializer.errors
        return Response(data)
    
class UserData(generics.ListAPIView):
    """View to get authenticated user's data"""
    queryset = User.objects.all().order_by('-id')
    serializer_class = GetUserIDSerializer
    permission_classes = (permissions.IsAuthenticated, )
    pagination_class = CustomPagination

class CategoryCreateView(generics.CreateAPIView):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (permissions.AllowAny, )

class CategoryListView(generics.ListAPIView):
    queryset = Categories.objects.all().order_by('id')
    serializer_class = CategoriesSerializer

    permission_classes = (permissions.AllowAny, )

class CategoryRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser, )

class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser, )

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all().order_by('-id')
    serializer_class = ProductSerializer
    permission_classes = (permissions.AllowAny, )
    pagination_class = CustomPagination

class ProductRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser, )

class ProductListCategory(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = (permissions.AllowAny, )
    pagination_class = CustomPagination

    def get_queryset(self):
        return Product.objects.filter(category_id=self.kwargs['category_id']).order_by('-id')

class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated, )

class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        return Order.objects.filter(user_id=self.kwargs['user_id']).order_by('-id')

class OrderRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated, )

class OrderItemCreateView(generics.CreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = (permissions.IsAuthenticated, )

class OrderItemRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = (permissions.IsAuthenticated, )

class ReviewCreateView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticated, )

class ReviewListView(generics.ListAPIView):
    queryset = Review.objects.all().order_by('id')
    serializer_class = ReviewSerializer
    permission_classes = (permissions.AllowAny, )

class ReviewRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticated, )

class ReviewListViewUser(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = (permissions.AllowAny, )

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_id']).order_by('-id')[:3]

class ChatMessageCreateView(generics.CreateAPIView):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer
    permission_classes = (permissions.AllowAny, )

class ChatMessageListView(generics.ListAPIView):
    # queryset = ChatMessage.objects.all().order_by('id')
    serializer_class = ChatMessageSerializer
    permission_classes = (permissions.AllowAny, )

    def get_queryset(self):
        return ChatMessage.objects.filter(user_id=self.kwargs['user_id']).order_by('-id')

class ChatMessageRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer
    permission_classes = (permissions.IsAuthenticated, )

class ChatSessionCreateView(generics.CreateAPIView):
    queryset = ChatSession.objects.all()
    serializer_class = ChatSessionSerializer
    permission_classes = (permissions.AllowAny, )

class ChatSessionListView(generics.ListAPIView):
    queryset = ChatSession.objects.all().order_by('id')
    serializer_class = ChatSessionSerializer
    permission_classes = (permissions.AllowAny, )

class ChatSessionRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = ChatSession.objects.all()
    serializer_class = ChatSessionSerializer
    permission_classes = (permissions.AllowAny, )
 
class FashionChatbot(APIView):
    def post(self,request,*args,**kwargs):
        user_input = request.data.get("message")
        user_id = request.data.get("user_id")

        permission_classes = (permissions.AllowAny, )

        user=User.objects.get(id=user_id)

        chat_message=ChatMessage.objects.create(user=user, message=user_input)

        bot_response=fashion_advisor(user_input,max_length=50)[0]["generated_text"]

        related_products=Product.objects.filter(description__icontains=user_input)

        response_message=f"{bot_response}\n\nhere are some related products:\n"

        for product in related_products:
            response_message += f"- {product.title} (${product.price})\n"

        return Response({"response": response_message}, status=status.HTTP_200_OK)



        