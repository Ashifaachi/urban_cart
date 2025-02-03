from django.http import JsonResponse,HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from .models import Product,Slider,MainCategory,SubCategory,Manufacturer
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    return render(request, 'admin1/admin_dashboard.html')
def add_item(request):
     context = {
        'main_category': MainCategory.objects.all(),
        'sub_category': SubCategory.objects.all(),
        'manufacturer':Manufacturer.objects.all(),
    }
     
     if request.method == 'POST':
        name = request.POST.get('name')
        manufacturer = request.POST.get('manufacturer')
        manufacturer = get_object_or_404(Manufacturer, name=manufacturer)
        main_category = request.POST.get('main_category')
        main_category = get_object_or_404(MainCategory, name=main_category)
        sub_category = request.POST.get('sub_category')
        sub_category = get_object_or_404(SubCategory, name=sub_category)
        image_url = request.POST.get('image_url')
        site_link = request.POST.get('site_link')
        ratings = float(request.POST.get('ratings', '0') or 0.0)
        no_of_ratings = int(request.POST.get('no_of_ratings', '0') or 0)
        discount_price = float(request.POST.get('discount_price', '0') or 0.0)
        actual_price = float(request.POST.get('actual_price', '0') or 0.0)
        product_stock = int(request.POST.get('product_stock', '0') or 0)
        product, created = Product.objects.get_or_create(
            name=name,
            defaults={
                'manufacturer':manufacturer,
                'main_category': main_category,
                'sub_category': sub_category,
                'image_url': image_url,
                'site_link': site_link,
                'ratings': ratings,
                'no_of_ratings':no_of_ratings,
                'product_stock': product_stock,
                'discount_price': discount_price,
                'actual_price':actual_price
            }
        )

        if not created:
            # If Product exists, update its quantity
            product.product_stock += product_stock
            product.save()
        else:
            # If newly created, save it now
            product.save()
       

        return redirect('add_item')

     return render(request, 'admin1/add_item.html',context)



    #return render(request, 'admin1/add_item.html')
# def delete_item(request):
#      if request.method == 'POST':
#         product_name = request.POST.get('product_name')

#         # Find the book with the specified name
#         product = Product.objects.filter(product_name=product_name)

#         if product.exists():
#             product.delete()  # Deletes the matching product(s)
#             message = f"product '{product_name}' deleted successfully."
#         else:
#             message = f"product '{product_name}' not found."

#         return render(request, 'admin1/delete_item.html', {'message': message})
#      return render(request, 'admin1/delete_item.html')
def delete_item(request):
    # Autocomplete functionality
    if 'term' in request.GET:
        qs = Product.objects.filter(name__icontains=request.GET.get('term'))
        titles = [product.name for product in qs][:10]
        return JsonResponse(titles, safe=False)

    search_products = None
    product = None  # Initialize product to None

    if request.method == 'POST':
        name = request.POST.get('name')

        # Find the product with the specified name
        product = Product.objects.filter(name=name)

        if product.exists():
            product.delete()  # Deletes the matching product(s)
            message = f"Product '{name}' deleted successfully."
        else:
            message = f"Product '{name}' not found."

        return render(request, 'admin1/delete_item.html', {'message': message,'search_products':search_products})

    return render(request, 'admin1/delete_item.html', { 'search_products':search_products})  # Default message for GET
     
    
# def update_item(request):
#       # ✅ Autocomplete functionality
#     if 'term' in request.GET:
#         qs = Product.objects.filter(name__icontains=request.GET.get('term'))
#         titles = [product.name for product in qs]
#         return JsonResponse(titles, safe=False)

#     product = None  # Initialize product variable
#     search_products = None
#     error_message = None
#     success_message = None

#     # ✅ Search functionality
#     search = request.POST.get('search_name')
#     if search:
#         search_products = Product.objects.filter(name__icontains=search)
#         if not search_products.exists():
#             error_message = f"No products found for '{search}'."
#             return render(request, 'admin1/update_item.html', {'error_message': error_message})
        

