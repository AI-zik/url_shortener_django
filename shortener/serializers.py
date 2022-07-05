from django.urls import reverse
from rest_framework import serializers
from .models import ShortenedLink


class ShortenedLinkSerializer(serializers.ModelSerializer):
    short_url = serializers.SerializerMethodField("get_full_url", read_only=True)

    class Meta:
        model = ShortenedLink
        fields = "__all__"

    def get_full_url(self, obj):
        request = self.context["request"]
        return request.build_absolute_uri(reverse('redirect', kwargs={"slug" : obj.slug}))