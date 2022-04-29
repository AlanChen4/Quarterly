from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Max
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from api.models import Asset, Portfolio, Review


class ReviewCreate(LoginRequiredMixin, CreateView):
    model = Review
    fields = ('description',)
    template_name = 'api/create_review.html'
    portfolio = Portfolio.objects.all() \
                .annotate(num_reviews=Count('review')) \
                .order_by('num_reviews')[0]

    assets = Asset.objects.filter(portfolio=portfolio)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.portfolio = self.portfolio

        return super().form_valid(form)

    def get_context_data(self):
        """
        Add respective portfolio to write review on to the context
        
        The portfolio to show will be sorted by, in this order:
        - Number of reviews
        - To be added...
        """
        context = super().get_context_data()
        context['portfolio'] = self.portfolio
        context['assets'] = self.assets

        return context

    def get_success_url(self):
        return reverse_lazy('portfolios')
