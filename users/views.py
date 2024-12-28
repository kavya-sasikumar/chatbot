from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, permissions, filters
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from chatbot.pagination import CustomPagination
import requests
import random
# from transformers import pipeline
import openai 

# from chatbot.pagination import CustomPagination
from django.contrib.auth.models import User
from .models import *
from .serializers import *

openai.api_key="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"
# fashion_advisor=pipeline("text-generation", model="gpt2-large")
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

class UserRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny, )

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

class VendorCreateView(generics.CreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = (permissions.IsAuthenticated, )

class VendorListView(generics.ListAPIView):
    queryset = Vendor.objects.all().order_by('id')
    serializer_class = VendorSerializer
    permission_classes = (permissions.AllowAny, )

class VendorRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    # queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = (permissions.IsAuthenticated, )
    lookup_field = 'user_id'

    def get_queryset(self):
        return Vendor.objects.filter(user_id=self.kwargs['user_id']).order_by('-id')

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

class ProductListVendor(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = (permissions.IsAuthenticated, )
    pagination_class = CustomPagination

    def get_queryset(self):
        return Product.objects.filter(user_id=self.kwargs['user_id']).order_by('-id')

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

class OrderItemListVendorView(generics.ListAPIView):
    serializer_class = OrderItemSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        return OrderItem.objects.filter(vendor_id=self.kwargs['vendor_id']).order_by('-id')

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
 
def fashion_advisor(prompt, max_tokens=200):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=[
            {"role": "system", "content": "You are a fashion advisor for females ONLY."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=max_tokens,
        temperature=0.7
    )
    return response['choices'][0]['message']['content'].strip()

class FashionChatbot(APIView):
    def post(self,request,*args,**kwargs):
        user_input = request.data.get("message")
        user_id = request.data.get("user_id")

        if not user_input or not user_id:
            return Response({"error": "Missing required parameters"}, status=status.HTTP_400_BAD_REQUEST)

        permission_classes = (permissions.AllowAny, )

        user=User.objects.get(id=user_id)

        chat_message=ChatMessage.objects.create(user=user, message=user_input)

        try:
            # ai_prompt = f"Give me fashion advice on how to match {user_input} for a woman"
            bot_response=fashion_advisor(user_input)

            related_products = Product.objects.filter(
                Q(title__icontains=user_input) | Q(description__icontains=user_input) | Q(color__icontains=user_input)
            )
 #this is github code
            response_message=f"{bot_response}\n\nHere are some related products:\n"
            if related_products.exists():
                for product in related_products:
                    response_message += f"- {product.title} (${product.price})\n"
            else:
                response_message += "No matching products found."

            return Response({"response": response_message}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class EventListView(generics.ListAPIView):
    queryset = Event.objects.all().order_by('title')
    serializer_class = EventSerializer
    permission_classes = (permissions.AllowAny, )
    
class EventImageListView(generics.ListAPIView):
    # queryset = ChatMessage.objects.all().order_by('id')
    serializer_class = EventImageSerializer
    permission_classes = (permissions.AllowAny, )

    def get_queryset(self):
        return EventImage.objects.filter(event_id=self.kwargs['event_id']).order_by('id')

# class GenerateAiStylingImage(APIView):
#     def post(self,request,*args,**kwargs):
#         descriptions = request.data.get("descriptions")
#         # user_id = request.data.get("user_id")

#         if not descriptions:
#             return Response({"error": "Missing required parameters"}, status=status.HTTP_400_BAD_REQUEST)

#         permission_classes = (permissions.AllowAny, )

#         # user=User.objects.get(id=user_id)

#         # chat_message=ChatMessage.objects.create(user=user, message=user_input)

#         try:
#             ai_prompt = f"{descriptions} I want an image that combines all three outfit descriptions BUT i want a totally new outfit generated based off of the theme of all three outfit descriptions i just want one NEW outfit in the image. After that, generate two other images with different styles from the first one you generated but also based on the descriptions I gave to you. for a woman"
#             bot_response=fashion_advisor(ai_prompt)

#             # related_products = Product.objects.filter(
#             #     Q(title__icontains=user_input) | Q(description__icontains=user_input) | Q(color__icontains=user_input)
#             # )
#  #this is github code
#             response_message=f"{bot_response}"
#             # if related_products.exists():
#             #     for product in related_products:
#             #         response_message += f"- {product.title} (${product.price})\n"
#             # else:
#             #     response_message += "No matching products found."

#             return Response({"response": response_message}, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GenerateAiStylingImage(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        descriptions = request.data.get("descriptions")
        
        if not descriptions:
            return Response({"error": "Missing required parameters"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Generate first image
            first_image_prompt = f"{descriptions} i want an image that combines all three outfit descriptions in each of the maps in the list sent BUT i want a totally new outfit generated based off of the theme of all three outfit descriptions i just want one NEW outfit in the image. Don’t give me just concepts, let me see it on an actual human model as something I can wear for an event as a woman."
            first_image = openai.Image.create(
                model="dall-e-3",
                prompt=first_image_prompt,
                n=1,
                size="1024x1024"
            )
            first_image_url = first_image.data[0].url

            # Generate second variant image
            # second_image_prompt = f"{descriptions} i want an image that combines all three outfit descriptions in each of the maps in the list sent BUT i want a totally new outfit generated based off of the theme of all three outfit descriptions i just want one NEW outfit in the image. Don’t give me just concepts, let me see it on an actual human model as something I can wear for an event as a woman."
            # second_image = openai.Image.create(
            #     model="dall-e-3",
            #     prompt=second_image_prompt,
            #     n=1,
            #     size="1024x1024"
            # )
            # second_image_url = second_image.data[0].url

            # Generate third variant image
            # third_image_prompt = f"{descriptions} i want an image that combines all three outfit descriptions in each of the maps in the list sent BUT i want a totally new outfit generated based off of the theme of all three outfit descriptions i just want one NEW outfit in the image. Don’t give me just concepts, let me see it on an actual human model as something I can wear for an event as a woman."
            # third_image = openai.Image.create(
            #     model="dall-e-3",
            #     prompt=third_image_prompt,
            #     n=1,
            #     size="1024x1024"
            # )
            # third_image_url = third_image.data[0].url

            return Response({
                "images": [
                    first_image_url
                    # second_image_url 
                    # third_image_url
                ]
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": "An unexpected error occurred: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GenerateAiStylingText(APIView):
    def post(self,request,*args,**kwargs):
        descriptions = request.data.get("descriptions")

        if not descriptions:
            return Response({"error": "Missing required parameters"}, status=status.HTTP_400_BAD_REQUEST)

        permission_classes = (permissions.AllowAny, )

        try:
            ai_prompt = f"Take these image selections by a particular user into consideration: {descriptions} Give the response as though you're referring to the user in the second person where it entails a profile of what kind of styling the user likes and do so in a horoscope-like manner. Also, add a profile for the personality of the user. The response should be in no more than 2 paragraphs and the word: horoscope shouldn't be used in it. Make keywords or phrases bold in your response."
            bot_response=fashion_advisor(ai_prompt)

            related_products = Product.objects.filter(
                Q(title__icontains=descriptions) | Q(description__icontains=descriptions) | Q(color__icontains=descriptions)
            )

            response_message=f"{bot_response}"

            return Response({"response": response_message}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GenerateAiStylingTextEvent(APIView):
    def post(self,request,*args,**kwargs):
        descriptions = request.data.get("descriptions")

        if not descriptions:
            return Response({"error": "Missing required parameters"}, status=status.HTTP_400_BAD_REQUEST)

        permission_classes = (permissions.AllowAny, )

        try:
            ai_prompt = f"Take these image selections by a particular user into consideration: {descriptions} Give the response as though you're referring to the user in the second person where it entails a profile of what kind of styling the user likes in relation to the theme of the dress styles in the description and do so in a horoscope-like manner. The response should be in no more than 2 paragraphs and the word: horoscope shouldn't be used in it. Make keywords or phrases bold in your response."
            bot_response=fashion_advisor(ai_prompt)

            related_products = Product.objects.filter(
                Q(title__icontains=descriptions) | Q(description__icontains=descriptions) | Q(color__icontains=descriptions)
            )

            response_message=f"{bot_response}\n\nHere are some related products:\n"
            if related_products.exists():
                for product in related_products:
                    response_message += f"- {product.title} (${product.price})\n"
            else:
                response_message += "No matching products found."

            return Response({"response": response_message}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RandomEventImagesAPIView(APIView):
    """
    API View to fetch 25 random EventImage records and return their details as JSON.
    """

    def get(self, request, *args, **kwargs):
        # Fetch all EventImage records and shuffle to pick 25 randomly
        all_images = list(EventImage.objects.all())
        random_images = random.sample(all_images, min(len(all_images), 25))

        # Prepare the response data
        image_data = [
            {
                "event_title": image.event.title,
                "image_url": request.build_absolute_uri(image.image.url),
                "description": image.description,
                "date_created": image.date_created,
                "date_updated": image.date_updated,
            }
            for image in random_images
        ]

        # Return the data as a JSON response
        return Response({"images": image_data})

class DeactivateAccountAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        try:
            # Get the authenticated user
            user = request.user
            # Set is_active to False
            user.is_active = False
            user.save()
            return Response(
                {"message": "Account has been deactivated successfully."},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


