import flet as ft
from storage.User_settings import d
import datetime

user_set = 'storage/User_settings.py'

def get_value_from_file(user_set, key):
    """Функция для получения значения по ключу из файла"""
    with open(user_set, 'r') as file:
        for line in file:
            if line.startswith(f"{key} ="):
                return line.split('=')[1].strip().strip("'")

def read_cards():
    """Функция для чтения карт из файла"""
    cards = []
    needs_update = False
    try:
        with open('cards.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
            
        # Обновляем файл, если нужно добавить даты
        updated_lines = []
        for line in lines:
            parts = line.strip().split('|')
            if len(parts) == 4:
                name, bank, grace_period, credit_limit = parts
                creation_date = datetime.datetime.now().strftime('%Y-%m-%d')
                updated_lines.append(f"{name}|{bank}|{grace_period}|{credit_limit}|{creation_date}")
                needs_update = True
            else:
                updated_lines.append(line.strip())

        # Перезаписываем файл, если были добавлены даты
        if needs_update:
            with open('cards.txt', 'w', encoding='utf-8') as file:
                for line in updated_lines:
                    file.write(line + '\n')

        # Читаем обновленные данные
        for line in updated_lines:
            parts = line.split('|')
            name, bank, grace_period, credit_limit, creation_date = parts
            cards.append({
                'name': name,
                'bank': bank,
                'grace_period': int(grace_period),
                'credit_limit': float(credit_limit),
                'creation_date': creation_date
            })
            
    except FileNotFoundError:
        pass
    return cards

def delete_card(index):
    """Функция для удаления карты"""
    cards = read_cards()
    if 0 <= index < len(cards):
        cards.pop(index)
        with open('cards.txt', 'w', encoding='utf-8') as file:
            for card in cards:
                card_str = f"{card['name']}|{card['bank']}|{card['grace_period']}|{card['credit_limit']}|{card['creation_date']}"
                file.write(card_str + '\n')
        return True
    return False

def calculate_remaining_days(creation_date_str, grace_period):
    """Расчет оставшихся дней льготного периода"""
    creation_date = datetime.datetime.strptime(creation_date_str, '%Y-%m-%d')
    current_date = datetime.datetime.now()
    days_passed = (current_date - creation_date).days
    remaining_days = max(0, grace_period - days_passed)
    return remaining_days

# [Все предыдущие импорты и функции остаются без изменений]

def HomeView(page):
    page.scroll = ft.ScrollMode.AUTO

    def get_bank_style(bank_name):
        bank_name = bank_name.lower()
        styles = {
            "сбер": {
                "color": "#21A038",
                "icon": ft.icons.SAVINGS_OUTLINED
            },
            "тинькофф": {
                "color": "#333333",
                "icon": ft.icons.CREDIT_CARD
            },
            "альфа": {
                "color": "#EF3124",
                "icon": ft.icons.ACCOUNT_BALANCE
            },
            "втб": {
                "color": "#009FDF",
                "icon": ft.icons.ACCOUNT_BALANCE_WALLET
            }
        }
        return styles.get(next((k for k in styles if k in bank_name), "default"), {
            "color": "#666666",
            "icon": ft.icons.CREDIT_CARD
        })

    cards_column = ft.Column(
        spacing=16,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )
    
    def refresh_cards():
        cards_column.controls.clear()
        cards = read_cards()
        total_limit = sum(card['credit_limit'] for card in cards)
        
        # Отображение общего баланса
        if get_value_from_file(user_set, "c") != '0':
            cards_column.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Text("Общий кредитный лимит", size=14),
                        ft.Text(
                            f"{total_limit:,.2f}{d}",
                            size=28,
                            weight="bold",
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=4),
                    margin=ft.margin.only(bottom=20),
                    padding=ft.padding.symmetric(horizontal=20, vertical=16),
                    border_radius=12,
                    bgcolor=ft.colors.SURFACE_VARIANT,
                    width=float("inf"),  # Для адаптивности
                )
            )
        
        if not cards:
            cards_column.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.icons.CREDIT_CARD_OFF_OUTLINED, size=48),
                        ft.Text(
                            "Нет добавленных карт",
                            size=16,
                            weight="bold",
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=12),
                    margin=ft.margin.only(top=40),
                    width=float("inf"),  # Для адаптивности
                )
            )
        
        for index, card in enumerate(cards):
            remaining_days = calculate_remaining_days(card['creation_date'], card['grace_period'])
            progress = remaining_days / card['grace_period']
            bank_style = get_bank_style(card['bank'])
            
            def create_delete_handler(idx):
                def handle_delete(e):
                    if delete_card(idx):
                        page.show_snack_bar(ft.SnackBar(content=ft.Text("Карта удалена")))
                        refresh_cards()
                        page.update()
                return handle_delete

            def create_details_handler(card_data):
                def handle_details(e):
                    pass
                return handle_details

            progress_color = (
                "#FF4444" if progress < 0.3
                else "#FFAA00" if progress < 0.6
                else "#00C853"
            )

            card_item = ft.Container(
                content=ft.Column([
                    ft.ResponsiveRow([
                        ft.Column([
                            ft.Row([
                                ft.Container(
                                    content=ft.Icon(
                                        bank_style['icon'],
                                        color=bank_style['color'],
                                        size=24
                                    ),
                                    padding=8,
                                    border_radius=8,
                                    bgcolor=ft.colors.with_opacity(0.1, bank_style['color'])
                                ),
                                ft.Column([
                                    ft.Text(
                                        card['name'],
                                        size=16,
                                        weight="bold",
                                    ),
                                    ft.Text(
                                        card['bank'],
                                        size=13,
                                        color=bank_style['color']
                                    ),
                                ], spacing=2),
                            ], spacing=12),
                        ], col={"sm": 12, "md": 6}),
                        ft.Column([
                            ft.Container(
                                content=ft.Text(
                                    f"{card['credit_limit']:,.0f}₽",
                                    size=18,
                                    weight="bold",
                                    text_align=ft.TextAlign.RIGHT,
                                ),
                                padding=ft.padding.symmetric(horizontal=12, vertical=4),
                                border_radius=8,
                                bgcolor=ft.colors.with_opacity(0.05, "#000000"),
                                alignment=ft.alignment.center_right,
                            ),
                        ], col={"sm": 12, "md": 6}, horizontal_alignment=ft.CrossAxisAlignment.END),
                    ]),
                    ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Text(
                                    "Льготный период",
                                    size=13,
                                ),
                                ft.Text(
                                    f"{remaining_days} из {card['grace_period']} дней",
                                    size=13,
                                    weight="bold",
                                    color=progress_color
                                ),
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.Container(height=6),
                            ft.ProgressBar(
                                value=progress,
                                height=4,
                                color=progress_color,
                                bgcolor=ft.colors.with_opacity(0.1, progress_color)
                            ),
                        ]),
                        margin=ft.margin.symmetric(vertical=12)
                    ),
                    ft.Row([
                        ft.Text(
                            f"Создано: {card['creation_date']}",
                            size=12,
                            color="#666666"
                        ),
                        ft.Row([
                            ft.IconButton(
                                icon=ft.icons.INFO_OUTLINE,
                                icon_size=18,
                                tooltip="Подробнее",
                                on_click=create_details_handler(card)
                            ),
                            ft.IconButton(
                                icon=ft.icons.DELETE_OUTLINE,
                                icon_size=18,
                                tooltip="Удалить",
                                on_click=create_delete_handler(index)
                            ),
                        ], spacing=0),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ]),
                padding=16,
                border_radius=12,
                border=ft.border.all(0.5, "#DEDEDE"),
                width=float("inf"),  # Для адаптивности
            )
            cards_column.controls.append(card_item)
        
        page.update()

    refresh_cards()

    return ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Text(
                    "Мои кредитные карты",
                    size=24,
                    weight="bold",
                    text_align=ft.TextAlign.CENTER,
                ),
                margin=ft.margin.only(bottom=24),
                width=float("inf"),  # Для адаптивности
            ),
            cards_column
        ]),
        padding=20,
        expand=True,
        width=float("inf"),  # Для адаптивности
    )

# [Остальные функции остаются без изменений]

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