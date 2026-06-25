from django.shortcuts import render

# Create your views here.
from django.shortcuts import render


def contact_us(request):
    return render(request, "contact/contact_us.html")
