from django.test import TestCase, Client
from django.urls import reverse
from .models import SuperCategory, Category, Car


class SuperCategoryModelTest(TestCase):
    def test_str(self):
        sc = SuperCategory.objects.create(superCategory_name='Car')
        self.assertEqual(str(sc), 'Car')


class CategoryModelTest(TestCase):
    def test_str(self):
        sc = SuperCategory.objects.create(superCategory_name='Car')
        cat = Category.objects.create(category_name='Sedan', superCategory_name=sc)
        self.assertEqual(str(cat), 'Sedan')

    def test_fk(self):
        sc = SuperCategory.objects.create(superCategory_name='Car')
        cat = Category.objects.create(category_name='SUV', superCategory_name=sc)
        self.assertEqual(cat.superCategory_name, sc)


class CarModelTest(TestCase):
    def setUp(self):
        self.sc = SuperCategory.objects.create(superCategory_name='Car')
        self.cat = Category.objects.create(category_name='Sedan', superCategory_name=self.sc)
        self.car = Car.objects.create(
            car_name='Toyota Corolla',
            car_category=self.cat,
            car_hourRate=25,
            car_deliveryRate=10,
            car_capacity=5,
            car_quantity=8,
        )

    def test_str(self):
        self.assertEqual(str(self.car), 'Toyota Corolla')

    def test_defaults(self):
        car = Car.objects.create(car_name='Test', car_category=self.cat)
        self.assertEqual(car.car_driverRate, 0)
        self.assertEqual(car.car_hourRate, 0)


class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_loads(self):
        response = self.client.get(reverse('shop:home'))
        self.assertEqual(response.status_code, 200)

    def test_home_uses_correct_template(self):
        response = self.client.get(reverse('shop:home'))
        self.assertTemplateUsed(response, 'shop/home.html')


class AboutViewTest(TestCase):
    def test_about_loads(self):
        response = self.client.get(reverse('shop:about'))
        self.assertEqual(response.status_code, 200)


class ContactViewTest(TestCase):
    def test_contact_loads(self):
        response = self.client.get(reverse('shop:contact'))
        self.assertEqual(response.status_code, 200)


class ProductDetailViewTest(TestCase):
    def setUp(self):
        sc = SuperCategory.objects.create(superCategory_name='Car')
        cat = Category.objects.create(category_name='Sedan', superCategory_name=sc)
        self.car = Car.objects.create(
            car_name='Honda Civic', car_category=cat, car_hourRate=28,
            car_deliveryRate=10, car_capacity=5, car_quantity=6,
        )

    def test_product_detail_loads(self):
        response = self.client.get(reverse('shop:product_detail', args=[self.car.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Honda Civic')

    def test_product_detail_404(self):
        response = self.client.get(reverse('shop:product_detail', args=[9999]))
        self.assertEqual(response.status_code, 404)


class SearchViewTest(TestCase):
    def setUp(self):
        sc = SuperCategory.objects.create(superCategory_name='Car')
        cat = Category.objects.create(category_name='Sedan', superCategory_name=sc)
        Car.objects.create(car_name='Toyota Corolla', car_category=cat, car_quantity=8)

    def test_search_finds_car(self):
        response = self.client.post(reverse('shop:search'), {'search_key': 'Toyota'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Toyota Corolla')

    def test_search_no_results(self):
        response = self.client.post(reverse('shop:search'), {'search_key': 'NonexistentCar'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No vehicles found')


class CategoryDetailViewTest(TestCase):
    def setUp(self):
        sc = SuperCategory.objects.create(superCategory_name='Car')
        self.cat = Category.objects.create(category_name='Sedan', superCategory_name=sc)
        Car.objects.create(car_name='Mazda3', car_category=self.cat, car_quantity=4)

    def test_category_detail_loads(self):
        response = self.client.get(reverse('shop:category_detail', args=[self.cat.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Mazda3')
