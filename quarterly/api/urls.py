from django.urls import path
from .views import *


urlpatterns = [
    path('', PortfolioList.as_view(), name='portfolios'),
    path('portfolio/', PortfolioCreate.as_view(), name='create_portfolio'),
    path('portfolio/<uuid:pk>/', PortfolioDetail.as_view(), name='edit_portfolio'),
    path('portfolio/<uuid:pk>/delete/', PortfolioDelete.as_view(), name='delete_portfolio'),

    path('assets/<uuid:pk>/', AssetCreate.as_view(), name='create_assets'),
    path('assets/<uuid:pk>/delete/', AssetDelete.as_view(), name='delete_asset'),
]