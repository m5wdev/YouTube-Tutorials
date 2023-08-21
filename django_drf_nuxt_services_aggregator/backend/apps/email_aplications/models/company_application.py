from django.db import models


class CompanyApplication(models.Model):
    name         = models.CharField('Имя клиента', max_length=255)
    phone        = models.CharField('Телефон клиента', max_length=255)
    company_name = models.CharField('Название компании', max_length=255)
    issue_type   = models.CharField('Тип техники', max_length=255)
    description  = models.TextField('Описание поломки', blank=True, null=True)
    created_at   = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self) -> str:
        return self.company_name

    class Meta:
        db_table = 'company_applications'
        verbose_name = 'Заявка компании'
        verbose_name_plural = 'Заявки компаний'
