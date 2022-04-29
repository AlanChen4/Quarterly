from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Max
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from api.models import Asset, Portfolio, Review


class ReviewCreate(LoginRequiredMixin, CreateView):
    model = Review
    fields = ('description',)
    template_name = 'api/create_review.html'

    def _get_valid_portfolio(self):
        """
        Return respective portfolio to write review on to the context
        
        Sort by:
        - Number of reviews
        - To be added...

        Exclude:
        - Portfolios that are your own
        - Portfolios you've already reviewed before
        """
        portfolios = Portfolio.objects.all() \
                    .annotate(num_reviews=Count('review')) \
                    .order_by('num_reviews')

        # exclude portfolios that are your own
        portfolios = portfolios.exclude(user=self.request.user)

        # only keep portfolios you haven't reviewed before
        for review in Review.objects.filter(author=self.request.user):
            portfolios = portfolios.exclude(id=review.portfolio.id)

        # select first portfolio to meet all conditions
        return portfolios[0] if len(portfolios) > 0 else None


    def dispatch(self, request, *args, **kwargs):
        self.portfolio = self._get_valid_portfolio()
        self.assets = Asset.objects.filter(portfolio=self.portfolio) if self.portfolio is not None else None

        return super(ReviewCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        print('portfolio', self.portfolio)
        form.instance.portfolio = self.portfolio

        return super().form_valid(form)

    def get_context_data(self):
        context = super().get_context_data()
        context['portfolio'] = self.portfolio
        context['assets'] = self.assets

        return context

    def get_success_url(self):
        return reverse_lazy('portfolios')


class ReviewDetail(LoginRequiredMixin, DetailView):
    model = Review
    template_name = 'api/detail_review.html'

    def get_context_data(self, **kwargs):
        portfolio = self.object.portfolio
        assets = Asset.objects.all().filter(portfolio=portfolio.id)

        context = super().get_context_data()
        context['portfolio'] = portfolio
        context['assets'] = assets

        return context