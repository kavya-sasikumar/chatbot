from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class UserCreateSerializer(serializers.ModelSerializer):

    """Create new user and add a password 2 for confirmation.
    The save method is overriden to allow for the unique data we requested."""

    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'password', 'password2',
                  'is_staff', 'is_superuser')

        extra_kwargs = {
            'password': {'write_only': True},
        }

    def save(self):
        user = User(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
            is_staff=self.validated_data['is_staff'],
            is_superuser=self.validated_data['is_superuser'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError(
                {'password': 'Passwords must match!'})
        user.set_password(password)
        user.save()
        return user

class GetUserIDSerializer(serializers.ModelSerializer):
    """A serializer class for the User Model to get the authenticated user's data"""
    user_data = serializers.SerializerMethodField('get_user_data')
    username = serializers.SerializerMethodField('get_username')
    profile_id = serializers.SerializerMethodField('get_profile_id')

    class Meta:
        model = User
        fields = ('id', 'user_data', 'username', 'profile_id')

    def get_user_data(self, obj):
        requestUser = self.context['request'].user
        request = self.context['request']
        return requestUser.id

    def get_username(self, obj):
        requestUser = self.context['request'].user
        request = self.context['request']
        return requestUser.username

    def get_profile_id(self, obj):
        requestUser = self.context['request'].user
        request = self.context['request']
        return requestUser.profile.id

class CategoriesSerializer(serializers.ModelSerializer):
    """A serializer for the categories model in our DB to convert the format to JSON """

    class Meta:
        model = Categories
        fields = ('id', 'title', 'description', 'date_created', 'date_updated')

class ProductSerializer(serializers.ModelSerializer):
   """A serializer for the product model in our DB to convert the format to JSON """

   class Meta:
       model = Product
       fields = ('title', 'description', 'color', 'price', 'image', 'stock', 'is_available', 'date_created', 'date_updated', 'category')

class OrderSerializer(serializers.ModelSerializer):
      """A serializer for the order model in our DB to convert the format to JSON """

      class Meta:
        model = Order
        fields = ('user', 'address', 'total_amount', 'status_type', 'order_date', 'date_updated')
        
class OrderItemSerializer(serializers.ModelSerializer):
     """A serializer for the order item model in our DB to convert the format to JSON """

     class Meta:
         model = OrderItem
         fields = ('order','product','quantity','price')

class ReviewSerializer(serializers.ModelSerializer):
    """A serializer for the review model in our DB to convert the format to JSON """

    class Meta:
        model = Review
        fields = ('user','product','rating','comment','date_created','date_updated')

class ChatMessage(serializers.ModelSerializer):
     """A serializer for the chat message model in our DB to convert the format to JSON """

     class Meta:
         model = ChatMessage
         fields = ('user','message','timestamp')

class ChatSession(serializers.ModelSerializer):
     """A serializer for the chat session model in our DB to convert the format to JSON """

     class Meta:
         model = ChatSession
         fields = ('user','start_time','end_time')
