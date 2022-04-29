from django.urls import path
from .views import *


urlpatterns = [
    path('', PortfolioList.as_view(), name='portfolios'),
    path('portfolio/', PortfolioCreate.as_view(), name='create_portfolio'),
    path('portfolio/<uuid:pk>/', PortfolioUpdate.as_view(), name='update_portfolio'),
    path('portfolio/<uuid:pk>/delete/', PortfolioDelete.as_view(), name='delete_portfolio'),

    path('assets/<uuid:pk>/create/', AssetCreate.as_view(), name='create_asset'),
    path('assets/<uuid:pk>/create/function', AssetCreateFunctionView, name='create_asset_function'),
    path('assets/<uuid:pk>/update/', AssetUpdate, name='update_asset'),

    path('review/', ReviewCreate.as_view(), name='create_review'),
    path('review/<uuid:pk>/', ReviewDetail.as_view(), name='review'),
]