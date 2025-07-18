"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from marketplace.views import (
    PostViewSet,
    ProductViewSet,
    ChatViewSet,
    MessageViewSet,
    ReviewViewSet,
    FavoriteViewSet,
    ReportViewSet,
    NotificationViewSet,
    CurrencyViewSet,
    UserViewSet, TypeMessageViewSet, MessageStatusViewSet,
)
from marketplace.views import RegisterView, UnitViewSet, TypePostViewSet, PostStatusViewSet, CategoriePostViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'posts', PostViewSet, basename='post')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'chats', ChatViewSet, basename='chat')
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'favorites', FavoriteViewSet, basename='favorite')
router.register(r'reports', ReportViewSet, basename='report')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'currencies', CurrencyViewSet, basename='currency')
router.register(r'units', UnitViewSet, basename='unit')
router.register(r'typepost' ,TypePostViewSet, basename='typepost')
router.register(r'categoriepost' ,CategoriePostViewSet, basename='categoriepost')
router.register(r'poststatus', PostStatusViewSet, basename='poststatus')
router.register(r'typemessage', TypeMessageViewSet, basename='typemessage')
router.register(r'messagestatus', MessageStatusViewSet, basename='messagestatus')

urlpatterns = [
    path('', RedirectView.as_view(url='/swagger/', permanent=False)),
    # Auth JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Inscription
    path('api/register/', RegisterView.as_view(), name='register'),

    # API REST via router
    path('api/', include(router.urls)),
]
