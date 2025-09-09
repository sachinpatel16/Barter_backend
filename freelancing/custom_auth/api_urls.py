from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView # type: ignore

from freelancing.custom_auth import api
# from trade_time_accounting.custom_auth.api import UserAccessPermissionAPIView

router = routers.SimpleRouter()
router.register("v1/auth", api.UserAuthViewSet, basename="auth")
router.register("v1/users", api.UserViewSet, basename="users")
# router.register("v1/custom_permission", api.CustomPermissionViewSet, basename="custom_permission")

#Merchant Profile
router.register("v1/merchant_profile", api.MerchantProfileViewSet, basename="merchant_profile")

#Wallet
router.register("v1/wallet", api.WalletViewSet, basename="wallet")

router.register("v1/category", api.CategoryViewSet, basename="category")
app_name = "custom-auth"

urlpatterns = [
    # JWT Token Endpoints
    # path('v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('v1/user_access_permissions/', UserAccessPermissionAPIView.as_view(), name='user-access-permissions'),
    # path("v1/user/reset/", api.SendPasswordResetEmailView.as_view(), name="user_reset"),
    # path(
    #     "v1/user/reset/<uid>/<token>/",
    #     api.UserPasswordResetView.as_view(),
    #     name="user_reset_view",
    # ),
    path("v1/wallet/history/", api.WalletHistoryListView.as_view(), name="wallet-history"),
    path("v1/wallet/summary/", api.WalletSummaryView.as_view(), name="wallet-summary"),
    path('v1/merchants/list/', api.MerchantListAPIView.as_view(), name='merchant-list'),
    
    # Razorpay Wallet APIs
    path("v1/wallet/razorpay/create-order/", api.RazorpayWalletAPIView.as_view(), name="razorpay-create-order"),
    path("v1/wallet/razorpay/verify-payment/", api.RazorpayPaymentVerificationAPIView.as_view(), name="razorpay-verify-payment"),
    path("v1/wallet/razorpay/cancel-order/", api.RazorpayCancelOrderAPIView.as_view(), name="razorpay-cancel-order"),
    path("v1/wallet/razorpay/transactions/", api.RazorpayTransactionListView.as_view(), name="razorpay-transactions"),
    
    # Merchant Deal System URLs
    path("v1/merchant-deals/", api.MerchantDealViewSet.as_view({'get': 'list', 'post': 'create'}), name="merchant-deals"),
    path("v1/merchant-deals/<int:pk>/", api.MerchantDealViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name="merchant-deal-detail"),
    path("v1/merchant-deals/<int:pk>/activate/", api.MerchantDealViewSet.as_view({'post': 'activate'}), name="merchant-deal-activate"),
    path("v1/merchant-deals/<int:pk>/deactivate/", api.MerchantDealViewSet.as_view({'post': 'deactivate'}), name="merchant-deal-deactivate"),
    path("v1/merchant-deals/<int:pk>/usage-history/", api.MerchantDealViewSet.as_view({'get': 'usage_history'}), name="merchant-deal-usage-history"),
    
    path("v1/deal-discovery/", api.DealDiscoveryViewSet.as_view({'get': 'list'}), name="deal-discovery"),
    path("v1/deal-discovery/by-points/", api.DealDiscoveryViewSet.as_view({'get': 'by_points'}), name="deal-discovery-by-points"),
    
    path("v1/deal-requests/", api.MerchantDealRequestViewSet.as_view({'get': 'list', 'post': 'create'}), name="deal-requests"),
    path("v1/deal-requests/<int:pk>/", api.MerchantDealRequestViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name="deal-request-detail"),
    path("v1/deal-requests/<int:pk>/accept/", api.MerchantDealRequestViewSet.as_view({'post': 'accept'}), name="deal-request-accept"),
    path("v1/deal-requests/<int:pk>/reject/", api.MerchantDealRequestViewSet.as_view({'post': 'reject'}), name="deal-request-reject"),
    
    path("v1/deal-confirmations/", api.MerchantDealConfirmationViewSet.as_view({'get': 'list', 'post': 'create'}), name="deal-confirmations"),
    path("v1/deal-confirmations/<int:pk>/", api.MerchantDealConfirmationViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name="deal-confirmation-detail"),
    path("v1/deal-confirmations/<int:pk>/complete/", api.MerchantDealConfirmationViewSet.as_view({'post': 'complete'}), name="deal-confirmation-complete"),
    path("v1/deal-confirmations/<int:pk>/usage-history/", api.MerchantDealConfirmationViewSet.as_view({'get': 'usage_history'}), name="deal-confirmation-usage-history"),
    
    path("v1/merchant-notifications/", api.MerchantNotificationViewSet.as_view({'get': 'list', 'post': 'create'}), name="merchant-notifications"),
    path("v1/merchant-notifications/<int:pk>/", api.MerchantNotificationViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name="merchant-notification-detail"),
    path("v1/merchant-notifications/<int:pk>/mark-read/", api.MerchantNotificationViewSet.as_view({'post': 'mark_read'}), name="merchant-notification-mark-read"),
    path("v1/merchant-notifications/mark-all-read/", api.MerchantNotificationViewSet.as_view({'post': 'mark_all_read'}), name="merchant-notification-mark-all-read"),
    path("v1/merchant-notifications/unread-count/", api.MerchantNotificationViewSet.as_view({'get': 'unread_count'}), name="merchant-notification-unread-count"),
    
    path("v1/deal-stats/", api.DealStatsViewSet.as_view({'get': 'list'}), name="deal-stats"),
    
    # Loyalty System URLs
    path("v1/visit-tracking/", api.UserVisitTrackingViewSet.as_view({'get': 'list', 'post': 'create'}), name="visit-tracking"),
    path("v1/visit-tracking/track-visit/", api.UserVisitTrackingViewSet.as_view({'post': 'track_visit'}), name="track-visit"),
    path("v1/visit-tracking/<int:pk>/", api.UserVisitTrackingViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name="visit-tracking-detail"),
    
    path("v1/loyalty-programs/", api.MerchantLoyaltyProgramViewSet.as_view({'get': 'list', 'post': 'create'}), name="loyalty-programs"),
    path("v1/loyalty-programs/<int:pk>/", api.MerchantLoyaltyProgramViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name="loyalty-program-detail"),
    path("v1/loyalty-programs/stats/", api.MerchantLoyaltyProgramViewSet.as_view({'get': 'stats'}), name="loyalty-program-stats"),
    
    path("v1/loyalty-rewards/", api.UserLoyaltyRewardViewSet.as_view({'get': 'list', 'post': 'create'}), name="loyalty-rewards"),
    path("v1/loyalty-rewards/<int:pk>/", api.UserLoyaltyRewardViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name="loyalty-reward-detail"),
    path("v1/loyalty-rewards/<int:pk>/use/", api.UserLoyaltyRewardViewSet.as_view({'post': 'use_reward'}), name="use-loyalty-reward"),
    path("v1/loyalty-rewards/give-manual/", api.UserLoyaltyRewardViewSet.as_view({'post': 'give_manual_reward'}), name="give-manual-reward"),
    
    # Comprehensive History APIs
    path("v1/history/point-history/", api.ComprehensiveHistoryViewSet.as_view({'get': 'point_history'}), name="comprehensive-point-history"),
    path("v1/history/merchant-point-flow/", api.ComprehensiveHistoryViewSet.as_view({'get': 'merchant_point_flow'}), name="merchant-point-flow"),
    path("v1/history/reward-usage-history/", api.ComprehensiveHistoryViewSet.as_view({'get': 'reward_usage_history'}), name="reward-usage-history"),
    path("v1/history/merchant-reward-given/", api.ComprehensiveHistoryViewSet.as_view({'get': 'merchant_reward_given'}), name="merchant-reward-given"),

    path("", include(router.urls))
]
