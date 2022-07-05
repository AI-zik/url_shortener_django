from django.urls import path
from .views import RedirectShortLinkView, ManageShortenedLinkView

urlpatterns = [
    path("links/", ManageShortenedLinkView.as_view(), name="manage_links"),
    path("<str:slug>/", RedirectShortLinkView.as_view(), name="redirect")
]