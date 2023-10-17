from django.shortcuts import render, get_object_or_404, reverse
from .models import Objektas, Klientas, MyBirza
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.forms import User
# from django.views.generic.edit import FormMixin
from .forms import ObjektasReviewForm, UserUpdateForm, ProfilisUpdateForm, UserObjektaiCreateUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
import csv
import pandas as pd

from django.http import HttpResponse

# Create your views here.

def index(request):
    num_objects = Objektas.objects.all().count()
    num_clients = Klientas.objects.all().count()
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_objects': num_objects,
        'num_clients': num_clients,
        'num_visits': num_visits,
    }

    return render(request, 'index.html', context=context)


def klientai(request):
    klientai = Klientas.objects.all()
    paginator = Paginator(Klientas.objects.all(), 3)
    page_number = request.GET.get('page')
    paged_klientai = paginator.get_page(page_number)
    context = {
        'klientai': paged_klientai,
    }
    return render(request, 'klientai.html', context=context)
#
#
def klientas(request, klientas_id):
    klientas = get_object_or_404(Klientas, pk=klientas_id)
    context = {
        'klientas': klientas,
    }
    return render(request, 'klientas.html', context=context)
#
#
class ObjektasListView(generic.ListView):
    model = Objektas
    template_name = "objektai.html"
    context_object_name = "objektai"
    paginate_by = 3
#
#
class ObjektasDetailView(generic.DetailView):
    model = Objektas
    template_name = "objektas.html"
    context_object_name = "objektas"
    # form_class = ObjektasReviewForm

#     def get_success_url(self):
#         return reverse('objektas', kwargs={"pk": self.object.id})
#
#     # standartinis post metodo perrašymas, naudojant FormMixin, galite kopijuoti tiesiai į savo projektą.
#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         form = self.get_form()
#         if form.is_valid():
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)
#
#     def form_valid(self, form):
#         form.instance.book = self.object
#         form.instance.reviewer = self.request.user
#         form.save()
#         return super().form_valid(form)
#
def search(request):
    """
    paprasta paieška. query ima informaciją iš paieškos laukelio,
    search_results prafiltruoja pagal įvestą tekstą knygų pavadinimus ir aprašymus.
    Icontains nuo contains skiriasi tuo, kad icontains ignoruoja ar raidės
    didžiosios/mažosios.
    """
    query = request.GET.get('query')
    search_results = Objektas.objects.filter(Q(adresas__icontains=query) |
        Q(klientas__vardas__icontains=query) | Q(klientas__pavarde__icontains=query))
    return render(request, 'search.html', {'objektai': search_results, 'query': query})
    # search_results = Klientas.objects.filter(
    #     Q(klientas__vardas__icontains=query) | Q(klientas__pavarde__icontains=query))
    # return render(request, 'search.html', {'objektai': search_results, 'query': query})
#
#
@csrf_protect
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, f"Vartotojo vardas {username} užimtas!")
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
                    return redirect('register')
                else:
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'Vartotojas {username} užregistruotas!')
                    return redirect('login')
        else:
            messages.error(request, "Slaptažodžiai nesutampa!")
            return redirect('register')
    else:
        return render(request, 'registration/register.html')

#
@login_required
def profilis(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfilisUpdateForm(request.POST, request.FILES, instance=request.user.profilis)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Profilis atnaujintas")
            return redirect('profilis')

    u_form = UserUpdateForm(instance=request.user)
    p_form = ProfilisUpdateForm(instance=request.user.profilis)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, "profilis.html")
#
#
class UserObjektaiListView(LoginRequiredMixin, generic.ListView):
    model = Objektas
    template_name = 'user_objektai.html'
    context_object_name = "objektai"

    def get_queryset(self):
        return Objektas.objects.filter(user=self.request.user)
#
#
class UserObjektaiDetailView(LoginRequiredMixin, generic.DetailView):
    model = Objektas
    template_name = 'user_objektas.html'
    context_object_name = "objektas"
#
#
class UserObjektaiCreateView(LoginRequiredMixin, generic.CreateView):
    model = Objektas
    template_name = 'user_objektas_form.html'
    success_url = "/solar/manoobjektai/"
    # fields = ['objektas', 'status']
    form_class = UserObjektaiCreateUpdateForm

    def form_valid(self, form):
        form.objektas.reader = self.request.user
        form.save()
        return super().form_valid(form)

#
class UserObjektaiUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Objektas
    template_name = 'user_objektas_form.html'
    # success_url = "/solar/manoobjektai/"
    fields = ['objektas', 'status']


    def get_success_url(self):
        return reverse('manoobjektas', kwargs={"pk": self.object.id})

    def form_valid(self, form):
        form.objektas.reader = self.request.user
        form.save()
        return super().form_valid(form)

    def test_func(self):
        objektas = self.get_object()
        return self.request.user == objektas.reader
#
class UserObjektaiDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Objektas
    template_name = 'user_objektas_delete.html'
    success_url = "/solar/manoobjektai/"
    context_object_name = 'objektas'
#
    def test_func(self):
        objektas = self.get_object()
        return self.request.user == objektas.reader

def my_view(request):
        birza_csv = pd.read_csv('birza.csv', encoding="UTF-8")
        birza_py = birza_csv.to_numpy()
        for row in birza_py:
            my_objects = birza_py
            return render(request, 'birza_template.html', {'my_objects': my_objects})
