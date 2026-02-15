from decimal import Decimal
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from .models import Car, SuperCategory, Category, Booking, Review, Favorite, Coupon
from .forms import RentalOrderForm, ReviewForm


class SuperCategoryMixin:
    def get_super_categories(self):
        return SuperCategory.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['superCategory'] = self.get_super_categories()
        if self.request.user.is_authenticated:
            context['favorites_count'] = Favorite.objects.filter(user=self.request.user).count()
        return context


class HomeView(SuperCategoryMixin, TemplateView):
    template_name = 'shop/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        super_categories = SuperCategory.objects.all()
        categorized_list = []

        for sc in super_categories:
            cars = Car.objects.filter(
                car_category__superCategory_name=sc
            ).select_related('car_category')

            if not cars.exists():
                continue

            car_list = list(cars)
            page_count = (len(car_list) + 2) // 3
            categorized_list.append((
                sc.superCategory_name,
                car_list,
                range(1, page_count),
                sc,
            ))

        context['product'] = categorized_list
        context['featured_cars'] = Car.objects.filter(is_featured=True).select_related('car_category')
        return context


class AboutView(SuperCategoryMixin, TemplateView):
    template_name = 'shop/about.html'


class ContactView(SuperCategoryMixin, TemplateView):
    template_name = 'shop/contact.html'


class ErrorView(SuperCategoryMixin, TemplateView):
    template_name = 'shop/error.html'


class ProductDetailView(SuperCategoryMixin, TemplateView):
    template_name = 'shop/productView.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = get_object_or_404(Car, pk=self.kwargs['pk'])
        context['product'] = product
        context['reviews'] = Review.objects.filter(car=product).select_related('user').order_by('-created_at')
        context['avg_rating'] = product.average_rating()
        context['review_count'] = product.review_count()

        if self.request.user.is_authenticated:
            context['is_favorited'] = Favorite.objects.filter(user=self.request.user, car=product).exists()
            context['has_reviewed'] = Review.objects.filter(user=self.request.user, car=product).exists()
            context['can_review'] = (
                not context['has_reviewed']
                and Booking.objects.filter(
                    user=self.request.user, car=product, status='completed'
                ).exists()
            )
        return context


class SuperCategoryDetailView(SuperCategoryMixin, TemplateView):
    template_name = 'shop/supercategory.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sc = get_object_or_404(SuperCategory, pk=self.kwargs['pk'])
        categories = Category.objects.filter(superCategory_name=sc)
        categorized_list = []

        for cat in categories:
            cars = Car.objects.filter(car_category=cat).select_related('car_category')
            if not cars.exists():
                continue
            car_list = list(cars)
            page_count = (len(car_list) + 3) // 4
            categorized_list.append((
                cat.category_name,
                car_list,
                range(1, page_count),
                cat,
            ))

        total_vehicles = sum(len(item[1]) for item in categorized_list)
        context['product'] = categorized_list
        context['Name'] = sc.superCategory_name
        context['supercategory'] = sc
        context['total_vehicles'] = total_vehicles
        context['category_count'] = len(categorized_list)
        context['empty'] = 1 if len(categorized_list) == 0 else 0
        return context


class CategoryDetailView(SuperCategoryMixin, TemplateView):
    template_name = 'shop/category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = get_object_or_404(Category, pk=self.kwargs['pk'])
        data = Car.objects.filter(car_category=cat)
        context['data'] = data
        context['category'] = cat.category_name
        context['category_obj'] = cat
        context['vehicle_count'] = data.count()
        context['empty'] = 0 if data.exists() else 1
        return context


class SearchSuggestView(View):
    def get(self, request):
        query = request.GET.get('q', '').strip()
        if not query:
            return JsonResponse([], safe=False)

        keywords = query.split()
        q = Q()
        for word in keywords:
            q |= Q(car_name__icontains=word)

        cars = Car.objects.filter(q)[:3]
        results = [
            {
                'id': car.id,
                'name': car.car_name,
                'image': car.car_image.url if car.car_image else '',
                'rate': car.car_hourRate,
                'category': str(car.car_category),
            }
            for car in cars
        ]
        return JsonResponse(results, safe=False)


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


class RentCarView(SuperCategoryMixin, TemplateView):
    template_name = 'shop/addcart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = get_object_or_404(Car, pk=self.kwargs['pk'])
        form = RentalOrderForm(initial={'car_id': product.pk})
        context['prod'] = product
        context['id'] = product.pk
        context['form'] = form
        return context


