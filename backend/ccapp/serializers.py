from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["email", "full_name", "phone", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            full_name=validated_data["full_name"],
            phone=validated_data.get("phone", ""),
            password=validated_data["password"],
        )
        return user


class ChatUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatUser
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    chat_user = serializers.StringRelatedField(read_only=True)
    chat_user_id = serializers.PrimaryKeyRelatedField(
        queryset=ChatUser.objects.all(), source="chat_user"
    )
    class Meta:
        model = User
        fields = ["id", "email", "full_name", "phone", "role", "chat_user", "chat_user_id", "created_at"]


# Contract =============================


class ContractSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="user"
    )

    class Meta:
        model = Contract
        # fields = '__all__'
        fields = [
            "id",
            "title",
            "description",
            "start_date",
            "end_date",
            "total_cost",
            "user",
            "user_id",
        ]


# Suncontractor =========================


class SubcontractorSerializer(serializers.ModelSerializer):
    # contact_person =  UserSerializer(read_only=True)
    # contact_person_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user')

    class Meta:
        model = Subcontractor
        fields = [
            "id",
            "name",
            "phone",
            "email",
            "address",
            "created_by",
            "contact_person",
        ]


# RFQs ==================================


class RFQSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, source="user"
    )

    subcontractor = SubcontractorSerializer(read_only=True)
    subcontractor_id = serializers.PrimaryKeyRelatedField(
        queryset=Subcontractor.objects.all(), write_only=True, source="subcontractor"
    )

    class Meta:
        model = RFQ
        fields = [
            "id",
            "title",
            "description",
            "created_at",
            "due_date",
            "status",
            "estimated_cost",
            "user",
            "user_id",
            "subcontractor",
            "subcontractor_id",
        ]


# Payment ==================================


class PaymentSerializer(serializers.ModelSerializer):
    contract = ContractSerializer(read_only=True)
    contract_id = serializers.PrimaryKeyRelatedField(
        queryset=Contract.objects.all(), write_only=True, source="contract"
    )

    class Meta:
        model = Payment
        fields = [
            "id",
            "contract",
            "contract_id",
            "amount",
            "execute_date",
            "status",
        ]


class MessageListSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField(read_only=True)
    receiver = serializers.StringRelatedField(read_only=True)
    sender_id = serializers.PrimaryKeyRelatedField(queryset=ChatUser.objects.all(), source='sender', write_only=True)
    receiver_id = serializers.PrimaryKeyRelatedField(queryset=ChatUser.objects.all(), source='receiver', write_only=True)

    class Meta:
        model = MessageList
        fields = ['id', 'sender', 'receiver', 'text', 'created_at', 'sender_id', 'receiver_id']