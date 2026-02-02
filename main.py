import flet as ft
import json
import os
from datetime import datetime
import calendar

# File to store data
DATA_FILE = "data.json"
MEAL_PRICE = 40000

class LunchApp:
    def __init__(self):
        self.data = self.load_data()
        
    def load_data(self):
        """Load data from JSON file"""
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def save_data(self):
        """Save data to JSON file"""
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def get_user_data(self, name):
        """Get user data or create new entry"""
        if name not in self.data:
            self.data[name] = {}
        return self.data[name]
    
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
        
        total_cost = days_attended * MEAL_PRICE
        return days_attended, total_cost

def main(page: ft.Page):
    page.title = "App Cơm Trưa"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.scroll = "auto"
    page.window.width = 400
    page.window.height = 700
    
    app = LunchApp()
    
    # UI Components
    # Pre-defined names list
    names = ["Anh Dương", "Anh Long", "Anh Vinh", "Hưng"]
    
    name_input = ft.Dropdown(
        label="Chọn tên",
        hint_text="Chọn tên của bạn",
        options=[ft.dropdown.Option(name) for name in names],
        border_color=ft.Colors.BLUE_400,
    )
    
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
    
    def show_home():
        """Show home screen"""
        main_container.controls.clear()
        main_container.controls.extend([
            ft.Text(
                "🍱 App Cơm Trưa",
                size=32,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_700,
            ),
            ft.Divider(height=20, thickness=2),
            ft.Text(
                f"Ngày hôm nay: {datetime.now().strftime('%d/%m/%Y')}",
                size=18,
                color=ft.Colors.GREY_700,
            ),
            ft.Row([month_dropdown, year_input], spacing=10),
            ft.Text("Chọn tháng/năm để xem báo cáo", size=14, color=ft.Colors.GREY_600),
            ft.Button(
                "📝 Điểm danh hôm nay",
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
        ])
        page.update()
    
    def show_attendance():
        """Show attendance screen for today with all users"""
        # Get today's date
        today = datetime.now()
        date_str = today.strftime("%Y-%m-%d")
        date_display = today.strftime("%d/%m/%Y")
        
        attendance_container.controls.clear()
        
        # Create checkboxes for each user for today
        checkboxes = []
        for name in names:
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
            ft.Row([
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    on_click=lambda _: show_home(),
                ),
                ft.Text(
                    f"Điểm danh ngày {date_display}",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_700,
                ),
            ]),
            ft.Divider(height=10, thickness=2),
            ft.Container(
                content=attendance_container,
                expand=True,
            ),
        ])
        page.update()
    
    def show_report():
        """Show monthly report for all users"""
        month = int(month_dropdown.value)
        year = int(year_input.value)
        
        report_container.controls.clear()
        
        # Create report for each user
        user_reports = []
        total_all_users = 0
        
        for name in names:
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
        ])
        page.update()
    
    # Initialize with home screen
    show_home()
    
    page.add(main_container)

if __name__ == "__main__":
    ft.app(main)
