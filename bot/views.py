from django.shortcuts import render, get_list_or_404, redirect

from .forms import CommentForm
from .models import Appointments, Comment, Employee


def index(request):
    return render(request, 'base.html')


def payment(request):
    appointment = get_list_or_404(Appointments)[-1]
    client_name = appointment.client.name
    client_phone = appointment.client.phone_number
    procedure_price = appointment.procedure.price

    context = {'client_name': client_name,
               'client_phone': client_phone,
               'price': procedure_price
               }

    return render(request, 'payment.html', context)


def comment_list(request):
    comments = Comment.objects.order_by('-created_date')
    return render(request, 'comments_views.html', {'comments': comments})


def add_comment_to_post(request):
    comments = Comment
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=True)
            comment.comments = comments
            comment.save()
            return redirect('comment_list')
    else:
        form = CommentForm()
    return render(request, 'comments_form.html', {'form': form})
