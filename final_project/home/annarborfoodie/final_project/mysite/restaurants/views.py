from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db.models import Q

from restaurants.models import Restaurant, Comment, Category, Fav
from restaurants.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView
from restaurants.forms import CommentForm


class FavListView(OwnerListView):
    model = Restaurant
    # By convention:
    template_name = "restaurants/res_list.html"

    def get(self, request):
        favorites = list()
        if request.user.is_authenticated:
            # rows = [{'id': 2}, {'id': 4} ... ]  (A list of rows)
            rows = request.user.favorite_restaurants.values('id')
            # favorites = [2, 4, ...] using list comprehension
            favorites = [ row['id'] for row in rows ]
        my_fav = Restaurant.objects.filter(id__in=favorites)
        context = {'res_list': my_fav}
        return render(request, self.template_name, context)


class CatListView(OwnerListView):
    model = Restaurant
    # By convention:
    template_name = "restaurants/res_list.html"
    context_object_name = 'res_list'

    def get_queryset(self):
        self.cat = get_object_or_404(Category, name=self.kwargs['category'])
        return Restaurant.objects.filter(category=self.cat)


class ResListView(OwnerListView):
    model = Restaurant
    # By convention:
    template_name = "restaurants/res_list.html"

    def get(self, request) :
        res_list = Restaurant.objects.all()
        # favorites = list()
        # if request.user.is_authenticated:
        #     # rows = [{'id': 2}, {'id': 4} ... ]  (A list of rows)
        #     rows = request.user.favorite_ads.values('id')
        #     # favorites = [2, 4, ...] using list comprehension
        #     favorites = [ row['id'] for row in rows ]

        strval = request.GET.get("search", False)
        if strval:
            # Multi-field search
            query = Q(name__contains=strval)
            query.add(Q(location__contains=strval), Q.OR)
            query.add(Q(description__contains=strval), Q.OR)
            res_list = Restaurant.objects.filter(query).select_related().order_by('-rating')[:10]

        ctx = {'res_list' : res_list}
        return render(request, self.template_name, ctx)


class ResDetailView(OwnerDetailView):
    model = Restaurant
    template_name = "restaurants/res_detail.html"
    def get(self, request, pk) :
        x = Restaurant.objects.get(id=pk)
        comments = Comment.objects.filter(restaurant=x).order_by('-updated_at')
        comment_form = CommentForm()

        favorites = list()
        if request.user.is_authenticated:
            # rows = [{'id': 2}, {'id': 4} ... ]  (A list of rows)
            rows = request.user.favorite_restaurants.values('id')
            # favorites = [2, 4, ...] using list comprehension
            favorites = [ row['id'] for row in rows ]

        context = {'restaurant': x, 'comments': comments, 'comment_form': comment_form, 'favorites': favorites}
        return render(request, self.template_name, context)


# class ResCreateView(LoginRequiredMixin, View):
class ResCreateView(OwnerCreateView):
    model = Restaurant
    template_name = 'restaurants/res_form.html'
    success_url = reverse_lazy('restaurants:all')
    fields = ['name', 'description',  'location', 'category', 'tag1', 'tag2', 'tag3', 'rating', 'price', 'pic1', 'pic2', 'pic3']


# class ResUpdateView(LoginRequiredMixin, View):
class ResUpdateView(OwnerUpdateView):
    model = Restaurant
    template_name = 'restaurants/res_form.html'
    success_url = reverse_lazy('restaurants:all')
    fields = ['name', 'description',  'location', 'category', 'tag1', 'tag2', 'tag3', 'rating', 'price', 'pic1', 'pic2', 'pic3']


class ResDeleteView(OwnerDeleteView):
    model = Restaurant
    template_name = 'restaurants/res_confirm_delete.html'
    success_url = reverse_lazy('restaurants:all')


class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        res = get_object_or_404(Restaurant, id=pk)
        comment = Comment(text=request.POST['comment'], owner=request.user, restaurant=res)
        comment.save()
        return redirect(reverse('restaurants:res_detail', args=[pk]))


class CommentDeleteView(OwnerDeleteView):
    model = Comment
    template_name = "restaurants/comment_delete.html"

    # https://stackoverflow.com/questions/26290415/deleteview-with-a-dynamic-success-url-dependent-on-id
    def get_success_url(self):
        res = self.object.restaurant
        return reverse('restaurants:res_detail', args=[res.id])


@method_decorator(csrf_exempt, name='dispatch')
class AddFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        t = get_object_or_404(Restaurant, id=pk)
        fav = Fav(user=request.user, restaurant=t)
        try:
            fav.save()  # In case of duplicate key
        except IntegrityError as e:
            pass
        return HttpResponse()


@method_decorator(csrf_exempt, name='dispatch')
class DeleteFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        t = get_object_or_404(Restaurant, id=pk)
        try:
            fav = Fav.objects.get(user=request.user, restaurant=t).delete()
        except Fav.DoesNotExist as e:
            pass

        return HttpResponse()





