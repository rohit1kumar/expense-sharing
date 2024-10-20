from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import User
from .serializers import UserSerializer
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated


class UserView(viewsets.ViewSet):
    """
    Create and Retrieve user details.
    """

    def get_permissions(self):
        """
        Allow any user to create a new user, but only authenticated users can view user details.
        """
        if self.action == "create":
            return []
        return [IsAuthenticated()]

    def create(self, request):
        """
        Create a new user.
        """
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["get"], url_path="current-user")
    def current_user(self, request, pk=None):
        """
        Get current user details.
        """
        user = get_object_or_404(User, id=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)