#     if request.method == 'POST':
#         search_name = request.POST.get('product_name')

#         # Try to find the book using search_name
#         product = get_object_or_404(Product, product_name=search_name)

#         # Update the book's attributes if found
#         if 'product_name' in request.POST:
#             product.product_name = request.POST.get('product_name', product.product_name)
#         if 'product_category' in request.POST:
#             product.product_category = request.POST.get('product_category', product.product_category)
#         if 'product_description' in request.POST:
#             product.product_description = request.POST.get('product_description', product.product_description)
#         if 'product_stock' in request.POST:
#             product.product_stock = int(request.POST.get('product_stock', product.product_stock))
#         if 'product_price' in request.POST:
#             product.product_price = float(request.POST.get('product_price', product.product_price))
#         if 'product_image1' in request.FILES:
#             product.product_image1 = request.FILES.get('product_image1', product.product_image1)
#         if 'product_image2' in request.FILES:
#             product.product_image2 = request.FILES.get('product_image2', product.product_image2)
#         if 'product_image3' in request.FILES:
#             product.product_image3 = request.FILES.get('product_image3', product.product_image3)

#         # Save the updated book
#         product.save()

#         return redirect('admin_dashboard')  # Redirect to the same page or another page
#     return render(request, 'admin1/update_item.html')
# def update_item(request):
#     main_category= MainCategory.objects.all()
#     sub_category= SubCategory.objects.all()
#     manufacturer = Manufacturer.objects.all()
#     context={
#         'main_category':main_category,
#         'sub_category':sub_category,
#         'manufacturer':manufacturer,
        
        
#     }

#     if request.method == 'POST':
#         search_name = request.POST.get('search_name')  # Separate search name for clarity
#         product = get_object_or_404(Product, name=search_name)
        
        

#         # Track if any changes were made
#         changes_made = False

#         # Update fields only if provided
#         if 'name' in request.POST:
#             product.name = request.POST['name']
#             changes_made = True
#         if 'main_category' in request.POST:
#             product.main_category = request.POST['main_category']
#             changes_made = True
#         if 'sub_category' in request.POST:
#             product.sub_category = request.POST['sub_category']
#             changes_made = True
#         if 'product_stock' in request.POST:
#             product.product_stock = int(request.POST.get('product_stock', '0') or 0)
#             changes_made = True
#         if 'discount_price' in request.POST:
#             product.discount_price = float(request.POST.get('discount_price', '0') or 0.0)
#             changes_made = True
#         if 'actual_price' in request.POST:
#             product.actual_price = float(request.POST.get('actual_price', '0') or 0.0)
#             changes_made = True
#         if 'image_url' in request.POST:
#             product.image_url = request.POST['image_url']
#             changes_made = True
#         if 'site_link' in request.POST:
#             product.site_link = request.POST['site_link']
#             changes_made = True
#         # if 'ratings' in request.POST:
#         #     product.ratings = request.POST['ratings']
#         #     changes_made = True
#         if 'ratings' in request.POST:
#             product.ratings = int(request.POST.get('ratings', '0') or 0)
#             changes_made = True
#         if 'no_of_ratings' in request.POST:
#             product.no_of_ratings = request.POST['no_of_ratings']
#             changes_made = True

#         # Save only if changes were made
#         if changes_made:
#             product.save()
#             return redirect('admin_dashboard')
#         else:
#             message = "No changes were made to the product."
#             return render(request, 'admin1/update_item.html', {'message': message})
   

    
#     return render(request, 'admin1/update_item.html',context)
      

   
# def list_item(request):
#     product = Product.objects.all()
#     return render(request,'admin1/list_item.html',{'product':product})
def list_item(request):
    product_list = Product.objects.all()
    paginator = Paginator(product_list, 9)  # Show 10 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'admin1/list_item.html', {'page_obj': page_obj})

    #return render(request, 'admin1/list_item.html')
