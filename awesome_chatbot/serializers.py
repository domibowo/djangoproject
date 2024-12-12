from rest_framework import serializers

from awesome_chatbot.models import ChatBotModel

class UpdateResponseSerializer(serializers.Serializer):
    message_request = serializers.CharField(required=True, error_messages={'required': "Message request is required."})
    bot_response = serializers.CharField(required=True, error_messages={'required': "Bot response is required."})
    
class ChatBotRequestSerializer(serializers.Serializer):
    message_request = serializers.CharField(required=True, error_messages={'required': "Message request is required."})

class ChatBotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatBotModel
        fields = ('message_request', 'bot_response', 'created_at')