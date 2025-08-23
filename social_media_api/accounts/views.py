from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from .models import CustomUser  # Make sure to import CustomUser
from ..posts.serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer
from .serializers import FollowActionSerializer, UserProfileWithFollowInfoSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    if request.method == 'GET':
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request):
    serializer = FollowActionSerializer(data=request.data)
    if serializer.is_valid():
        user_id = serializer.validated_data['user_id']
        user_to_follow = get_object_or_404(CustomUser.objects.all(), id=user_id)
        
        if request.user.follow(user_to_follow):
            return Response({
                'message': f'You are now following {user_to_follow.username}'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Cannot follow this user'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow_user(request):
    serializer = FollowActionSerializer(data=request.data)
    if serializer.is_valid():
        user_id = serializer.validated_data['user_id']
        user_to_unfollow = get_object_or_404(CustomUser.objects.all(), id=user_id)
        
        if request.user.unfollow(user_to_unfollow):
            return Response({
                'message': f'You have unfollowed {user_to_unfollow.username}'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Cannot unfollow this user'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FollowUserView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FollowActionSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            user_to_follow = get_object_or_404(CustomUser.objects.all(), id=user_id)
            
            if request.user.follow(user_to_follow):
                return Response({
                    'message': f'You are now following {user_to_follow.username}'
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': 'Cannot follow this user'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FollowActionSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            user_to_unfollow = get_object_or_404(CustomUser.objects.all(), id=user_id)
            
            if request.user.unfollow(user_to_unfollow):
                return Response({
                    'message': f'You have unfollowed {user_to_unfollow.username}'
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': 'Cannot unfollow this user'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FollowersListView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileWithFollowInfoSerializer
    
    def get(self, request):
        followers = request.user.followers.all()
        serializer = self.get_serializer(followers, many=True, context={'request': request})
        return Response(serializer.data)

class FollowingListView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileWithFollowInfoSerializer
    
    def get(self, request):
        following = request.user.following.all()
        serializer = self.get_serializer(following, many=True, context={'request': request})
        return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow_user(request):
    serializer = FollowActionSerializer(data=request.data)
    if serializer.is_valid():
        user_id = serializer.validated_data['user_id']
        user_to_unfollow = get_object_or_404(CustomUser, id=user_id)
        
        if request.user.unfollow(user_to_unfollow):
            return Response({
                'message': f'You have unfollowed {user_to_unfollow.username}'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Cannot unfollow this user'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_followers(request):
    followers = request.user.followers.all()
    serializer = UserProfileWithFollowInfoSerializer(followers, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_following(request):
    following = request.user.following.all()
    serializer = UserProfileWithFollowInfoSerializer(following, many=True, context={'request': request})
    return Response(serializer.data)