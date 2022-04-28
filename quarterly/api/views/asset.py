import uuid
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, DeleteView
from django.urls import reverse_lazy

from api.models import Asset, Portfolio


class AssetCreate(LoginRequiredMixin, CreateView):
    model = Asset
    fields = ('ticker', 'name', 'holdings')
    template_name = 'api/create_assets.html'

    def form_valid(self, form):
        portfolio_id = uuid.UUID(self.request.get_full_path().split('/')[2])
        form.instance.portfolio = Portfolio.objects.get(id=portfolio_id)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # add all assets related to this portfolio
        portfolio_id = uuid.UUID(self.request.get_full_path().split('/')[2])
        portfolio = Portfolio.objects.filter(id=portfolio_id)
        if portfolio.exists():
            assets = Asset.objects.filter(portfolio=portfolio.get(id=portfolio_id))
            context['assets'] = assets
            context['portfolio'] = portfolio.get(id=portfolio_id)
        else:
            context['assets'] = []
            context['portfolio'] = None

        return context

    def get_success_url(self):
        portfolio_id = uuid.UUID(self.request.get_full_path().split('/')[2])
        return reverse_lazy('create_assets', kwargs={'pk': portfolio_id})


class AssetDelete(LoginRequiredMixin, DeleteView):
    model = Asset
    context_object_name = 'asset'
    template_name = 'api/confirm_delete_asset.html'

    def get_queryset(self):
        asset_id = uuid.UUID(self.request.get_full_path().split('/')[2])
        return super().get_queryset().filter(id=asset_id)

    def get_success_url(self):
        portfolio_id = self.object.portfolio.id
        return reverse_lazy('create_assets', kwargs={'pk': portfolio_id})
