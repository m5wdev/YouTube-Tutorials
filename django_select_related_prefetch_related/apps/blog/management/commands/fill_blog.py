import random
from django.core.management.base import BaseCommand

from apps.blog.models import Blog, Category, Tag, Communities


class Command(BaseCommand):
    def handle(self, *args, **options):
        Blog.objects.all().delete()
        Category.objects.all().delete()
        Tag.objects.all().delete()
        Communities.objects.all().delete()

        blog_template = {
            'body': '''We can put our signals in the Models module. But for signals we need to import some other modules which may have side-effects. So, it is a good idea to avoid putting it inside the models module or in the application root module.\n\nDjango Community recommends creating a separate file for signals and put it in an app confile file. See how I do it in bellow code.''',
        }

        blog_posts = [Blog(title=f"Публикация в блоге {i}", **blog_template) for i in range(1, 1001)]
        Blog.objects.bulk_create(blog_posts)

        categories = [Category(name=f"Категория {i}") for i in range(1, 6)]
        Category.objects.bulk_create(categories)

        tags = [Tag(name=f"Тег {i}") for i in range(1, 11)]
        Tag.objects.bulk_create(tags)

        tags_ids_list = list(Tag.objects.values_list('id', flat=True))

        communities = [Communities(name=f"Сообщество {i}") for i in range(1, 21)]
        Communities.objects.bulk_create(communities)

        for blog_post in Blog.objects.all():
            blog_post.category = Category.objects.order_by('?')[0]
            random_tag_ids = random.sample(tags_ids_list, random.randint(1, 5))
            blog_post.tags.set(random_tag_ids)
            blog_post.save()
            print(blog_post.title)

        for community in Communities.objects.all():
            blog_posts_ids_list = list(Blog.objects.values_list('id', flat=True))
            random_blog_ids = random.sample(blog_posts_ids_list, random.randint(1, 1000))
            community.blog_posts.set(random_blog_ids)
            community.save()
            print(community.name)
