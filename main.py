import flet as ft
from views.settings_view import SettingsView
from views.home_view import HomeView
from views.profile_view import ProfileView
from storage.User_settings import a



def main(page: ft.Page):
    page.window_width = 600  # ширина в пикселях
    page.window_height = 900 # высота в пикселях
    # Функция для обновления текущего экрана
    def update_view(index):
        if index == 0:
            content.controls.clear()
            content.controls.append(HomeView(page))
        elif index == 1:
            content.controls.clear()
            content.controls.append(ProfileView(page))
        elif index == 2:
            content.controls.clear()
            content.controls.append(SettingsView(page))
        page.update()

    # Основное содержимое, которое обновляется
    content = ft.Column()
    page.theme_mode = a
    
    # Начальное содержимое
    update_view(0)

    # Навигационный бар
    page.floating_action_button = None
    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon=ft.icons.CREDIT_CARD, label="Карты"),
            ft.NavigationDestination(icon=ft.icons.ADD, label="Добавить карту"),
            ft.NavigationDestination(icon=ft.icons.SETTINGS, label="Настройки"),
        
        ],
        on_change=lambda e: update_view(e.control.selected_index),
        
    )
    # Добавляем содержимое на страницу
    page.add(content)
    page.update()
ft.app(target=main)
