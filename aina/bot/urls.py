from django.conf.urls import include, url
from .views import AinaBotView
urlpatterns = [
                  url(r'^main/?$', AinaBotView.as_view())

               ]