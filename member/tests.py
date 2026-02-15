from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import memberBasic, memberPhoneNumber, websiteType, memberWebsite


class MemberBasicModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass1234')
        self.member = memberBasic.objects.create(username=self.user, firstName='Test', lastName='User')

    def test_str(self):
        self.assertEqual(str(self.member), 'testuser')

    def test_member_age_null_guard(self):
        self.assertIsNone(self.member.memberAge())

    def test_member_age_with_date(self):
        from datetime import date
        self.member.memberBirthDate = date(2000, 1, 1)
        self.member.save()
        age = self.member.memberAge()
        self.assertIsNotNone(age)
        self.assertGreater(age, 0)


class MemberPhoneNumberModelTest(TestCase):
    def test_str(self):
        user = User.objects.create_user(username='testuser', password='testpass1234')
        phone = memberPhoneNumber.objects.create(userName=user, phoneNumber='01234567890')
        self.assertEqual(str(phone), 'testuser')


class LoginViewTest(TestCase):
    def test_login_page_loads(self):
        response = self.client.get(reverse('member:login'))
        self.assertEqual(response.status_code, 200)

    def test_login_with_valid_credentials(self):
        user = User.objects.create_user(username='testuser', password='testpass1234')
        memberBasic.objects.create(username=user)
        response = self.client.post(reverse('member:login'), {
            'username': 'testuser',
            'password': 'testpass1234',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('member:profile'))

    def test_login_with_wrong_password(self):
        User.objects.create_user(username='testuser', password='testpass1234')
        response = self.client.post(reverse('member:login'), {
            'username': 'testuser',
            'password': 'wrongpass',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('member:login'))


class ProfileViewTest(TestCase):
    def test_profile_requires_login(self):
        response = self.client.get(reverse('member:profile'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/member/login/', response.url)

    def test_profile_loads_authenticated(self):
        user = User.objects.create_user(username='testuser', password='testpass1234')
        memberBasic.objects.create(username=user, firstName='Test', lastName='User')
        self.client.login(username='testuser', password='testpass1234')
        response = self.client.get(reverse('member:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')


class SignUpViewTest(TestCase):
    def test_signup_page_loads(self):
        response = self.client.get(reverse('member:signup'))
        self.assertEqual(response.status_code, 200)


class PhoneViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass1234')
        memberBasic.objects.create(username=self.user)
        self.client.login(username='testuser', password='testpass1234')

    def test_phone_add_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse('member:phone_add'))
        self.assertEqual(response.status_code, 302)

    def test_phone_add_loads(self):
        response = self.client.get(reverse('member:phone_add'))
        self.assertEqual(response.status_code, 200)

    def test_phone_add_post(self):
        response = self.client.post(reverse('member:phone_add'), {'phoneNumber': '01234567890'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(memberPhoneNumber.objects.filter(userName=self.user).exists())


class WebsiteViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass1234')
        memberBasic.objects.create(username=self.user)
        self.wt = websiteType.objects.create(name='GitHub')
        self.client.login(username='testuser', password='testpass1234')

    def test_website_add_loads(self):
        response = self.client.get(reverse('member:website_add'))
        self.assertEqual(response.status_code, 200)

    def test_website_add_post(self):
        response = self.client.post(reverse('member:website_add'), {
            'address': 'https://github.com/testuser',
            'type': self.wt.pk,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(memberWebsite.objects.filter(userName=self.user).exists())
