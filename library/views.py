from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, DetailView
from .models import Rack, Book
from django.db.models import Count, Q
from django.contrib import messages
from .forms import RackForm, BookForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse


@method_decorator(login_required, name='dispatch')
class RackView(TemplateView):
    template_name = 'library/rack.html'

    def get(self, request):
        racks = Rack.objects.annotate(total_books=Count('book'))
        return render(request, self.template_name, {'page': 'rack', 'racks': racks})

    def post(self, request):
        # Super User Check
        superuser = request.user.is_superuser
        if not superuser:
            messages.success(request, 'Error - Only super user can perform this action.')
            return render(request, self.template_name, {'alert': 'alert-danger'})

        form = RackForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()

            messages.success(request, 'Rack has been saved successfully.')
            racks = Rack.objects.annotate(total_books=Count('book'))
            return render(request, self.template_name, {'alert': 'alert-success', 'page': 'rack', 'racks': racks})
        else:
            messages.success(request, 'Error - Please try again...')
            return render(request, self.template_name, {'alert': 'alert-danger', 'form': form})


class RackDetailView(DetailView):
    model = Rack



@method_decorator(login_required, name='dispatch')
class BookView(TemplateView):
    template_name = 'library/book.html'

    def get(self, request):

        search = request.GET.get('search')
        if search is None:
            books = Book.objects.all()
            racks = Rack.objects.all()
            return render(request, self.template_name, {'page': 'book', 'racks': racks, 'books': books})
        else:
            books = Book.objects.filter(Q(title__contains=search) | Q(author__contains=search) |
                                        Q(published_year__contains=search)).values('title', 'author',
                                                                                   'published_year', 'rack__name')
            books_list = list(books)
            return JsonResponse(books_list, safe=False)

    def post(self, request):
        # Super User Check
        superuser = request.user.is_superuser
        if not superuser:
            messages.success(request, 'Error - Only super user can perform this action.')
            return render(request, self.template_name, {'alert': 'alert-danger'})

        form = BookForm(request.POST or None, request.FILES or None)
        rack_id = request.POST['rack_id']
        rack = get_object_or_404(Rack, pk=rack_id)
        if form.is_valid():
            # Current Racks & books
            current_books = Book.objects.all()
            current_racks = Rack.objects.all()
            context = {'alert': 'alert-danger', 'page': 'book', 'racks': current_books, 'books': current_racks,
                       'form': form}

            books = rack.book_set.all()
            # Only 10 books can be added in a rack.
            if books.count() >= 10:
                messages.success(request, 'Only 10 books can be added in a rack.')
                return render(request, self.template_name, context)

            for book in books:
                if book.title == form.cleaned_data.get("title"):
                    messages.success(request, 'You already added that book.')
                    return render(request, self.template_name, context)

            book = form.save(commit=False)
            book.rack = rack
            book.save()

            messages.success(request, 'Book has been saved successfully.')
            books = Book.objects.all()
            racks = Rack.objects.all()
            return render(request, self.template_name, {'alert': 'alert-success', 'page': 'book', 'racks': racks,
                                                        'books': books})
        else:
            messages.success(request, 'Error - Please try again...')
            return render(request, self.template_name, {'alert': 'alert-danger', 'form': form})
