from django.contrib import admin
from .models import memberBasic,memberPhoneNumber,pendingAccount,memberWebsite, websiteType

admin.site.register(memberBasic)
admin.site.register(memberPhoneNumber)
admin.site.register(pendingAccount)
admin.site.register(memberWebsite)
admin.site.register(websiteType)