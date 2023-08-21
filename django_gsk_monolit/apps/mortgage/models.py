from django.db import models

from django.utils.html import mark_safe
from django.core.validators import MaxValueValidator, MinValueValidator, FileExtensionValidator
from ckeditor.fields import RichTextField

from apps.core.classes.file_processing import FileProcessing
from apps.core.classes.singleton_model import SingletonModel

from apps.realty.models.object import Object


class WayToBuy(SingletonModel):
    military = models.ManyToManyField(Object, verbose_name='Военная ипотека', related_name='mortgage_object_military', blank=True, help_text='Выберите Объекты подходящие под военную ипотеку')
    mother   = models.ManyToManyField(Object, verbose_name='Материнский капитал', related_name='mortgage_object_mother', blank=True, help_text='Выберите Объекты подходящие под материнский капитал')

    def __str__(self):
        return 'Способы покупки (Военная ипотека, Материнский капитал)'

    class Meta:
        verbose_name = 'Способы покупки (Военная ипотека, Материнский капитал)'
        verbose_name_plural = 'Способы покупки (Военная ипотека, Материнский капитал)'


def logo_upload_path(instance, filename):
    filename = FileProcessing(filename)
    filename = filename.newFileNameFromField(instance.name, None, 'logo')
    return 'mortgage/banks/{filename}'.format(filename=filename)

class Bank(models.Model):
    name = models.CharField('Название банка', unique=True, max_length=255)
    logo = models.FileField('Логотип банка (svg, png)', validators=[FileExtensionValidator(['svg', 'png'])], upload_to=logo_upload_path, blank=True, null=True)

    # Thumbnails for admin
    def logo_admin_thumb(self):
        return mark_safe('<img src="{}" alt="" style="width: 256px; height: auto;" />'.format(self.logo.url))
    logo_admin_thumb.short_description = 'Thumbnail'
    # END Thumbnails for admin

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Банк'
        verbose_name_plural = 'Банки'


class Offer(models.Model):
    bank                 = models.ForeignKey(Bank, verbose_name='Банк', on_delete=models.CASCADE)
    title                = models.CharField('Название программы', max_length=255, help_text='Название ипотечного кредита')

    # Первоначальный взнос
    first_payment_from   = models.DecimalField('от', max_digits=4, decimal_places=2, blank=True, null=True)
    first_payment_to     = models.DecimalField('до', max_digits=4, decimal_places=2, blank=True, null=True)

    # Срок кредита
    loan_term_from       = models.PositiveIntegerField('от', validators=[MinValueValidator(1), MaxValueValidator(50)], blank=True, null=True)
    loan_term_to         = models.PositiveIntegerField('до', validators=[MinValueValidator(1), MaxValueValidator(50)], blank=True, null=True)

    # Проецентная ставка
    rate_from            = models.DecimalField('от', max_digits=4, decimal_places=2, blank=True, null=True)
    rate_to              = models.DecimalField('до', max_digits=4, decimal_places=2, blank=True, null=True)

    description          = RichTextField('Описание', blank=True, null=True, help_text='Описание и дополнительные условия')
    object               = models.ManyToManyField(Object, verbose_name='Объект(ы)', blank=True, help_text='Выберите Объекты подходящие под данную ипотечную программу')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Ипотечная программа'
        verbose_name_plural = 'Ипотечные программы'

    # Первоначальный взнос
    def first_payment_dispaly(self):
        self.first_payment_from = str(round(self.first_payment_from, 1)).replace('.0', '')
        self.first_payment_to   = str(round(self.first_payment_to, 1)).replace('.0', '')

        if self.first_payment_from == self.first_payment_to:
            return f'{self.first_payment_from}%'
        elif self.first_payment_from and self.first_payment_to:
            return f'{self.first_payment_from} &ndash; {self.first_payment_to}%'
        elif not self.first_payment_to:
            return f'от {self.first_payment_from}%'
        elif not self.first_payment_from:
            return f'до {self.first_payment_to}%'

    # Срок кредита
    def loan_term_display(self):
        self.loan_term_from = str(round(self.loan_term_from, 1)).replace('.0', '')
        self.loan_term_to   = str(round(self.loan_term_to, 1)).replace('.0', '')

        if self.loan_term_from == self.loan_term_to:
            return f'{self.loan_term_from} лет'
        elif self.loan_term_from and self.loan_term_to:
            return f'{self.loan_term_from} &ndash; {self.loan_term_to} лет'
        elif not self.loan_term_to:
            return f'от {self.loan_term_from} лет'
        elif not self.loan_term_from:
            return f'до {self.loan_term_to} лет'

    # Проецентная ставка
    def rate_display(self):
        self.rate_from = str(round(self.rate_from, 1)).replace('.0', '')
        self.rate_to   = str(round(self.rate_to, 1)).replace('.0', '')

        if self.rate_from == self.rate_to:
            return f'{self.rate_from}%'
        elif self.rate_from and self.rate_to:
            return f'{self.rate_from} &ndash; {self.rate_to}%'
        elif not self.rate_to:
            return f'от {self.rate_from}%'
        elif not self.rate_from:
            return f'до {self.rate_to}%'
