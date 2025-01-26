import flet as ft

user_set = 'storage/User_settings.py'

def get_value_from_file(user_set, key):
    """Функция для получения значения по ключу из файла"""
    with open(user_set, 'r') as file:
        for line in file:
            if line.startswith(f"{key} ="):
                return line.split('=')[1].strip().strip("'")

def SettingsView(page: ft.Page):
    togle = get_value_from_file(user_set, "b")

    def change_them(e):
        if page.theme_mode == 'dark':
            page.theme_mode = 'light'
            with open(user_set, 'r') as file:
                lines = file.readlines()
                lines[10] = "a = 'light'\n"
                lines[11] = "b = 'False'\n"
            with open(user_set, 'w') as file:
                file.writelines(lines)
            togle = 'False'
        else:
            page.theme_mode = 'dark'
            with open(user_set, 'r') as file:
                lines = file.readlines()
                lines[10] = "a = 'dark'\n"
                lines[11] = "b = 'True'\n"
            with open(user_set, 'w') as file:
                file.writelines(lines)
            togle = 'True'
        
        page.update()

    settings_card = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.ListTile(
                    leading=ft.Icon(ft.icons.PALETTE),
                    title=ft.Text("Внешний вид", weight="bold"),
                    subtitle=ft.Text("Настройте внешний вид приложения"),
                ),
                ft.Divider(),
                ft.Container(
                    content=ft.Row([
                        ft.Row([
                            ft.Icon(
                                ft.icons.DARK_MODE if togle == "True" else ft.icons.LIGHT_MODE,
                                color="amber" if togle == "True" else None
                            ),
                            ft.Text(
                                "Тёмная тема" if togle == "True" else "Светлая тема",
                                weight="bold",
                                size=14
                            ),
                        ]),
                        ft.Switch(
                            on_change=change_them,
                            value=togle == "True",
                            active_color="amber",
                        ),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    padding=ft.padding.only(left=16, right=16, bottom=16),
                )
            ]),
            padding=10,
        )
    )

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=ft.Text(
                        "Настройки",
                        size=32,
                        weight="bold",
                    ),
                    margin=ft.margin.only(bottom=20),
                ),
                settings_card,
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.ListTile(
                                leading=ft.Icon(ft.icons.INFO),
                                title=ft.Text("О приложении", weight="bold"),
                                subtitle=ft.Text("Информация о приложении"),
                            ),
                            ft.Divider(),
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("Версия: 1.0.0", weight="bold"),
                                    ft.Text("Разработчик: Ваше имя"),
                                    ft.Text("© 2024 Все права защищены"),
                                ]),
                                padding=ft.padding.all(16),
                            ),
                        ]),
                        padding=10,
                    ),
                ),
            ],
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        ),
        padding=ft.padding.all(20),
    )