# def slide(request):
#     if request.method == 'POST':
#         add_head = request.POST.get('add_head')
#         add_sub_head = request.POST.get('add_sub_head')
#         add_text = request.POST.get('add_text')
#         add_price = request.POST.get('add_price')
#         add_image = request.FILES.get('add_image')
       

#         slider = Slider(
#             add_head=add_head,
#             add_sub_head=add_sub_head,
#             add_text=add_text,
#             add_price=add_price,
#             add_image=add_image,
            
#         )
#         slider.save()
#         # show in home app inner index page in 4 houre
#         response.set_cookie('add_head', add_head, max_age=14400)
#         response.set_cookie('add_sub_head', add_sub_head, max_age=14400)
#         response.set_cookie('add_text', add_text, max_age=14400)
#         response.set_cookie('add_price', add_price, max_age=14400)
#         response.set_cookie('add_image', add_image, max_age=14400)
#         return redirect('admin1/add_item.html')
        
#     return render(request, 'admin1/slide.html')

def slide(request):
    if request.method == 'POST':
        add_head = request.POST.get('add_head')
        add_sub_head = request.POST.get('add_sub_head')
        add_text = request.POST.get('add_text')
        add_price = request.POST.get('add_price')
        add_image = request.FILES.get('add_image')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        # Save the slider data in the database
        slider = Slider(
            add_head=add_head,
            add_sub_head=add_sub_head,
            add_text=add_text,
            add_price=add_price,
            add_image=add_image,
            start_time=start_time,
            end_time=end_time
        )
        slider.save()

        return redirect('slide')

       

    return render(request, 'admin1/slide.html')

    
   
# def add_category(request):
#     return render(request, 'add_category.html')
# def delete_category(request):
#     return render(request, 'delete_category.html')


def update_item(request):
     if 'term' in request.GET:
        qs = Product.objects.filter(name__icontains=request.GET.get('term'))[:10]
        titles = list()
        for product in qs:
            titles.append(product.name)
        return JsonResponse(titles,safe=False)
     
     # Handle search functionality
     search = request.POST.get('search_name')
     if search:
        search_products = Product.objects.filter(name__icontains=search)
        if not search_products.exists():
            error_message = f"No products found for '{search}'."
            return render(request, 'admin1/update_item.html', {'error_message': error_message})
     else:
        search_products = None

     # Try to find the book using search_name
     product = get_object_or_404(Product, product_name=search)

     if request.method == 'POST':
          if 'name' in request.POST:
              name = request.POST.get('name')
          elif 'main_category' in request.POST:
              main_category=request.POST.get('main_category')
          elif 'sub_category' in request.POST:
              sub_category=request.POST.get('sub_category')
          elif 'manufacturer' in request.POST:
              manufacturer=request.POST.get('manufacturer')
          elif 'image_url' in request.POST:
              image_url=request.POST.get('image_url')
          elif 'site_link' in request.POST:
              site_link=request.POST.get('site_link')
          elif 'ratings' in request.POST:
              ratings=request.POST.get('ratings')
          elif 'no_of_ratings' in request.POST:
              no_of_ratings=request.POST.get('no_of_ratings')
          elif 'product_stock' in request.POST:
              product_stock=request.POST.get('product_stock')
          elif 'discount_price' in request.POST:
              discount_price=request.POST.get('discount_price')
          elif 'actual_price' in request.POST:
              actual_price=request.POST.get('actual_price')
          product.save()

        
              
         
     context = {
        
        'search_products': search_products,
    }
     return render(request, 'admin1/update_item.html',context)


# def update_item(request):
#     # Handle autocomplete functionality
#     if 'term' in request.GET:
#         qs = Product.objects.filter(name__icontains=request.GET.get('term'))[:10]
#         titles = [product.name for product in qs]
#         return JsonResponse(titles, safe=False)
    
