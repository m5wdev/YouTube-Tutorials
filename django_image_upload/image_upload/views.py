from django.shortcuts import render, redirect

from .models import Image
from .forms import ImageUploadForm, ResizeImageForm

import PIL

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from urllib.request import urlopen
from io import BytesIO


def images_homepage_view(request):
    context = {
        "page_title": "Homepage",
        "objects_list": Image.objects.filter(active=True).order_by('modified_image').reverse()
    }

    # Delete original_img_url from session
    if request.session.get('image_id'):
        del request.session['image_id']
        request.session.modified = True
    if request.session.get('original_img_url'):
        del request.session['original_img_url']
        request.session.modified = True
    if request.session.get('original_img_path'):
        del request.session['original_img_path']
        request.session.modified = True

    return render(request, "homepage.html", context)


def image_upload_view(request):
    context = {
        "page_title": "Upload Image",
    }

    if request.POST:
        form = ImageUploadForm(request.POST, request.FILES)

        if form.is_valid():
            image     = form.cleaned_data['image']
            image_url = form.cleaned_data['image_url']

            # TODO: if image or image_url

            # Save to Object
            image = Image(extended_image=image)
            image.save()

            # Write original_img_url to session
            request.session['image_id'] = image.id
            request.session['original_img_url'] = image.extended_image.url
            request.session.modified = True

            return redirect('image:sizing')
        else:
            context['form'] = form
    else:
        form = ImageUploadForm()
        context['form'] = form

    return render(request, "images_upload/upload.html", context)


def image_sizing_view(request):
    context = {
        "page_title": "Sizing Image",
    }

    if request.POST:
        form = ResizeImageForm(request.POST)

        if form.is_valid():
            width  = form.cleaned_data['width']
            if width:
                width = int(form.cleaned_data['width'])
            print(f"form width {width}")

            height = form.cleaned_data['height']
            if height:
                height = int(form.cleaned_data['height'])
            print(f"form height {height}")

            image_id = request.session.get('image_id')
            original_img_url = request.session.get('original_img_url')

            # Generate temp file
            site_url = f"{request.scheme}://{request.get_host()}"
            # image_url = 'http://127.0.0.1:8000' + original_img_url
            image_url = f"{site_url}{original_img_url}"

            img_temp = NamedTemporaryFile()
            img_temp.write(urlopen(image_url).read())
            img_temp.flush()

            # Save to model
            iu = Image.objects.get(id=image_id)
            iu.active = True
            iu.modified_image.save(f"image_{iu.pk}.jpg", File(img_temp))
            iu.save()

            # Modify image with Pillow
            response = urlopen(image_url).read()

            im_pil = PIL.Image.open(BytesIO(response))

            print(f"image_width {im_pil.size[0]}")
            print(f"image_height {im_pil.size[1]}")

            # TODO: if height
            # TODO: if width and height

            # if width
            if width and height is None:
                calc_width    = int((float(im_pil.size[0]) / 100) * width)
                # calc proportion
                width_percent = (calc_width / float(im_pil.size[0]))
                calc_height   = int((float(im_pil.size[1]) * float(width_percent)))

                print(f"calc_width {calc_width}")
                print(f"calc_height {calc_height}")

                im_pil = im_pil.resize((calc_width, calc_height), PIL.Image.ANTIALIAS)
                # im_pil.save(iu.modified_image.path, 'JPEG')
            else:
                # im_pil = im_pil.resize((256, 256), PIL.Image.ANTIALIAS)
                im_pil = im_pil.resize((int(im_pil.size[0]), int(im_pil.size[1])), PIL.Image.ANTIALIAS)
            im_pil.save(iu.modified_image.path, 'JPEG')

            return redirect('image:homepage')
        else:
            context['form'] = form
    else:
        form = ResizeImageForm()
        context['form'] = form

    return render(request, "images_upload/sizing.html", context)