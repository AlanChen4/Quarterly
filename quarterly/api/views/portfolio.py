from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormMixin
from django.urls import reverse_lazy

from api.forms import PortfolioForm
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


class PortfolioDetail(LoginRequiredMixin, FormMixin, DetailView):
    model = Portfolio
    form_class = PortfolioForm
    content_object_name = 'portfolio'
    template_name = 'api/edit_portfolio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # add all assets linked to this portfolio
        context['assets'] = Asset.objects.filter(portfolio=self.object)

        return context

    def get_initial(self):
        initial = super().get_initial()
        
        initial['nickname'] = self.object.nickname
        initial['description'] = self.object.description

        return initial


class PortfolioCreate(LoginRequiredMixin, CreateView):
    model = Portfolio
    fields = ('nickname', 'description')
    template_name = 'api/create_portfolio.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('create_assets', kwargs={'pk': self.object.id})


class PortfolioDelete(LoginRequiredMixin, DeleteView):
    model = Portfolio
    template_name = 'api/confirm_delete_portfolio.html'

    def get_queryset(self):
        portfolio_id = self.kwargs['pk']
        return super().get_queryset().filter(user=self.request.user, id=portfolio_id)

    def get_success_url(self):
        return reverse_lazy('portfolios')