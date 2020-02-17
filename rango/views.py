from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

def index(request):
    # Query the database for a list of ALL categories currently stored. # Order the categories by no. likes in descending order.
    # Retrieve the top 5 only - or all if less than 5.
    # Place the list in our context_dict dictionary
    # that will be passed to the template engine.
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {}
    context_dict = {'categories': category_list}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!' 
    context_dict['pages'] = page_list
    # Render the response and send it back!
    return render(request, 'rango/index.html', context_dict)

def about(request):
    return render(request,'rango/about.html')

def show_category(request, category_name_slug):

     context_dict = {}
     try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
         category = Category.objects.get(slug=category_name_slug)
         # Retrieve all of the associated pages.
         # Note that filter() will return a list of page objects or an empty list
         pages = Page.objects.filter(category=category)
         context_dict['pages'] = pages
         context_dict['category'] = category
     except Category.DoesNotExist:
         context_dict['category'] = None 
         context_dict['pages'] = None
     return render(request, 'rango/category.html', context=context_dict)
    
def add_category(request):
     form = CategoryForm()

     # A HTTP POST?
     if request.method == 'POST':
         form = CategoryForm(request.POST)

         # Have we been provided with a valid form?
         if form.is_valid():
             # Save the new category to the database.
             form.save(commit=True)
             # Now that the category is saved, we could confirm this.
             # For now, just redirect the user back to the index view.
             return redirect('/rango/')
         else:
             # The supplied form contained errors
             # just print them to the terminal.
             print(form.errors)
     return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):
     try:
         category = Category.objects.get(slug=category_name_slug)
     except Category.DoesNotExist:
         category = None

     # You cannot add a page to a Category that does not exist...
     if category is None:
         return redirect('/rango/')

     form = PageForm()

     if request.method == 'POST':
         form = PageForm(request.POST)

         if form.is_valid():
             if category:
                 page = form.save(commit=False)
                 page.category = category
                 page.views = 0
                 page.save()

                 return redirect(reverse('rango:show_category',
                                         kwargs={'category_name_slug':
                                                 category_name_slug}))
         else:
             print(form.errors)
     context_dict = {'form': form, 'category': category}
     return render(request, 'rango/add_page.html', context=context_dict)