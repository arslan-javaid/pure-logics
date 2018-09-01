from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from .models import Rack, Book
from django.db.models import Count
from django.contrib import messages
from .forms import RackForm, BookForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@method_decorator(login_required, name='dispatch')
class RackView(TemplateView):
    template_name = 'library/rack.html'

    def get(self, request):
        racks = Rack.objects.annotate(total_books=Count('book'))
        return render(request, self.template_name, {'page': 'rack', 'racks': racks})

    def post(self, request):
        form = RackForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()

            messages.success(request, 'Rack has been saved successfully.')
            racks = Rack.objects.annotate(total_books=Count('book'))
            return render(request, self.template_name, {'alert': 'alert-success', 'page': 'rack', 'racks': racks})
        else:
            messages.success(request, 'Error - Please try again...')
            return render(request, self.template_name, {'alert': 'alert-danger', 'form': form})


@method_decorator(login_required, name='dispatch')
class BookView(TemplateView):
    template_name = 'library/book.html'

    def get(self, request):
        books = Book.objects.all()
        racks = Rack.objects.all()
        return render(request, self.template_name, {'page': 'book', 'racks': racks, 'books': books})

    def post(self, request):
        form = BookForm(request.POST or None, request.FILES or None)
        rack_id = request.POST['rack_id']
        rack = get_object_or_404(Rack, pk=rack_id)
        if form.is_valid():
            books = rack.book_set.all()
            for book in books:
                if book.title == form.cleaned_data.get("title"):
                    messages.success(request, 'You already added that book.')
                    return render(request, self.template_name, {'alert': 'alert-danger', 'form': form})

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
