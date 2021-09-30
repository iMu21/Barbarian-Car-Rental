from django.shortcuts import render
from django.http import HttpResponse
from .models import Car
from .models import SuperCategory
from .models import Category


def home(request):
    try:
        cars = Car.objects.all()
        superCategory = SuperCategory.objects.all()
        category = Category.objects.all()
        n = len(cars)

        categorizedList = []
        superList = []
        catList = []
        catWiseSuper = []
        for j in range(len(superCategory)):
            superList.append(str(superCategory[j].superCategory_name))
            categorizedList.append((str(superCategory[j].superCategory_name), []))

        for j in range(len(category)):
            name = category[j].category_name
            catList.append(name)
            name = category[j].superCategory_name
            catWiseSuper.append(name)

        for j in range(n):
            catName = cars[j].car_category
            i = catList.index(str(catName))
            i = superList.index(str(catWiseSuper[i]))
            categorizedList[i][1].append(cars[j])

        for j in range(len(categorizedList)):
            x = len(categorizedList[j][1])
            if x % 3 == 0:
                x = x//3
            else:
                x = (x//3)+1
            categorizedList[j] += ((range(1, x)),)
        j = int(0)
        while j < (len(categorizedList)):
            if len(categorizedList[j][1]) == 0:
                categorizedList.pop(j)
            else:
                j += 1

        params = {'superCategory':superCategory,'superList': superList, 'jrange': range(int(0), int(
            len(superCategory))), 'product_len': n, 'product': categorizedList}
        return render(request, 'shop/home.html', params)
    except:
        return render(request, 'shop/error.html',params)


def about(request):
    superCategory = SuperCategory.objects.all()
    params = {'superCategory': superCategory}
    return render(request, 'shop/about.html',params)


def contact(request):
    superCategory = SuperCategory.objects.all()
    params={'superCategory':superCategory}
    return render(request, 'shop/contact.html',params)


def productView(request):
    try:
        a = int(request.GET.get('val'))
        product = Car.objects.all()
        superCategory = SuperCategory.objects.all()

        for i in range(len(product)):
            if int(product[i].id) == a:
                prams = {'superCategory': superCategory,'product': product[i]}
                return render(request, "shop/productView.html", prams)
    except:
        superCategory = SuperCategory.objects.all()
        params={'superCategory':superCategory}
        return render(request,"shop/error.html",params)


def supercategory(request):
    try:
        superCat = request.GET.get('val')
        category = Category.objects.all()
        product = Car.objects.all()
        superCategory = SuperCategory.objects.all()
        n = len(product)
        categorizedList = []
        catList = []

        for i in range(len(category)):
            if str(category[i].superCategory_name) == str(superCat):
                catList.append(str(category[i].category_name))
                categorizedList.append((str(category[i].category_name), []))


        for j in range(n):
            catName = str(product[j].car_category)
            if str(catName) in catList:
                i = catList.index(str(catName))
                categorizedList[i][1].append(product[j])

        for j in range(len(categorizedList)):
            x = len(categorizedList[j][1])
            if x % 4 == 0:
                x = x // 4
            else:
                x = (x //4) + 1
            categorizedList[j] += ((range(1, x)),)
        j = int(0)
        while j < (len(categorizedList)):
            if len(categorizedList[j][1]) == 0:
                categorizedList.pop(j)
            else:
                j += 1
        empty=int(0)
        if len(categorizedList)==0:
            empty=int(1)
        print(superCat,empty)
        params = {'empty':empty,'superCategory': superCategory, 'jrange': range(int(0), int(len(catList))),
                  'product': categorizedList, 'Name': superCat}

        return render(request, 'shop/supercategory.html', params)
    except:
        superCategory = SuperCategory.objects.all()
        params={'superCategory':superCategory}
        return render(request,"shop/error.html",params)


def search(request):
    try:
        superCategory=SuperCategory.objects.all()
        search_key=request.POST
        search_key = search_key.get('search_key', False)
        product = Car.objects.all()
        search_key=list(search_key.split())
        data=[]
        for i in product:
            name=str(i.car_name)
            for j in search_key:
                if j.lower() in str(name).lower():
                    data.append(i)
                    break
        empty=int(0)
        if len(data)==0:
            empty=int(1)
        params={'data':data,'empty':empty,'superCategory':superCategory}
        return render(request,"shop/search.html",params)
    except:
        superCategory = SuperCategory.objects.all()
        params = {'superCategory': superCategory}
        return render(request, "shop/error.html", params)

def category(request):
    try:
        superCategory=SuperCategory.objects.all()
        category = request.GET.get('val')
        product = Car.objects.all()
        data=[]
        for i in product:
            name=str(i.car_category)
            if name==str(category):
                data.append(i)
        empty=int(0)
        if len(data)==0:
            empty=int(1)
        print(data)
        params={'data':data,'empty':empty,'superCategory':superCategory,'category':category}
        return render(request,"shop/category.html",params)
    except:
        superCategory = SuperCategory.objects.all()
        params = {'superCategory': superCategory}
        return render(request, "shop/error.html", params)


def error(request):
    superCategory = SuperCategory.objects.all()
    params = {'superCategory': superCategory}
    return render(request, "shop/error.html",params)


def addcart(request):
    try:
        a = request.GET.get('val')
        product = Car.objects.all()
        superCategory = SuperCategory.objects.all()
        for i in range(len(product)):
            if int(product[i].id) == int(a):
                params = {'superCategory': superCategory,"id":int(a),"prod": product[i]}
                return render(request, "shop/addcart.html", params)
        return render(request, "shop/error.html")
    except:
        superCategory = SuperCategory.objects.all()
        params = {'superCategory': superCategory}
        return render(request,"shop/error.html",params)


def checkout(request):
    return HttpResponse("checkout")

def confirmBuying(request):
    superCategory = SuperCategory.objects.all()
    product = Car.objects.all()
    customer_name=request.POST['customer_name']
    customer_email = request.POST['customer_email']
    customer_mobile = request.POST['customer_mobile']
    customer_address = request.POST['customer_address']
    car_id = request.POST['car_id']
    car_quantity = int(request.POST['totalRentCar'])
    car_rentHour = int(request.POST['totalRentHour'])
    car_hourRate = ''
    car_deliveryRate =  ''
    prod=''
    for i in range(len(product)):
        b=product[i].id
        if int(b)-int(car_id)==0:
            prod=product[i]
            car_hourRate = int(prod.car_hourRate)
            car_deliveryRate = int(prod.car_deliveryRate)

    total_cost = car_hourRate*car_rentHour+car_deliveryRate*car_quantity
    print(prod)


    params={'superCategory': superCategory,'car_quantity':car_quantity,
            'total_cost':total_cost,'prod':prod,'customer_name':customer_name,
            'customer_email':customer_email,'customer_mobile':customer_mobile,'customer_address':customer_address}
    return render(request,"shop/confirmBuying.html",params)

