from geopy import distance
import geocoder
import folium
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from .models import *
# Create your views here.


def home(request):
    products = product.objects.all().order_by('-time')

    return render(request, 'shop/Home.html', {'products': products})


def search(request):
    if request.method == 'POST':
        # product search
        item = request.POST['search']
        products = product.objects.filter(name=item).order_by('-time')
        if products:
            return render(request, 'shop/Home.html', {'products': products})
        else:
            msg1 = "Ooooh!!! Pole"
            msg2 = "Hakuna mfanano wa ulichokitafuta"
            return render(request, 'shop/Home.html', {'msg1': msg1, 'msg2': msg2})


def search_cartegory(request):
    if request.method == 'POST':
        # product search
        item = request.POST['Cartegory']
        products = product.objects.filter(cartegory=item).order_by('-time')
        if products:
            return render(request, 'shop/Home.html', {'products': products})
        else:
            msg1 = "Ooooh!!! Pole"
            msg2 = "Hakuna mfanano wa ulichokitafuta"
            return render(request, 'shop/Home.html', {'msg1': msg1, 'msg2': msg2})


def show_map(request):
    products = product.objects.all().order_by('-time')

    if request.method == 'POST':
        # product location
        sellerlocation = request.POST['productlocation']
        pid = request.POST['pid']
        pname = request.POST['productname']

        productid = product.objects.get(id=pid)
        products = product.objects.filter(
            name=productid.name).order_by('-time')

        def seller_location(sellerlocation, productid):

            print('seller locatiooonnn wooow:::>>>', sellerlocation)

            location = geocoder.osm(sellerlocation)
            country = location.country
            region = location.region
            name = sellerlocation
            lat = location.lat
            lng = location.lng

            productlocation = product_location.objects.create(
                product=productid, nation=country, region=region, name=name, latitude=lat, longtude=lng)
            productlocation.save()
            for row in product_location.objects.all().reverse():
                if product_location.objects.filter(product=row.product).count() > 1:
                    row.delete()
            return(lat, lng)

        def customer_location(request):
            """
            def get_client_ip(request):
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ip = x_forwarded_for.split(',')[-1].strip()
                else:
                    ip = request.META.get('REMOTE_ADDR')
                return ip
            ip = get_client_ip(request)

            print("...........>>>>>", ip)
            """
            # the ip and map for user codes
            data = geocoder.ip("me")
            ip = data.ip
            country = data.country
            region = data.city
            userlat = data.lat
            userlong = data.lng

            userlocation = user_location.objects.create(
                ip=ip, nation=country, region=region, latitude=userlat, longtude=userlong)
            userlocation.save()
            for row in user_location.objects.all().reverse():
                if user_location.objects.filter(ip=row.ip).count() > 1:
                    row.delete()
            return(userlat, userlong)

        # location function calling
        loc1 = seller_location(sellerlocation, productid)
        loc2 = customer_location(request)

        # map and makers for product and user

        def showmap(loc1, loc2, sellerlocation, pname):
            m1 = folium.Map(location=loc1, zoom_start=22)
            customer_mark = folium.Marker(location=loc2, popup="My location",
                                          tooltip="Customer").add_to(m1)
            product_mark = folium.Marker(location=loc1, popup=sellerlocation,
                                         tooltip=pname).add_to(m1)

            m2 = m1._repr_html_()
            return(m2)
        n = productid
        m = showmap(loc1, loc2, sellerlocation, pname)
        context = {'products': products, 'm': m, 'n': n}

    return render(request, 'shop/display_map.html', context)


def register(request):
    if request.method == 'POST':
        name1 = request.POST['fname']
        name3 = request.POST['lname']
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        kazi = request.POST['kazi']
        simu = request.POST['phonenumber']
        sehemu = request.POST['sehemu']

        user = User.objects.create_user(
            first_name=name1, last_name=name3, username=username, password=password, email=email, kazi=kazi, sehemu=sehemu, simu=simu)
        user.save()
        return redirect('/')

    return render(request, 'shop/Kujisajili.html')


