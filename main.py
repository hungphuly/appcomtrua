import flet as ft
import json
import os
from datetime import datetime, timedelta
import calendar
import asyncio
import time

# File to store data
DATA_FILE = "data.json"
MEAL_PRICE = 40000

# Vietnamese day names
WEEKDAYS_VN = {
    0: "Thứ Hai",
    1: "Thứ Ba",
    2: "Thứ Tư",
    3: "Thứ Năm",
    4: "Thứ Sáu",
    5: "Thứ Bảy",
    6: "Chủ Nhật"
}

def format_date_with_weekday(date_obj):
    """Format date as 'Thứ X, DD/MM/YYYY'"""
    weekday_name = WEEKDAYS_VN[date_obj.weekday()]
    date_str = date_obj.strftime("%d/%m/%Y")
    return f"{weekday_name}, {date_str}"

class LunchApp:
    def __init__(self):
        self.data = self.load_data()
        
    def load_data(self):
        """Load data from JSON file with migration support"""
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Migrate old format to new format
            if 'settings' not in data:
                # Old format detected, migrate
                old_attendance = data.copy()
                data = {
                    'settings': {
                        'names': ["Anh Dương", "Anh Long", "Anh Vinh", "Hưng"],
                        'meal_price': 40000
                    },
                    'attendance': old_attendance
                }
                self.data = data
                self.save_data()  # Save migrated data
                return data
            
            return data
        
        # New installation - return default structure
        return {
            'settings': {
                'names': ["Anh Dương", "Anh Long", "Anh Vinh", "Hưng"],
                'meal_price': 40000
            },
            'attendance': {}
        }
    
    def save_data(self):
        """Save data to JSON file"""
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def get_names(self):
        """Get list of user names"""
        return self.data['settings']['names']
    
    def add_name(self, name):
        """Add a new user name"""
        if name and name not in self.data['settings']['names']:
            self.data['settings']['names'].append(name)
            self.save_data()
            return True
        return False
    
    def delete_name(self, name):
        """Delete a user name (keeps attendance data)"""
        if name in self.data['settings']['names']:
            self.data['settings']['names'].remove(name)
            self.save_data()
            return True
        return False
    
    def get_meal_price(self):
        """Get current meal price"""
        return self.data['settings']['meal_price']
    
    def set_meal_price(self, price):
        """Set meal price"""
        try:
            price_int = int(price)
            if price_int > 0:
                self.data['settings']['meal_price'] = price_int
                self.save_data()
                return True
        except ValueError:
            pass
        return False
    
    def get_user_data(self, name):
        """Get user data or create new entry"""
        if 'attendance' not in self.data:
            self.data['attendance'] = {}
        
        if name not in self.data['attendance']:
            self.data['attendance'][name] = {}
        return self.data['attendance'][name]
    
    def mark_attendance(self, name, date_str, attended):
        """Mark attendance for a specific date"""
        user_data = self.get_user_data(name)
        user_data[date_str] = attended
        self.save_data()
    
    def get_monthly_report(self, name, month, year):
        """Generate monthly report for a user"""
        user_data = self.get_user_data(name)
        month_key_prefix = f"{year}-{month:02d}"
        
        days_attended = 0
        for date_str, attended in user_data.items():
            if date_str.startswith(month_key_prefix) and attended:
                days_attended += 1
        
        total_cost = days_attended * self.get_meal_price()
        return days_attended, total_cost

