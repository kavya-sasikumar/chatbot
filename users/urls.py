from django.urls import path
from .views import *

urlpatterns = [

    #Users
    path('create-user/', user_create),
    path('check-user/', UserData.as_view()),
    path('update-user-names/<int:pk>/', UserRetrieveUpdateView.as_view()),
    path('deactivate-account/', DeactivateAccountAPIView.as_view()),
    
    # Categories
    path('create-categories/', CategoryCreateView.as_view()),
    path('category/<int:pk>/', CategoryRetrieveUpdateView.as_view()),
    path('categories/', CategoryListView.as_view()),

    # Vendor
    path('create-vendor/', VendorCreateView.as_view()),
    path('vendor/<int:user_id>/', VendorRetrieveUpdateView.as_view()),
    path('vendors/', VendorListView.as_view()),

    # Chat
    path('chat/', FashionChatbot.as_view()),

    # Product
    path('create-product/', ProductCreateView.as_view()),
    path('product/<int:pk>/', ProductRetrieveUpdateView.as_view()),
    path('products/', ProductListView.as_view()),
    path('vendor-products/<int:user_id>/', ProductListVendor.as_view()),
    path('category-products/<int:category_id>/', ProductListCategory.as_view()),
    
    # Order
    path('create-order/', OrderCreateView.as_view()),
    path('order/<int:pk>/', OrderRetrieveUpdateView.as_view()),
    path('orders/<int:user_id>/', OrderListView.as_view()),

    # OrderItem
    path('create-orderitem/', OrderItemCreateView.as_view()),
    path('orderitem/<int:pk>/', OrderItemRetrieveUpdateView.as_view()),
    path('orderitems/<int:vendor_id>/', OrderItemListVendorView.as_view()),

    # Review
    path('create-review/', ReviewCreateView.as_view()),
    path('review/<int:pk>/', ReviewRetrieveUpdateView.as_view()),
    path('reviews/', ReviewListView.as_view()),
    path('product-reviews/<int:product_id>/', ReviewListViewUser.as_view()),

    # Chat Message
    path('create-chatmessage/', ChatMessageCreateView.as_view()),
    path('chatmessage/<int:pk>/', ChatMessageRetrieveUpdateView.as_view()),
    path('chatmessages/<int:user_id>/', ChatMessageListView.as_view()),

    # Chat Session
    path('create-chatsession/', ChatSessionCreateView.as_view()),
    path('chatsession/<int:pk>/', ChatSessionRetrieveUpdateView.as_view()),
    path('chatsessions/', ChatSessionListView.as_view()),

    # Events
    path('events/', EventListView.as_view()),
    path('event-images/<int:event_id>/', EventImageListView.as_view()),
    path('generate-ai-styling-images/', GenerateAiStylingImage.as_view()),
    path('generate-ai-styling-text-event/', GenerateAiStylingTextEvent.as_view()),
    path('generate-ai-styling-text/', GenerateAiStylingText.as_view()),

    # On-boarding
    path('random-event-images/', RandomEventImagesAPIView.as_view()),
 ]


