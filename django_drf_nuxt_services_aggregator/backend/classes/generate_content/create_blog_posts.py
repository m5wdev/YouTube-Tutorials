from apps.blog.models import Blog


class CreateBlogPosts:
    title        = 'Blog Post'
    description  = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. A erat nam at lectus. Aliquet porttitor lacus luctus accumsan tortor posuere ac ut. Venenatis lectus magna fringilla urna porttitor rhoncus dolor purus non. Sed faucibus turpis in eu.\n\nLorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. A erat nam at lectus. Aliquet porttitor lacus luctus accumsan tortor posuere ac ut. Venenatis lectus magna fringilla urna porttitor rhoncus dolor purus non. Sed faucibus turpis in eu.'

    meta_title = 'blog meta title'
    meta_descr = 'blog meta description'
    group_name = '1'

    create_qty = 10
    count_in_db = Blog.objects.all().count()


    @classmethod
    def create_record(cls, counter):
        new_post = Blog()
        new_post.title = f'{cls.title} {counter}'
        new_post.description = cls.description
        new_post.meta_title  = cls.meta_title
        new_post.meta_descr  = cls.meta_descr
        new_post.group_name  = cls.group_name
        new_post.save()
        print('Blog Post Created!', new_post.title)


    @classmethod
    def fill_db(cls, qty=create_qty):
        start = 0

        # if cls.count_in_db > 0:
        if cls.count_in_db == 0:
            start = cls.count_in_db
            qty += cls.count_in_db

            for i in range(start, qty):
                cls.create_record(i)
