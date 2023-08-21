from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from apps.news.models.news import News, NewsImage
from apps.news.models.actions import Actions, ActionsPartner


class NewsListView(ListView):
    model = News
    queryset = News.objects.filter(active=True).order_by('-updated')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Новости'
        context['page_meta_description'] = 'Новости Группы Компаний Монолит'

        # Object list pagination
        paginator = Paginator(context['object_list'], 11)
        page = self.request.GET.get('page')
        try:
            context['object_list'] = paginator.page(page)
        except PageNotAnInteger:
            context['object_list'] = paginator.page(1)
        except EmptyPage:
            context['object_list'] = paginator.page(paginator.num_pages)
        # END Object list pagination

        return context


class NewsDetailView(DetailView):
    model = News
    queryset = News.objects.filter(active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['opts'] = News._meta
        context['news_images'] = NewsImage.objects.filter(news=self.get_object().pk)
        context['other_news'] = News.objects.filter(active=True).exclude(id=self.get_object().pk).order_by('?')[:6]
        return context


class ActionsListView(ListView):
    model = Actions
    queryset = Actions.objects.filter(active=True).order_by('-date_start')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Акции'
        context['page_meta_description'] = 'Действующие акции Группы Компаний Монолит'
        return context


class ActionsDetailView(DetailView):
    model = Actions
    queryset = Actions.objects.filter(active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['opts'] = Actions._meta
        context['page_title'] = f'{self.get_object().title}'
        context['action_partners'] = ActionsPartner.objects.filter(action=self.get_object().pk)
        context['other_actions'] = Actions.objects.filter(active=True).exclude(id=self.get_object().pk).order_by('?')[:4]        
        return context
