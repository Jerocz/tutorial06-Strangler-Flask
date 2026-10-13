from django.urls import path
from .views import CompraView, compra_rapida_fbv, CompraRapidaView, CompraRapidaServiceView, InventarioView
from .api.views import CompraAPIView

urlpatterns = [
    # Usamos .as_view() para habilitar la CBV
    path('compra/<int:libro_id>/', CompraView.as_view(), name='finalizar_compra'),

    # las 3 versiones de compra rapida
    path('compra-rapida/fbv/<int:libro_id>/', compra_rapida_fbv, name='compra_rapida_fbv'),
    path('compra-rapida/cbv/<int:libro_id>/', CompraRapidaView.as_view(), name='compra_rapida_cbv'),
    path('compra-rapida/<int:libro_id>/', CompraRapidaServiceView.as_view(), name='compra_rapida'),

    # Tutorial 03 - inventario en HTML y API REST
    path('inventario/', InventarioView.as_view(), name='inventario'),
    path('api/v1/comprar/', CompraAPIView.as_view(), name='api_comprar'),
]
