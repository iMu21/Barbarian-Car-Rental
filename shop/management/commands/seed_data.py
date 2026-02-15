from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from shop.models import SuperCategory, Category, Car, Coupon, Booking, Review, Favorite
from member.models import memberBasic, websiteType


class Command(BaseCommand):
    help = 'Seed the database with test data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')

        # --- SuperCategories ---
        super_categories = {}
        for name in ['Car', 'Motorcycle', 'Bicycle']:
            obj, created = SuperCategory.objects.get_or_create(superCategory_name=name)
            super_categories[name] = obj
            status = 'created' if created else 'already exists'
            self.stdout.write(f'  SuperCategory: {name} ({status})')

        # --- Categories ---
        category_map = {
            'Car': ['Sedan', 'SUV', 'Hatchback', 'Electric'],
            'Motorcycle': ['Sport', 'Cruiser', 'Scooter'],
            'Bicycle': ['Mountain', 'Road'],
        }

        categories = {}
        for super_name, cat_names in category_map.items():
            for cat_name in cat_names:
                obj, created = Category.objects.get_or_create(
                    category_name=cat_name,
                    superCategory_name=super_categories[super_name],
                )
                categories[cat_name] = obj
                status = 'created' if created else 'already exists'
                self.stdout.write(f'  Category: {cat_name} -> {super_name} ({status})')

        # --- Vehicles ---
        vehicles = [
            # Sedans
            {'car_name': 'Toyota Corolla', 'car_category': 'Sedan', 'car_driverRate': 250, 'car_hourRate': 600, 'car_deliveryRate': 500, 'car_capacity': 5, 'car_quantity': 8, 'car_image': 'shop/images/Toyota_Corolla.jpg'},
            {'car_name': 'Honda Civic', 'car_category': 'Sedan', 'car_driverRate': 300, 'car_hourRate': 750, 'car_deliveryRate': 500, 'car_capacity': 5, 'car_quantity': 6, 'car_image': 'shop/images/Honda_Civic.jpg'},
            {'car_name': 'Hyundai Elantra', 'car_category': 'Sedan', 'car_driverRate': 250, 'car_hourRate': 550, 'car_deliveryRate': 400, 'car_capacity': 5, 'car_quantity': 5, 'car_image': 'shop/images/Hyundai_Elantra.jpg'},
            {'car_name': 'Mazda Mazda3', 'car_category': 'Sedan', 'car_driverRate': 300, 'car_hourRate': 700, 'car_deliveryRate': 500, 'car_capacity': 5, 'car_quantity': 4, 'car_image': 'shop/images/Mazda_Mazda3.jpg'},
            # SUVs
            {'car_name': 'Honda CR-V', 'car_category': 'SUV', 'car_driverRate': 400, 'car_hourRate': 1200, 'car_deliveryRate': 800, 'car_capacity': 7, 'car_quantity': 5, 'car_image': 'shop/images/Honda_CR-V.jpg'},
            {'car_name': 'BMW X5', 'car_category': 'SUV', 'car_driverRate': 500, 'car_hourRate': 2500, 'car_deliveryRate': 1000, 'car_capacity': 7, 'car_quantity': 3, 'car_image': 'shop/images/BMW_X5.jpg'},
            {'car_name': 'Kia Sportage', 'car_category': 'SUV', 'car_driverRate': 350, 'car_hourRate': 1000, 'car_deliveryRate': 700, 'car_capacity': 5, 'car_quantity': 6, 'car_image': 'shop/images/Kia_Sportage.jpg'},
            # Hatchbacks
            {'car_name': 'Volkswagen Golf', 'car_category': 'Hatchback', 'car_driverRate': 250, 'car_hourRate': 650, 'car_deliveryRate': 450, 'car_capacity': 5, 'car_quantity': 7, 'car_image': 'shop/images/Volkswagen_Golf.jpg'},
            {'car_name': 'MINI Cooper', 'car_category': 'Hatchback', 'car_driverRate': 300, 'car_hourRate': 900, 'car_deliveryRate': 500, 'car_capacity': 4, 'car_quantity': 4, 'car_image': 'shop/images/MINI_Cooper.jpg'},
            {'car_name': 'Kia Rio', 'car_category': 'Hatchback', 'car_driverRate': 200, 'car_hourRate': 450, 'car_deliveryRate': 350, 'car_capacity': 5, 'car_quantity': 8, 'car_image': 'shop/images/Kia_Rio.jpg'},
            # Electric
            {'car_name': 'Toyota Prius', 'car_category': 'Electric', 'car_driverRate': 300, 'car_hourRate': 850, 'car_deliveryRate': 600, 'car_capacity': 5, 'car_quantity': 4, 'car_image': 'shop/images/Toyota_Prius.jpg'},
            {'car_name': 'Chevrolet Bolt', 'car_category': 'Electric', 'car_driverRate': 350, 'car_hourRate': 1100, 'car_deliveryRate': 700, 'car_capacity': 5, 'car_quantity': 3, 'car_image': 'shop/images/Chevrolet_Bolt.jpg'},
            {'car_name': 'Hyundai Ioniq', 'car_category': 'Electric', 'car_driverRate': 300, 'car_hourRate': 950, 'car_deliveryRate': 600, 'car_capacity': 5, 'car_quantity': 4, 'car_image': 'shop/images/Hyundai_Ioniq.jpg'},
            # Sport Motorcycles
            {'car_name': 'Suzuki GSX R150', 'car_category': 'Sport', 'car_driverRate': 0, 'car_hourRate': 250, 'car_deliveryRate': 200, 'car_capacity': 2, 'car_quantity': 6, 'car_image': 'shop/images/Suzuki_GSX_R150.jpg'},
            {'car_name': 'TVS Apache RTR 160 4v', 'car_category': 'Sport', 'car_driverRate': 0, 'car_hourRate': 200, 'car_deliveryRate': 150, 'car_capacity': 2, 'car_quantity': 5, 'car_image': 'shop/images/TVS_Apache_RTR_160_4v.jpg'},
            # Cruisers
            {'car_name': 'Suzuki Intruder 150 ABS', 'car_category': 'Cruiser', 'car_driverRate': 0, 'car_hourRate': 300, 'car_deliveryRate': 250, 'car_capacity': 2, 'car_quantity': 3, 'car_image': 'shop/images/Suzuki_Intruder_150_ABS.jpg'},
            {'car_name': 'TVS Rockz 125', 'car_category': 'Cruiser', 'car_driverRate': 0, 'car_hourRate': 150, 'car_deliveryRate': 150, 'car_capacity': 2, 'car_quantity': 4, 'car_image': 'shop/images/TVS_Rockz_125.jpg'},
            # Scooters
            {'car_name': 'Suzuki Burgman 200 ABS', 'car_category': 'Scooter', 'car_driverRate': 0, 'car_hourRate': 200, 'car_deliveryRate': 150, 'car_capacity': 2, 'car_quantity': 5, 'car_image': 'shop/images/Suzuki_Burgman_200_ABS.jpg'},
            {'car_name': 'TVS Ntorq 125', 'car_category': 'Scooter', 'car_driverRate': 0, 'car_hourRate': 120, 'car_deliveryRate': 100, 'car_capacity': 2, 'car_quantity': 7, 'car_image': 'shop/images/TVS_Ntorq_125.jpg'},
            # Mountain Bikes
            {'car_name': 'Phoenix Mountain Bike ATV 4.0', 'car_category': 'Mountain', 'car_driverRate': 0, 'car_hourRate': 80, 'car_deliveryRate': 100, 'car_capacity': 1, 'car_quantity': 10, 'car_image': 'shop/images/Phoenix_Snowmobile_ATV_mountain_bike_4.0_super_speed_off_road_vehicle.jpg'},
            # Road Bikes
            {'car_name': 'Phoenix Road Bike SC15A', 'car_category': 'Road', 'car_driverRate': 0, 'car_hourRate': 60, 'car_deliveryRate': 80, 'car_capacity': 1, 'car_quantity': 8, 'car_image': 'shop/images/Phoenix_Bicycle_SC15A7003RB.jpg'},
        ]

        car_objects = {}
        for v in vehicles:
            cat_name = v.pop('car_category')
            obj, created = Car.objects.get_or_create(
                car_name=v['car_name'],
                defaults={**v, 'car_category': categories[cat_name]},
            )
            car_objects[obj.car_name] = obj
            if not created and not obj.car_image:
                obj.car_image = v.get('car_image', '')
                obj.save()
                self.stdout.write(f'  Vehicle: {obj.car_name} (image updated)')
            else:
                status = 'created' if created else 'already exists'
                self.stdout.write(f'  Vehicle: {obj.car_name} ({status})')

        # --- Featured Vehicles ---
        featured_vehicles = {
            'BMW X5': 'Premium luxury SUV experience',
            'Honda Civic': 'Most popular sedan choice',
            'MINI Cooper': 'Compact and stylish city car',
            'Toyota Prius': 'Eco-friendly electric driving',
        }
        for car_name, tagline in featured_vehicles.items():
            if car_name in car_objects:
                car = car_objects[car_name]
                if not car.is_featured:
                    car.is_featured = True
                    car.featured_tagline = tagline
                    car.save()
                    self.stdout.write(f'  Featured: {car_name} (set)')
                else:
                    self.stdout.write(f'  Featured: {car_name} (already featured)')

        # --- Users ---
        users = {}
        # Admin superuser
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@barbariancarrental.com',
                password='admin1234',
            )
            memberBasic.objects.get_or_create(
                username=admin,
                defaults={'firstName': 'Admin', 'lastName': 'User'},
            )
            users['admin'] = admin
            self.stdout.write('  User: admin (superuser, created)')
        else:
            users['admin'] = User.objects.get(username='admin')
            self.stdout.write('  User: admin (already exists)')

        # Test users
        test_users = [
            {'username': 'john_doe', 'email': 'john@example.com', 'password': 'testpass1234', 'first': 'John', 'last': 'Doe'},
            {'username': 'jane_smith', 'email': 'jane@example.com', 'password': 'testpass1234', 'first': 'Jane', 'last': 'Smith'},
        ]

        for u in test_users:
            if not User.objects.filter(username=u['username']).exists():
                user = User.objects.create_user(
                    username=u['username'],
                    email=u['email'],
                    password=u['password'],
                )
                memberBasic.objects.get_or_create(
                    username=user,
                    defaults={'firstName': u['first'], 'lastName': u['last']},
                )
                users[u['username']] = user
                self.stdout.write(f'  User: {u["username"]} (created)')
            else:
                users[u['username']] = User.objects.get(username=u['username'])
                self.stdout.write(f'  User: {u["username"]} (already exists)')

        # --- Website Types ---
        website_types = ['GitHub', 'LinkedIn', 'Twitter']
        for wt_name in website_types:
            obj, created = websiteType.objects.get_or_create(name=wt_name)
            status = 'created' if created else 'already exists'
            self.stdout.write(f'  WebsiteType: {wt_name} ({status})')

        # --- Coupons ---
        now = timezone.now()
        coupons_data = [
            {
                'code': 'WELCOME10',
                'description': '10% off your first booking!',
                'discount_type': 'percentage',
                'discount_value': 10,
                'max_discount': 1500,
                'min_order_amount': 2000,
                'max_uses': 100,
                'valid_from': now - timedelta(days=30),
                'valid_until': now + timedelta(days=365),
            },
            {
                'code': 'FLAT500',
                'description': 'Flat 500 BDT off on orders above 3000 BDT',
                'discount_type': 'fixed',
                'discount_value': 500,
                'min_order_amount': 3000,
                'max_uses': 50,
                'valid_from': now - timedelta(days=7),
                'valid_until': now + timedelta(days=180),
            },
            {
                'code': 'SUMMER25',
                'description': '25% off summer special! Max discount 3000 BDT',
                'discount_type': 'percentage',
                'discount_value': 25,
                'max_discount': 3000,
                'min_order_amount': 5000,
                'max_uses': 200,
                'valid_from': now - timedelta(days=10),
                'valid_until': now + timedelta(days=90),
            },
        ]
        for cd in coupons_data:
            obj, created = Coupon.objects.get_or_create(
                code=cd['code'],
                defaults=cd,
            )
            status = 'created' if created else 'already exists'
            self.stdout.write(f'  Coupon: {cd["code"]} ({status})')

        # --- Sample Bookings ---
        john = users.get('john_doe')
        jane = users.get('jane_smith')

        if john and not Booking.objects.filter(user=john).exists():
            corolla = car_objects.get('Toyota Corolla')
            civic = car_objects.get('Honda Civic')
            bmw = car_objects.get('BMW X5')

            if corolla:
                # 600/hr x 5hrs = 3000 subtotal, 250/hr x 5hrs = 1250 driver, 500 delivery = 4750
                Booking.objects.create(
                    user=john, car=corolla, status='completed',
                    customer_name='John Doe', customer_email='john@example.com',
                    customer_mobile='01712345678', customer_address='123 Main St, Dhaka',
                    rental_hours=5, car_quantity=1, include_driver=True,
                    delivery_date=date.today() - timedelta(days=10),
                    delivery_time='10:00',
                    hourly_rate=600, driver_rate=250, delivery_rate=500,
                    subtotal=3000, driver_cost=1250, delivery_cost=500,
                    discount_amount=0, total_cost=4750,
                )
                self.stdout.write('  Booking: john_doe -> Toyota Corolla (completed)')

            if civic:
                # 750/hr x 3hrs = 2250 subtotal, no driver, 500 delivery = 2750
                Booking.objects.create(
                    user=john, car=civic, status='confirmed',
                    customer_name='John Doe', customer_email='john@example.com',
                    customer_mobile='01712345678', customer_address='123 Main St, Dhaka',
                    rental_hours=3, car_quantity=1, include_driver=False,
                    delivery_date=date.today() + timedelta(days=5),
                    delivery_time='14:00',
                    hourly_rate=750, driver_rate=300, delivery_rate=500,
                    subtotal=2250, driver_cost=0, delivery_cost=500,
                    discount_amount=0, total_cost=2750,
                )
                self.stdout.write('  Booking: john_doe -> Honda Civic (confirmed)')

            if bmw:
                # 2500/hr x 4hrs = 10000 subtotal, 500/hr x 4hrs = 2000 driver, 1000 delivery = 13000
                Booking.objects.create(
                    user=john, car=bmw, status='completed',
                    customer_name='John Doe', customer_email='john@example.com',
                    customer_mobile='01712345678', customer_address='123 Main St, Dhaka',
                    rental_hours=4, car_quantity=1, include_driver=True,
                    delivery_date=date.today() - timedelta(days=20),
                    delivery_time='09:00',
                    hourly_rate=2500, driver_rate=500, delivery_rate=1000,
                    subtotal=10000, driver_cost=2000, delivery_cost=1000,
                    discount_amount=0, total_cost=13000,
                )
                self.stdout.write('  Booking: john_doe -> BMW X5 (completed)')

        if jane and not Booking.objects.filter(user=jane).exists():
            golf = car_objects.get('Volkswagen Golf')
            if golf:
                # 650/hr x 6hrs = 3900 subtotal, no driver, 450 delivery = 4350
                Booking.objects.create(
                    user=jane, car=golf, status='completed',
                    customer_name='Jane Smith', customer_email='jane@example.com',
                    customer_mobile='01898765432', customer_address='456 Park Ave, Dhaka',
                    rental_hours=6, car_quantity=1, include_driver=False,
                    delivery_date=date.today() - timedelta(days=15),
                    delivery_time='11:00',
                    hourly_rate=650, driver_rate=250, delivery_rate=450,
                    subtotal=3900, driver_cost=0, delivery_cost=450,
                    discount_amount=0, total_cost=4350,
                )
                self.stdout.write('  Booking: jane_smith -> Volkswagen Golf (completed)')

        # --- Sample Reviews ---
        if john and not Review.objects.filter(user=john).exists():
            corolla = car_objects.get('Toyota Corolla')
            bmw = car_objects.get('BMW X5')
            if corolla:
                Review.objects.create(
                    user=john, car=corolla, rating=5,
                    comment='Excellent car! Very clean and comfortable. The rental process was smooth.',
                )
                self.stdout.write('  Review: john_doe -> Toyota Corolla (5/5)')
            if bmw:
                Review.objects.create(
                    user=john, car=bmw, rating=4,
                    comment='Great luxury SUV. Very powerful and spacious. A bit pricey but worth it.',
                )
                self.stdout.write('  Review: john_doe -> BMW X5 (4/5)')

        if jane and not Review.objects.filter(user=jane).exists():
            golf = car_objects.get('Volkswagen Golf')
            if golf:
                Review.objects.create(
                    user=jane, car=golf, rating=4,
                    comment='Nice compact car, perfect for city driving. Good fuel economy too.',
                )
                self.stdout.write('  Review: jane_smith -> Volkswagen Golf (4/5)')

        # --- Sample Favorites ---
        if john and not Favorite.objects.filter(user=john).exists():
            for car_name in ['BMW X5', 'Honda Civic', 'Toyota Prius']:
                car = car_objects.get(car_name)
                if car:
                    Favorite.objects.create(user=john, car=car)
                    self.stdout.write(f'  Favorite: john_doe -> {car_name}')

        if jane and not Favorite.objects.filter(user=jane).exists():
            for car_name in ['MINI Cooper', 'Volkswagen Golf']:
                car = car_objects.get(car_name)
                if car:
                    Favorite.objects.create(user=jane, car=car)
                    self.stdout.write(f'  Favorite: jane_smith -> {car_name}')

        self.stdout.write(self.style.SUCCESS('Seeding complete!'))
