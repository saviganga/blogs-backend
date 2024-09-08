from rest_framework import serializers

from api import models as api_models
from api import utils as api_utils
from django.utils import timezone

from xuser import models as xuser_models


class CreateBlogPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = api_models.BlogPost
        fields = "__all__"

    def create(self, validated_data, author):

        title = validated_data.get('title', None)
        content = validated_data.get('content', None)
        slug = validated_data.get('slug')

        if title is None or content is None:
            return False, "Oops! title and content cannot be blank"

        
        drafts = [
            {
                "reference": api_utils.create_draft_reference(),
                "title": title,
                "content": content,
                "created_at": str(timezone.now()),
                "published_at": "",
                "published_by": ""
            }
        ]

        blog_post = self.Meta.model.objects.create(
            title=title,
            slug=slug,
            author=author,
            drafts=drafts
        )


        return True, ReadBlogPostSerializer(blog_post).data
        
class ReadBlogPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = api_models.BlogPost
        fields = "__all__"


class PublishBlogPostSerializer(serializers.Serializer):

    reference = serializers.CharField()

    def publish(self, validated_data, blog, user):

        try:
            valid_user = xuser_models.AdminUser.objects.get(id=user.id)
        except Exception as e:
            return False, "Oops! This feature is only available for admins"
        
        reference = validated_data.get('reference')

        draft = next( (d for d in blog.drafts if d.get('reference').lower() == reference.lower() ), None )
        if draft is None:
            return False, "Oops! draft with this reference not found"
        
        blog.content = draft.get('content')
        time_now = timezone.now()
        draft['published_at'] = str(time_now)
        draft['published_by'] = user.user_name
        blog.published_at = str(time_now)
        blog.is_published=True
        blog.save()

        return True, ReadBlogPostSerializer(blog).data






class UpdateBlogPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = api_models.BlogPost
        fields = ["content"]

    def update(self, validated_data, blog):

        blog_drafts = blog.drafts
        new_draft = {
            "reference": api_utils.create_draft_reference(),
            "title": blog.title,
            "content": validated_data.get('content'),
            "created_at": str(timezone.now()),
            "published_at": "",
            "published_by": ""
        }
        blog_drafts.insert(0, new_draft)
        blog.drafts = blog_drafts
        blog.save()
        return True, ReadBlogPostSerializer(blog).data
