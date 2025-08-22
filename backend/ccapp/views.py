from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, viewsets
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer, UserSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .models import Contract, Subcontractor, RFQ
from .serializers import ContractSerializer, SubcontractorSerializer, RFQSerializer
from rest_framework import generics


User = get_user_model()

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class UserListView(APIView):
    # permission_classes = [permissions.AllowAny]  # Optional: only allow logged-in users
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
class UserDetailView(APIView):
    #permission_classes = [permissions.AllowAny]  # Or [permissions.IsAuthenticated] if you want auth
    # permission_classes = [IsAuthenticated]
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    def put(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

class UserMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
# Contract ============================
class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [permissions.AllowAny]

    # def get_queryset(self):
    #     return Contract.objects.all()

# Subcontractor =======================

class SubcontractorViewSet(viewsets.ModelViewSet):
    queryset = Subcontractor.objects.all().order_by('-created_at')
    serializer_class = SubcontractorSerializer
    permission_classes = [permissions.AllowAny]

# RFQs ================================

class RFQListCreateView(generics.ListCreateAPIView):
    queryset = RFQ.objects.all()
    serializer_class = RFQSerializer


class RFQDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RFQ.objects.all()
    serializer_class = RFQSerializer

# Email with Attachments ====================

import io
from django.core.mail import EmailMessage
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from .models import RFQ

def send_rfq_email(request, rfq_id):
    rfq = RFQ.objects.select_related("user", "subcontractor").get(id=rfq_id)

    # 1) Generate PDF in memory
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 800, "Request for Quotation (RFQ)")
    p.setFont("Helvetica", 12)
    p.drawString(100, 770, f"Title: {rfq.title}")
    p.drawString(100, 750, f"Description: {rfq.description}")
    p.drawString(100, 730, f"Estimated Cost: {rfq.estimated_cost}")
    p.drawString(100, 710, f"Due Date: {rfq.due_date}")
    p.showPage()
    p.save()
    buffer.seek(0)

    # 2) Create Email
    subject = f"RFQ #{rfq.id} - {rfq.title}"
    body = f"""
Hello {rfq.subcontractor.contact_person},

Please find attached the RFQ document for "{rfq.title}".

Best regards,  
Contact Helicon
"""
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email="noreply@helicon.com",
        to=[rfq.subcontractor.email],
    )

    # 3) Attach PDF
    email.attach(f"rfq_{rfq.id}.pdf", buffer.getvalue(), "application/pdf")

    # 4) Send Email
    email.send()

    return HttpResponse({"status": "Email sent with PDF"})