from django import forms


class ImageUploadForm(forms.Form):
    image_url = forms.CharField(required=False)
    image     = forms.ImageField(required=False)

    def clean(self):
        cleaned_data = super().clean()

        image     = cleaned_data.get('image')
        image_url = cleaned_data.get('image_url')

        if image is None and image_url == '':
            self.add_error('image', 'Загрузите файл!')
            self.add_error('image_url', '...или добавьте url изображения в данное поле!')

        if image != '' and image_url != '':
            self.add_error('image', 'Заполните только одно поле!')
            self.add_error('image_url', 'Заполните только одно поле!')

        return cleaned_data

    # def clean_image(self):
    #     cd = self.cleaned_data
    #     # if len(cd['first_name']) < 2:
    #     #     raise forms.ValidationError("First name can't be less than 2 characters")
    #     return cd['image']


class ResizeImageForm(forms.Form):
    width  = forms.IntegerField(required=False, max_value=99, help_text="% от текущей ширины")
    height = forms.IntegerField(required=False, max_value=99, help_text="% от текущей высоты")