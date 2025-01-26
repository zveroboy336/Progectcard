import flet as ft
import json
from views.home_view import HomeView
import datetime

def ProfileView(page):
    def get_bank_color(bank_name):
        colors = {
            "Сбербанк": ft.colors.GREEN,
            "Тинькофф": ft.colors.YELLOW,
            "Альфа-банк": ft.colors.RED,
            "ВТБ": ft.colors.BLUE
        }
        return colors.get(bank_name, ft.colors.GREY)

    card_name = ft.TextField(
        label="Название карты",
        hint_text="Введите название карты",
        width=300,
        border_radius=8,
        prefix_icon=ft.icons.CREDIT_CARD
    )
    
    banks = ["Сбербанк", "ВТБ", "Тинькофф", "Альфа-банк"]
    bank_dropdown = ft.Dropdown(
        label="Выберите банк",
        options=[ft.dropdown.Option(bank) for bank in banks],
        width=300,
        border_radius=8,
        prefix_icon=ft.icons.ACCOUNT_BALANCE
    )
    
    grace_period = ft.TextField(
        label="Льготный период",
        hint_text="Количество дней",
        keyboard_type=ft.KeyboardType.NUMBER,
        width=300,
        border_radius=8,
        prefix_icon=ft.icons.CALENDAR_TODAY
    )
    
    credit_limit = ft.TextField(
        label="Кредитный лимит",
        hint_text="Введите сумму",
        keyboard_type=ft.KeyboardType.NUMBER,
        prefix_text="₽",
        width=300,
        border_radius=8,
        prefix_icon=ft.icons.MONEY
    )

    def save_card_to_file(card_data):
        try:
            try:
                with open('cards.txt', 'r', encoding='utf-8') as file:
                    cards = [line.strip() for line in file.readlines()]
            except FileNotFoundError:
                cards = []
            
            creation_date = datetime.datetime.now().strftime('%Y-%m-%d')
            card_str = f"{card_data['name']}|{card_data['bank']}|{card_data['grace_period']}|{card_data['credit_limit']}|{creation_date}"
            cards.append(card_str)
            
            with open('cards.txt', 'w', encoding='utf-8') as file:
                for card in cards:
                    file.write(card + '\n')
            return True
        except Exception as e:
            print(f"Ошибка при сохранении карты: {e}")
        return False

    def add_card(e):
        if not all([card_name.value, bank_dropdown.value, grace_period.value, credit_limit.value]):
            page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Row([
                        ft.Icon(ft.icons.WARNING, color=ft.colors.AMBER),
                        ft.Text("Пожалуйста, заполните все поля")
                    ])
                )
            )
            return
        
        try:
            grace_days = int(grace_period.value)
            limit = float(credit_limit.value)
            if grace_days <= 0 or limit <= 0:
                raise ValueError("Значения должны быть положительными")
        except ValueError:
            page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Row([
                        ft.Icon(ft.icons.ERROR, color=ft.colors.RED),
                        ft.Text("Проверьте правильность ввода числовых значений")
                    ])
                )
            )
            return

        card_data = {
            "name": card_name.value,
            "bank": bank_dropdown.value,
            "grace_period": grace_days,
            "credit_limit": limit
        }

        if save_card_to_file(card_data):
            page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Row([
                        ft.Icon(ft.icons.CHECK_CIRCLE, color=ft.colors.GREEN),
                        ft.Text("Карта успешно добавлена")
                    ])
                )
            )
            page.navigation_bar.selected_index = 0
            content_column = page.controls[0]
            content_column.controls.clear()
            content_column.controls.append(HomeView(page))
            page.update()
        else:
            page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Row([
                        ft.Icon(ft.icons.ERROR, color=ft.colors.RED),
                        ft.Text("Ошибка при сохранении карты")
                    ])
                )
            )

    def cancel(e):
        page.navigation_bar.selected_index = 0
        content_column = page.controls[0]
        content_column.controls.clear()
        content_column.controls.append(HomeView(page))
        page.update()

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=ft.Text(
                        "Добавление новой карты",
                        size=32,
                        weight="bold",
                    ),
                    margin=ft.margin.only(bottom=20),
                ),
                
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.ListTile(
                                leading=ft.Icon(ft.icons.ADD_CARD),
                                title=ft.Text("Информация о карте", weight="bold"),
                                subtitle=ft.Text("Заполните данные о новой кредитной карте"),
                            ),
                            ft.Divider(),
                            ft.Container(
                                content=ft.Column([
                                    card_name,
                                    bank_dropdown,
                                    grace_period,
                                    credit_limit
                                ], 
                                spacing=20,
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                ),
                                padding=ft.padding.all(20),
                            ),
                            ft.Divider(),
                            ft.Container(
                                content=ft.Row(
                                    [
                                        ft.ElevatedButton(
                                            text="Добавить карту",
                                            icon=ft.icons.ADD,
                                            on_click=add_card,
                                            bgcolor=ft.colors.BLUE,
                                            color=ft.colors.WHITE,
                                            style=ft.ButtonStyle(
                                                shape=ft.RoundedRectangleBorder(radius=8)
                                            )
                                        ),
                                        ft.OutlinedButton(
                                            text="Отмена",
                                            icon=ft.icons.CANCEL,
                                            on_click=cancel,
                                            style=ft.ButtonStyle(
                                                shape=ft.RoundedRectangleBorder(radius=8)
                                            )
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ),
                                padding=ft.padding.all(20),
                            ),
                        ]),
                        padding=10,
                    ),
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        ),
        padding=ft.padding.all(20),
    )