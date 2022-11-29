from django.urls import path
from .views import *
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('register/', create_user),
    path('login/', obtain_auth_token), # WTF???
    path('logout/', logout_view),

    # path('all/', list_user),
    path('all/', ListUserView.as_view()),

    path('profile/', profile),
    path('update/', update_user),
    path('change_password/', change_password),

    path('account/<user_viewed_pk>/', view_account),

    # password reset
    path('send_code/', send_code),

    path('reset_password/', reset_password),

]