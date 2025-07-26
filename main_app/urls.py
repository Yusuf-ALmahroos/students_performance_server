from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import RegisterView, LoginView, CourseViewSet, RecordViewSet, UserViewSet

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()

router.register(r'courses', CourseViewSet)
router.register(r'records', RecordViewSet)
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    # JWT endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #auth endpoints
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    #course and record endpoints
    path('', include(router.urls))
]