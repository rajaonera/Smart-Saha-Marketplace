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
from django.urls import path, include, re_path
from django.views.generic import RedirectView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from marketplace.models import permissions
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
    UserViewSet,
    TypeMessageViewSet,
    MessageStatusViewSet,
    SemenceViewSet
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
router.register(r'semences', SemenceViewSet, basename='semence')
router.register(r'category_semences', CategoriePostViewSet, basename='category_semence')

schema_view = get_schema_view(
    openapi.Info(
        title="Smart Saha API",
        default_version='v1',
        description="Documentation de l'API Smart Saha",
        terms_of_service="https://www.smart_saha.com/terms/",
        contact=openapi.Contact(email="hugueszeus@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', RedirectView.as_view(url='/swagger/', permanent=False)),
    # Auth JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Inscription
    path('api/register/', RegisterView.as_view(), name='register'),

    # API REST via router
    path('api/', include(router.urls)),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]
