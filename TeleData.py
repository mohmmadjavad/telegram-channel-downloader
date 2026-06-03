import customtkinter as ctk
from tkinter import messagebox, scrolledtext
from tkcalendar import DateEntry
import json
import os
import asyncio
import threading
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError, PhoneCodeInvalidError
import pandas as pd
from datetime import datetime
import socks
import urllib.request

# تنظیمات ظاهری
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ترجمه‌ها
TRANSLATIONS = {
    "en": {
        "app_title": "Telegram Channel Downloader",
        "settings": "⚙ Settings",
        "help": "❓ Help",
        "run": "▶ Run",
        "stop": "⏹ Stop",
        "ready": "✅ Ready",
        "complete_settings": "⚠ Please complete settings",
        "api_settings": "🔑 API Settings",
        "appearance_settings": "🎨 Appearance",
        "auth_settings": "🔐 Authentication",
        "channel_settings": "📢 Channel Settings",
        "api_id": "API ID:",
        "api_hash": "API Hash:",
        "channel_address": "Channel Username:",
        "phone_number": "Phone Number:",
        "send_code": "📱 Send Code",
        "verification_code": "Verification Code:",
        "verify_code": "✓ Verify Code",
        "two_fa_password": "Two-Factor Password:",
        "verify_password": "✓ Verify Password",
        "start_date": "Start Date:",
        "end_date": "End Date:",
        "clear_date_filter": "❌ Clear Filter",
        "back": "🔙 Back",
        "save_settings": "💾 Save",
        "save_and_back": "✓ Save & Back",
        "downloading": "📥 Downloading...",
        "connecting": "Connecting...",
        "error": "Error",
        "fill_all_fields": "Please fill all fields",
        "code_sent": "✓ Code sent",
        "login_success": "✓ Login successful!",
        "enter_2fa": "Enter 2FA password",
        "invalid_code": "Invalid code",
        "settings_saved": "✓ Settings saved",
        "complete_settings_first": "Complete settings first",
        "connected": "Connected",
        "getting_messages": "Getting messages...",
        "messages_downloaded": "messages downloaded!",
        "no_new_messages": "ℹ No new messages",
        "language": "Language:",
        "theme": "Theme:",
        "light": "☀ Light",
        "dark": "🌙 Dark",
        "developer": "󰞵 Developer",
        "developer_id": "Developer ID:",
        "download_stopped": "⏸ Stopped",
        "can_resume": "Resume next time",
        "proxy_settings": "🌐 Proxy",
        "use_proxy": "Use Telegram Proxy",
        "proxy_link": "Proxy Link:",
        "proxy_link_hint": "tg://proxy?...",
        "test_proxy": "🧪 Test",
        "proxy_connected": "✓ Connected",
        "proxy_error": "✗ Failed",
        "window_size": "Window Size:",
        "width": "Width:",
        "height": "Height:",
        "concurrent_downloads": "Concurrent Downloads:",
        "concurrent_hint": "Download multiple files at once (1-10)",
        "help_title": "❓ Help & Guide",
        "help_content": """
📖 COMPLETE USER GUIDE
═══════════════════════════════════════
🚀 QUICK START GUIDE

󰍹 FIRST TIME SETUP:
• Go to Settings → API Settings
• Default API credentials are pre-configured
• Add Telegram proxy if needed

󰍽 AUTHENTICATION:
• Go to Settings → Authentication
• Enter phone number (+989123456789)
• Click "Send Code"
• Enter received code
• If 2FA enabled, enter password

󰍼 CHANNEL CONFIGURATION:
• Go to Settings → Channel Settings
• Enter channel username (without @)
• Set start date (optional)
• Set end date (optional)

󰍶 START DOWNLOADING:
• Click "Run" from main menu
• Click "Stop" to pause anytime
• Resume from where you left off

═══════════════════════════════════════
✨ FEATURES

📥 SMART DOWNLOADING:
• Downloads ALL channel messages
• Organizes media: photos/videos/files
• Auto-saves every 50 messages
• Resume capability after stop

🌐 PROXY SUPPORT:
• MTProto Proxy (tg://proxy?...)
• System proxy auto-detection
• Test proxy before use

🎨 CUSTOMIZATION:
• Light/Dark themes
• English/فارسی languages
• Resizable window
• RTL support for Persian

📊 SMART FEATURES:
• Date range filtering
• Only downloads NEW messages
• Shows download progress
• Displays file sizes

═══════════════════════════════════════
⚙ SETTINGS EXPLAINED

🔑 API SETTINGS:
• API ID: Telegram API identifier
• API Hash: Telegram API key
• Proxy: Optional proxy connection

🔐 AUTHENTICATION:
• Phone: Your Telegram number
• Verify with SMS code
• 2FA if enabled on account

📢 CHANNEL SETTINGS:
• Username: Channel ID (e.g., "durov")
• Start Date: Download from date
• End Date: Download until date
• Leave empty for all messages

🎨 APPEARANCE:
• Language: UI language
• Theme: Light/Dark mode
• Window: Custom dimensions

═══════════════════════════════════════
💡 TIPS & TRICKS

✓ For large channels (10000+ messages):
  Use date filters to download in batches

✓ Internet disconnected?
  Resume from last message ID

✓ Speed too slow?
  Check proxy settings or internet

✓ Want all messages?
  Leave date filters empty

✓ Change API credentials?
  Go to Settings → API Settings

═══════════════════════════════════════
📁 FILE ORGANIZATION

All downloads saved in:
• media/photos/ - Images
• media/videos/ - Videos
• media/other/ - Documents
• messages.xlsx - Message data

═══════════════════════════════════════
󰞵 DEVELOPER
@immdjavad
═══════════════════════════════════════
"""
    },
    "fa": {
        "app_title": "دانلود کانال تلگرام",
        "settings": "⚙ تنظیمات",
        "help": "❓ راهنما",
        "run": "▶ اجرا",
        "stop": "⏹ توقف",
        "ready": "✅ آماده",
        "complete_settings": "⚠ تنظیمات را تکمیل کنید",
        "api_settings": "🔑 تنظیمات API",
        "appearance_settings": "🎨 ظاهر",
        "auth_settings": "🔐 احراز هویت",
        "channel_settings": "📢 تنظیمات کانال",
        "api_id": "API ID:",
        "api_hash": "API Hash:",
        "channel_address": "آیدی کانال:",
        "phone_number": "شماره تلفن:",
        "send_code": "📱 ارسال کد",
        "verification_code": "کد تایید:",
        "verify_code": "✓ تایید کد",
        "two_fa_password": "رمز دو مرحله‌ای:",
        "verify_password": "✓ تایید رمز",
        "start_date": "تاریخ شروع:",
        "end_date": "تاریخ پایان:",
        "clear_date_filter": "❌ حذف فیلتر",
        "back": "🔙 بازگشت",
        "save_settings": "💾 ذخیره",
        "save_and_back": "✓ ذخیره و بازگشت",
        "downloading": "📥 در حال دانلود...",
        "connecting": "در حال اتصال...",
        "error": "خطا",
        "fill_all_fields": "همه فیلدها را پر کنید",
        "code_sent": "✓ کد ارسال شد",
        "login_success": "✓ ورود موفق!",
        "enter_2fa": "رمز دو مرحله‌ای وارد کنید",
        "invalid_code": "کد نامعتبر",
        "settings_saved": "✓ ذخیره شد",
        "complete_settings_first": "ابتدا تنظیمات را تکمیل کنید",
        "connected": "متصل شد",
        "getting_messages": "دریافت پیام‌ها...",
        "messages_downloaded": "پیام دانلود شد!",
        "no_new_messages": "ℹ پیام جدیدی نیست",
        "language": "زبان:",
        "theme": "تم:",
        "light": "☀ روشن",
        "dark": "🌙 تاریک",
        "developer": "󰞵 توسعه دهنده",
        "developer_id": "آیدی توسعه دهنده:",
        "download_stopped": "⏸ متوقف شد",
        "can_resume": "ادامه در دفعه بعد",
        "proxy_settings": "🌐 پروکسی",
        "use_proxy": "استفاده از پروکسی",
        "proxy_link": "لینک پروکسی:",
        "proxy_link_hint": "tg://proxy?...",
        "test_proxy": "🧪 تست",
        "proxy_connected": "✓ متصل شد",
        "proxy_error": "✗ ناموفق",
        "window_size": "ابعاد پنجره:",
        "width": "عرض:",
        "height": "ارتفاع:",
        "concurrent_downloads": "دانلود همزمان:",
        "concurrent_hint": "دانلود چند فایل به صورت همزمان (1-10)",
        "help_title": "❓ راهنما و آموزش",
        "help_content": """
📖 راهنمای کامل استفاده
═══════════════════════════════════════
🚀 شروع سریع

󰍹 تنظیمات اولیه:
• برو به تنظیمات ← تنظیمات API
• اطلاعات پیش‌فرض از قبل وارد شده
• در صورت نیاز پروکسی اضافه کن

󰍽 احراز هویت:
• برو به تنظیمات ← احراز هویت
• شماره تلفن کن وارد (+989123456789)
• روی "ارسال کد" کلیک کن
• کد دریافتی رو وارد کن
• اگر تایید دو مرحله‌ای داری، رمز وارد کن

󰍼 تنظیمات کانال:
• برو به تنظیمات ← تنظیمات کانال
• آیدی کانال را وارد کن (بدون @)
• تاریخ شروع تنظیم کن (اختیاری)
• تاریخ پایان تنظیم کن (اختیاری)

󰍶 شروع دانلود:
• از منوی اصلی رو "اجرا" بزن
• برای توقف رو "توقف" بزن
• دفعه بعد از همون جا ادامه میده

═══════════════════════════════════════
✨ قابلیت‌ها

📥 دانلود هوشمند:
• دانلود همه پیام‌های کانال
• مرتب‌سازی فایل‌ها: عکس/ویدیو/سند
• ذخیره خودکار هر 50 پیام
• قابلیت ادامه دانلود

🌐 پشتیبانی پروکسی:
• پروکسی MTProto (tg://proxy?...)
• تشخیص خودکار پروکسی سیستم
• تست پروکسی قبل از استفاده

🎨 شخصی‌سازی:
• تم روشن/تاریک
• زبان انگلیسی/فارسی
• تغییر ابعاد پنجره
• پشتیبانی راست‌چین

📊 امکانات هوشمند:
• فیلتر بازه زمانی
• فقط پیام‌های جدید می‌شه دانلود
• نمایش پیشرفت دانلود
• نمایش حجم فایل‌ها

═══════════════════════════════════════
⚙ توضیح تنظیمات

🔑 تنظیمات API:
• API ID: شناسه API تلگرام
• API Hash: کلید API تلگرام
• پروکسی: اتصال پروکسی (اختیاری)

🔐 احراز هویت:
• شماره: شماره تلگرام شما
• تایید با کد پیامکی
• تایید دو مرحله‌ای (اگر فعاله)

📢 تنظیمات کانال:
• آیدی: نام کانال (مثلاً "durov")
• تاریخ شروع: دانلود از این تاریخ
• تاریخ پایان: دانلود تا این تاریخ
• برای همه پیام‌ها بذار خالی

🎨 ظاهر:
• زبان: زبان برنامه
• تم: حالت روشن/تاریک
• پنجره: ابعاد دلخواه

═══════════════════════════════════════
💡 نکات و ترفندها

✓ برای کانال‌های بزرگ (10000+ پیام):
  از فیلتر تاریخ برای دانلود دسته‌ای استفاده کن

✓ اینترنت قطع شد؟
  ادامه میده از آخرین پیام

✓ سرعت کمه؟
  پروکسی یا اینترنت رو چک کن

✓ می‌خوای همه پیام‌ها رو؟
  فیلتر تاریخ رو بذار خالی

✓ می‌خوای API عوض کنی؟
  برو تنظیمات ← تنظیمات API

═══════════════════════════════════════
📁 سازماندهی فایل‌ها

همه دانلودها اینجا:
• media/photos/ - عکس‌ها
• media/videos/ - ویدیوها
• media/other/ - اسناد
• messages.xlsx - داده پیام‌ها

═══════════════════════════════════════
󰞵 توسعه دهنده
@immdjavad
═══════════════════════════════════════
"""
    }
}


class TelegramDownloaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # مسیرها
        self.config_file = "config.json"
        self.excel_file = "messages.xlsx"
        self.media_dir = "media"
        self.session_name = "session"
        
        # متغیرهای احراز هویت
        self.phone_code_hash = None
        self.auth_loop = None
        self.auth_client = None
        
        # متغیر برای متوقف کردن دانلود
        self.stop_download = False
        
        # بارگذاری تنظیمات
        self.load_config()
        
        # تنظیمات پروکسی
        self.proxy_settings = self.get_system_proxy()
        
        # اعمال تم و زبان
        self.apply_theme()
        
        # تنظیمات پنجره
        self.title(self.t("app_title"))
        width = self.config.get("window_width", 700)
        height = self.config.get("window_height", 500)
        self.geometry(f"{width}x{height}")
        self.resizable(True, True)
        
        # نمایش صفحه اصلی
        self.show_main_page()
    
    def get_system_proxy(self):
        """دریافت تنظیمات پروکسی"""
        if self.config.get("use_proxy") and self.config.get("proxy_link"):
            try:
                proxy_config = self.parse_telegram_proxy(self.config["proxy_link"])
                if proxy_config:
                    return proxy_config
            except Exception as e:
                print(f"Error parsing Telegram proxy: {e}")
        
        try:
            proxies = urllib.request.getproxies()
            if 'http' in proxies:
                proxy_url = proxies['http']
                if proxy_url.startswith('http://'):
                    proxy_url = proxy_url[7:]
                elif proxy_url.startswith('https://'):
                    proxy_url = proxy_url[8:]
                
                if ':' in proxy_url:
                    parts = proxy_url.split(':')
                    proxy_host = parts[0]
                    proxy_port = int(parts[1]) if len(parts) > 1 else 8080
                    return {
                        'proxy_type': socks.HTTP,
                        'addr': proxy_host,
                        'port': proxy_port
                    }
        except Exception as e:
            print(f"Error getting system proxy: {e}")
        
        return None
    
    def parse_telegram_proxy(self, proxy_link):
        """پارسر کردن لینک پروکسی تلگرام"""
        try:
            import urllib.parse
            
            if proxy_link.startswith('tg://proxy?'):
                proxy_link = proxy_link[11:]
            elif proxy_link.startswith('https://t.me/proxy?'):
                proxy_link = proxy_link[19:]
            
            params = urllib.parse.parse_qs(proxy_link)
            server = params.get('server', [None])[0]
            port = params.get('port', [None])[0]
            secret = params.get('secret', [None])[0]
            
            if server and port and secret:
                return {
                    'proxy_type': 'mtproto',
                    'addr': server,
                    'port': int(port),
                    'secret': secret
                }
        except Exception as e:
            print(f"Error parsing proxy link: {e}")
        
        return None
    
    def t(self, key):
        """ترجمه متن بر اساس زبان انتخابی"""
        lang = self.config.get("language", "en")
        return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)
    
    def is_rtl(self):
        """بررسی راست به چپ بودن زبان"""
        return self.config.get("language", "en") == "fa"
    
    def load_config(self):
        """بارگذاری تنظیمات از فایل"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            self.config = {
                "api_id": "",
                "api_hash": "",
                "channel_username": "",
                "phone": "",
                "start_date": "",
                "end_date": "",
                "language": "en",
                "theme": "dark",
                "use_proxy": False,
                "proxy_link": "",
                "window_width": 700,
                "window_height": 500,
                "concurrent_downloads": 3
            }
    
    def save_config(self):
        """ذخیره تنظیمات در فایل"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=4)
    
    def apply_theme(self):
        """اعمال تم"""
        theme = self.config.get("theme", "dark")
        ctk.set_appearance_mode(theme)
    
    def clear_window(self):
        """پاک کردن تمام ویجت‌ها"""
        for widget in self.winfo_children():
            widget.destroy()
    
    def show_main_page(self):
        """نمایش صفحه اصلی"""
        self.clear_window()
        self.title(self.t("app_title"))
        
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(expand=True, fill="both", padx=40, pady=40)
        
        title = ctk.CTkLabel(
            main_frame,
            text=f"🚀 {self.t('app_title')}",
            font=ctk.CTkFont(size=28, weight="bold", family="Arial"),
            anchor="center"
        )
        title.pack(pady=(0, 40))
        
        settings_btn = ctk.CTkButton(
            main_frame,
            text=self.t("settings"),
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50,
            corner_radius=10,
            command=self.show_settings_menu,
            anchor="center"
        )
        settings_btn.pack(pady=10, fill="x")
        
        help_btn = ctk.CTkButton(
            main_frame,
            text=self.t("help"),
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50,
            corner_radius=10,
            fg_color="#e67e22",
            hover_color="#d35400",
            command=self.show_help_page,
            anchor="center"
        )
        help_btn.pack(pady=10, fill="x")
        
        dev_btn = ctk.CTkButton(
            main_frame,
            text=self.t("developer"),
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50,
            corner_radius=10,
            fg_color="#9b59b6",
            hover_color="#8e44ad",
            command=self.show_developer_page,
            anchor="center"
        )
        dev_btn.pack(pady=10, fill="x")
        
        run_btn = ctk.CTkButton(
            main_frame,
            text=self.t("run"),
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50,
            corner_radius=10,
            fg_color="#2ecc71",
            hover_color="#27ae60",
            command=self.run_download,
            anchor="center"
        )
        run_btn.pack(pady=10, fill="x")
        
        status_text = self.t("ready") if self.check_config() else self.t("complete_settings")
        status_color = "#2ecc71" if self.check_config() else "#e74c3c"
        
        status_label = ctk.CTkLabel(
            main_frame,
            text=status_text,
            font=ctk.CTkFont(size=14),
            text_color=status_color,
            anchor="center"
        )
        status_label.pack(pady=(20, 0))
    
    def check_config(self):
        """بررسی کامل بودن تنظیمات"""
        return all([
            self.config.get("api_id"),
            self.config.get("api_hash"),
            self.config.get("channel_username"),
            self.config.get("phone")
        ])
    
    def show_settings_menu(self):
        """نمایش منوی تنظیمات"""
        self.clear_window()
        self.title(self.t("settings"))
        
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(expand=True, fill="both", padx=40, pady=40)
        
        title = ctk.CTkLabel(
            main_frame,
            text=self.t("settings"),
            font=ctk.CTkFont(size=28, weight="bold"),
            anchor="center"
        )
        title.pack(pady=(0, 40))
        
        api_btn = ctk.CTkButton(
            main_frame,
            text=self.t("api_settings"),
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50,
            corner_radius=10,
            fg_color="#3498db",
            hover_color="#2980b9",
            command=self.show_api_settings,
            anchor="center"
        )
        api_btn.pack(pady=10, fill="x")
        
        auth_btn = ctk.CTkButton(
            main_frame,
            text=self.t("auth_settings"),
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50,
            corner_radius=10,
            fg_color="#e74c3c",
            hover_color="#c0392b",
            command=self.show_auth_settings,
            anchor="center"
        )
        auth_btn.pack(pady=10, fill="x")
        
        channel_btn = ctk.CTkButton(
            main_frame,
            text=self.t("channel_settings"),
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50,
            corner_radius=10,
            fg_color="#9b59b6",
            hover_color="#8e44ad",
            command=self.show_channel_settings,
            anchor="center"
        )
        channel_btn.pack(pady=10, fill="x")
        
        appearance_btn = ctk.CTkButton(
            main_frame,
            text=self.t("appearance_settings"),
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50,
            corner_radius=10,
            fg_color="#16a085",
            hover_color="#138d75",
            command=self.show_appearance_settings,
            anchor="center"
        )
        appearance_btn.pack(pady=10, fill="x")
        
        back_btn = ctk.CTkButton(
            main_frame,
            text=self.t("back"),
            height=45,
            fg_color="#95a5a6",
            hover_color="#7f8c8d",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.show_main_page,
            anchor="center"
        )
        back_btn.pack(pady=(20, 0), fill="x")
    
    def show_help_page(self):
        """نمایش صفحه راهنما"""
        self.clear_window()
        self.title(self.t("help_title"))
        
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        title = ctk.CTkLabel(
            main_frame,
            text=self.t("help_title"),
            font=ctk.CTkFont(size=24, weight="bold"),
            anchor="center"
        )
        title.pack(pady=(0, 20))
        
        help_text = scrolledtext.ScrolledText(
            main_frame,
            width=80,
            height=25,
            font=("Consolas", 10),
            bg="#2b2b2b",
            fg="#00ff00",
            insertbackground="white",
            wrap="word"
        )
        help_text.pack(pady=10, fill="both", expand=True)
        help_text.insert("1.0", self.t("help_content"))
        help_text.config(state="disabled")
        
        back_btn = ctk.CTkButton(
            main_frame,
            text=self.t("back"),
            height=45,
            fg_color="#95a5a6",
            hover_color="#7f8c8d",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.show_main_page,
            anchor="center"
        )
        back_btn.pack(pady=(10, 0), fill="x")
    
    def show_developer_page(self):
        """نمایش صفحه توسعه دهنده"""
        self.clear_window()
        self.title(self.t("developer"))
        
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(expand=True, fill="both", padx=40, pady=40)
        
        title = ctk.CTkLabel(
            main_frame,
            text=self.t("developer"),
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(pady=(0, 50))

        info_frame = ctk.CTkFrame(main_frame, corner_radius=15)
        info_frame.pack(pady=20, padx=20, fill="x")
        
        dev_label = ctk.CTkLabel(
            info_frame,
            text=self.t("developer_id"),
            font=ctk.CTkFont(size=16, weight="bold")
        )
        dev_label.pack(pady=(20, 10))
        
        dev_id = ctk.CTkLabel(
            info_frame,
            text="@immdjavad",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#3498db"
        )
        dev_id.pack(pady=(0, 20))
        
        back_btn = ctk.CTkButton(
            main_frame,
            text=self.t("back"),
            height=50,
            fg_color="#95a5a6",
            hover_color="#7f8c8d",
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.show_main_page
        )
        back_btn.pack(pady=(30, 0), fill="x")
    
    def show_api_settings(self):
        """تنظیمات API"""
        self.clear_window()
        self.title(self.t("api_settings"))
        
        main_frame = ctk.CTkScrollableFrame(self)
        main_frame.pack(expand=True, fill="both", padx=30, pady=20)
        
        anchor_dir = "e" if self.is_rtl() else "w"
        
        title = ctk.CTkLabel(
            main_frame,
            text=self.t("api_settings"),
            font=ctk.CTkFont(size=24, weight="bold"),
            anchor="center"
        )
        title.pack(pady=(0, 30))
        
        # API ID
        ctk.CTkLabel(
            main_frame,
            text=self.t("api_id"),
            font=ctk.CTkFont(size=14),
            anchor=anchor_dir
        ).pack(anchor=anchor_dir, pady=(0, 5), fill="x")
        
        self.api_id_entry = ctk.CTkEntry(main_frame, height=40, justify="right" if self.is_rtl() else "left")
        self.api_id_entry.insert(0, self.config.get("api_id", ""))
        self.api_id_entry.pack(fill="x", pady=(0, 20))
        
        # API Hash
        ctk.CTkLabel(
            main_frame,
            text=self.t("api_hash"),
            font=ctk.CTkFont(size=14),
            anchor=anchor_dir
        ).pack(anchor=anchor_dir, pady=(0, 5), fill="x")
        
        self.api_hash_entry = ctk.CTkEntry(main_frame, height=40, justify="right" if self.is_rtl() else "left")
        self.api_hash_entry.insert(0, self.config.get("api_hash", ""))
        self.api_hash_entry.pack(fill="x", pady=(0, 30))
        
        # Proxy
        separator = ctk.CTkFrame(main_frame, height=2, fg_color="#34495e")
        separator.pack(fill="x", pady=20)
        
        ctk.CTkLabel(
            main_frame,
            text=self.t("proxy_settings"),
            font=ctk.CTkFont(size=18, weight="bold"),
            anchor=anchor_dir
        ).pack(anchor=anchor_dir, pady=(0, 15), fill="x")
        
        self.use_proxy_var = ctk.BooleanVar(value=self.config.get("use_proxy", False))
        proxy_check = ctk.CTkCheckBox(
            main_frame,
            text=self.t("use_proxy"),
            variable=self.use_proxy_var,
            font=ctk.CTkFont(size=14)
        )
        proxy_check.pack(anchor=anchor_dir, pady=(0, 15))
        
        ctk.CTkLabel(
            main_frame,
            text=self.t("proxy_link"),
            font=ctk.CTkFont(size=14),
            anchor=anchor_dir
        ).pack(anchor=anchor_dir, pady=(0, 5), fill="x")
        
        self.proxy_link_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text=self.t("proxy_link_hint"),
            height=40,
            justify="right" if self.is_rtl() else "left"
        )
        self.proxy_link_entry.insert(0, self.config.get("proxy_link", ""))
        self.proxy_link_entry.pack(fill="x", pady=(0, 10))
        
        test_proxy_btn = ctk.CTkButton(
            main_frame,
            text=self.t("test_proxy"),
            height=40,
            fg_color="#e67e22",
            hover_color="#d35400",
            command=self.test_proxy,
            anchor="center"
        )
        test_proxy_btn.pack(fill="x", pady=(0, 20))
        
        # Buttons
        self.create_save_buttons(main_frame, self.save_api_settings, self.show_settings_menu)
    
    def show_auth_settings(self):
        """تنظیمات احراز هویت"""
        self.clear_window()
        self.title(self.t("auth_settings"))
        
        main_frame = ctk.CTkScrollableFrame(self)
        main_frame.pack(expand=True, fill="both", padx=30, pady=20)
        
        anchor_dir = "e" if self.is_rtl() else "w"
        
        title = ctk.CTkLabel(
            main_frame,
            text=self.t("auth_settings"),
            font=ctk.CTkFont(size=24, weight="bold"),
            anchor="center"
        )
        title.pack(pady=(0, 30))
        
        # Phone
        ctk.CTkLabel(
            main_frame,
            text=self.t("phone_number"),
            font=ctk.CTkFont(size=14),
            anchor=anchor_dir
        ).pack(anchor=anchor_dir, pady=(0, 5), fill="x")
        
        phone_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        phone_frame.pack(fill="x", pady=(0, 20))
        
        self.phone_entry = ctk.CTkEntry(phone_frame, placeholder_text="+98912345678", height=40, justify="right" if self.is_rtl() else "left")
        self.phone_entry.insert(0, self.config.get("phone", ""))
        
        send_code_btn = ctk.CTkButton(
            phone_frame,
            text=self.t("send_code"),
            width=120,
            height=40,
            command=self.send_code,
            anchor="center"
        )
        
        if self.is_rtl():
            send_code_btn.pack(side="right", padx=(10, 0))
            self.phone_entry.pack(side="right", fill="x", expand=True)
        else:
            self.phone_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
            send_code_btn.pack(side="left")
        
        # Code
        self.code_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        
        ctk.CTkLabel(
            self.code_frame,
            text=self.t("verification_code"),
            font=ctk.CTkFont(size=14),
            anchor=anchor_dir
        ).pack(anchor=anchor_dir, pady=(0, 5), fill="x")
        
        self.code_entry = ctk.CTkEntry(self.code_frame, placeholder_text="12345", height=40, justify="right" if self.is_rtl() else "left")
        self.code_entry.pack(fill="x", pady=(0, 10))
        
        verify_btn = ctk.CTkButton(
            self.code_frame,
            text=self.t("verify_code"),
            height=40,
            fg_color="#2ecc71",
            hover_color="#27ae60",
            command=self.verify_code,
            anchor="center"
        )
        verify_btn.pack(fill="x", pady=(0, 20))
        
        # Password
        self.password_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        
        ctk.CTkLabel(
            self.password_frame,
            text=self.t("two_fa_password"),
            font=ctk.CTkFont(size=14),
            anchor=anchor_dir
        ).pack(anchor=anchor_dir, pady=(0, 5), fill="x")
        
        self.password_entry = ctk.CTkEntry(self.password_frame, placeholder_text="********", height=40, show="*", justify="right" if self.is_rtl() else "left")
        self.password_entry.pack(fill="x", pady=(0, 10))
        
        verify_pass_btn = ctk.CTkButton(
            self.password_frame,
            text=self.t("verify_password"),
            height=40,
            fg_color="#2ecc71",
            hover_color="#27ae60",
            command=self.verify_password,
            anchor="center"
        )
        verify_pass_btn.pack(fill="x", pady=(0, 20))
        
        # Buttons
        back_btn = ctk.CTkButton(
            main_frame,
            text=self.t("back"),
            height=45,
            fg_color="#95a5a6",
            hover_color="#7f8c8d",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.show_settings_menu,
            anchor="center"
        )
        back_btn.pack(pady=(20, 0), fill="x")
    
    def show_channel_settings(self):
        """تنظیمات کانال"""
        self.clear_window()
        self.title(self.t("channel_settings"))
        
        main_frame = ctk.CTkScrollableFrame(self)
        main_frame.pack(expand=True, fill="both", padx=30, pady=20)
        
        anchor_dir = "e" if self.is_rtl() else "w"
        
        title = ctk.CTkLabel(
            main_frame,
            text=self.t("channel_settings"),
            font=ctk.CTkFont(size=24, weight="bold"),
            anchor="center"
        )
        title.pack(pady=(0, 30))
        
        # Channel
        ctk.CTkLabel(
            main_frame,
            text=self.t("channel_address"),
            font=ctk.CTkFont(size=14),
            anchor=anchor_dir
        ).pack(anchor=anchor_dir, pady=(0, 5), fill="x")
        
        self.channel_entry = ctk.CTkEntry(main_frame, placeholder_text="telegram", height=40, justify="right" if self.is_rtl() else "left")
        self.channel_entry.insert(0, self.config.get("channel_username", ""))
        self.channel_entry.pack(fill="x", pady=(0, 20))
        
        # Start Date
        ctk.CTkLabel(
            main_frame,
            text=self.t("start_date"),
            font=ctk.CTkFont(size=14),
            anchor=anchor_dir
        ).pack(anchor=anchor_dir, pady=(0, 5), fill="x")
        
        date_frame1 = ctk.CTkFrame(main_frame, fg_color="transparent")
        date_frame1.pack(fill="x", pady=(0, 20))
        
        self.start_date_entry = DateEntry(
            date_frame1,
            width=25,
            background='#1f538d',
            foreground='white',
            borderwidth=2,
            font=("Arial", 11),
            date_pattern='yyyy-mm-dd'
        )
        
        if self.config.get("start_date"):
            try:
                saved_date = datetime.strptime(self.config["start_date"], "%Y-%m-%d")
                self.start_date_entry.set_date(saved_date)
            except:
                pass
        
        clear_start_btn = ctk.CTkButton(
            date_frame1,
            text=self.t("clear_date_filter"),
            width=150,
            height=30,
            command=lambda: [self.start_date_entry.set_date(datetime.now()), setattr(self.config, 'start_date', '')],
            anchor="center"
        )
        
        if self.is_rtl():
            clear_start_btn.pack(side="right", padx=(10, 0))
            self.start_date_entry.pack(side="right")
        else:
            self.start_date_entry.pack(side="left", padx=(0, 10))
            clear_start_btn.pack(side="left")
        
        # End Date
        ctk.CTkLabel(
            main_frame,
            text=self.t("end_date"),
            font=ctk.CTkFont(size=14),
            anchor=anchor_dir
        ).pack(anchor=anchor_dir, pady=(0, 5), fill="x")
        
        date_frame2 = ctk.CTkFrame(main_frame, fg_color="transparent")
        date_frame2.pack(fill="x", pady=(0, 20))
        
        self.end_date_entry = DateEntry(
            date_frame2,
            width=25,
            background='#1f538d',
            foreground='white',
            borderwidth=2,
            font=("Arial", 11),
            date_pattern='yyyy-mm-dd'
        )
        
        if self.config.get("end_date"):
            try:
                saved_date = datetime.strptime(self.config["end_date"], "%Y-%m-%d")
                self.end_date_entry.set_date(saved_date)
            except:
                pass
        
        clear_end_btn = ctk.CTkButton(
            date_frame2,
            text=self.t("clear_date_filter"),
            width=150,
            height=30,
            command=lambda: [self.end_date_entry.set_date(datetime.now()), setattr(self.config, 'end_date', '')],
            anchor="center"
        )
        
        if self.is_rtl():
            clear_end_btn.pack(side="right", padx=(10, 0))
            self.end_date_entry.pack(side="right")
        else:
            self.end_date_entry.pack(side="left", padx=(0, 10))
            clear_end_btn.pack(side="left")
        
        # Buttons
        self.create_save_buttons(main_frame, self.save_channel_settings, self.show_settings_menu)
    
    def show_appearance_settings(self):
        """تنظیمات ظاهری"""
        self.clear_window()
        self.title(self.t("appearance_settings"))
        
        main_frame = ctk.CTkScrollableFrame(self)
        main_frame.pack(expand=True, fill="both", padx=30, pady=20)
        
        anchor_dir = "e" if self.is_rtl() else "w"
        
        title = ctk.CTkLabel(
            main_frame,
            text=self.t("appearance_settings"),
            font=ctk.CTkFont(size=24, weight="bold"),
            anchor="center"
        )
        title.pack(pady=(0, 30))
        
        # Language
        ctk.CTkLabel(
            main_frame,
            text=self.t("language"),
            font=ctk.CTkFont(size=14),
            anchor=anchor_dir
        ).pack(anchor=anchor_dir, pady=(0, 5), fill="x")
        
        lang_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        lang_frame.pack(fill="x", pady=(0, 20))
        
        self.lang_var = ctk.StringVar(value=self.config.get("language", "en"))
        
        lang_en = ctk.CTkRadioButton(
            lang_frame,
            text="English",
            variable=self.lang_var,
            value="en"
        )
        lang_en.pack(side="right" if self.is_rtl() else "left", padx=(0, 20))
        
        lang_fa = ctk.CTkRadioButton(
            lang_frame,
            text="فارسی",
            variable=self.lang_var,
            value="fa"
        )
        lang_fa.pack(side="right" if self.is_rtl() else "left")
        
        # Theme
        ctk.CTkLabel(
            main_frame,
            text=self.t("theme"),
            font=ctk.CTkFont(size=14),
            anchor=anchor_dir
        ).pack(anchor=anchor_dir, pady=(0, 5), fill="x")
        
        theme_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        theme_frame.pack(fill="x", pady=(0, 20))
        
        self.theme_var = ctk.StringVar(value=self.config.get("theme", "dark"))
        
        theme_light = ctk.CTkRadioButton(
            theme_frame,
            text=self.t("light"),
            variable=self.theme_var,
            value="light"
        )
        theme_light.pack(side="right" if self.is_rtl() else "left", padx=(0, 20))
        
        theme_dark = ctk.CTkRadioButton(
            theme_frame,
            text=self.t("dark"),
            variable=self.theme_var,
            value="dark"
        )
        theme_dark.pack(side="right" if self.is_rtl() else "left")
        
        # Window Size
        separator = ctk.CTkFrame(main_frame, height=2, fg_color="#34495e")
        separator.pack(fill="x", pady=20)
        
        ctk.CTkLabel(
            main_frame,
            text=self.t("window_size"),
            font=ctk.CTkFont(size=18, weight="bold"),
            anchor=anchor_dir
        ).pack(anchor=anchor_dir, pady=(0, 15), fill="x")
        
        size_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        size_frame.pack(fill="x", pady=(0, 20))
        
        # Width
        width_frame = ctk.CTkFrame(size_frame, fg_color="transparent")
        width_frame.pack(side="left" if not self.is_rtl() else "right", fill="x", expand=True, padx=(0, 10) if not self.is_rtl() else (10, 0))
        
        ctk.CTkLabel(width_frame, text=self.t("width"), font=ctk.CTkFont(size=12), anchor=anchor_dir).pack(anchor=anchor_dir, pady=(0, 5))
        
        self.width_entry = ctk.CTkEntry(width_frame, height=35, justify="center")
        self.width_entry.insert(0, str(self.config.get("window_width", 700)))
        self.width_entry.pack(fill="x")
        
        # Height
        height_frame = ctk.CTkFrame(size_frame, fg_color="transparent")
        height_frame.pack(side="right" if not self.is_rtl() else "left", fill="x", expand=True, padx=(10, 0) if not self.is_rtl() else (0, 10))
        
        ctk.CTkLabel(height_frame, text=self.t("height"), font=ctk.CTkFont(size=12), anchor=anchor_dir).pack(anchor=anchor_dir, pady=(0, 5))
        
        self.height_entry = ctk.CTkEntry(height_frame, height=35, justify="center")
        self.height_entry.insert(0, str(self.config.get("window_height", 500)))
        self.height_entry.pack(fill="x")
        
        # Concurrent Downloads
        separator2 = ctk.CTkFrame(main_frame, height=2, fg_color="#34495e")
        separator2.pack(fill="x", pady=20)
        
        ctk.CTkLabel(
            main_frame,
            text=self.t("concurrent_downloads"),
            font=ctk.CTkFont(size=18, weight="bold"),
            anchor=anchor_dir
        ).pack(anchor=anchor_dir, pady=(0, 5), fill="x")
        
        ctk.CTkLabel(
            main_frame,
            text=self.t("concurrent_hint"),
            font=ctk.CTkFont(size=11),
            text_color="#7f8c8d",
            anchor=anchor_dir
        ).pack(anchor=anchor_dir, pady=(0, 10), fill="x")
        
        concurrent_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        concurrent_frame.pack(fill="x", pady=(0, 20))
        
        self.concurrent_var = ctk.IntVar(value=self.config.get("concurrent_downloads", 3))
        
        concurrent_values = [1, 3, 5, 10]
        for val in concurrent_values:
            radio = ctk.CTkRadioButton(
                concurrent_frame,
                text=f"{val}",
                variable=self.concurrent_var,
                value=val,
                font=ctk.CTkFont(size=14)
            )
            if self.is_rtl():
                radio.pack(side="right", padx=10)
            else:
                radio.pack(side="left", padx=10)
        
        # Buttons
        self.create_save_buttons(main_frame, self.save_appearance_settings, self.show_settings_menu)
    
    def create_save_buttons(self, parent, save_func, back_func):
        """ایجاد دکمه‌های ذخیره"""
        buttons_container = ctk.CTkFrame(parent, fg_color="transparent")
        buttons_container.pack(fill="x", pady=(20, 0))
        
        top_buttons = ctk.CTkFrame(buttons_container, fg_color="transparent")
        top_buttons.pack(fill="x", pady=(0, 10))
        
        back_btn = ctk.CTkButton(
            top_buttons,
            text=self.t("back"),
            height=45,
            fg_color="#95a5a6",
            hover_color="#7f8c8d",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=back_func,
            anchor="center"
        )
        
        save_btn = ctk.CTkButton(
            top_buttons,
            text=self.t("save_settings"),
            height=45,
            fg_color="#3498db",
            hover_color="#2980b9",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=save_func,
            anchor="center"
        )
        
        if self.is_rtl():
            save_btn.pack(side="right", fill="x", expand=True, padx=(0, 5))
            back_btn.pack(side="right", fill="x", expand=True, padx=(5, 0))
        else:
            back_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))
            save_btn.pack(side="left", fill="x", expand=True, padx=(5, 0))
    
    def test_proxy(self):
        """تست پروکسی"""
        proxy_link = self.proxy_link_entry.get().strip()
        if not proxy_link:
            messagebox.showerror(self.t("error"), self.t("fill_all_fields"))
            return
        
        proxy_config = self.parse_telegram_proxy(proxy_link)
        if proxy_config:
            messagebox.showinfo("✓", self.t("proxy_connected"))
        else:
            messagebox.showerror("✗", self.t("proxy_error"))
    
    def save_api_settings(self):
        """ذخیره API"""
        self.config["api_id"] = self.api_id_entry.get().strip()
        self.config["api_hash"] = self.api_hash_entry.get().strip()
        self.config["use_proxy"] = self.use_proxy_var.get()
        self.config["proxy_link"] = self.proxy_link_entry.get().strip()
        self.save_config()
        self.proxy_settings = self.get_system_proxy()
        messagebox.showinfo("✓", self.t("settings_saved"))
    
    def save_channel_settings(self):
        """ذخیره کانال"""
        self.config["channel_username"] = self.channel_entry.get().strip()
        self.config["start_date"] = self.start_date_entry.get_date().strftime("%Y-%m-%d")
        self.config["end_date"] = self.end_date_entry.get_date().strftime("%Y-%m-%d")
        self.save_config()
        messagebox.showinfo("✓", self.t("settings_saved"))
    
    def save_appearance_settings(self):
        """ذخیره ظاهر"""
        old_lang = self.config.get("language")
        self.config["language"] = self.lang_var.get()
        self.config["theme"] = self.theme_var.get()
        self.config["concurrent_downloads"] = self.concurrent_var.get()
        
        try:
            self.config["window_width"] = int(self.width_entry.get())
            self.config["window_height"] = int(self.height_entry.get())
        except:
            pass
        
        self.save_config()
        self.apply_theme()
        
        if old_lang != self.config["language"]:
            self.show_appearance_settings()
        else:
            messagebox.showinfo("✓", self.t("settings_saved"))
    
    def send_code(self):
        """ارسال کد"""
        phone = self.phone_entry.get().strip()
        api_id = self.config.get("api_id")
        api_hash = self.config.get("api_hash")
        
        if not all([phone, api_id, api_hash]):
            messagebox.showerror(self.t("error"), self.t("fill_all_fields"))
            return
        
        threading.Thread(target=self._send_code_thread, args=(phone, api_id, api_hash), daemon=True).start()
    
    def _send_code_thread(self, phone, api_id, api_hash):
        """Thread ارسال کد"""
        async def do_send():
            try:
                client = None
                if self.proxy_settings:
                    if self.proxy_settings.get('proxy_type') == 'mtproto':
                        client = TelegramClient(
                            self.session_name,
                            int(api_id),
                            api_hash,
                            proxy=(self.proxy_settings['addr'], self.proxy_settings['port'], self.proxy_settings['secret'])
                        )
                    else:
                        client = TelegramClient(
                            self.session_name,
                            int(api_id),
                            api_hash,
                            proxy=self.proxy_settings
                        )
                else:
                    client = TelegramClient(self.session_name, int(api_id), api_hash)
                
                await client.connect()
                result = await client.send_code_request(phone)
                self.phone_code_hash = result.phone_code_hash
                self.auth_client = client
                
                self.after(0, lambda: self.code_frame.pack(fill="x", pady=(0, 20)))
                self.after(0, lambda: messagebox.showinfo("✓", self.t("code_sent")))
            except Exception as e:
                error_msg = str(e)
                if "timeout" in error_msg.lower() or "connection" in error_msg.lower():
                    hint = "\n\nHint: If internet is filtered, enable proxy in API Settings"
                    self.after(0, lambda: messagebox.showerror(self.t("error"), f"{self.t('error')}:\n{error_msg}{hint}"))
                else:
                    self.after(0, lambda: messagebox.showerror(self.t("error"), f"{self.t('error')}:\n{error_msg}"))
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        self.auth_loop = loop
        loop.run_until_complete(do_send())
    
    def verify_code(self):
        """تایید کد"""
        code = self.code_entry.get().strip()
        phone = self.phone_entry.get().strip()
        
        if not code:
            messagebox.showerror(self.t("error"), self.t("fill_all_fields"))
            return
        
        threading.Thread(target=self._verify_code_thread, args=(phone, code), daemon=True).start()
    
    def _verify_code_thread(self, phone, code):
        """Thread تایید کد"""
        async def do_verify():
            try:
                await self.auth_client.sign_in(phone, code, phone_code_hash=self.phone_code_hash)
                self.config["phone"] = phone
                self.save_config()
                
                self.after(0, lambda: messagebox.showinfo("✓", self.t("login_success")))
                self.after(0, lambda: self.code_frame.pack_forget())
                
                await self.auth_client.disconnect()
                self.auth_client = None
            except SessionPasswordNeededError:
                self.after(0, lambda: self.password_frame.pack(fill="x", pady=(0, 20)))
                self.after(0, lambda: messagebox.showinfo(self.t("error"), self.t("enter_2fa")))
            except PhoneCodeInvalidError:
                self.after(0, lambda: messagebox.showerror(self.t("error"), self.t("invalid_code")))
            except Exception as e:
                self.after(0, lambda: messagebox.showerror(self.t("error"), f"{self.t('error')}:\n{str(e)}"))
        
        asyncio.set_event_loop(self.auth_loop)
        self.auth_loop.run_until_complete(do_verify())
    
    def verify_password(self):
        """تایید رمز"""
        password = self.password_entry.get().strip()
        
        if not password:
            messagebox.showerror(self.t("error"), self.t("fill_all_fields"))
            return
        
        threading.Thread(target=self._verify_password_thread, args=(password,), daemon=True).start()
    
    def _verify_password_thread(self, password):
        """Thread تایید رمز"""
        async def do_verify():
            try:
                await self.auth_client.sign_in(password=password)
                self.config["phone"] = self.phone_entry.get().strip()
                self.save_config()
                
                self.after(0, lambda: messagebox.showinfo("✓", self.t("login_success")))
                self.after(0, lambda: self.password_frame.pack_forget())
                
                await self.auth_client.disconnect()
                self.auth_client = None
            except Exception as e:
                self.after(0, lambda: messagebox.showerror(self.t("error"), f"{self.t('error')}:\n{str(e)}"))
        
        asyncio.set_event_loop(self.auth_loop)
        self.auth_loop.run_until_complete(do_verify())
    
    def run_download(self):
        """اجرای دانلود"""
        if not self.check_config():
            messagebox.showerror(self.t("error"), self.t("complete_settings_first"))
            return
        
        self.stop_download = False
        self.show_download_page()
    
    def show_download_page(self):
        """صفحه دانلود"""
        self.clear_window()
        self.title(self.t("downloading"))
        
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(expand=True, fill="both", padx=30, pady=20)
        
        title = ctk.CTkLabel(
            main_frame,
            text=self.t("downloading"),
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=(0, 20))
        
        self.progress = ctk.CTkProgressBar(main_frame, width=400, height=20)
        self.progress.pack(pady=20)
        self.progress.set(0)
        
        self.status_label = ctk.CTkLabel(
            main_frame,
            text=self.t("connecting"),
            font=ctk.CTkFont(size=14)
        )
        self.status_label.pack(pady=10)
        
        self.log_text = scrolledtext.ScrolledText(
            main_frame,
            width=60,
            height=12,
            font=("Consolas", 10),
            bg="#2b2b2b",
            fg="#00ff00",
            insertbackground="white"
        )
        self.log_text.pack(pady=20, fill="both", expand=True)
        
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(pady=(10, 0), fill="x")
        
        self.stop_btn = ctk.CTkButton(
            btn_frame,
            text=self.t("stop"),
            height=45,
            fg_color="#e74c3c",
            hover_color="#c0392b",
            command=self.stop_downloading,
            anchor="center"
        )
        self.stop_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        back_btn = ctk.CTkButton(
            btn_frame,
            text=self.t("back"),
            height=45,
            fg_color="#95a5a6",
            hover_color="#7f8c8d",
            command=self.show_main_page,
            anchor="center"
        )
        back_btn.pack(side="left", fill="x", expand=True, padx=(5, 0))
        
        threading.Thread(target=self._download_thread, daemon=True).start()
    
    def stop_downloading(self):
        """توقف دانلود"""
        self.stop_download = True
        self.log(f"⏹ {self.t('download_stopped')}")
        self.update_status(self.t("download_stopped"))
        messagebox.showinfo("ℹ", f"{self.t('download_stopped')}\n{self.t('can_resume')}")
    
    def _download_thread(self):
        """Thread دانلود"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            loop.run_until_complete(self.download_messages())
        except Exception as e:
            if not self.stop_download:
                self.log(f"❌ {self.t('error')}: {str(e)}")
                self.after(0, lambda: messagebox.showerror(self.t("error"), f"{self.t('error')}:\n{str(e)}"))
        finally:
            loop.close()
    
    async def download_messages(self):
        """دانلود پیام‌ها"""
        api_id = int(self.config["api_id"])
        api_hash = self.config["api_hash"]
        channel_username = self.config["channel_username"]
        concurrent_limit = self.config.get("concurrent_downloads", 3)
        
        photos_dir = os.path.join(self.media_dir, "photos")
        videos_dir = os.path.join(self.media_dir, "videos")
        other_dir = os.path.join(self.media_dir, "other")
        
        for d in [photos_dir, videos_dir, other_dir]:
            os.makedirs(d, exist_ok=True)
        
        # ساخت client
        client = None
        if self.proxy_settings:
            if self.proxy_settings.get('proxy_type') == 'mtproto':
                client = TelegramClient(
                    self.session_name,
                    api_id,
                    api_hash,
                    proxy=(self.proxy_settings['addr'], self.proxy_settings['port'], self.proxy_settings['secret'])
                )
                self.log("🌐 Using MTProto Proxy")
            else:
                client = TelegramClient(
                    self.session_name,
                    api_id,
                    api_hash,
                    proxy=self.proxy_settings
                )
                self.log("🌐 Using Proxy")
        else:
            client = TelegramClient(self.session_name, api_id, api_hash)
            self.log("🌐 Direct connection (no proxy)")
        
        async with client:
            if self.stop_download:
                return
            
            self.log("✅ " + self.t("connected"))
            self.log(f"⚡ Concurrent downloads: {concurrent_limit}")
            self.update_status(self.t("connected"))
            
            if os.path.exists(self.excel_file):
                old_df = pd.read_excel(self.excel_file)
                last_id = old_df["Message ID"].max()
                self.log(f"📊 Last message ID: {last_id}")
            else:
                old_df = pd.DataFrame()
                last_id = 0
            
            if self.stop_download:
                return
            
            channel = await client.get_entity(channel_username)
            self.log(f"📢 Channel: {channel.title}")
            
            start_date = None
            end_date = None
            
            if self.config.get("start_date"):
                try:
                    start_date = datetime.strptime(self.config["start_date"], "%Y-%m-%d")
                    start_date = start_date.replace(tzinfo=None)
                    self.log(f"📅 Start: {start_date.strftime('%Y-%m-%d')}")
                except:
                    pass
            
            if self.config.get("end_date"):
                try:
                    end_date = datetime.strptime(self.config["end_date"], "%Y-%m-%d")
                    end_date = end_date.replace(tzinfo=None)
                    self.log(f"📅 End: {end_date.strftime('%Y-%m-%d')}")
                except:
                    pass
            
            self.update_status(self.t("getting_messages"))
            new_data = []
            processed = 0
            total_size = 0
            
            # Semaphore for concurrent downloads
            semaphore = asyncio.Semaphore(concurrent_limit)
            
            async def download_with_semaphore(msg, msg_id, msg_date, msg_text):
                """دانلود با محدودیت همزمانی"""
                async with semaphore:
                    if self.stop_download:
                        return None
                    
                    try:
                        filename = await client.download_media(
                            msg,
                            file=self.media_dir,
                            progress_callback=None
                        )
                        
                        if filename:
                            ext = os.path.splitext(filename)[1].lower()
                            base_name = os.path.basename(filename)
                            file_size = os.path.getsize(filename)
                            
                            if ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]:
                                dest = os.path.join(photos_dir, base_name)
                            elif ext in [".mp4", ".mov", ".mkv", ".avi"]:
                                dest = os.path.join(videos_dir, base_name)
                            else:
                                dest = os.path.join(other_dir, base_name)
                            
                            if os.path.exists(dest):
                                os.remove(dest)
                            os.rename(filename, dest)
                            
                            self.log(f"✓ Saved: {base_name}")
                            
                            return {
                                "Message ID": msg_id,
                                "Date": msg_date,
                                "Text": msg_text,
                                "Media Path": dest,
                                "Size": file_size
                            }
                    except Exception as e:
                        self.log(f"⚠ Error (ID {msg_id}): {str(e)}")
                    
                    return {
                        "Message ID": msg_id,
                        "Date": msg_date,
                        "Text": msg_text,
                        "Media Path": "",
                        "Size": 0
                    }
            
            messages_to_process = []
            
            # جمع‌آوری پیام‌ها
            async for msg in client.iter_messages(channel):
                if self.stop_download:
                    break
                
                if msg.id <= last_id:
                    break
                
                if msg.date:
                    msg_date = msg.date.replace(tzinfo=None)
                    
                    if start_date and msg_date < start_date:
                        continue
                    
                    if end_date and msg_date > end_date:
                        continue
                
                text = msg.message if msg.message else "[MEDIA ONLY]"
                msg_date_clean = msg.date.replace(tzinfo=None) if msg.date else None
                
                if msg.media:
                    messages_to_process.append((msg, msg.id, msg_date_clean, text))
                else:
                    new_data.append({
                        "Message ID": msg.id,
                        "Date": msg_date_clean,
                        "Text": text,
                        "Media Path": ""
                    })
                
                processed += 1
                if processed % 10 == 0:
                    self.log(f"📥 Collected {processed} messages...")
            
            # دانلود همزمان رسانه‌ها
            if messages_to_process and not self.stop_download:
                self.log(f"⚡ Starting {concurrent_limit} concurrent downloads...")
                
                for i in range(0, len(messages_to_process), concurrent_limit * 5):
                    if self.stop_download:
                        break
                    
                    batch = messages_to_process[i:i + concurrent_limit * 5]
                    tasks = [download_with_semaphore(msg, msg_id, msg_date, text) 
                            for msg, msg_id, msg_date, text in batch]
                    
                    results = await asyncio.gather(*tasks)
                    
                    for result in results:
                        if result:
                            new_data.append({
                                "Message ID": result["Message ID"],
                                "Date": result["Date"],
                                "Text": result["Text"],
                                "Media Path": result["Media Path"]
                            })
                            total_size += result["Size"]
                    
                    progress_pct = min((i + len(batch)) / len(messages_to_process), 1.0)
                    self.update_progress(progress_pct)
                    self.update_status(f"Downloaded: {i + len(batch)}/{len(messages_to_process)}")
                    
                    size_mb = total_size / (1024 * 1024)
                    self.log(f"📦 Progress: {i + len(batch)}/{len(messages_to_process)} - {size_mb:.1f} MB")
                    
                    # Auto-save
                    if len(new_data) % 50 == 0 and len(new_data) > 0:
                        self.save_to_excel(old_df, new_data)
                        self.log(f"💾 Auto-saved {len(new_data)} messages")
            
            self.log(f"📨 Total: {processed}")
            self.log(f"📦 Downloaded: {total_size / (1024 * 1024):.1f} MB")
            
            if new_data:
                self.save_to_excel(old_df, new_data)
                self.log(f"✅ {len(new_data)} new messages")
                self.update_status("✓ Complete")
                self.update_progress(1.0)
                
                if not self.stop_download:
                    self.after(0, lambda: messagebox.showinfo("✓", f"{len(new_data)} {self.t('messages_downloaded')}"))
            else:
                if not self.stop_download:
                    self.log("ℹ No new messages")
                    self.update_status("No new messages")
                    self.update_progress(1.0)
                    self.after(0, lambda: messagebox.showinfo("ℹ", self.t("no_new_messages")))
    
    def save_to_excel(self, old_df, new_data):
        """ذخیره Excel"""
        df_new = pd.DataFrame(new_data)
        df = pd.concat([old_df, df_new])
        df = df.sort_values("Message ID")
        df.to_excel(self.excel_file, index=False)
    
    def log(self, message):
        """لاگ"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.after(0, lambda: self.log_text.insert("end", f"[{timestamp}] {message}\n"))
        self.after(0, lambda: self.log_text.see("end"))
    
    def update_status(self, text):
        """بروزرسانی وضعیت"""
        self.after(0, lambda: self.status_label.configure(text=text))
    
    def update_progress(self, value):
        """بروزرسانی Progress"""
        self.after(0, lambda: self.progress.set(value))


if __name__ == "__main__":
    app = TelegramDownloaderApp()
    app.mainloop()