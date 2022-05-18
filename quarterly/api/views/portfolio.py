from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.middleware.csrf import get_token
from django.views.generic.base import TemplateView
from django.views.generic.edit import DeleteView
from django.views.generic.list import ListView
from django.urls import reverse, reverse_lazy

from api.forms import AssetFormSet, PortfolioForm, PortfolioFormAnon
from api.models import Asset, Portfolio, Review


class PortfolioList(LoginRequiredMixin, ListView):
    model = Portfolio
    context_object_name = 'portfolios'
    template_name = 'api/portfolios.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # add all reviews for portfolios belonging to this account to the context
        reviews = []
        portfolios = Portfolio.objects.filter(user=self.request.user)
        for portfolio in portfolios:
            reviews_for_portfolio = Review.objects.filter(portfolio=portfolio)
            if reviews_for_portfolio.count() > 0:
                for review in reviews_for_portfolio:
                    reviews.append(review)
        context['reviews'] = reviews

        return context

    def get_queryset(self):
        return Portfolio.objects.all().filter(user=self.request.user)


class PortfolioUpdate(LoginRequiredMixin, TemplateView):
    model = Portfolio
    template_name = 'api/update_portfolio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        portfolio = Portfolio.objects.get(id=self.kwargs['pk'])
        assets = Asset.objects.filter(portfolio=portfolio)

        context['portfolio'] = portfolio
        context['portfolio_form'] = PortfolioForm(initial={
            'nickname': portfolio.nickname,
            'risk_tolerance': portfolio.risk_tolerance,
            'description': portfolio.description,
        })
        context['asset_formset'] = AssetFormSet(initial=[{
            'ticker': asset.ticker,
            'name': asset.name,
            'holdings': asset.holdings
        } for asset in assets])
        context['my_csrf_token'] = get_token(self.request)

        return context

    def get_success_url(self):
        return reverse_lazy('update_portfolio', kwargs={'pk': self.kwargs['pk']}) 


@login_required
def PortfolioUpdateFunction(request, **kwargs):
    if request.method == 'POST':
        post_data = request.POST

        # update portfolio
        portfolio = Portfolio.objects.get(id=kwargs['pk'])
        portfolio.nickname = post_data['nickname']
        portfolio.risk_tolerance = post_data['risk_tolerance']
        portfolio.description = post_data['description']
        portfolio.save()

        # delete all assets and then re-add the new ones
        assets = Asset.objects.filter(portfolio=portfolio)
        assets.delete()

        for i in range(0, len(post_data.keys())):
            ticker_key = f"form-{i}-ticker"
            name_key = f"form-{i}-name"
            holdings_key = f"form-{i}-holdings"

            if ticker_key not in post_data or post_data[ticker_key] == '':
                break

            Asset.objects.create(
                portfolio=portfolio,
                ticker=str(post_data[ticker_key]),
                name=str(post_data[name_key]),
                holdings=float(post_data[holdings_key])
            )

        return HttpResponseRedirect(reverse('update_portfolio', kwargs={'pk': kwargs['pk']}))
    else:
        return HttpResponse(status=405)


class PortfolioCreate(TemplateView):
    model = Portfolio
    template_name = 'api/create_portfolio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['asset_formset'] = AssetFormSet
        context['my_csrf_token'] = get_token(self.request)
        context['portfolio_form'] = PortfolioForm

        return context

    def get_success_url(self):
        return reverse_lazy('portfolios')


class PortfolioCreateAnon(TemplateView):
    template_name = 'api/create_portfolio_anon.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['asset_formset'] = AssetFormSet
        context['my_csrf_token'] = get_token(self.request)
        context['portfolio_form'] = PortfolioFormAnon

        return context


class PortfolioReviews(TemplateView):
    template_name = 'api/portfolio_reviews.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        portfolio = Portfolio.objects.get(id=self.kwargs['pk'])
        context['portfolio'] = portfolio
        context['reviews'] = Review.objects.filter(portfolio=portfolio)

        return context


def PortfolioCreateFunction(request):
    if request.method == 'POST':
        post_data = request.POST

        # create portfolio
        portfolio = Portfolio.objects.create(
            user=request.user if request.user.is_authenticated else None,
            nickname='Anonymous',
            risk_tolerance=str(post_data['risk_tolerance']),
            description=str(post_data['description'])
        )

        # add assets
        for i in range(0, len(post_data.keys())):
            ticker_key = f"form-{i}-ticker"
            name_key = f"form-{i}-name"
            holdings_key = f"form-{i}-holdings"

            if ticker_key not in post_data:
                break

            Asset.objects.create(
                portfolio=portfolio,
                ticker=str(post_data[ticker_key]),
                name=str(post_data[name_key]),
                holdings=float(post_data[holdings_key])
            )

        if post_data['anonymous'] == 'True':
            return HttpResponseRedirect(reverse('portfolio_reviews', kwargs={'pk': portfolio.id}))
        return HttpResponseRedirect(reverse('portfolios'))
    else:
        return HttpResponse(status=405)


class PortfolioDelete(LoginRequiredMixin, DeleteView):
    model = Portfolio
    template_name = 'api/confirm_delete_portfolio.html'

    def get_queryset(self):
        portfolio_id = self.kwargs['pk']
        return super().get_queryset().filter(user=self.request.user, id=portfolio_id)

    def get_success_url(self):
        return reverse_lazy('portfolios')