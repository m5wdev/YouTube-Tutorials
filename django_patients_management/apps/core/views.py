# from django.shortcuts import render
from django.views.generic import TemplateView


class HomepageView(TemplateView):
    template_name = 'pages/homepage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Главная'
        return context
