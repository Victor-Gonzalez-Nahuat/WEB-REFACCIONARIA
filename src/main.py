import flet as ft
import requests

API_URL = "https://api-refaccionaria-production.up.railway.app/producto/"

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.RED)
    page.title = "Consulta de Producto"
    page.padding = 10

    

    logo = ft.Image(
    src="https://i.ibb.co/8LxBQKh2/images.png",  # Asegúrate de que el logo esté en una URL accesible públicamente
    width=60,
    height=60,
    fit=ft.ImageFit.CONTAIN
    )

    titulo_empresa = ft.Text(
        "REFACCIONARIA FALLA",
        size=26,
        weight=ft.FontWeight.BOLD,
        color=ft.colors.WHITE
    )
    titulo = ft.Text("Buscar Producto por Código", size=28, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)
    codigo_input = ft.TextField(label="Código del producto", width=1000, color=ft.colors.WHITE, border_color=ft.colors.WHITE, cursor_color=ft.colors.WHITE)
    nombre_input = ft.TextField(label="Nombre del producto", width=400)
    
    encabezado = ft.Container(
        content=ft.Column([
            ft.Row([
                logo,
                titulo_empresa
            ]),
            titulo,
            codigo_input
        ]),
        padding=20,
        bgcolor="#e9423a",
        border_radius=ft.BorderRadius(top_left=0, top_right=0, bottom_left= 20, bottom_right= 20),  # Esquinas inferiores redondeadas
    )
    resultado_card = ft.Container()

    def buscar_producto(e):
        codigo = codigo_input.value.strip()
        if not codigo:
            resultado_card.content = ft.Text("⚠️ Por favor, introduce un código válido.", size=16)
            page.update()
            return

        try:
            res = requests.get(API_URL + codigo)
            if res.status_code == 200:
                data = res.json()
                resultado_card.content = ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text(f"🛠 Nombre: {data['nombre']}", size=20, weight=ft.FontWeight.BOLD),
                            ft.Text(f"🔢 Código: {data['codigo']}"),
                            ft.Text(f"📚 Grupo: {data['grupo']}"),
                            ft.Text(f"🔼 Máximo: {data['maximo']}"),
                            ft.Text(f"🔽 Mínimo: {data['minimo']}"),
                            ft.Text(f"💲 Precio: ${data['precio']:.2f}"),
                            ft.Text(f"📦 Existencia: {data['existencia']}"),
                            ft.Text(f"🧾 Último costo: ${data['ultimo_costo']:.2f}"),
                            ft.Text(f"📅 Última venta: {data['ultima_venta']}"),
                            ft.Text(f"🏭 Proveedor: {data['proveedor']}"),
                        ]),
                        padding=20,
                    ),
                    elevation=4,
                )
            else:
                resultado_card.content = ft.Text("❌ Producto no encontrado.", size=16)
        except Exception as ex:
            resultado_card.content = ft.Text(f"🚫 Error al conectar con la API: {str(ex)}", size=16)

        page.update()
    
    def copiar_al_portapapeles(codigo):
        page.set_clipboard(codigo)
        snack_bar = ft.SnackBar(
        content=ft.Text("✅ Código copiado al portapapeles."),
        bgcolor=ft.colors.GREEN
        )
        page.open(snack_bar)
        page.update()

    def buscar_por_nombre(nombre):
        if not nombre.strip():
            resultado_card.content = ft.Text("⚠️ Por favor, introduce un nombre válido.", size=16)
            cerrar_dialogo()
            page.update()
            return

        try:
            res = requests.get(API_URL + f"nombre/{nombre}")
            if res.status_code == 200:
                data = res.json()
                resultado_card.content = ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text(f"🛠 Nombre: {data['nombre']}", size=20, weight=ft.FontWeight.BOLD),
                            ft.Text(f"🔢 Código: {data['codigo']}"),
                            ft.ElevatedButton("Copiar codigo", on_click= lambda e: copiar_al_portapapeles(data['codigo']))
                        ]),
                        padding=20,
                    ),
                    elevation=4,
                )
            else:
                resultado_card.content = ft.Text("❌ Producto no encontrado por nombre.", size=16)
        except Exception as ex:
            resultado_card.content = ft.Text(f"🚫 Error al conectar con la API: {str(ex)}", size=16)
        page.close(dialogo_busqueda)
        nombre_input.value = ""
        cerrar_dialogo()
        page.update()

    def abrir_dialogo(e):
        page.open(dialogo_busqueda)
        page.update()

    def cerrar_dialogo():
        page.close(dialogo_busqueda)
        page.update()

    botones = ft.Row([
        ft.ElevatedButton("Buscar", on_click=buscar_producto, width=200, height=40, icon=ft.icons.SEARCH),
        ft.ElevatedButton("Buscar codigo", on_click=abrir_dialogo, width=200, height=40, icon=ft.icons.SEARCH)
    ])
    dialogo_busqueda = ft.AlertDialog(
        modal=True,
        title=ft.Text("Buscar por nombre"),
        content=ft.Column([
            nombre_input,
            ft.ElevatedButton("Buscar", on_click=lambda e: buscar_por_nombre(nombre_input.value), icon=ft.icons.SEARCH)
        ], tight=True),
        actions=[ft.TextButton("Cerrar", on_click=lambda e: cerrar_dialogo())],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    page.add(
        ft.Column([
            encabezado,
            botones,
            resultado_card
        ], spacing=20)
    )

ft.app(target=main)
