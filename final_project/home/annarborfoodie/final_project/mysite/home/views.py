from django.shortcuts import render
from django.views import View
from restaurants.models import Restaurant

class HomeView(View):
    def get(self, request):
        suggested_res = Restaurant.objects.order_by('-rating')[:4]
        ctx = {'restaurants': suggested_res}
        return render(request, 'home/main.html', ctx)
