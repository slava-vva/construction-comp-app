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
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    # chat_user = serializers.StringRelatedField(read_only=True)
    chat_user = ChatUserSerializer(read_only=True)

    chat_user_id = serializers.PrimaryKeyRelatedField(
        queryset=ChatUser.objects.all(),
        source="chat_user",
        required=False,
        allow_null=True,
    )

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "full_name",
            "phone",
            "role",
            "chat_user",
            "chat_user_id",
            "created_at",
        ]


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
        queryset=User.objects.all(), source="user"
    )

    subcontractor = SubcontractorSerializer(read_only=True)
    subcontractor_id = serializers.PrimaryKeyRelatedField(
        queryset=Subcontractor.objects.all(), source="subcontractor"
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
    sender_id = serializers.PrimaryKeyRelatedField(
        queryset=ChatUser.objects.all(), source="sender", write_only=True
    )
    receiver_id = serializers.PrimaryKeyRelatedField(
        queryset=ChatUser.objects.all(), source="receiver", write_only=True
    )

    class Meta:
        model = MessageList
        fields = [
            "id",
            "sender",
            "receiver",
            "text",
            "created_at",
            "sender_id",
            "receiver_id",
        ]


# construction object ==========================


class ConstructionObjectSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="user"
    )

    class Meta:
        model = ConstructionObject
        fields = [
            "id",
            "title",
            "description",
            "start_date",
            "end_date",
            "location",
            "total_cost",
            "status",
            "user",
            "user_id",
            "created_at",
        ]


# Bidding ===============================


# Basic nested serializers for referenced objects (adjust fields to your actual models)
class SimpleContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = (
            serializers.get_model("contracts", "Contract") if False else None
        )  # placeholder


# Instead of trying to import unknown models dynamically, import real ones:


class BiddingParticipantSerializer(serializers.ModelSerializer):
    subcontractor = SubcontractorSerializer(read_only=True)
    subcontractor_id = serializers.PrimaryKeyRelatedField(
        queryset=Subcontractor.objects.all(), source="subcontractor", write_only=True
    )

    class Meta:
        model = BiddingParticipant
        fields = [
            "id",
            "subcontractor",
            "subcontractor_id",
            "offered_price",
            "conditions",
            "status",
            "replied_status",
            "proposal",
            "in_short_list",
            "mail_subject",
            "mail_body",
            "replied_at",
            "created_at",
        ]


class BiddingSerializer(serializers.ModelSerializer):
    contract = ContractSerializer(read_only=True)
    contract_id = serializers.PrimaryKeyRelatedField(
        queryset=Contract.objects.all(),
        source="contract",
        write_only=True,
        required=False,
        allow_null=True,
    )
    construction_object = ConstructionObjectSerializer(read_only=True)
    construction_object_id = serializers.PrimaryKeyRelatedField(
        queryset=ConstructionObject.objects.all(),
        source="construction_object",
        write_only=True,
        required=False,
        allow_null=True,
    )
    rfq = RFQSerializer(read_only=True)
    rfq_id = serializers.PrimaryKeyRelatedField(
        queryset=RFQ.objects.all(),
        source="rfq",
        write_only=True,
        required=False,
        allow_null=True,
    )

    participants = BiddingParticipantSerializer(many=True, read_only=True)
    # For writing participants in one go, accept participants_payload
    participants_payload = serializers.ListField(
        child=serializers.DictField(), write_only=True, required=False
    )

    created_by = serializers.SerializerMethodField()

    class Meta:
        model = Bidding
        fields = [
            "id",
            "title",
            "description",
            "contract",
            "contract_id",
            "construction_object",
            "construction_object_id",
            "rfq",
            "rfq_id",
            "subcontractors",
            "participants",
            "participants_payload",
            "start_date",
            "end_date",
            "status",
            "created_by",
            "created_at",
        ]
        read_only_fields = ["subcontractors", "participants", "created_at"]

    def get_created_by(self, obj):
        user = obj.created_by
        if not user:
            return None
        return {
            "id": user.id,
            "email": getattr(user, "email", ""),
            "full_name": getattr(user, "full_name", ""),
        }

    def create(self, validated_data):
        participants_payload = validated_data.pop("participants_payload", [])
        bidding = super().create(validated_data)
        # create participants if provided
        for p in participants_payload:
            subcontractor = Subcontractor.objects.get(id=p.get("subcontractor_id"))
            BiddingParticipant.objects.create(
                bidding=bidding,
                subcontractor=subcontractor,
                offered_price=p.get("offered_price"),
                conditions=p.get("conditions", ""),
                status=p.get("status", "submitted"),
                replied_status=p.get("replied_status", "pending"),
                proposal=p.get("proposal", ""),
                in_short_list=p.get("in_short_list", False),
                mail_subject=p.get("mail_subject", ""),
                mail_body=p.get("mail_body", "")
            )
        return bidding

    def update(self, instance, validated_data):
        participants_payload = validated_data.pop("participants_payload", None)
        instance = super().update(instance, validated_data)
        if participants_payload is not None:
            # replace participants: naive approach - delete existing and create new ones
            instance.participants.all().delete()
            for p in participants_payload:
                subcontractor = Subcontractor.objects.get(id=p.get("subcontractor_id"))
                BiddingParticipant.objects.create(
                    bidding=instance,
                    subcontractor=subcontractor,
                    offered_price=p.get("offered_price"),
                    conditions=p.get("conditions", ""),
                    status=p.get("status", "submitted"),
                    replied_status=p.get("replied_status", "pending"),
                    proposal=p.get("proposal", ""),
                    in_short_list=p.get("in_short_list", False),
                    mail_subject=p.get("mail_subject", ""),
                    mail_body=p.get("mail_body", "")
                )
        return instance
