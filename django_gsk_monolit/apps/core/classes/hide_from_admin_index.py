"""
    Hide model from admin index

    Usage example:

        class YourModelAdmin(HideFromAdminIndex, admin.ModelAdmin):
            ...
"""


class HideFromAdminIndex:
    def get_model_perms(self, request):
        return dict()
