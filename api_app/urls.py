from django.urls import path
from .views import *


urlpatterns = [
    path('navbar/create/', create_navabar),
    path('navbar/all/', get_all_navbars),


    path('navbar_child/create/', create_navabar_child),
    path('navbar_child/all/', get_all_navbar_childs),

]
