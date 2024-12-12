import chatterbot
import chatterbot.logic
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets

from awesome_chatbot.models import ChatBotModel
from awesome_chatbot.serializers import ChatBotRequestSerializer, ChatBotSerializer, UpdateResponseSerializer
from chatterbot.trainers import ListTrainer
from chatterbot import ChatBot, comparisons, response_selection

DomBot = ChatBot(
    'DomBot',
    logic_adapters=[
        {
            "import_path": [
                "chatterbot.logic.BestMatch",
                "chatterbot.logic.TimeLogicAdapter",
                "chatterbot.logic.MathematicalEvaluation"
            ],
            "statement_comparison_function": comparisons.LevenshteinDistance,
            "response_selection_method": response_selection.get_first_response
        }
    ],
    preprocessors=['chatterbot.preprocessors.clean_whitespace'],
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///chatterbot_db.sqlite3',
)

class ChatBotViewSet(viewsets.ModelViewSet):
    queryset = ChatBotModel.objects.all()
    serializer_class = ChatBotSerializer

    @action(detail=False, methods=['post'], url_path='update_response')
    def update_bot_response(self, request, *args, **kwargs):
        # Validate with UpdateResponseSerializer
        serializer = UpdateResponseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        message_request = serializer.validated_data['message_request']
        correct_response = serializer.validated_data['bot_response']
        
        # Train the bot
        list_trainer = ListTrainer(DomBot)
        list_trainer.train([message_request, correct_response])

        # Custom response for training confirmation
        return Response({
            "message_request": message_request,
            "bot_response": "Terima kasih telah melatih saya kata-kata baru ini!",
            "need_correction": False,
            "status_code": status.HTTP_201_CREATED,
            "error_message": ""
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='chatbot_response')
    def chatbot_response(self, request, *args, **kwargs):
        # Validate with ChatBotRequestSerializer
        serializer = ChatBotRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        message_request = serializer.validated_data['message_request']

        if not message_request:
            return Response({
                "message_request": message_request,
                "bot_response": "Perintah yang anda masukkan adalah kosong. Silakan masukkan perintah yang ingin saya jawab.",
                "need_correction": True,
                "status_code": status.HTTP_400_BAD_REQUEST,
                "error_message": "Bad Request"
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            bot_response = DomBot.get_response(message_request)
            if bot_response.confidence > 0.7:
                return Response({
                    "message_request": message_request,
                    "bot_response": str(bot_response),
                    "need_correction": False,
                    "status_code": status.HTTP_200_OK,
                    "error_message": ""
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "message_request": message_request,
                    "bot_response": "Saya tidak yakin bagaimana menjawabnya. Tolong bantu saya!",
                    "need_correction": True,
                    "status_code": status.HTTP_200_OK,
                    "error_message": ""
                }, status=status.HTTP_200_OK)
        except ConnectionError:
            return Response({
                "message_request": message_request,
                "bot_response": "Koneksi terputus. Silakan coba lagi nanti.",
                "need_correction": False,
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "error_message": "Internal Server Error"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)