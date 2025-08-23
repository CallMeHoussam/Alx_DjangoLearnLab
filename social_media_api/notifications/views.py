from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Notification
from .serializers import NotificationSerializer, NotificationUpdateSerializer

class NotificationListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['created_at', 'is_read']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)

class NotificationDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationUpdateSerializer
    
    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)
    
    def perform_update(self, serializer):
        instance = self.get_object()
        if not instance.is_read:
            instance.mark_as_read()

class NotificationMarkAllReadView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
        return Response({'message': 'All notifications marked as read'})

class UnreadNotificationCountView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        count = Notification.objects.filter(recipient=request.user, is_read=False).count()
        return Response({'unread_count': count})