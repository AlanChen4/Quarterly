from django.urls import path
from .views import *


urlpatterns = [
    path('', PortfolioList.as_view(), name='portfolios'),
    path('portfolio/', PortfolioCreate.as_view(), name='create_portfolio'),
    path('portfolio/create/', PortfolioCreateFunction, name='create_portfolio_function'),
    path('portfolio/anon/', PortfolioCreateAnon.as_view(), name='create_portfolio_anon'),
    path('portfolio/<uuid:pk>/', PortfolioUpdate.as_view(), name='update_portfolio'),
    path('portfolio/<uuid:pk>/reviews/', PortfolioReviews.as_view(), name='portfolio_reviews'),
    path('portfolio/<uuid:pk>/update/', PortfolioUpdateFunction, name='update_portfolio_function'),
    path('portfolio/<uuid:pk>/delete/', PortfolioDelete.as_view(), name='delete_portfolio'),

    path('assets/<uuid:pk>/create/', AssetCreate.as_view(), name='create_asset'),
    path('assets/<uuid:pk>/create/function/', AssetCreateFunctionView, name='create_asset_function'),
    path('assets/<uuid:pk>/delete/', AssetDelete, name='delete_asset'),

    path('review/portfolios/', PickPortfolio.as_view(), name='pick_portfolio'),
    path('review/<uuid:portfolio_id>/create/', ReviewCreate.as_view(), name='create_review'),
    path('reviews/', ReviewList.as_view(), name='reviews'),
    path('review/<uuid:pk>/', ReviewDetail.as_view(), name='review'),
    path('review/<uuid:pk>/rate/', RateReview, name='rate_review'),

    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
]