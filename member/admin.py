from django.contrib import admin
from .models import memberBasic, memberPhoneNumber, pendingAccount, memberWebsite, websiteType


@admin.register(memberBasic)
class MemberBasicAdmin(admin.ModelAdmin):
    list_display = ('username', 'firstName', 'lastName', 'memberDivision', 'memberDistrict', 'joinAt')
    search_fields = ('username__username', 'firstName', 'lastName')
    list_filter = ('memberDivision', 'memberDistrict')


@admin.register(memberPhoneNumber)
class MemberPhoneNumberAdmin(admin.ModelAdmin):
    list_display = ('userName', 'phoneNumber')
    search_fields = ('userName__username', 'phoneNumber')


@admin.register(pendingAccount)
class PendingAccountAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'joinAt')
    search_fields = ('username', 'email')


@admin.register(memberWebsite)
class MemberWebsiteAdmin(admin.ModelAdmin):
    list_display = ('userName', 'address', 'type')
    search_fields = ('userName__username', 'address')
    list_filter = ('type',)


@admin.register(websiteType)
class WebsiteTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
