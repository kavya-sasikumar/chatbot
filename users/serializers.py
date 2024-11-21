from rest_framework import serializers
from django.contrib.auth.models import User
from django.db.models import Avg, Count
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

    class Meta:
        model = User
        fields = ('id', 'user_data', 'username')

    def get_user_data(self, obj):
        requestUser = self.context['request'].user
        request = self.context['request']
        return requestUser.id

    def get_username(self, obj):
        requestUser = self.context['request'].user
        request = self.context['request']
        return requestUser.username


class CategoriesSerializer(serializers.ModelSerializer):
    """A serializer for the categories model in our DB to convert the format to JSON """

    class Meta:
        model = Categories
        fields = ('id', 'title', 'description', 'date_created', 'date_updated')

class ReviewSerializer(serializers.ModelSerializer):
     """A serializer for the review item model in our DB to convert the format to JSON """
     username = serializers.CharField(source="user.username", read_only=True)
     class Meta: 
         model=Review
         fields=('user', 'product', 'rating', 'comment', 'date_created', 'date_updated',"username")
         
         extra_kwargs = {
            "user": {'write_only': True},
            "username": {'read_only': True},
         }


class ProductSerializer(serializers.ModelSerializer):
    """A serializer for the product model in our DB to convert the format to JSON """
    average_rating = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'id', 'title', 'description', 'color', 'price', 'image', 'stock', 
            'is_available', 'date_created', 'date_updated', 'category', 
            'average_rating', 'total_reviews'
        )

    def get_average_rating(self, obj):
        """Calculate and return the average rating for the product."""
        avg_rating = Review.objects.filter(product=obj).aggregate(Avg('rating'))
        return avg_rating['rating__avg'] if avg_rating['rating__avg'] is not None else 0

    def get_total_reviews(self, obj):
        """Calculate and return the total number of reviews for the product."""
        total_reviews = Review.objects.filter(product=obj).aggregate(Count('id'))
        return total_reviews['id__count']

class OrderItemSerializer(serializers.ModelSerializer):
     """A serializer for the order item model in our DB to convert the format to JSON """
     class Meta: 
         model = OrderItem 
         fields = ('product', 'quantity', 'price')

class OrderSerializer(serializers.ModelSerializer): 
    """A serializer for the order model in our DB to convert the format to JSON """
    items = OrderItemSerializer(many=True)

    class Meta: 
        model = Order 
        fields = ('user', 'address', 'total_amount', 'status_type', 'order_date', 'date_updated', 'items')

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order

class ChatMessageSerializer(serializers.ModelSerializer):
     """A serializer for the chat message item model in our DB to convert the format to JSON """
     class Meta: 
         model=ChatMessage
         fields=('user', 'message', 'timestamp')

class ChatSessionSerializer(serializers.ModelSerializer):
     """A serializer for the chat session item model in our DB to convert the format to JSON """
     class Meta: 
         model = ChatSession
         fields=('user', 'start_time', 'end_time')

class EventSerializer(serializers.ModelSerializer):
     """A serializer for the event item model in our DB to convert the format to JSON """
     class Meta: 
         model = Event
         fields=('title', 'description', 'slug', 'date_created', 'date_updated')

class EventImageSerializer(serializers.ModelSerializer):
     """A serializer for the event image item model in our DB to convert the format to JSON """
     class Meta: 
         model = EventImage
         fields=('event', 'image', 'description', 'date_created', 'date_updated')
         
        
