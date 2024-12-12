from django.urls import path, include
from rest_framework.routers import DefaultRouter

from awesome_chatbot import views

# Create a router and register our ViewSets with it.
router = DefaultRouter()
router.register(r'awesome_chatbot', views.ChatBotViewSet, basename='awesome_chatbot')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]