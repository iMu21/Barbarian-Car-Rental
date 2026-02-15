from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q, Sum, Count
import uuid

from .models import memberWebsite, pendingAccount, memberBasic, memberPhoneNumber, websiteType
from .forms import (
    LoginForm, SignUpForm, VerificationForm, ProfileEditForm,
    PhoneNumberForm, WebsiteForm,
)
from shop.models import SuperCategory, Car, Booking, Favorite


class SuperCategoryMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['superCategory'] = SuperCategory.objects.all()
        if self.request.user.is_authenticated:
            context['favorites_count'] = Favorite.objects.filter(user=self.request.user).count()
        return context


class DashboardView(LoginRequiredMixin, SuperCategoryMixin, TemplateView):
    template_name = 'member/dashboard.html'
    login_url = '/member/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        bookings = Booking.objects.filter(user=user).select_related('car')
        active_bookings = bookings.filter(status__in=['pending', 'confirmed', 'active'])
        past_bookings = bookings.filter(status__in=['completed', 'cancelled'])

        stats = bookings.aggregate(
            total_spent=Sum('total_cost'),
            booking_count=Count('id'),
        )

        context['active_bookings'] = active_bookings
        context['past_bookings'] = past_bookings
        context['total_spent'] = stats['total_spent'] or 0
        context['booking_count'] = stats['booking_count'] or 0
        context['favorites_total'] = Favorite.objects.filter(user=user).count()
        return context


class ProfileView(LoginRequiredMixin, SuperCategoryMixin, TemplateView):
    template_name = 'member/profile.html'
    login_url = '/member/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = get_object_or_404(memberBasic, username=self.request.user)
        context['member'] = member
        context['memberPhone'] = memberPhoneNumber.objects.filter(userName=self.request.user)
        context['website'] = memberWebsite.objects.filter(userName=self.request.user)
        return context


class ProfileEditView(LoginRequiredMixin, SuperCategoryMixin, TemplateView):
    template_name = 'member/profileEdit.html'
    login_url = '/member/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = get_object_or_404(memberBasic, username=self.request.user)
        context['member'] = member
        context['form'] = ProfileEditForm(instance=member)
        return context

    def post(self, request, *args, **kwargs):
        member = get_object_or_404(memberBasic, username=request.user)
        form = ProfileEditForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
        return redirect('member:profile')


class PhoneAddView(LoginRequiredMixin, SuperCategoryMixin, TemplateView):
    template_name = 'member/phoneAdd.html'
    login_url = '/member/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PhoneNumberForm()
        return context

    def post(self, request, *args, **kwargs):
        form = PhoneNumberForm(request.POST)
        if form.is_valid():
            phone = form.save(commit=False)
            phone.userName = request.user
            phone.save()
            messages.success(request, 'Your phone number has been saved.')
        return redirect('member:profile')


class PhoneEditView(LoginRequiredMixin, SuperCategoryMixin, TemplateView):
    template_name = 'member/phoneEdit.html'
    login_url = '/member/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        phone = get_object_or_404(memberPhoneNumber, pk=self.kwargs['pk'], userName=self.request.user)
        context['phone'] = phone
        context['form'] = PhoneNumberForm(instance=phone)
        return context

    def post(self, request, *args, **kwargs):
        phone = get_object_or_404(memberPhoneNumber, pk=kwargs['pk'], userName=request.user)
        form = PhoneNumberForm(request.POST, instance=phone)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your phone number has been updated.')
        return redirect('member:profile')


class PhoneDeleteView(LoginRequiredMixin, View):
    login_url = '/member/login/'

    def get(self, request, pk):
        phone = get_object_or_404(memberPhoneNumber, pk=pk, userName=request.user)
        phone.delete()
        messages.warning(request, 'Your number has been deleted.')
        return redirect('member:profile')


class WebsiteAddView(LoginRequiredMixin, SuperCategoryMixin, TemplateView):
    template_name = 'member/websiteAdd.html'
    login_url = '/member/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = WebsiteForm()
        context['websiteType'] = websiteType.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        form = WebsiteForm(request.POST)
        if form.is_valid():
            website = form.save(commit=False)
            website.userName = request.user
            website.save()
            messages.success(request, 'Your website address has been saved.')
        return redirect('member:profile')


