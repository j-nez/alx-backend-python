from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True) #not part of model fields
    class Meta:
        model = User
        fields = __all__
        extra_kwargs = {"password": {"write_only": True}} #allows auto generation of password and applies the write only contraint

    #object level validation for password typing reduncancy
    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise.serializers.ValidationError("Password does not match")
        data.pop("confirm_password")
        return super().validate(data) #DRF validation sequence is continued
    
    #hashing passaword and replacing it in vlaidated data
    def create(Self, validated_data):
        password = validated_data.get("password")
        validated_data["password"] = make_password(password)

        return super().create(validated_data) #DRF CRUD is continued

class MessagesSerializer(serializers.ModelSerializer):
    #with this there is no need  for nested serializtion but you lose accesst to all the user details in a get request
    sender_id = serializers.PrimaryKeyRelatedField(queryset = User.objects.all(), source ="sender_id", write_only=True)
    class Meta:
        model = Message
        fields = [
            'message_id',
            'sender_id',
            'message_body',
            'sent_at',
        ]
    def validate_message_body(self, body): 
        if len(body.strip()) == 0:
            raise serializers.ValidateError("Message body can not be empty")
        return body

class ConversationSerializer(serializers.ModelSerializer):
    participant = serializers.SerializerMethodField() #read only field
    participant_id = serilaizers.PrimaryKeyRelatedField(queryset = User.objects.all(), write_only = True)

    class Meta:
        model = Conversation
        fields = __all__
    def get_participant(self, obj):

        return [user.username for user in obj.participants_id.all()]