from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status, permissions

from api import models as api_models
from api import serializers as api_serializers
from api import utils as api_utils

from xuser.responses import u_responses
from xuser import utils as xuser_utils


class BlogPostViewSet(ModelViewSet):
   
    queryset = api_models.BlogPost.objects.all()
    serializer_class = api_serializers.ReadBlogPostSerializer
    write_serializer_class = api_serializers.CreateBlogPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        
        return self.queryset.all()
    
    def get_permissions(self):
        if self.action.lower() in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = self.permission_classes

        x =  [permission() for permission in permission_classes]
        return x
    
    def create(self, request, *args, **kwargs):

        request.data['author'] = str(self.request.user.id)
        is_slug, slug = api_utils.create_blog_slug(request.data.get('title'))
        if not is_slug:
            return Response(
                data=u_responses.user_error_response(message=slug),
                status=status.HTTP_400_BAD_REQUEST,
            )
        request.data['slug'] = slug
        
        try:
            serializer = self.write_serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response(
                data=u_responses.user_error_response(message=xuser_utils.handle_serializer_errors(serializer_error=serializer.errors)),
                status=status.HTTP_400_BAD_REQUEST,
            )

        is_blog, blog_post = serializer.create(validated_data=serializer.validated_data, author=request.user)
        if not is_blog:
            return Response(
                data=u_responses.user_error_response(message=blog_post),
                status=status.HTTP_400_BAD_REQUEST,
            )
                
        success_response = {"message": "Blog created successfully", "data": blog_post}
        return Response(
            data=u_responses.user_success_response(data=success_response),
            status=status.HTTP_201_CREATED,
        )


    def list(self, request, *args, **kwargs):

        try:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.serializer_class(queryset, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.serializer_class(queryset, many=True)
            success_response = {
                "message": "Successfully fetched blog posts",
                "data": serializer.data
            }
            
            return Response(
                    data=u_responses.user_success_response(data=success_response),
                    status=status.HTTP_200_OK,
                )
        except Exception as e:
            return Response(
                data=u_responses.user_error_response(message="Unable to fetch blog posts"),
                status=status.HTTP_400_BAD_REQUEST,
            )

    def retrieve(self, request, *args, **kwargs):

        try:
            instance = self.get_object()
            serializer = self.serializer_class(instance)
            data = serializer.data

            success_response = {
                "message": "Successfully fetched blog post",
                "data": data
            }

            return Response(
                data=u_responses.user_success_response(data=success_response),
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                data=u_responses.user_error_response(message="Unable to retrieve blog post"),
                status=status.HTTP_400_BAD_REQUEST,
            )
    
    # def destroy(self, request, *args, **kwargs):

    #     try:
    #         instance = self.get_object()
    #     except Exception as get_instance_error:
    #        return Response(
    #             data=u_responses.user_error_response(message="Unable to get user profile"),
    #             status=status.HTTP_400_BAD_REQUEST,
    #         )
        
    #     instance.delete()

    #     return Response(status=status.HTTP_204_NO_CONTENT)
    
