from django.shortcuts import render
from pms import models
# Create your views here.


def depart_list(request):
    queryset = models.Department.objects.all()
    return render(request, 'depart_list.html', {'queryset': queryset})

