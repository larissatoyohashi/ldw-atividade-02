import flet as ft
from src.views.residencias import view_residencias
from src.state import estado_global

def main(page: ft.Page):
    page.title = estado_global.titulo_app
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT 
    
    page.add(view_residencias(page))

if __name__ == "__main__":
    ft.run(main, view=ft.AppView.WEB_BROWSER)