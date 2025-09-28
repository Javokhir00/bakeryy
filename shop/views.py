from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from shop.models import Product, Category, Comment, CartItem, Like
from django.contrib import messages
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import json





class Index(View):
    def get(self, request, category_slug = None):
        search_query = request.GET.get('q', '')
        categories = Category.objects.all()

        if category_slug:
            products = Product.objects.filter(category__slug = category_slug)
            category = Category.objects.get(slug = category_slug)
            # paginate category products
            page = request.GET.get('page')
            paginator = Paginator(products, 10)
            try:
                products_page = paginator.page(page)
            except PageNotAnInteger:
                products_page = paginator.page(1)
            except EmptyPage:
                products_page = paginator.page(paginator.num_pages)
            return render(request, 'shop/list.html', {'products': products_page, 'category': category, 'categories': categories, 'paginator': paginator, 'page_obj': products_page})
        else:
            products = Product.objects.all()  # .order_by('price')

            if search_query:
                products = products.filter(name__icontains=search_query)

            # paginate home products
            page = request.GET.get('page')
            paginator = Paginator(products, 10)
            try:
                products_page = paginator.page(page)
            except PageNotAnInteger:
                products_page = paginator.page(1)
            except EmptyPage:
                products_page = paginator.page(paginator.num_pages)
            context = {'products': products_page, 'categories': categories, 'paginator': paginator, 'page_obj': products_page}
            return render(request, 'shop/home.html', context)




def all_product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    context = {'products': products, 'categories': categories}
    return render(request, 'shop/list.html', context)



def product_detail(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        categories = Category.objects.all()
        context = {'product': product, 'categories': categories}
        return render(request, 'shop/detail.html', context)
    except Product.DoesNotExist:
        return HttpResponse('Product not found')



def comment_add(request, product_id):
    product = get_object_or_404(Product, id = product_id)

    # Check if user is authenticated
    if not request.user.is_authenticated:
        messages.error(request, "Please log in to write a comment.")
        return redirect('users:login')

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        content = request.POST.get('content')
        rating = request.POST.get('rating')

        if name and email and content and rating:
            Comment.objects.create(
                product=product,
                name=name,
                email=email,
                content=content,
                rating=rating
            )
            messages.success(request, "Comment successfully added")
        else:
            messages.error(request, "Invalid input")

        return redirect('shop:product_detail', product_id=product_id)

    return redirect('shop:product_detail', product_id=product.id)


def get_cart_products(request):
    """API endpoint to get product information for cart items"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_ids = data.get('product_ids', [])
            
            products = Product.objects.filter(id__in=product_ids).values('id', 'name', 'price', 'image')
            products_dict = {str(product['id']): product for product in products}
            
            return JsonResponse({'products': products_dict})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


def add_to_cart(request, product_id):
    """Add product to user's cart"""
    # Check authentication manually to avoid redirects
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'Authentication required'}, status=401)
    
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)
    
    try:
        product = get_object_or_404(Product, id=product_id)
        
        # Handle both form data and JSON data
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            quantity = int(data.get('quantity', 1))
        else:
            quantity = int(request.POST.get('quantity', 1))
        
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        # Always return JSON response for consistency
        return JsonResponse({
            'success': True,
            'message': f"{product.name} added to cart!",
            'cart_count': CartItem.objects.filter(user=request.user).count()
        })
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f"Error adding to cart: {str(e)}"
        }, status=400)


@login_required
@require_POST
def remove_from_cart(request, product_id):
    """Remove product from user's cart"""
    product = get_object_or_404(Product, id=product_id)
    CartItem.objects.filter(user=request.user, product=product).delete()
    messages.success(request, f"{product.name} removed from cart!")
    return redirect('shop:index')


@login_required
def get_user_cart(request):
    """Get user's cart items"""
    cart_items = CartItem.objects.filter(user=request.user).select_related('product')
    cart_data = []
    
    for item in cart_items:
        cart_data.append({
            'id': item.product.id,
            'name': item.product.name,
            'price': float(item.product.price),
            'image': item.product.image.url,
            'quantity': item.quantity,
            'total_price': float(item.total_price)
        })
    
    return JsonResponse({'cart_items': cart_data})


@login_required
def clear_cart(request):
    """Clear user's entire cart"""
    CartItem.objects.filter(user=request.user).delete()
    messages.success(request, "Cart cleared!")
    return redirect('shop:index')


@login_required
def toggle_like(request, product_id):
    """Toggle like status for a product"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)
    
    try:
        product = get_object_or_404(Product, id=product_id)
        like, created = Like.objects.get_or_create(
            user=request.user,
            product=product
        )
        
        if not created:
            # Unlike the product
            like.delete()
            is_liked = False
            message = f"You unliked {product.name}"
        else:
            # Like the product
            is_liked = True
            message = f"You liked {product.name}"
        
        return JsonResponse({
            'success': True,
            'is_liked': is_liked,
            'message': message,
            'like_count': product.likes.count()
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f"Error toggling like: {str(e)}"
        }, status=400)


@login_required
def get_user_likes(request):
    """Get user's liked products"""
    try:
        liked_products = Like.objects.filter(user=request.user).values_list('product_id', flat=True)
        return JsonResponse({'liked_products': list(liked_products)})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
