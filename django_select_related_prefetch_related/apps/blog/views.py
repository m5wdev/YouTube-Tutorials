# from django.shortcuts import render

from django.db.models import Prefetch

from .utils import query_debugger
from .models import Blog, Communities


@query_debugger
def bld():
    # qs = Blog.objects.all()
    # qs = Blog.objects.select_related('category')
    # qs = Blog.objects.select_related('category').select_related('author')
    qs = Blog.objects.select_related('category', 'author')

    print(qs.query)

    posts = []
    for item in qs:
        posts.append({
            'id': item.id,
            'title': item.title,
            'slug': item.slug,
            'category': item.category,
            'body': item.body,
            'tags': item.tags,
            'author': item.author,
            'created': item.created,
            'updated': item.updated,
        })

    return posts


@query_debugger
def cld():
    # qs = Communities.objects.all()
    # qs = Communities.objects.prefetch_related('blog_posts')
    qs = Communities.objects.prefetch_related(
        Prefetch('blog_posts', queryset=Blog.objects.filter(tags__name__in=['Тег 1', 'Тег 2', 'Тег 3', 'Тег 4', 'Тег 5', 'Тег 6']))
        # Prefetch('blog_posts', queryset=Blog.objects.all())
    )

    print(qs.query)

    communities = []
    for item in qs:
        # blog_posts = [post.title for post in item.blog_posts.filter(tags__name__in=['Тег 1', 'Тег 2', 'Тег 3', 'Тег 4', 'Тег 5', 'Тег 6'])]
        blog_posts = [post.title for post in item.blog_posts.all()] # Prefetch

        # print(item.blog_posts.all())
        # print(blog_posts)

        communities.append({
            'id': item.id,
            'name': item.name,
            # 'blog_posts': item.blog_posts.all(),
            'blog_posts': blog_posts, # Prefetch
        })

    return communities