#     # Handle search functionality
#     search = request.POST.get('search_name')
#     if search:
#         search_products = Product.objects.filter(name__icontains=search)
#         if not search_products.exists():
#             error_message = f"No products found for '{search}'."
#             return render(request, 'admin1/update_item.html', {'error_message': error_message})
#     else:
#         search_products = None

#     # Get the product to update
#     product = get_object_or_404(Product, name=search)  # Assuming you're using `name` to find the product

#     if request.method == 'POST':
#         # Update only the fields that are provided in the POST request
#         fields_updated = False
#         if 'name' in request.POST and request.POST.get('name'):
#             product.name = request.POST.get('name')
#             fields_updated = True
#         if 'main_category' in request.POST and request.POST.get('main_category'):
#             product.main_category = request.POST.get('main_category')
#             fields_updated = True
#         if 'sub_category' in request.POST and request.POST.get('sub_category'):
#             product.sub_category = request.POST.get('sub_category')
#             fields_updated = True
#         if 'manufacturer' in request.POST and request.POST.get('manufacturer'):
#             product.manufacturer = request.POST.get('manufacturer')
#             fields_updated = True
#         if 'image_url' in request.POST and request.POST.get('image_url'):
#             product.image_url = request.POST.get('image_url')
#             fields_updated = True
#         if 'site_link' in request.POST and request.POST.get('site_link'):
#             product.site_link = request.POST.get('site_link')
#             fields_updated = True
#         if 'ratings' in request.POST and request.POST.get('ratings'):
#             product.ratings = float(request.POST.get('ratings'))
#             fields_updated = True
#         if 'no_of_ratings' in request.POST and request.POST.get('no_of_ratings'):
#             product.no_of_ratings = int(request.POST.get('no_of_ratings'))
#             fields_updated = True
#         if 'product_stock' in request.POST and request.POST.get('product_stock'):
#             product.product_stock = int(request.POST.get('product_stock'))
#             fields_updated = True
#         if 'discount_price' in request.POST and request.POST.get('discount_price'):
#             product.discount_price = float(request.POST.get('discount_price'))
#             fields_updated = True
#         if 'actual_price' in request.POST and request.POST.get('actual_price'):
#             product.actual_price = float(request.POST.get('actual_price'))
#             fields_updated = True

#         if fields_updated:
#             product.save()  # Save only if at least one field was updated
#             success_message = "Product updated successfully."
#         else:
#             success_message = "No fields were updated."

#         context = {
#             'success_message': success_message,
#             'search_products': search_products,
#         }
#         return render(request, 'admin1/update_item.html', context)

#     # Render the update page
#     context = {
#         'search_products': search_products,
#     }
#     return render(request, 'admin1/update_item.html', context)
# def update_item(request):
#     # Autocomplete functionality
#     if 'term' in request.GET:
#         qs = Product.objects.filter(name__icontains=request.GET.get('term'))
#         titles = [product.name for product in qs]
#         return JsonResponse(titles, safe=False)

#     # Search functionality
    
#     search = request.POST.get('search_name')
#     if search:
#         search_products = Product.objects.filter(name__icontains=search)
#         if not search_products.exists():
#             error_message = f"No products found for '{search}'."
#             return render(request, 'admin1/update_item.html', {'error_message': error_message})
#     else:
#         search_products = None

#     # Handle product update
#     product = get_object_or_404(Product, name=search)
#     if 'product_id' in request.GET:  # Use product_id to fetch the product
#         product = get_object_or_404(Product, id=request.GET['product_id'])

