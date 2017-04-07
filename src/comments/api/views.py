from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import authentication, permissions

from comments.models import Comment

from .serializers import CommentSerializer

class CommentListAPIView(generics.ListAPIView):
    serializer_class = CommentSerializer
    # authentication_classes = []
    permission_classes = []

    def get_queryset(self, *args, **kwargs):
        url = self.request.GET.get("url")
        if url:
            return Comment.objects.filter(url=url)
        return Comment.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        response = Response(serializer.data)
        response.set_cookie('isUser', 'false')
        if request.user.is_authenticated():
            response.set_cookie('isUser', 'true')
        return response



class CommentCreateAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        if self.request.user.is_authenticated():
            serializer.save(user=self.request.user)




