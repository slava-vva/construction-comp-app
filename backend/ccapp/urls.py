from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

from rest_framework_simplejwt.views import TokenRefreshView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = DefaultRouter()
router.register(r'contracts', ContractViewSet)
router.register(r'subcontractors', SubcontractorViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'messages', MessageListViewSet)
router.register(r'chat-users', ChatUserViewSet)
router.register(r"construction-objects", ConstructionObjectViewSet, basename="constructionobject")
router.register(r"biddings", BiddingViewSet, basename="bidding")

# urlpatterns = [    path('', include(router.urls)),]


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login_s/', LoginView.as_view(), name='login'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path("users/email/<str:email>/", UserDetailView.as_view(), name="user-detail-by-email"),
    # path('me/', current_user),
    path('me/', UserMeView.as_view(), name='user-me'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('rfqs/', RFQListCreateView.as_view(), name='rfq-list'),
    path('rfqs/<int:pk>/', RFQDetailView.as_view(), name='rfq-detail'),
    path("telegram/fetch/", fetch_telegram, name="telegram-fetch"),
    path("telegram/send/", send_telegram, name="telegram-send"),
    path("telegram/poll/", telegram_poll, name="telegram_poll"),
    
]

urlpatterns += router.urls