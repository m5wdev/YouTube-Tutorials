"""
    Stop logging recent actions in admin

    Usage example:

        class BlogAdmin(TurnOffAdminLogging, admin.ModelAdmin):
            ...
"""


class TurnOffAdminLogging:
    def log_addition(self, *args):
        return

    def log_change(self, *args):
        return

    def log_deletion(self, *args):
        return
