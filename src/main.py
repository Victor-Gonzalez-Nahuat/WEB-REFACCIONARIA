import flet as ft
import requests

def main(page: ft.Page):
    response = requests.get("https://api-refaccionaria-production.up.railway.app/productos/")
    productos = response.json()

    page.add(ft.Text("Lista de Productos", size=30, weight=ft.FontWeight.BOLD))

    productos_text = []
    for producto in productos:
        producto_str = f"Producto: {producto['nombre']} | Código: {producto['codigo']}"
        productos_text.append(ft.Text(producto_str, size=20))

    page.add(ft.Column(
        controls=productos_text,
        spacing=10,
        alignment=ft.MainAxisAlignment.CENTER
    ))

    page.background = ft.colors.LIGHT_BLUE
    page.padding = 20

ft.app(main)
