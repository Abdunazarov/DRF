from django.urls import path
from .views import TestViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('Test/', TestViewset)

urlpatterns = [
    path('', )

]