#     if request.method == 'POST' and product:
#         fields_updated = False
#         # Update product details only if the fields are provided
#         if 'name' in request.POST and request.POST.get('name'):
#             product.name = request.POST.get('name')
#             fields_updated = True
#         if 'main_category' in request.POST and request.POST.get('main_category'):
#             product.main_category = request.POST.get('main_category')
#             fields_updated = True
#         if 'sub_category' in request.POST and request.POST.get('sub_category'):
#             product.sub_category = request.POST.get('sub_category')
#             fields_updated = True
#         if 'manufacturer' in request.POST and request.POST.get('manufacturer'):
#             product.manufacturer = request.POST.get('manufacturer')
#             fields_updated = True
#         if 'image_url' in request.POST and request.POST.get('image_url'):
#             product.image_url = request.POST.get('image_url')
#             fields_updated = True
#         if 'site_link' in request.POST and request.POST.get('site_link'):
#             product.site_link = request.POST.get('site_link')
#             fields_updated = True
#         if 'ratings' in request.POST and request.POST.get('ratings'):
#             product.ratings = float(request.POST.get('ratings'))
#             fields_updated = True
#         if 'no_of_ratings' in request.POST and request.POST.get('no_of_ratings'):
#             product.no_of_ratings = int(request.POST.get('no_of_ratings'))
#             fields_updated = True
#         if 'product_stock' in request.POST and request.POST.get('product_stock'):
#             product.product_stock = int(request.POST.get('product_stock'))
#             fields_updated = True
#         if 'discount_price' in request.POST and request.POST.get('discount_price'):
#             product.discount_price = float(request.POST.get('discount_price'))
#             fields_updated = True
#         if 'actual_price' in request.POST and request.POST.get('actual_price'):
#             product.actual_price = float(request.POST.get('actual_price'))
#             fields_updated = True

#         if fields_updated:
#             product.save()  # Save only if at least one field was updated
#             success_message = "Product updated successfully."
#         else:
#             success_message = "No fields were updated."

#         context = {
#             'success_message': success_message,
#             'search_products': search_products,
#             'product': product,
#         }
#         return render(request, 'admin1/update_item.html', context)
# def update_item(request):
#     # Autocomplete functionality
#     if 'term' in request.GET:
#         qs = Product.objects.filter(name__icontains=request.GET.get('term'))
#         titles = [product.name for product in qs][:10]
#         return JsonResponse(titles, safe=False)

#     # Search functionality
#     search_products = None
#     product = None  # Initialize product to None

#     if request.method == 'POST':  # Handle form submission
#         search = request.POST.get('search_name')
#         if search:
#             search_products = Product.objects.filter(name__icontains=search)
#             if not search_products.exists():
#                 error_message = f"No products found for '{search}'."
#                 return render(request, 'admin1/update_item.html', {'error_message': error_message})
#             # If only one product matches, pre-select it
#             if search_products.count() == 1:
#                 product = search_products.first()

#     if 'product_id' in request.GET:  # If a product_id is provided
#         product = get_object_or_404(Product, id=request.GET['product_id'])

