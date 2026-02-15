from django.db import models
from django.contrib.auth.models import User
from datetime import date


class pendingAccount(models.Model):
    username = models.CharField(max_length=100)
    firstName = models.CharField(max_length=100, null=True, blank=True)
    lastName = models.CharField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    authToken = models.CharField(max_length=100)
    joinAt = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Pending Account"
        verbose_name_plural = "Pending Accounts"

    def __str__(self):
        return str(self.username)


class memberBasic(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    firstName = models.CharField(max_length=100, null=True, blank=True)
    lastName = models.CharField(max_length=100, null=True, blank=True)
    memberProfilePhoto = models.ImageField(null=True, blank=True, upload_to="images/ProfilePhoto/")
    memberCoverPhoto = models.ImageField(null=True, blank=True, upload_to="images/CoverPhoto/")
    memberDivision = models.CharField(max_length=50, null=True, blank=True)
    memberDistrict = models.CharField(max_length=50, null=True, blank=True)
    memberBirthDate = models.DateField(blank=True, null=True)
    about = models.CharField(max_length=500, blank=True, null=True)
    joinAt = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = "Member Basic"
        verbose_name_plural = "Member Basics"

    def memberAge(self):
        if self.memberBirthDate is None:
            return None
        today = date.today()
        return today.year - self.memberBirthDate.year

    def __str__(self):
        return str(self.username)


class memberPhoneNumber(models.Model):
    userName = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    phoneNumber = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = "Member Phone Number"
        verbose_name_plural = "Member Phone Numbers"

    def __str__(self):
        return str(self.userName)


class websiteType(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)
    websitelogo = models.ImageField(upload_to="logo/website/")

    class Meta:
        verbose_name = "Website Type"
        verbose_name_plural = "Website Types"

    def __str__(self):
        return str(self.name)


class memberWebsite(models.Model):
    userName = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    type = models.ForeignKey(websiteType, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = "Member Website"
        verbose_name_plural = "Member Websites"

    def __str__(self):
        return str(self.userName) + '|' + str(self.type)
