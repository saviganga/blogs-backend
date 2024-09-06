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