class WebsiteEditView(LoginRequiredMixin, SuperCategoryMixin, TemplateView):
    template_name = 'member/websiteEdit.html'
    login_url = '/member/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        website = get_object_or_404(memberWebsite, pk=self.kwargs['pk'], userName=self.request.user)
        context['website'] = website
        context['form'] = WebsiteForm(instance=website)
        return context

    def post(self, request, *args, **kwargs):
        website = get_object_or_404(memberWebsite, pk=kwargs['pk'], userName=request.user)
        form = WebsiteForm(request.POST, instance=website)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your {website.type} address has been updated.')
        return redirect('member:profile')


class WebsiteDeleteView(LoginRequiredMixin, View):
    login_url = '/member/login/'

    def get(self, request, pk):
        website = get_object_or_404(memberWebsite, pk=pk, userName=request.user)
        website.delete()
        messages.warning(request, 'Your website address has been deleted.')
        return redirect('member:profile')


class SignUpView(SuperCategoryMixin, TemplateView):
    template_name = 'member/signUp.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SignUpForm()
        return context

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            token = str(uuid.uuid4())
            obj = pendingAccount.objects.create(
                username=cd['username'],
                firstName=cd['firstName'],
                lastName=cd['lastName'],
                email=cd['email'],
                authToken=token,
                password=cd['password'],
            )
            send_verification_email(cd['email'], token)
            return redirect('member:verification')
        else:
            for error in form.non_field_errors():
                messages.error(request, error)
            for field, errors in form.errors.items():
                if field != '__all__':
                    for error in errors:
                        messages.error(request, error)
            return redirect('member:signup')


class VerificationView(SuperCategoryMixin, TemplateView):
    template_name = 'member/signUpConfirmation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = VerificationForm()
        return context

    def post(self, request, *args, **kwargs):
        form = VerificationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            token = cd['token']
            email = cd['email']
            pending = pendingAccount.objects.filter(authToken=token, email=email).first()
            if pending:
                user = User.objects.create(username=pending.username, email=pending.email)
                user.set_password(pending.password)
                user.save()
                memberBasic.objects.create(
                    username=user,
                    firstName=pending.firstName,
                    lastName=pending.lastName,
                    joinAt=pending.joinAt,
                )
                pendingAccount.objects.filter(email=email).delete()
                pendingAccount.objects.filter(username=user.username).delete()
                messages.success(request, 'Signed Up successfully. Log In here.')
                return redirect('member:login')
        messages.error(request, 'Incorrect Email or Verification Code')
        return redirect('member:verification')


class LoginView(SuperCategoryMixin, TemplateView):
    template_name = 'member/logIn.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = LoginForm()
        return context

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = cd['username']
            password = cd['password']

            user_obj = User.objects.filter(username=username).first()
            if user_obj is None:
                messages.error(request, 'User not found.')
                return redirect('member:login')

            profile_obj = pendingAccount.objects.filter(username=username).first()
            if profile_obj:
                messages.error(request, 'Profile is not verified, check your mail.')
                return redirect('member:login')

            user = authenticate(username=username, password=password)
            if user is None:
                messages.error(request, 'Wrong password.')
                return redirect('member:login')

            login(request, user)
            return redirect('member:profile')

        return redirect('member:login')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('member:login')


class SearchView(SuperCategoryMixin, TemplateView):
    template_name = 'shop/search.html'

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_key = self.request.POST.get('search_key', '') or self.request.GET.get('search_key', '')
        keywords = search_key.split()

        if keywords:
            q = Q()
            for word in keywords:
                q |= Q(car_name__icontains=word)
            data = Car.objects.filter(q)
        else:
            data = Car.objects.none()

        context['data'] = data
        context['empty'] = 0 if data.exists() else 1
        return context


def send_verification_email(email, token):
    subject = "Email confirmation for Barbarian Car Rental"
    message = f"This is your verification code: {token}"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
