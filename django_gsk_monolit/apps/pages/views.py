from django.views.generic import DetailView, TemplateView

from apps.pages.models import Pages


class PageDetailView(DetailView):
    model = Pages
    queryset = Pages.objects.filter(active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['opts'] = Pages._meta
        context['page_title'] = self.get_object().title
        return context