def loging(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['password']

        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            pics = product.objects.filter(seller=request.user)
            userdata = User.objects.filter(username=request.user)
            return render(request, 'shop/mteja wetu.html', {'userdata': userdata, 'pics': pics})
        else:
            pass
    return render(request, 'shop/mteja wetu.html')


"""code to add products"""


def add_product(request):
    if request.method == 'POST' and request.FILES['pic']:
        name = request.POST['name']
        cartegory = request.POST['cartegory']
        price = request.POST['price']
        discription = request.POST['discription']
        image = request.FILES['pic']
        time = datetime.now()

        save_product = product.objects.create(
            name=name, cartegory=cartegory, price=price, discription=discription, image=image, time=time, seller=request.user)
        save_product.save()
        return redirect('mteja wetu')

    pics = product.objects.filter(seller=request.user)
    userdata = User.objects.filter(username=request.user)
    return render(request, 'shop/mteja wetu.html', {'userdata': userdata, 'pics': pics})


def update_product(request, id):
    if request.method == 'POST' and request.FILES['pic']:
        name = request.POST['name']
        cartegory = request.POST['cartegory']
        price = request.POST['price']
        discription = request.POST['discription']
        image = request.FILES['pic']
        time = datetime.now()

        old_product = product.objects.get(id=id)
        old_product.name = name
        old_product.cartegory = cartegory
        old_product.price = price
        old_product.discription = discription
        old_product.image = image
        old_product.time = time

        new_product = product.objects.create(
            name=name, cartegory=cartegory, price=price, discription=discription, image=image, time=time, seller=request.user)
        new_product.save()
        return redirect('mteja wetu')


def delete_product(request, id):
    product_delete = product.objects.get(id=id)
    product_delete.delete()

    return redirect('mteja wetu')


def about_us(request):
    return render(request, 'shop/Kuhusu Sisi.html')


def Distance(request):
    products = product.objects.all().order_by('-time')

    if request.method == 'POST':
        # product location
        seller_id = request.POST['seller_id']
        product_id = request.POST['product_id']
        user_place = request.POST['user_place']

        user = User.objects.get(id=seller_id)
        product_loc = user.sehemu
        req_product = product.objects.get(id=product_id)

        def seller_location(product_loc, product_id):
            location = geocoder.osm(product_loc)
            country = location.country
            region = location.region
            name = product_loc
            lat = location.lat
            lng = location.lng

            productlocation = product_location.objects.create(
                product=req_product, nation=country, region=region, name=name, latitude=lat, longtude=lng)
            productlocation.save()

            for row in product_location.objects.all().reverse():
                if product_location.objects.filter(product=row.product).count() > 1:
                    row.delete()
            return(lat, lng)

        def customer_location(request, user_place):

            # the ip and map for user codes
            data = geocoder.osm(user_place)
            dat = geocoder.ip("me")
            ip = dat.ip
            country = data.country
            region = data.region
            userlat = data.lat
            userlong = data.lng

            userlocation = user_location.objects.create(
                ip=ip, nation=country, region=region, latitude=userlat, longtude=userlong)
            userlocation.save()

            for row in user_location.objects.all().reverse():
                if user_location.objects.filter(ip=row.ip).count() > 1:
                    row.delete()
            return(userlat, userlong)

        # location function calling
        loc1 = seller_location(product_loc, product_id)
        loc2 = customer_location(request, user_place)
        sellerlocation = product_loc
        pname = req_product.name

        Distance = distance.distance(loc1, loc2)

        # map and makers for product and user
        def showmap(loc1, loc2, sellerlocation, pname):
            m1 = folium.Map(location=loc1, zoom_start=22)
            customer_mark = folium.Marker(location=loc2, popup="Sehemu Nilipo",
                                          tooltip="Mimi").add_to(m1)
            product_mark = folium.Marker(location=loc1, popup=sellerlocation,
                                         tooltip=pname).add_to(m1)

            m2 = m1._repr_html_()
            return(m2)
        n = req_product
        m = showmap(loc1, loc2, sellerlocation, pname)

        context = {'products': products, 'm': m, 'n': n, 'Distance': Distance}

    return render(request, 'shop/display_map.html', context)
