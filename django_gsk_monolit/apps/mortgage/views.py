from django.views.generic import TemplateView
from django.db.models import Q
from apps.mortgage.models import Offer, WayToBuy


class MortgageView(TemplateView):
    template_name = 'mortgage/mortgage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Ипотека'
        context['mortgage_offers'] = Offer.objects.all().order_by('title')
        return context


class MortgageCorporactiveView(TemplateView):
    template_name = 'mortgage/corporactive.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Корпорактив'
        return context


class MortgageMilitaryView(TemplateView):
    template_name = 'mortgage/military.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Военная ипотека'

        # Check if object id=1 in WayToBuy exists and military is not None
        context['objects_military'] = None
        if WayToBuy.objects.filter(id=1).exists() and WayToBuy.objects.filter( ~Q(military=None) ):
            way_to_buy = WayToBuy.objects.get(id=1)
            context['objects_military'] = way_to_buy.military.filter(all_sold=False)

        return context


class MortgageMotherView(TemplateView):
    template_name = 'mortgage/mother.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Материнский капитал'
        return context
