from django.db import models


class CompanyAbuse(models.Model):
    company_name = models.CharField('Название компании', max_length=255)
    abuse_type   = models.CharField('Категория жалобы', max_length=255)
    description  = models.TextField('Комментарий пользователя', blank=True, null=True)
    created_at   = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self) -> str:
        return self.company_name

    class Meta:
        db_table = 'company_abuse'
        verbose_name = 'Жалоба'
        verbose_name_plural = 'Жалобы'
