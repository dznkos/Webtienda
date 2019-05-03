from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, CreateView, ListView, RedirectView, UpdateView, TemplateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse

from django.db.models import Q, Max, Min

from tienda.productos.models import Producto, Comentario, CarritoCompras

User = get_user_model()

class Indice(TemplateView):
    template_name = 'index.html'


class ListadoProducto(ListView):
    template_name = 'listado_productos.html'
    model = Producto
    paginate_by = 10

    def get_queryset(self):
        query = None

        if ('nombre' in self.request.GET) and self.request.GET['nombre'] != "":
            query = Q(nombre=self.request.GET["nombre"])

        if ('maximo' in self.request.GET) and self.request.GET['maximo'] != "":
            try:
                if query == None:
                    query = Q(precio__lte=int(float(self.request.GET['maximo'])))
                else:
                    query = query & Q(precio__lte=int(float(self.request.GET['maximo'])))
            except:
                pass
        
        if ('minimo' in self.request.GET) and self.request.GET['minimo'] != "":
            try:
                if query == None:
                    query = Q(precio__gte=int(float(self.request.GET['minimo'])))
                else:
                    query = query & Q(precio__gte=int(float(self.request.GET['minimo'])))
            except:
                pass

        if query is not None:
            productos = Producto.objects.filter(query)
        else:
            productos = Producto.objects.all()
        return productos

    def get_context_data(self, **kwargs):
        context = super(ListadoProducto, self).get_context_data(**kwargs)
        context['maximo'] = Producto.objects.all().aggregate(Max('precio'))['precio__max']
        context['minimo'] = Producto.objects.all().aggregate(Min('precio'))['precio__min']
        return context

#utilizamos las clasese generic de django para los detalles de producto
class DetalleProducto(DetailView):
    template_name = 'detalle.html'
    model = Producto

class ComentarioProducto(CreateView):
    template_name = 'detalle.html'
    model = Comentario
    fields = ('comentario','usuario','producto',)
    
    def get_success_url(self):
        return "/detalle_producto/{}/".format(self.object.producto.pk)

class Salir(LogoutView):
    next_page = reverse_lazy('indice')

class Ingresar(LoginView):
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('indice'))
        else:
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)
    
    def get_success_url(self):
        return reverse('indice')

#clase de verificacion usuario, actualizacion vista
class CambiarPerfil(LoginRequiredMixin, UpdateView):
    model = User
    #unicos campos modificables
    fields = ('telefono', 'last_name', 'first_name','email',)
    success_url = '/'
    template_name = 'perfil.html'

    def get_object(self, queryset=None):
        return self.request.user

class AniadirCarrito(LoginRequiredMixin, CreateView):
    model = CarritoCompras
    fields = ('usuario','producto','precio',)
    success_url = reverse_lazy('indice')
    login_url = 'ingresar'

class EliminarCarrito(LoginRequiredMixin, DeleteView):
    queryset = CarritoCompras.objects.filter(comprado=False)
    model = CarritoCompras
    success_url = reverse_lazy('indice')
    login_url = 'ingresar'

class ListarCarrito(LoginRequiredMixin, ListView):
    template_name = 'carrito.html'
    model = CarritoCompras
    queryset = CarritoCompras.objects.filter(comprado=False,pendiente=False)
    login_url = 'ingresar'

    def get_context_data(self, **kwargs):
        context = super(ListarCarrito, self).get_context_data(**kwargs)
        context['tab'] = 'sincomprar'
        return context

class ListarCarritoPendientes(LoginRequiredMixin,ListView):
    template_name = 'carrito.html'
    model = CarritoCompras
    queryset = CarritoCompras.objects.filter(comprado=False,pendiente=True)
    login_url = 'ingresar'

    def get_context_data(self, **kwargs):
        context = super(ListarCarritoPendientes, self).get_context_data(**kwargs)
        context['tab'] = 'pendientes'
        return context

class ListarCarritoFinalizadas(LoginRequiredMixin,ListView):
    template_name = 'carrito.html'
    model = CarritoCompras
    queryset = CarritoCompras.objects.filter(comprado=True,pendiente=False)
    login_url = 'ingresar'

    def get_context_data(self, **kwargs):
        context = super(ListarCarritoFinalizadas, self).get_context_data(**kwargs)
        context['tab'] = 'finalizadas'
        return context