from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def cover(request):
    return render(request, 'cover.html')

def about(request):
    return render(request,'about.html')

@login_required
def index(request):
    return render(request, 'index.html')