import flet as ft
from src.api import get_residencias, create_residencia

def view_residencias(page: ft.Page):
    nome_input = ft.TextField(label="Nome/Endereço da Residência", expand=True)
    valor_input = ft.TextField(label="Valor (R$)", keyboard_type=ft.KeyboardType.NUMBER, expand=True)
    
    lista_residencias = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO, spacing=10)

    def carregar_lista():
        lista_residencias.controls.clear()
        dados = get_residencias()
        
        if not dados:
            lista_residencias.controls.append(
                ft.Text("Nenhuma residência encontrada.", italic=True, color=ft.Colors.GREY_500)
            )
        else:
            for item in dados:
                nome = item.get("nome", "Sem nome")
                valor = item.get("valor", 0)
                
                lista_residencias.controls.append(
                    ft.Card(
                        content=ft.Container(
                            padding=15,
                            content=ft.Text(f"🏠 {nome}   |   R$ {valor}", size=16, weight=ft.FontWeight.W_500)
                        )
                    )
                )

    def enviar_formulario(e):
        if not nome_input.value or not valor_input.value:
            exibir_feedback("Por favor, preencha todos os campos!", ft.Colors.RED_400)
            return

        nova_residencia = {
            "nome": nome_input.value,
            "valor": float(valor_input.value)
        }

        sucesso = create_residencia(nova_residencia)
        
        if sucesso:
            exibir_feedback("Residência cadastrada com sucesso!", ft.Colors.GREEN_600)
            nome_input.value = ""
            valor_input.value = ""
            carregar_lista()
            page.update()
        else:
            exibir_feedback("Erro ao conectar com o servidor.", ft.Colors.RED_400)

    def exibir_feedback(mensagem, cor):
        page.snack_bar = ft.SnackBar(ft.Text(mensagem), bgcolor=cor)
        page.snack_bar.open = True
        page.update()

    btn_salvar = ft.ElevatedButton("Cadastrar", on_click=enviar_formulario, icon="save", color=ft.Colors.WHITE, bgcolor=ft.Colors.BLUE_500)
    
    carregar_lista()

    return ft.Column([
        ft.Text("Cadastrar Nova Residência", size=24, weight=ft.FontWeight.BOLD),
        ft.Row([nome_input, valor_input]),
        btn_salvar,
        ft.Divider(height=30),
        ft.Text("Residências Cadastradas", size=20, weight=ft.FontWeight.BOLD),
        ft.Container(content=lista_residencias, expand=True)
    ], expand=True)