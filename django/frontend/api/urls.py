from django.urls import path

from .views import FrontListView

urlpatterns = [path('', FrontListView.as_view())]