#     if request.method == 'POST' and product:
#         fields_updated = False
#         # Update product details only if fields are provided
#         if 'name' in request.POST and request.POST.get('name'):
#             new_name = float(request.POST.get('name'))
#             if product.name != new_name:
#                 product.name = new_name
#                 fields_updated = True
#                 print(f"Updated name to: {new_name}")
#             else:
#                 print("name is the same; no update needed.")
#         if 'main_category' in request.POST and request.POST.get('main_category'):
#             new_main_category = float(request.POST.get('main_category'))
#             if product.main_category != new_main_category:
#                 product.main_category = new_main_category
#                 fields_updated = True
#                 print(f"Updated main_category to: {new_main_category}")
#             else:
#                 print("main_category is the same; no update needed.")
#         if 'sub_category' in request.POST and request.POST.get('sub_category'):
#             new_sub_category = float(request.POST.get('sub_category'))
#             if product.sub_category != new_sub_category:
#                 product.sub_category = new_sub_category
#                 fields_updated = True
#                 print(f"Updated sub_category to: {new_sub_category}")
#             else:
#                 print("sub_category is the same; no update needed.")
#         if 'manufacturer' in request.POST and request.POST.get('manufacturer'):
#             new_manufacturer = float(request.POST.get('manufacturer'))
#             if product.manufacturer != new_manufacturer:
#                 product.manufacturer = new_manufacturer
#                 fields_updated = True
#                 print(f"Updated manufacturer to: {new_manufacturer}")
#             else:
#                 print("manufacturer is the same; no update needed.")
#         if 'image_url' in request.POST and request.POST.get('image_url'):
#             new_image_url = float(request.POST.get('image_url'))
#             if product.image_url != new_image_url:
#                 product.image_url = new_image_url
#                 fields_updated = True
#                 print(f"Updated image_url to: {new_image_url}")
#             else:
#                 print("image_url is the same; no update needed.")
#         if 'site_link' in request.POST and request.POST.get('site_link'):
#             new_site_link = float(request.POST.get('site_link'))
#             if product.site_link != new_site_link:
#                 product.site_link = new_site_link
#                 fields_updated = True
#                 print(f"Updated site_link to: {new_site_link}")
#             else:
#                 print("site_link is the same; no update needed.")
#         if 'ratings' in request.POST and request.POST.get('ratings'):
#             new_ratings = float(request.POST.get('ratings'))
#             if product.ratings != new_ratings:
#                 product.ratings = new_ratings
#                 fields_updated = True
#                 print(f"Updated ratings to: {new_ratings}")
#             else:
#                 print("ratings is the same; no update needed.")
#         if 'no_of_ratings' in request.POST and request.POST.get('no_of_ratings'):
#             new_no_of_ratings = float(request.POST.get('no_of_ratings'))
#             if product.no_of_ratings != new_no_of_ratings:
#                 product.no_of_ratings = new_no_of_ratings
#                 fields_updated = True
#                 print(f"Updated no_of_ratings to: {new_no_of_ratings}")
#             else:
#                 print("no_of_ratings is the same; no update needed.")
#         if 'product_stock' in request.POST and request.POST.get('product_stock'):
#             new_product_stock = float(request.POST.get('product_stock'))
#             if product.product_stock != new_product_stock:
#                 product.product_stock = new_product_stock
#                 fields_updated = True
#                 print(f"Updated product_stock to: {new_product_stock}")
#             else:
#                 print("product_stock is the same; no update needed.")
#         if 'discount_price' in request.POST and request.POST.get('discount_price'):
#             new_discount_price = float(request.POST.get('discount_price'))
#             if product.discount_price != new_discount_price:
#                 product.discount_price = new_discount_price
#                 fields_updated = True
#                 print(f"Updated discount_price to: {new_discount_price}")
#             else:
#                 print("discount_price is the same; no update needed.")
#         if 'actual_price' in request.POST and request.POST.get('actual_price'):
#              new_actual_price = float(request.POST.get('actual_price'))
#              if product.actual_price != new_actual_price:
#                 product.actual_price = new_actual_price
#                 fields_updated = True
#                 print(f"Updated actual_price to: {new_actual_price}")
#              else:
#                 print("Actual price is the same; no update needed.")

#         if fields_updated:
#             product.save()  # Save only if at least one field was updated
#             success_message = "Product updated successfully."
#         else:
#             success_message = "No fields were updated."

#         context = {
#             'success_message': success_message,
#             'search_products': search_products,
#             'product': product,
#         }
#         return render(request, 'admin1/update_item.html', context)

#     return render(request, 'admin1/update_item.html', {'search_products': search_products, 'product': product})
# def update_item(request):
#     # Autocomplete functionality
#     if 'term' in request.GET:
#         qs = Product.objects.filter(name__icontains=request.GET.get('term'))
#         titles = [product.name for product in qs][:10]
#         return JsonResponse(titles, safe=False)

#     search_products = None
#     product = None  # Initialize product to None

#     if request.method == 'POST':  # Handle form submission for search
#         search = request.POST.get('search_name')
#         if search:
#             search_products = Product.objects.filter(name__icontains=search)
#             if not search_products.exists():
#                 error_message = f"No products found for '{search}'."
#                 return render(request, 'admin1/update_item.html', {'error_message': error_message})
#             # If only one product matches, pre-select it
#             if search_products.count() == 1:
#                 product = search_products.first()

