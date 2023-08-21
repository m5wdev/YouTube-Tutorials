from django.db import models


class RepairApplication(models.Model):
    name       = models.CharField('Имя', max_length=255)
    phone      = models.CharField('Телефон', max_length=255)
    issue_type = models.CharField('Что сломалось', max_length=255)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = 'repair_applications'
        verbose_name = 'Заявка на ремонт'
        verbose_name_plural = 'Заявки на ремонт'