def main(page: ft.Page):
    page.title = "App Cơm Trưa"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.scroll = "auto"
    page.window.width = 400
    page.window.height = 700
    
    app = LunchApp()
    
    # UI Components
    
    # Date picker for attendance
    selected_date = [datetime.now()]  # Use list to make it mutable in closure
    
    def on_date_picked(e):
        """Handle date picker selection"""
        if e.control.value:
            selected_date[0] = e.control.value
            show_attendance()
    
    date_picker = ft.DatePicker(
        on_change=on_date_picked,
        first_date=datetime(2020, 1, 1),
        last_date=datetime(2030, 12, 31),
    )
    page.overlay.append(date_picker)
    
    month_dropdown = ft.Dropdown(
        label="Tháng",
        width=150,
        options=[ft.dropdown.Option(str(i), f"Tháng {i}") for i in range(1, 13)],
        value=str(datetime.now().month),
    )
    
    year_input = ft.TextField(
        label="Năm",
        value=str(datetime.now().year),
        width=150,
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    
    attendance_container = ft.Column(spacing=10, scroll="auto")
    report_container = ft.Column(spacing=10)
    main_container = ft.Column(spacing=15, expand=True)
    
    def show_splash():
        """Show splash screen with logo for 5 seconds"""
        main_container.controls.clear()
        
        # Check if logo exists
        logo_path = "logo.png"
        logo_widget = None
        
        if os.path.exists(logo_path):
            logo_widget = ft.Image(
                src=logo_path,
                width=200,
                height=200,
            )
        
        splash_content = ft.Column(
            [
                ft.Container(height=150),
                logo_widget if logo_widget else ft.Container(height=50),
                ft.Container(height=30),
                ft.Text(
                    "APP cơm trưa",
                    size=36,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.ORANGE_700,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    "🍱",
                    size=48,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        )
        
        main_container.controls.append(
            ft.Container(
                content=splash_content,
                bgcolor=ft.Colors.ORANGE_50,
                expand=True,
            )
        )
        page.update()
        
        # Wait 5 seconds then show home
        time.sleep(5)
        show_home()
    
    def show_home():
        """Show home screen"""
        main_container.controls.clear()
        main_container.controls.extend([
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        "🍱 App Cơm Trưa",
                        size=32,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLUE_700,
                    ),
                    ft.Divider(height=20, thickness=2),
                    ft.Text(
                        f"Ngày hôm nay: {format_date_with_weekday(datetime.now())}",
                        size=16,
                        color=ft.Colors.GREY_700,
                    ),
                    ft.Row([month_dropdown, year_input], spacing=10),
                    ft.Text("Chọn tháng/năm để xem báo cáo", size=14, color=ft.Colors.GREY_600),
                    ft.Container(height=10),
                    ft.Button(
                        "📝 Điểm danh",
                        icon=ft.Icons.CHECK_CIRCLE,
                        on_click=lambda _: show_attendance(),
                        bgcolor=ft.Colors.BLUE_400,
                        color=ft.Colors.WHITE,
                        expand=True,
                    ),
                    ft.Button(
                        "📊 Xem báo cáo tháng",
                        icon=ft.Icons.ASSESSMENT,
                        on_click=lambda _: show_report(),
                        bgcolor=ft.Colors.GREEN_400,
                        color=ft.Colors.WHITE,
                        expand=True,
                    ),
                    ft.Button(
                        "⚙️ Cài đặt",
                        icon=ft.Icons.SETTINGS,
                        on_click=lambda _: show_settings(),
                        bgcolor=ft.Colors.ORANGE_400,
                        color=ft.Colors.WHITE,
                        expand=True,
                    ),
                ]),
                padding=20,
            )
        ])
        page.update()
    
    def show_settings():
        """Show settings menu"""
        main_container.controls.clear()
        main_container.controls.extend([
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.IconButton(
                            icon=ft.Icons.ARROW_BACK,
                            on_click=lambda _: show_home(),
                        ),
                        ft.Text(
                            "⚙️ Cài đặt",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.ORANGE_700,
                        ),
                    ]),
                    ft.Divider(height=20, thickness=2),
                    ft.Container(height=20),
                    ft.Button(
                        "👥 Quản lý tên",
                        icon=ft.Icons.PEOPLE,
                        on_click=lambda _: show_name_management(),
                        bgcolor=ft.Colors.PURPLE_400,
                        color=ft.Colors.WHITE,
                        expand=True,
                    ),
                    ft.Button(
                        "💰 Cài đặt tiền ăn",
                        icon=ft.Icons.ATTACH_MONEY,
                        on_click=lambda _: show_price_settings(),
                        bgcolor=ft.Colors.AMBER_400,
                        color=ft.Colors.WHITE,
                        expand=True,
                    ),
                ]),
                padding=20,
            )
        ])
        page.update()
    
    def show_name_management():
        """Show name management screen"""
        def refresh_names():
            """Refresh the names list display"""
            names_list.controls.clear()
            for name in app.get_names():
                names_list.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Text(
                                f"👤 {name}",
                                size=18,
                                expand=True,
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                icon_color=ft.Colors.RED_400,
                                tooltip="Xóa",
                                on_click=lambda e, n=name: delete_name_handler(n),
                            ),
                        ]),
                        padding=10,
                        bgcolor=ft.Colors.BLUE_50,
                        border_radius=5,
                        margin=ft.margin.only(bottom=5),
                    )
                )
            page.update()
        
        def add_name_handler(e):
            """Handle adding new name"""
            new_name = name_input_field.value.strip()
            if new_name:
                if app.add_name(new_name):
                    name_input_field.value = ""
                    status_text.value = f"✅ Đã thêm '{new_name}'"
                    status_text.color = ft.Colors.GREEN_700
                    refresh_names()
                else:
                    status_text.value = f"⚠️ Tên '{new_name}' đã tồn tại"
                    status_text.color = ft.Colors.ORANGE_700
            else:
                status_text.value = "⚠️ Vui lòng nhập tên"
                status_text.color = ft.Colors.RED_700
            page.update()
        
        def delete_name_handler(name):
            """Handle deleting a name"""
            if len(app.get_names()) > 1:
                app.delete_name(name)
                status_text.value = f"✅ Đã xóa '{name}'"
                status_text.color = ft.Colors.GREEN_700
                refresh_names()
            else:
                status_text.value = "⚠️ Phải có ít nhất 1 tên"
                status_text.color = ft.Colors.RED_700
            page.update()
        
        name_input_field = ft.TextField(
            label="Tên mới",
            hint_text="Nhập tên người dùng",
            expand=True,
        )
        
        status_text = ft.Text("", size=14)
        names_list = ft.Column(spacing=5, scroll="auto")
        
        main_container.controls.clear()
        main_container.controls.extend([
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.IconButton(
                            icon=ft.Icons.ARROW_BACK,
                            on_click=lambda _: show_settings(),
                        ),
                        ft.Text(
                            "👥 Quản lý tên",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.PURPLE_700,
                        ),
                    ]),
                    ft.Divider(height=10, thickness=2),
                    ft.Row([
                        name_input_field,
                        ft.ElevatedButton(
                            "➕ Thêm",
                            on_click=add_name_handler,
                            bgcolor=ft.Colors.GREEN_400,
                            color=ft.Colors.WHITE,
                        ),
                    ]),
                    status_text,
                    ft.Container(height=10),
                    ft.Text("Danh sách tên:", size=16, weight=ft.FontWeight.BOLD),
                    ft.Container(
                        content=names_list,
                        expand=True,
                    ),
                ]),
                padding=20,
                expand=True,
            )
        ])
        
        refresh_names()
        page.update()
    
    def show_price_settings():
        """Show price settings screen"""
        current_price = app.get_meal_price()
        
        def save_price_handler(e):
            """Handle saving new price"""
            new_price = price_input_field.value.strip()
            if app.set_meal_price(new_price):
                status_text.value = f"✅ Đã cập nhật giá: {int(new_price):,} VND"
                status_text.color = ft.Colors.GREEN_700
                current_price_display.value = f"Giá hiện tại: {app.get_meal_price():,} VND"
            else:
                status_text.value = "⚠️ Giá không hợp lệ (phải là số > 0)"
                status_text.color = ft.Colors.RED_700
            page.update()
        
        price_input_field = ft.TextField(
            label="Giá tiền mới",
            hint_text="Nhập giá tiền ăn",
            keyboard_type=ft.KeyboardType.NUMBER,
            value=str(current_price),
        )
        
        status_text = ft.Text("", size=14)
        current_price_display = ft.Text(
            f"Giá hiện tại: {current_price:,} VND",
            size=20,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.GREEN_700,
        )
        
        main_container.controls.clear()
        main_container.controls.extend([
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.IconButton(
                            icon=ft.Icons.ARROW_BACK,
                            on_click=lambda _: show_settings(),
                        ),
                        ft.Text(
                            "💰 Cài đặt tiền ăn",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.AMBER_700,
                        ),
                    ]),
                    ft.Divider(height=10, thickness=2),
                    ft.Container(height=20),
                    current_price_display,
                    ft.Container(height=30),
                    price_input_field,
                    ft.Container(height=10),
                    ft.ElevatedButton(
                        "💾 Lưu",
                        on_click=save_price_handler,
                        bgcolor=ft.Colors.GREEN_400,
                        color=ft.Colors.WHITE,
                        expand=True,
                    ),
                    ft.Container(height=10),
                    status_text,
                ]),
                padding=20,
            )
        ])
        page.update()
    
    def show_attendance():
        """Show attendance screen with date selection"""
        # Get selected date
        current_date = selected_date[0]
        date_str = current_date.strftime("%Y-%m-%d")
        date_display = format_date_with_weekday(current_date)
        
        attendance_container.controls.clear()
        
        # Create checkboxes for each user for selected date
        checkboxes = []
        for name in app.get_names():
            user_data = app.get_user_data(name)
            is_checked = user_data.get(date_str, False)
            
            checkbox = ft.Checkbox(
                label=name,
                value=is_checked,
                data={"name": name, "date": date_str},
                on_change=lambda e: app.mark_attendance(
                    e.control.data["name"],
                    e.control.data["date"],
                    e.control.value
                )
            )
            checkboxes.append(checkbox)
        
        attendance_container.controls.extend(checkboxes)
        
        main_container.controls.clear()
        main_container.controls.extend([
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.IconButton(
                            icon=ft.Icons.ARROW_BACK,
                            on_click=lambda _: show_home(),
                        ),
                        ft.Text(
                            "Điểm danh",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLUE_700,
                        ),
                    ]),
                    ft.Divider(height=10, thickness=2),
                    
                    # Date selection area
                    ft.Container(
                        content=ft.Column([
                            ft.Text(
                                date_display,
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLUE_900,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            ft.Container(height=5),
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK_IOS,
                                    icon_size=20,
                                    on_click=lambda _: change_date(-1),
                                    tooltip="Ngày trước",
                                ),
                                ft.ElevatedButton(
                                    "📅 Chọn ngày",
                                    icon=ft.Icons.CALENDAR_MONTH,
                                    on_click=lambda _: date_picker.pick_date(),
                                    bgcolor=ft.Colors.ORANGE_300,
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.ARROW_FORWARD_IOS,
                                    icon_size=20,
                                    on_click=lambda _: change_date(1),
                                    tooltip="Ngày sau",
                                ),
                            ], alignment=ft.MainAxisAlignment.CENTER),
                        ]),
                        bgcolor=ft.Colors.BLUE_50,
                        padding=15,
                        border_radius=10,
                        border=ft.border.all(2, ft.Colors.BLUE_200),
                    ),
                    
                    ft.Container(height=10),
                    ft.Text("Chọn người ăn:", size=16, weight=ft.FontWeight.BOLD),
                    ft.Container(
                        content=attendance_container,
                        expand=True,
                    ),
                ]),
                padding=20,
                expand=True,
            )
        ])
        page.update()
    
    def change_date(delta):
        """Change selected date by delta days"""
        selected_date[0] = selected_date[0] + timedelta(days=delta)
        show_attendance()
    
    def show_report():
        """Show monthly report for all users"""
        month = int(month_dropdown.value)
        year = int(year_input.value)
        
        report_container.controls.clear()
        
        # Create report for each user
        user_reports = []
        total_all_users = 0
        
        for name in app.get_names():
            days_attended, total_cost = app.get_monthly_report(name, month, year)
            total_all_users += total_cost
            
            user_reports.append(
                ft.Container(
                    content=ft.Column([
                        ft.Text(f"👤 {name}", size=18, weight=ft.FontWeight.BOLD),
                        ft.Text(f"Số ngày ăn: {days_attended} ngày", size=16),
                        ft.Text(
                            f"Tổng tiền: {total_cost:,} VND",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.GREEN_700,
                        ),
                    ]),
                    padding=15,
                    bgcolor=ft.Colors.BLUE_50,
                    border_radius=10,
                    border=ft.border.all(2, ft.Colors.BLUE_200),
                    margin=ft.margin.only(bottom=10),
                )
            )
        
        report_container.controls.extend(user_reports)
        
        # Add total summary at bottom
        report_container.controls.append(
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        f"TỔNG TẤT CẢ",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLUE_900,
                    ),
                    ft.Text(
                        f"{total_all_users:,} VND",
                        size=22,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.RED_700,
                    ),
                ]),
                padding=15,
                bgcolor=ft.Colors.AMBER_50,
                border_radius=10,
                border=ft.border.all(3, ft.Colors.AMBER_400),
            )
        )
        
        main_container.controls.clear()
        main_container.controls.extend([
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.IconButton(
                            icon=ft.Icons.ARROW_BACK,
                            on_click=lambda _: show_home(),
                        ),
                        ft.Text(
                            f"BÁO CÁO THÁNG {month}/{year}",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLUE_700,
                        ),
                    ]),
                    ft.Divider(height=20, thickness=2),
                    report_container,
                ]),
                padding=20,
            )
        ])
        page.update()
    
    # Initialize with splash screen
    page.add(main_container)
    show_splash()

if __name__ == "__main__":
    ft.run(main)