#     if 'product_id' in request.GET:  # If a product_id is provided
#         product = get_object_or_404(Product, id=request.GET['product_id'])

#     if request.method == 'POST' and product:
#         fields_updated = False
#         success_message = ""

#         # Define updatable fields and their types
#         updatable_fields = {
#             'name': str,
#             'main_category': str,
#             'sub_category': str,
#             'manufacturer': str,
#             'image_url': str,
#             'site_link': str,
#             'ratings': float,
#             'no_of_ratings': int,
#             'product_stock': int,
#             'discount_price': float,
#             'actual_price': float,
#         }

#         # Update product fields dynamically
#         for field, field_type in updatable_fields.items():
#             if field in request.POST and request.POST.get(field):
#                 new_value = field_type(request.POST.get(field))
#                 if getattr(product, field) != new_value:
#                     setattr(product, field, new_value)
#                     fields_updated = True

#         if fields_updated:
#             product.save()  # Save only if at least one field was updated
#             success_message = f"Product '{product.name}' updated successfully."
#         else:
#             success_message = "No fields were updated."

#         return render(request, 'admin1/update_item.html', {
#             'success_message': success_message,
#             'search_products': search_products,
#             'product': product,
#         })

#     return render(request, 'admin1/update_item.html', {'search_products': search_products, 'product': product})

    # # If no product is found, return with an error
    # if not product:
    #     return render(request, 'admin1/update_item.html', {'error_message': 'Product not found.'})

    # Render the update page
    # context = {
    #     'search_products': search_products,
    #     'product': product,  # Pass the product object for editing
    # }
    # return render(request, 'admin1/update_item.html', context)



# def update_item(request):
#     # ✅ Autocomplete functionality
#     if 'term' in request.GET:
#         qs = Product.objects.filter(name__icontains=request.GET.get('term'))
#         titles = [product.name for product in qs]
#         return JsonResponse(titles, safe=False)

#     product = None  # Initialize product variable
#     search_products = None
#     error_message = None
#     success_message = None

#     # ✅ Search functionality
#     search = request.POST.get('search_name')
#     if search:
#         search_products = Product.objects.filter(name__icontains=search)
#         if not search_products.exists():
#             error_message = f"No products found for '{search}'."
#             return render(request, 'admin1/update_item.html', {'error_message': error_message})

#     # ✅ Fetch product using `product_id` if available
#     product_id = request.GET.get('product_id')
#     if product_id:
#         product = get_object_or_404(Product, id=product_id)
#     elif search_products and search_products.count() == 1:
#         product = search_products.first()

#     if not product:
#         error_message = "No product found for the given search criteria."
#         return render(request, 'admin1/update_item.html', {'error_message': error_message})

#     # ✅ Handle product update
#     if request.method == 'POST':
#         fields_updated = False
#         update_fields = [
#             'name', 'main_category', 'sub_category', 'manufacturer', 'image_url',
#             'site_link', 'ratings', 'no_of_ratings', 'product_stock',
#             'discount_price', 'actual_price'
#         ]

#         for field in update_fields:
#             if field in request.POST and request.POST.get(field):
#                 value = request.POST.get(field)
#                 # Convert values where necessary
#                 if field in ['ratings', 'discount_price', 'actual_price']:
#                     value = float(value)
#                 elif field in ['no_of_ratings', 'product_stock']:
#                     value = int(value)
                
#                 setattr(product, field, value)
#                 fields_updated = True

#         if fields_updated:
#             product.save()
#             success_message = "Product updated successfully."
#         else:
#             success_message = "No fields were updated."

#     # ✅ Return updated context
#     context = {
#         'success_message': success_message,
#         'error_message': error_message,
#         'search_products': search_products,
#         'product': product,
#     }
#     return render(request, 'admin1/update_item.html', context)


