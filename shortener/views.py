import random
import string
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import RedirectView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import ShortenedLinkSerializer
from .models import ShortenedLink

def get_random_string(length):
    available_chars = string.ascii_letters + string.digits
    result = "".join(random.choice(available_chars) for i in range(length))
    return result

class RedirectShortLinkView(RedirectView):

    permanent = True

    def get_redirect_url(*args, **kwargs):
        slug = kwargs["slug"]
        address = get_object_or_404(ShortenedLink, slug=slug)
        return address.url

@method_decorator(csrf_exempt, name='dispatch')
class ManageShortenedLinkView(APIView):

    def post(self, request, format=None):
        data = request.data
        length = random.randint(6, 10)
        data["slug"] = get_random_string(length)


        slug = data["slug"]
        is_taken = True

        # checking to see whether the slug is already used or if the slug 
        # matches the create the url view. 
        while is_taken or data["slug"] == reverse('manage_links')[:-1]:
            if data["slug"] == reverse('manage_links')[:-1]:
                data["slug"] = get_random_string(length)

            else:
                try:
                    valid_link = ShortenedLink.objects.get(slug=data["slug"])
                except:
                    is_taken = False
                    data["slug"] = get_random_string(length)

        serializer = ShortenedLinkSerializer(data=data, context={'request' : request})
        if serializer.is_valid():
            try:
                link = ShortenedLink.objects.get(url=data["url"])
            except:
                serializer.save()
            else:
                serializer = ShortenedLinkSerializer(link, context={'request' : request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)