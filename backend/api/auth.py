from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from core.serializers import UserSerializer, EmployeeSerializer
import uuid

User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        # Create user with verification token
        verification_token = str(uuid.uuid4())
        user = serializer.save(
            is_active=False,
            verification_token=verification_token
        )
        
        # Send verification email
        send_verification_email(user.email, verification_token)
        
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'message': 'Please check your email to verify your account'
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def candidate_register(request):
    data = request.data.copy()
    data['is_employee'] = False
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        verification_token = str(uuid.uuid4())
        user = serializer.save(
            is_active=False,
            verification_token=verification_token
        )
        send_verification_email(user.email, verification_token)
        
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'message': 'Please check your email to verify your account'
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def verify_email(request):
    token = request.query_params.get('token')
    try:
        user = User.objects.get(verification_token=token)
        user.is_active = True
        user.verification_token = ''
        user.save()
        return Response({'message': 'Email verified successfully'})
    except User.DoesNotExist:
        return Response(
            {'error': 'Invalid verification token'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

def send_verification_email(email, token):
    verification_url = f"{settings.FRONTEND_URL}/verify-email?token={token}"
    send_mail(
        'Verify your email',
        f'Please click this link to verify your email: {verification_url}',
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    try:
        user = User.objects.get(email=email)
        if not user.is_active:
            return Response(
                {'error': 'Please verify your email first'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        if user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user_type': 'employee' if user.is_employee else 'candidate'
            })
        else:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_400_BAD_REQUEST
            )
    except User.DoesNotExist:
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_400_BAD_REQUEST
        )