# def update_item(request):
#     # ✅ Autocomplete functionality
#     if 'term' in request.GET:
#         qs = Product.objects.filter(name__icontains=request.GET.get('term'))
#         titles = [product.name for product in qs]
#         return JsonResponse(titles, safe=False)

#     product = None
#     search_products = None
#     error_message = None

#     # ✅ If product ID is passed in GET request (after clicking search result)
#     product_id = request.GET.get('product_id')
#     if product_id:
#         product = get_object_or_404(Product, id=product_id)

#     # ✅ Search functionality
#     search = request.POST.get('search_name')
#     if search:
#         search_products = Product.objects.filter(name__icontains=search)
#         if not search_products.exists():
#             error_message = f"No products found for '{search}'."
#         return render(request, 'admin1/update_item.html', {
#             'error_message': error_message,
#             'search_products': search_products
#         })
#     product = get_object_or_404(Product, name=search)
#     # ✅ Updating the product
#     if request.method == 'POST' and product:
#         product.name = request.POST.get('name', product.name)
#         product.manufacturer = request.POST.get('manufacturer', product.manufacturer)
#         product.main_category = request.POST.get('main_category', product.main_category)
#         product.sub_category = request.POST.get('sub_category', product.sub_category)
#         product.image_url = request.POST.get('image_url', product.image_url)
#         product.site_link = request.POST.get('site_link', product.site_link)
#         product.ratings = request.POST.get('ratings', product.ratings)
#         product.no_of_ratings = request.POST.get('no_of_ratings', product.no_of_ratings)
#         product.discount_price = request.POST.get('discount_price', product.discount_price)
#         product.actual_price = request.POST.get('actual_price', product.actual_price)
#         product.product_stock = request.POST.get('product_stock', product.product_stock)

#         product.save()
#         return redirect('admin_dashboard')  # Redirect after updating

#     return render(request, 'admin1/update_item.html', {
#         'product': product,
#         'search_products': search_products
#     })


# def update_item(request):
#     # ✅ Autocomplete functionality
#     if 'term' in request.GET:
#         qs = Product.objects.filter(name__icontains=request.GET.get('term'))
#         titles = [product.name for product in qs]
#         return JsonResponse(titles, safe=False)

#     product = None
#     search_products = None
#     error_message = None

#     # ✅ If product ID is passed in GET request (after clicking search result)
#     product_id = request.GET.get('product_id')
#     if product_id:
#         product = get_object_or_404(Product, id=product_id)

#     # ✅ Search functionality
#     if request.method == 'POST':
#         search = request.POST.get('search_name')
#         if search:
#             search_products = Product.objects.filter(name__icontains=search)
#             if not search_products.exists():
#                 error_message = f"No products found for '{search}'."
#             else:
#                 return render(request, 'admin1/update_item.html', {
#                     'error_message': error_message,
#                     'search_products': search_products
#                 })

#     # ✅ If a product is selected for updating
#     if request.method == 'POST' and product:
#         product.name = request.POST.get('name', product.name)
#         product.manufacturer = request.POST.get('manufacturer', product.manufacturer)
#         product.main_category = request.POST.get('main_category', product.main_category)
#         product.sub_category = request.POST.get('sub_category', product.sub_category)
#         product.image_url = request.POST.get('image_url', product.image_url)
#         product.site_link = request.POST.get('site_link', product.site_link)
#         product.ratings = request.POST.get('ratings', product.ratings)
#         product.no_of_ratings = request.POST.get('no_of_ratings', product.no_of_ratings)
#         product.discount_price = request.POST.get('discount_price', product.discount_price)
#         product.actual_price = request.POST.get('actual_price', product.actual_price)
#         product.product_stock = request.POST.get('product_stock', product.product_stock)

#         # Save the updated product
#         product.save()
#         return redirect('admin_dashboard')  # Redirect after updating

#     return render(request, 'admin1/update_item.html', {
#         'product': product,
#         'search_products': search_products,
#         'error_message': error_message
#     })
