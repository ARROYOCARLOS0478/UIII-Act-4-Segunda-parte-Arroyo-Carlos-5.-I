# app_Proveedor/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Proveedor, Distribuidor, Producto # Solo trabajaremos con Proveedor por ahora
from django.db import IntegrityError # Para manejar errores de unique

# ----------------- Funciones para PROVEEDOR ------------------------------------------------------------
# [0] INICIO DEL SISTEMA (Muestra el inicio.html)
def inicio_sistema(request):
    """Muestra la página de inicio/bienvenida del sistema."""
    return render(request, 'inicio.html')

# [1] INICIO PROVEEDOR (Muestra la tabla de proveedores)
def inicio_proveedor(request):
    """Muestra la lista de proveedores."""
    proveedores = Proveedor.objects.all().order_by('nombre_empresa')
    return render(request, 'proveedor/ver_proveedores.html', {'proveedores': proveedores})


# [2] AGREGAR PROVEEDOR (GET y POST)
def agregar_proveedor(request):
    if request.method == 'POST':
        # Captura de datos del formulario POST (sin forms.py)
        try:
            Proveedor.objects.create(
                nombre_empresa=request.POST.get('nombre_empresa'),
                contacto_principal=request.POST.get('contacto_principal'),
                telefono=request.POST.get('telefono'),
                email=request.POST.get('email'),
                direccion=request.POST.get('direccion'),
                activo=request.POST.get('activo') == 'on' # Checkbox activo
            )
            # Redirigir a la lista de proveedores después de agregar
            return redirect('ver_proveedores')
        except IntegrityError:
            # Manejo básico de datos duplicados (e.g., email o nombre_empresa)
            contexto = {'error': 'Error: El Nombre de la Empresa o Email ya existe.', 'es_post': True}
            return render(request, 'proveedor/agregar_proveedor.html', contexto)
        except Exception as e:
             contexto = {'error': f'Error al guardar: {e}', 'es_post': True}
             return render(request, 'proveedor/agregar_proveedor.html', contexto)
    
    # Si es GET, simplemente renderiza el formulario
    return render(request, 'proveedor/agregar_proveedor.html')


# [3] ACTUALIZAR PROVEEDOR (GET - Muestra el formulario con datos actuales)
def actualizar_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    return render(request, 'proveedor/actualizar_proveedor.html', {'proveedor': proveedor})


# [4] REALIZAR ACTUALIZACION PROVEEDOR (POST - Guarda los cambios)
def realizar_actualizacion_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    
    if request.method == 'POST':
        try:
            proveedor.nombre_empresa = request.POST.get('nombre_empresa')
            proveedor.contacto_principal = request.POST.get('contacto_principal')
            proveedor.telefono = request.POST.get('telefono')
            proveedor.email = request.POST.get('email')
            proveedor.direccion = request.POST.get('direccion')
            proveedor.activo = request.POST.get('activo') == 'on' # Checkbox activo
            
            # Guardar en la BD
            proveedor.save()
            return redirect('ver_proveedores')
        except IntegrityError:
            contexto = {'error': 'Error: El Nombre de la Empresa o Email ya existe.', 'proveedor': proveedor}
            return render(request, 'proveedor/actualizar_proveedor.html', contexto)
        except Exception as e:
            contexto = {'error': f'Error al actualizar: {e}', 'proveedor': proveedor}
            return render(request, 'proveedor/actualizar_proveedor.html', contexto)
    
    return redirect('ver_proveedores') # Si no es POST, regresa a la lista


# [5] BORRAR PROVEEDOR (GET - Muestra confirmación/se utiliza como acción directa)
def borrar_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    
    if request.method == 'POST':
        proveedor.delete()
        return redirect('ver_proveedores')
        
    # Si es GET, muestra la página de confirmación
    return render(request, 'proveedor/borrar_proveedor.html', {'proveedor': proveedor})

# [6] INICIO/VER DISTRIBUIDOR-----------------------------------------------------------------------------------------------
def inicio_distribuidor(request):
    """Muestra la lista de distribuidores."""
    distribuidores = Distribuidor.objects.all().order_by('nombre_distribuidor')
    # Usamos un nuevo template para mostrar la tabla
    return render(request, 'distribuidor/ver_distribuidores.html', {'distribuidores': distribuidores})

# [7] AGREGAR DISTRIBUIDOR (GET y POST)
def agregar_distribuidor(request):
    if request.method == 'POST':
        try:
            # Captura de datos del formulario POST (sin forms.py)
            Distribuidor.objects.create(
                nombre_distribuidor=request.POST.get('nombre_distribuidor'),
                tipo_servicio=request.POST.get('tipo_servicio'),
                ciudad=request.POST.get('ciudad'),
                pais=request.POST.get('pais'),
                tiempo_entrega_dias=request.POST.get('tiempo_entrega_dias'),
                comision=request.POST.get('comision')
            )
            return redirect('ver_distribuidores')
        except IntegrityError:
            contexto = {'error': 'Error: El Nombre del Distribuidor ya existe.', 'es_post': True}
            return render(request, 'distribuidor/agregar_distribuidor.html', contexto)
    
    # Si es GET, simplemente renderiza el formulario
    return render(request, 'distribuidor/agregar_distribuidor.html')


# [8] ACTUALIZAR DISTRIBUIDOR (GET - Muestra el formulario con datos actuales)
def actualizar_distribuidor(request, pk):
    distribuidor = get_object_or_404(Distribuidor, pk=pk)
    return render(request, 'distribuidor/actualizar_distribuidor.html', {'distribuidor': distribuidor})


# [9] REALIZAR ACTUALIZACION DISTRIBUIDOR (POST - Guarda los cambios)
def realizar_actualizacion_distribuidor(request, pk):
    distribuidor = get_object_or_404(Distribuidor, pk=pk)
    
    if request.method == 'POST':
        try:
            distribuidor.nombre_distribuidor = request.POST.get('nombre_distribuidor')
            distribuidor.tipo_servicio = request.POST.get('tipo_servicio')
            distribuidor.ciudad = request.POST.get('ciudad')
            distribuidor.pais = request.POST.get('pais')
            distribuidor.tiempo_entrega_dias = request.POST.get('tiempo_entrega_dias')
            distribuidor.comision = request.POST.get('comision')
            
            distribuidor.save()
            return redirect('ver_distribuidores')
        except IntegrityError:
            contexto = {'error': 'Error: El Nombre del Distribuidor ya existe.', 'distribuidor': distribuidor}
            return render(request, 'distribuidor/actualizar_distribuidor.html', contexto)
    
    return redirect('ver_distribuidores') 


# [10] BORRAR DISTRIBUIDOR (GET/POST - Muestra confirmación/se utiliza como acción directa)
def borrar_distribuidor(request, pk):
    distribuidor = get_object_or_404(Distribuidor, pk=pk)
    
    if request.method == 'POST':
        distribuidor.delete()
        return redirect('ver_distribuidores')
        
    # Si es GET, muestra la página de confirmación
    return render(request, 'distribuidor/borrar_distribuidor.html', {'distribuidor': distribuidor})

