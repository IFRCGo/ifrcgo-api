from django.contrib import admin
from api.logger import logger
from api.models import User
import registrations.models as models
from reversion_compare.admin import CompareVersionAdmin


class PendingAdmin(CompareVersionAdmin):
    search_fields = ('user__username', 'user__email', 'admin_contact_1', 'admin_contact_2')
    list_display = (
        'get_username_and_mail', 'created_at',
        'admin_contact_1', 'admin_1_validated', 'admin_1_validated_date',
        'admin_contact_2', 'admin_2_validated', 'admin_2_validated_date',
        'email_verified', 'user_is_active'
    )
    actions = ('activate_users',)

    # Get the 'user' objects with a JOIN query
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')

    def get_username_and_mail(self, obj):
        return obj.user.username + ' - ' + obj.user.email

    def user_is_active(self, obj):
        return 'Yes' if obj.user.is_active else ''

    def activate_users(self, request, queryset):
        for pu in queryset:
            usr = User.objects.filter(id=pu.user_id).first()
            if usr:
                if usr.is_active is False:
                    usr.is_active = True
                    usr.save()
                else:
                    logger.info(f'User {usr.username} was already active')
            else:
                logger.info(f'There is no User record with the ID: {pu.user_id}')

    def get_actions(self, request):
        actions = super(PendingAdmin, self).get_actions(request)
        if not request.user.is_superuser:
            del actions['activate_users']
        return actions


class DomainWhitelistAdmin(CompareVersionAdmin):
    list_display = ('domain_name', 'description', 'is_active')
    search_fields = ('domain_name',)
    ordering = ('domain_name',)


admin.site.register(models.Pending, PendingAdmin)
admin.site.register(models.DomainWhitelist, DomainWhitelistAdmin)
