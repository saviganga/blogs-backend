from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status, permissions
from rest_framework.decorators import action


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
            queryset = self.filter_queryset(self.get_queryset().filter(is_published=True))
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

    def update(self, request, *args, **kwargs):

        try:
            partial = kwargs.pop("partial", False)
            instance = self.get_object()
        except Exception as get_instance_error:
           return Response(
                data={
                    "status": "FAILED",
                    "message": "Unable to get blog post"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if request.user != instance.author:
            return Response(
                data={
                    "status": "FAILED",
                    "message": "Oops! This feature is only for blog authors"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        
        serializer = api_serializers.UpdateBlogPostSerializer(instance, data=request.data, partial=partial)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as validate_serializer_error:
            return Response(
                data={
                    "status": "FAILED",
                    "message": "Unable to get blog post",
                    "data": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        is_updated, updated_blog = serializer.update(validated_data=serializer.validated_data, blog=instance)
        if not is_updated:
            return Response(
                data={
                    "status": "FAILED",
                    "message": "Unable to update blog post"
                },
                status=status.HTTP_400_BAD_REQUEST
            )


        return Response(
            data={
                "status": "SUCCESS",
                "message": "Successfully updated user profile",
                "data": updated_blog
            },
            status=status.HTTP_200_OK
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

    @action(methods=["get"], detail=True)
    def drafts(self, request, pk=None):

        try:
            blog = self.get_object()
        except Exception as e:
            return Response(
                data=u_responses.user_error_response(message="Unable to retrieve blog post"),
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        if request.user != blog.author:
            return Response(
                data=u_responses.user_error_response(message="This feature is only available to blog authors"),
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        drafts = blog.get_drafts()

        return Response(
            data={
                "status": "SUCCESS",
                "message": "success",
                "data": drafts
            }
        )
    
    @action(methods=["post"], detail=True)
    def publish_draft(self, request, pk=None):
        

        try:
            serializer = api_serializers.PublishBlogPostSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response(
                data=u_responses.user_error_response(message=xuser_utils.handle_serializer_errors(serializer_error=serializer.errors)),
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            blog = self.get_object()
        except Exception as e:
            return Response(
                data=u_responses.user_error_response(message="Unable to retrieve blog post"),
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        is_published, published_draft = serializer.publish(validated_data=serializer.validated_data, blog=blog, user=request.user)
        if not is_published:


            return Response(
                data={
                    "status": "FAILED",
                    "message": published_draft
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(
            data={
                "status": "SUCCESS",
                "message": "success",
                "data": published_draft
            },
            status=status.HTTP_200_OK
        )
    
    @action(methods=["get"], detail=False)
    def unpublished(self, request, *args, **kwargs):

        try:
            if (request.headers.get('entity', None) is not None) and (request.headers.get('entity').lower() == 'admin'):
                queryset = self.filter_queryset(self.get_queryset())
            else:
                queryset = self.filter_queryset(self.get_queryset().filter(is_published=False, author__id=request.user.id))
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

    
    @action(methods=["get"], detail=False, permission_classes=[permissions.AllowAny])
    def health(self, request, pk=None):

        return Response(
                    data=u_responses.user_success_response(),
                    status=status.HTTP_200_OK,
                )

        






        
    