class ConfirmOrderView(SuperCategoryMixin, TemplateView):
    template_name = 'shop/confirmBuying.html'

    def post(self, request, *args, **kwargs):
        form = RentalOrderForm(request.POST)
        context = self.get_context_data(**kwargs)

        if form.is_valid():
            cd = form.cleaned_data
            prod = get_object_or_404(Car, pk=cd['car_id'])
            quantity = cd['totalRentCar']
            hours = cd['totalRentHour']
            include_driver = cd.get('include_driver', False)
            coupon_code = cd.get('coupon_code', '').strip()

            hourly_rate = Decimal(prod.car_hourRate)
            driver_rate = Decimal(prod.car_driverRate)
            delivery_rate = Decimal(prod.car_deliveryRate)

            subtotal = hourly_rate * hours * quantity
            driver_cost = driver_rate * hours * quantity if include_driver else Decimal(0)
            delivery_cost = delivery_rate * quantity
            pre_discount_total = subtotal + driver_cost + delivery_cost

            discount_amount = Decimal(0)
            coupon = None
            if coupon_code:
                try:
                    coupon = Coupon.objects.get(code__iexact=coupon_code)
                    if coupon.is_valid:
                        discount_amount = Decimal(str(coupon.calculate_discount(float(pre_discount_total))))
                except Coupon.DoesNotExist:
                    pass

            total_cost = pre_discount_total - discount_amount

            booking = Booking(
                car=prod,
                user=request.user if request.user.is_authenticated else None,
                coupon=coupon if discount_amount > 0 else None,
                customer_name=cd['customer_name'],
                customer_email=cd['customer_email'],
                customer_mobile=cd['customer_mobile'],
                customer_address=cd['customer_address'],
                rental_hours=hours,
                car_quantity=quantity,
                include_driver=include_driver,
                delivery_date=cd['deliveryDate'],
                delivery_time=cd['deliveryTime'],
                hourly_rate=hourly_rate,
                driver_rate=driver_rate,
                delivery_rate=delivery_rate,
                subtotal=subtotal,
                driver_cost=driver_cost,
                delivery_cost=delivery_cost,
                discount_amount=discount_amount,
                total_cost=total_cost,
            )
            booking.save()

            if coupon and discount_amount > 0:
                coupon.current_uses += 1
                coupon.save()

            context.update({
                'booking': booking,
                'prod': prod,
            })
            return self.render_to_response(context)

        context['form'] = form
        return redirect('shop:error')


class BookingDetailView(LoginRequiredMixin, SuperCategoryMixin, TemplateView):
    template_name = 'shop/booking_detail.html'
    login_url = '/member/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        booking = get_object_or_404(Booking, pk=self.kwargs['pk'], user=self.request.user)
        context['booking'] = booking
        return context


class BookingCancelView(LoginRequiredMixin, View):
    login_url = '/member/login/'

    def post(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk, user=request.user)
        if booking.status in ('pending', 'confirmed'):
            booking.status = 'cancelled'
            booking.save()
        return redirect('shop:booking_detail', pk=booking.pk)


class ReviewCreateView(LoginRequiredMixin, SuperCategoryMixin, TemplateView):
    template_name = 'shop/review_form.html'
    login_url = '/member/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car = get_object_or_404(Car, pk=self.kwargs['pk'])
        context['car'] = car
        context['form'] = ReviewForm()
        return context

    def post(self, request, *args, **kwargs):
        car = get_object_or_404(Car, pk=self.kwargs['pk'])

        has_completed_booking = Booking.objects.filter(
            user=request.user, car=car, status='completed'
        ).exists()
        already_reviewed = Review.objects.filter(user=request.user, car=car).exists()

        if not has_completed_booking or already_reviewed:
            return redirect('shop:product_detail', pk=car.pk)

        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.car = car
            completed_booking = Booking.objects.filter(
                user=request.user, car=car, status='completed'
            ).first()
            review.booking = completed_booking
            review.save()
            return redirect('shop:product_detail', pk=car.pk)

        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)


class FavoriteToggleView(LoginRequiredMixin, View):
    login_url = '/member/login/'

    def post(self, request, pk):
        car = get_object_or_404(Car, pk=pk)
        favorite, created = Favorite.objects.get_or_create(user=request.user, car=car)

        if not created:
            favorite.delete()
            is_favorited = False
        else:
            is_favorited = True

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'is_favorited': is_favorited,
                'favorites_count': Favorite.objects.filter(user=request.user).count(),
            })

        return redirect('shop:product_detail', pk=pk)


class FavoriteListView(LoginRequiredMixin, SuperCategoryMixin, TemplateView):
    template_name = 'shop/favorites.html'
    login_url = '/member/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favorites'] = Favorite.objects.filter(
            user=self.request.user
        ).select_related('car', 'car__car_category')
        return context


class CouponValidateView(View):
    def post(self, request):
        import json
        try:
            data = json.loads(request.body)
            code = data.get('code', '').strip()
        except (json.JSONDecodeError, AttributeError):
            code = request.POST.get('code', '').strip()

        if not code:
            return JsonResponse({'valid': False, 'error': 'Please enter a coupon code.'})

        try:
            coupon = Coupon.objects.get(code__iexact=code)
        except Coupon.DoesNotExist:
            return JsonResponse({'valid': False, 'error': 'Invalid coupon code.'})

        if not coupon.is_valid:
            return JsonResponse({'valid': False, 'error': 'This coupon has expired or is no longer valid.'})

        return JsonResponse({
            'valid': True,
            'discount_type': coupon.discount_type,
            'discount_value': float(coupon.discount_value),
            'max_discount': float(coupon.max_discount) if coupon.max_discount else None,
            'min_order_amount': float(coupon.min_order_amount),
            'description': coupon.description,
        })
