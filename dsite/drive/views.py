from django.shortcuts import render
from .models import Image
# Create your views here.
def index(request, number=1):
    image_list = Image.objects.filter(id__gt=(number-1)*30, id__lte=number*30)
    context = {'image_list': image_list}
    return render(request, 'drive/index.html', context)

def details(request, number):
    image = Image.objects.get(id=number)
    context = {'image': image}
    return render(request, 'drive/details.html', context)