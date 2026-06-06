from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from .models import Product, Category, DISTRICT_CHOICES
from .serializers import CategorySerializer, ProductSerializer
from django.http import JsonResponse
from django.contrib import messages

def product_detail_page(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'product_detail.html', {'product': product})

# --- 🚀 ҚИСМИ API (БАРОИ ИН КИ URLS.PY ХАТО НАДИҲАД) ---
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# 1. Саҳифаи Асосӣ (Ҷустуҷӯи Оптимизатсияшуда)
def home_page(request):
    products = Product.objects.all().order_by('-created_at')
    categories = Category.objects.all()
    
    # 🔍 Ҷустуҷӯ аз рӯи номи маҳсулот
    search_query = request.GET.get('search')
    if search_query and search_query.strip():
        products = products.filter(title__icontains=search_query.strip())
        
    # 📍 Филтри шаҳрҳо
    location_query = request.GET.get('location')
    if location_query and location_query.strip():
        products = products.filter(location=location_query.strip())

    # 📂 Филтри категорияҳо
    category_id = request.GET.get('category')
    if category_id and category_id.strip():
        products = products.filter(category_id=category_id.strip())

    context = {
        'products': products,
        'categories': categories,
        'districts': DISTRICT_CHOICES,
    }
    return render(request, 'product_list.html', context)

# 2. Саҳифаи маҳсулотҳои интихобшуда
def favorites_page(request):
    fav_ids = request.session.get('favorites', [])
    favorite_products = Product.objects.filter(id__in=fav_ids)
    return render(request, 'favorites.html', {'favorite_products': favorite_products})

# 3. Функсияи AJAX барои Интихобшудаҳо
def toggle_favorite_api(request, product_id):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        favorites = request.session.get('favorites', [])
        
        if product_id in favorites:
            favorites.remove(product_id)
            status = 'removed'
        else:
            favorites.append(product_id)
            status = 'added'
            
        request.session['favorites'] = favorites
        request.session.modified = True
        return JsonResponse({'status': status})
    return JsonResponse({'error': 'Invalid request'}, status=400)

# 4. Саҳифаи иловакунии маҳсулот
def add_product_page(request):
    if request.method == 'POST':
        has_delivery = 'has_delivery' in request.POST
        title = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        location = request.POST.get('location')
        phone = request.POST.get('phone')
        category_id = request.POST.get('category')
        status = request.POST.get('status', 'new')

        image_file = request.FILES.get('images')

        product = Product.objects.create(
            title=title,
            price=price,
            description=description,
            location=location,
            phone=phone,
            category_id=category_id,
            has_delivery=has_delivery,
            status=status,
            image=image_file,
            owner=request.user if request.user.is_authenticated else None
        )

        messages.success(request, "📦 Эълони шумо бо муваффақият гузошта шуд!")
        return redirect('/')

    categories = Category.objects.all()
    return render(request, 'add_product.html', {'categories': categories, 'districts': DISTRICT_CHOICES})

# 5. Саҳифаи Расонидан
def delivery_page(request):
    return render(request, 'delivery.html')

# 6. Саҳифаи Профил (ТЕГИ @login_required НЕСТ КАРДА ШУД 🛠️)
def profile_page(request):
    # Агар корбар логин бошад, маҳсулотҳои худашро нишон медиҳад, вагарна ҳамаи маҳсулотҳоро
    if request.user.is_authenticated:
        my_products = Product.objects.filter(owner=request.user).order_by('-created_at')
    else:
        my_products = Product.objects.all().order_by('-created_at')[:3] # Намуна барои меҳмон
    
    context = {
        'username': 'Темирзод Ҷалолиддин',
        'status': 'Барномасоз',
        'phone': '+992 ХХХ ХХХ ХХХ',
        'my_products': my_products,
    }
    return render(request, 'profile.html', context)

# 🌟 ИСЛОҲИ ТУГМАИ НЕСТ КАРДАН (ТЕГИ @login_required НЕСТ КАРДА ШУД 🛠️)
def delete_product_api(request, product_id):
    if request.method == 'POST':
        # Кӯшиш мекунад маҳсулотро нест кунад
        try:
            if request.user.is_authenticated:
                product = Product.objects.get(id=product_id, owner=request.user)
            else:
                product = Product.objects.get(id=product_id)
            product.delete()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
        
    return JsonResponse({'status': 'error', 'message': 'Дархости нодуруст'}, status=400)