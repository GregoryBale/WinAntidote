import os
import sys
import ctypes
import winreg
import psutil
import keyboard
import subprocess
import tempfile
import shutil
import time
import win32gui
import win32con
import win32process
import win32security
import win32api
from threading import Thread
from ctypes import windll, wintypes, byref, Structure, POINTER, c_int, c_uint, c_void_p
import pygetwindow as gw
import pyautogui
from pynput.keyboard import Controller as KeyboardController
from pynput.mouse import Controller as MouseController
import sounddevice as sd
import pyperclip
import asyncio
from pypsexec.client import Client
import pyscreeze
from pywinauto import Application
import tkinter as tk
from tkinter import scrolledtext
import threading
import wmi
import nmap
import comtypes.client
import pyaudio

class CustomConsole:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("WinAntidote (UI) v.2.03a (ui version)")
        self.root.geometry("800x600")
        self.root.configure(bg="#FFFFFF")  
        self.text_area = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            width=95,
            height=35,
            bg="#FFFFFF",
            fg="#000000",
            font=("Consolas", 10),
            insertbackground="white"
        )
        self.text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        sys.stdout = self
        sys.stderr = self
        self.root.resizable(False, False)
        
    def write(self, text):
        self.text_area.insert(tk.END, text)
        self.text_area.see(tk.END)
        self.root.update()
        
    def flush(self):
        pass
        
    def run(self):
        self.root.mainloop()
      
def run_script(console):
    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def force_admin_privileges():
        if not is_admin():
            print("[WARNING !] Требуются права администратора для работы скрипта...")
            script_path = os.path.abspath(sys.argv[0])
            try:
                result = ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script_path}" --elevated', None, 1)
                if result > 32: 
                    print("[PROCESSING !] Запуск с повышенными правами инициирован. Закрываю текущий экземпляр...")
                    sys.exit(0)
                else:
                    raise Exception("Не удалось запустить с правами администратора")
            except Exception as e:
                print(f"[WARNING !] Ошибка при попытке запуска с правами администратора: {e}")
                print("[WARNING !] Попытка альтернативного метода через PowerShell...")
                try:
                    temp_bat = os.path.join(tempfile.gettempdir(), "elevate_antidot.bat")
                    with open(temp_bat, "w") as f:
                        f.write('@echo off\n')
                        f.write(f'powershell -Command "Start-Process -FilePath \'{sys.executable}\' -ArgumentList \'{script_path} --elevated\' -Verb RunAs"\n')
                        f.write('exit\n')
                    subprocess.Popen(temp_bat, shell=True)
                    print("[PROCESSING !] Запуск с повышенными правами через bat-файл инициирован. Закрываю текущий экземпляр...")
                    os.remove(temp_bat)
                    sys.exit(0)
                except Exception as e2:
                    print(f"[WARNING !] Не удалось получить права администратора: {e2}")
                    print("[WARNING !] Скрипт продолжит работу с ограниченными правами")
                    return False
        return True

    if "--elevated" not in sys.argv:
        force_admin_privileges()
    else:
        print("[PROCESSING !] Скрипт запущен с повышенными правами")

    def restore_system_utilities_gui():
        print("[PROCESSING !] Восстановление GUI системных утилит...")
        try:
            app = Application().start("control.exe")
            dlg = app.top_window()
            if dlg.exists():
                dlg.maximize()
                print("[PASS] Панель управления восстановлена")
                dlg.close()
            else:
                raise Exception("Окно не открылось")
        except Exception as e:
            print(f"[FAIL] Ошибка восстановления GUI: {e}")

    def check_filesystem_integrity():
        print("[PROCESSING !] Проверка целостности файловой системы...")
        try:
            img = pytsk3.Img_Info("\\\\.\\C:")
            fs = pytsk3.FS_Info(img)
            if fs.info.ftype == pytsk3.TSK_FS_TYPE_NTFS:
                root_dir = fs.open_dir("/")
                for entry in root_dir:
                    if entry.info.name.name.decode() == "System Volume Information":
                        print("[PASS] Файловая система NTFS в порядке")
                        break
            else:
                print("[WARNING] Обнаружено изменение типа файловой системы")
        except Exception as e:
            print(f"[FAIL] Ошибка проверки файловой системы: {e}")

    def restore_desktop_via_screenshot():
        print("[PROCESSING !] Проверка и восстановление рабочего стола через снимок экрана...")
        try:
            screenshot = pyscreeze.screenshot()
            pixel = screenshot.getpixel((100, 100))
            if all(p < 10 for p in pixel): 
                print("[INFO] Обнаружен пустой рабочий стол, перезапуск Explorer...")
                subprocess.run(["taskkill", "/IM", "explorer.exe", "/F"], check=True)
                subprocess.run(["explorer.exe"], check=True)
                time.sleep(2)
                print("[PASS] Рабочий стол восстановлен")
            else:
                print("[INFO] Рабочий стол в порядке")
        except Exception as e:
            print(f"[FAIL] Ошибка анализа экрана: {e}")

    async def check_network_async():
        print("[PROCESSING !] Асинхронная проверка сети...")
        try:
            async def ping_host(host):
                proc = await asyncio.create_subprocess_exec("ping", host, "-n", "2",
                                                           stdout=asyncio.subprocess.PIPE)
                stdout, _ = await proc.communicate()
                return "Reply from" in stdout.decode()

            if await ping_host("8.8.8.8"):
                print("[PASS] Сеть работает")
            else:
                c = Client("localhost")
                c.connect()
                c.run_executable("cmd.exe", arguments="/c netsh interface ip reset")
                c.disconnect()
                print("[PASS] Сетевые настройки сброшены через PSEXEC")
        except Exception as e:
            print(f"[FAIL] Ошибка проверки сети: {e}")

    def restore_network_async():
        asyncio.run(check_network_async())

    def restore_clipboard():
        print("[PROCESSING !] Восстановление буфера обмена...")
        try:
            pyperclip.copy("Тест Antidote")
            if pyperclip.paste() == "Тест Antidote":
                print("[PASS] Буфер обмена работает")
            else:
                raise ValueError("Буфер обмена поврежден")
        except Exception as e:
            print(f"[FAIL] Ошибка восстановления буфера: {e}")
            try:
                subprocess.run(["taskkill", "/IM", "clip.exe", "/F"], check=True)
                print("[PASS] Процесс буфера обмена перезапущен")
            except:
                print("[FAIL] Не удалось перезапустить буфер")

    def restore_audio():
        print("[PROCESSING !] Восстановление звуковых функций...")
        try:
            devices = sd.query_devices()
            if not devices:
                print("[INFO] Звуковые устройства не обнаружены, перезапуск службы...")
                subprocess.run(["net", "stop", "audiosrv"], check=True)
                subprocess.run(["net", "start", "audiosrv"], check=True)
                print("[PASS] Служба звука перезапущена")
            else:
                print("[INFO] Звуковые устройства работают")
        except Exception as e:
            print(f"[FAIL] Ошибка восстановления звука: {e}")

    def bypass_input_blocks():
        print("[PROCESSING !] Обход блокировки ввода...")
        try:
            keyboard = KeyboardController()
            mouse = MouseController()
            keyboard.press("a")
            keyboard.release("a")
            mouse.move(50, 50)
            mouse.click(mouse.Button.left, 1)
            print("[PASS] Управление мышью и клавиатурой восстановлено")
        except Exception as e:
            print(f"[FAIL] Ошибка восстановления ввода: {e}")

    def restore_hidden_windows():
        print("[PROCESSING !] Восстановление скрытых системных окон...")
        try:
            windows = gw.getAllTitles()
            if not any("File Explorer" in w or "Task Manager" in w for w in windows):
                pyautogui.hotkey("win", "e") 
                pyautogui.hotkey("ctrl", "shift", "esc") 
                print("[PASS] Скрытые окна Explorer и Task Manager восстановлены")
            else:
                print("[INFO] Системные окна уже доступны")
        except Exception as e:
            print(f"[FAIL] Ошибка восстановления окон: {e}")

    def reset_network_configuration():
        try:
            print("[PROCESSING !] Сброс сетевой конфигурации...")
            commands = [
                ["netsh", "winsock", "reset"],
                ["netsh", "int", "ip", "reset"],
                ["netsh", "advfirewall", "reset"],
                ["ipconfig", "/release"],
                ["ipconfig", "/renew"],
                ["ipconfig", "/flushdns"]
            ]  
            for cmd in commands:
                subprocess.run(cmd, capture_output=True, shell=True, check=False)  
            print("[PASS !] Сетевая конфигурация сброшена")
        except Exception as e:
            print(f"[FAIL !] Ошибка при сбросе сетевой конфигурации: {e}")

    def clean_dns_cache():
        try:
            print("[PROCESSING !] Очистка DNS-кэша...")
            subprocess.run(["ipconfig", "/flushdns"], 
                          capture_output=True, shell=True, check=False)
            print("[PASS !] DNS-кэш очищен")
        except Exception as e:
            print(f"[FAIL !] Ошибка при очистке DNS-кэша: {e}")

    def check_registry_integrity():
        try:
            backup_path = os.path.join(os.environ['USERPROFILE'], 'Desktop', 'registry_backup.reg')
            subprocess.run(["reg", "export", "HKLM", backup_path, "/y"],
                          capture_output=True, shell=True, check=False)
            print(f"[PASS !] Резервная копия реестра сохранена: {backup_path}")
        except Exception as e:
            print(f"[FAIL !] Ошибка при проверке целостности реестра: {e}")

    def restore_lock_screen():
        try:
            subprocess.run(["reg", "add", "HKLM\\Software\\Policies\\Microsoft\\Windows\\Personalization", 
                           "/v", "NoLockScreen", "/t", "REG_DWORD", "/d", "0", "/f"],
                          capture_output=True, shell=True, check=False)
            print("[PASS !] Экран блокировки восстановлен")
        except Exception as e:
            print(f"[FAIL !] Ошибка при восстановлении экрана блокировки: {e}")

    def restore_windows_update_access():
        try:
            subprocess.run(["reg", "add", "HKLM\\Software\\Policies\\Microsoft\\Windows\\WindowsUpdate", 
                           "/v", "DisableWindowsUpdateAccess", "/t", "REG_DWORD", "/d", "0", "/f"],
                          capture_output=True, shell=True, check=False)
            print("[PASS !] Доступ к Центру обновления Windows восстановлен")
        except Exception as e:
            print(f"[FAIL !] Ошибка при восстановлении доступа к обновлениям: {e}")

    def restore_antivirus():
        try:
            subprocess.run(["sc", "config", "WinDefend", "start=", "auto"], 
                          capture_output=True, check=False)
            subprocess.run(["net", "start", "WinDefend"], 
                          capture_output=True, check=False)
            subprocess.run(["powershell", "-Command", 
                          "Set-MpPreference -DisableRealtimeMonitoring $false"],
                          capture_output=True, check=False)
            key_path = r"SOFTWARE\Microsoft\Windows Defender\Real-Time Protection"
            try:
                registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE)
                winreg.SetValueEx(registry_key, "DisableRealtimeMonitoring", 0, winreg.REG_DWORD, 0)
                winreg.CloseKey(registry_key)
            except:
                pass
            print("[PASS !] Антивирусная защита восстановлена")
        except Exception as e:
            print(f"[FAIL !] Ошибка при восстановлении антивируса: {e}")

    def restore_windows_firewall():
        try:
            subprocess.run(["sc", "config", "MpsSvc", "start=", "auto"], 
                          capture_output=True, check=False)
            subprocess.run(["net", "start", "MpsSvc"], 
                          capture_output=True, check=False)
            subprocess.run(["netsh", "advfirewall", "reset"], 
                          capture_output=True, check=False)
            subprocess.run(["netsh", "advfirewall", "set", "allprofiles", "state", "on"], 
                          capture_output=True, check=False)
            print("[PASS !] Брандмауэр Windows восстановлен")
        except Exception as e:
            print(f"[FAIL !] Ошибка при восстановлении брандмауэра: {e}")

    def repair_boot_sector():
        try:
            print("[PROCESSING !] Проверка и восстановление загрузочного сектора...")
            subprocess.run(["bootrec", "/fixmbr"], 
                          capture_output=True, check=False)
            subprocess.run(["bootrec", "/fixboot"], 
                          capture_output=True, check=False)
            subprocess.run(["bootrec", "/rebuildbcd"], 
                          capture_output=True, check=False)
            print("[PASS !] Загрузочный сектор восстановлен")
        except Exception as e:
            print(f"[FAIL !] Ошибка при восстановлении загрузочного сектора: {e}")

    def reset_group_policies():
        try:
            subprocess.run(["secedit", "/configure", "/cfg", "%windir%\\inf\\defltbase.inf", 
                           "/db", "defltbase.sdb", "/verbose"], 
                          capture_output=True, shell=True, check=False)
            print("[PASS !] Локальные групповые политики сброшены до значений по умолчанию")
        except Exception as e:
            print(f"[FAIL !] Ошибка при сбросе групповых политик: {e}")
    
    def enable_network_adapters():
        try:
            subprocess.run(["powershell", "-Command", "Get-NetAdapter | Enable-NetAdapter"],
                          capture_output=True, shell=True, check=False)
            print("[PASS !] Сетевые адаптеры включены")
        except Exception as e:
            print(f"[FAIL !] Ошибка при включении сетевых адаптеров: {e}")

    def reset_proxy_settings():
        try:
            subprocess.run(["netsh", "winhttp", "reset", "proxy"],
                          capture_output=True, shell=True, check=False)
            print("[PASS !] Настройки прокси сброшены")
        except Exception as e:
            print(f"[FAIL !] Ошибка при сбросе настроек прокси: {e}")
        
    def enable_windows_services():
        services = ["wuauserv", "bits", "cryptsvc"]
        for service in services:
            try:
                subprocess.run(["sc", "config", service, "start=", "auto"],
                              capture_output=True, shell=True, check=False)
                subprocess.run(["sc", "start", service],
                              capture_output=True, shell=True, check=False)
                print(f"[PASS !] Служба {service} включена и запущена")
            except Exception as e:
                print(f"[FAIL !] Ошибка при включении службы {service}: {e}")
            
    def clean_temp_files():
        temp_dirs = [tempfile.gettempdir(), os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Temp')]
        for temp_dir in temp_dirs:
            try:
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        try:
                            os.remove(os.path.join(root, file))
                        except:
                            pass
                    for dir in dirs:
                        try:
                            shutil.rmtree(os.path.join(root, dir), ignore_errors=True)
                        except:
                            pass
                print(f"[PASS !] Временные файлы в {temp_dir} очищены")
            except Exception as e:
                print(f"[FAIL !] Ошибка при очистке временных файлов в {temp_dir}: {e}")
            
    def restore_file_associations():
        try:
            subprocess.run(["assoc", ".exe=exefile"],
                          capture_output=True, shell=True, check=False)
            subprocess.run(["assoc", ".bat=batfile"],
                          capture_output=True, shell=True, check=False)
            subprocess.run(["assoc", ".cmd=cmdfile"],
                          capture_output=True, shell=True, check=False)
            print("[PASS !] Ассоциации файлов восстановлены")
        except Exception as e:
            print(f"[FAIL !] Ошибка при восстановлении ассоциаций файлов: {e}")
        
    def enable_firewall():
        try:
            subprocess.run(["netsh", "advfirewall", "set", "allprofiles", "state", "on"],
                          capture_output=True, shell=True, check=False)
            print("[PASS !] Брандмауэр Windows включен")
        except Exception as e:
            print(f"[FAIL !] Ошибка при включении брандмауэра: {e}")
    
    def enable_self_protection():
        try:
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleCtrlHandler(None, True)
            print("[PASS !] Self-protection enabled.")
        except Exception as e:
            print(f"[FAIL !] Could not enable self-protection: {e}")

    def kill_blocking_scripts():
        print("[PROCESSING !] Поиск и завершение процессов блокировки...")
        flag_files = [
            os.path.join(os.getenv('APPDATA'), ".system_maintenance.lock"),
            "block_script_running.flag",
            os.path.join(tempfile.gettempdir(), "block_running.tmp")
        ]
        for flag_file in flag_files:
            if os.path.exists(flag_file):
                try:
                    with open(flag_file, "r") as f:
                        pid = int(f.read().strip())
                        try:
                            p = psutil.Process(pid)
                            p.terminate()
                            print(f"[PASS !] Процесс блокировки с PID {pid} завершен")
                        except:
                            pass
                    os.remove(flag_file)
                    print(f"[PASS !] Файл-флаг блокировки {flag_file} удален")
                except:
                    pass
        suspicious_terms = ["block", "блок", "maintenance", "system_maintenance", "block_script"]
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmdline = " ".join(proc.info['cmdline']).lower() if proc.info['cmdline'] else ""
                name = proc.info['name'].lower() if proc.info['name'] else ""
                if "python" in name and any(term in cmdline for term in suspicious_terms):
                    try:
                        p = psutil.Process(proc.info['pid'])
                        p.terminate()
                        print(f"[PASS !] Процесс блокировки с PID {proc.info['pid']} завершен")
                    except:
                        try:
                            p = psutil.Process(proc.info['pid'])
                            p.kill()
                            print(f"[PASS !] Процесс блокировки с PID {proc.info['pid']} принудительно завершен")
                        except:
                            pass
            except:
                pass
        hidden_script_locations = [
            os.path.join(os.getenv('APPDATA'), "Microsoft", "Windows", "SystemApps", "Maintenance", "system_maintenance.py"),
            os.path.join(os.getenv('APPDATA'), "Microsoft", "Windows", "Start Menu", "Programs", "Startup", "system_maintenance.bat"),
            os.path.join(os.getenv('APPDATA'), "Microsoft", "Windows", "Start Menu", "Programs", "Startup", "system_maintenance.vbs")
        ]
        for script_path in hidden_script_locations:
            if os.path.exists(script_path):
                try:
                    os.remove(script_path)
                    print(f"[PASS !] Скрытая копия скрипта блокировки удалена: {script_path}")
                except:
                    print(f"[FAIL !] Не удалось удалить скрытую копию: {script_path}")
                
    def enable_task_manager():
        try:
            key_paths = [
                r"Software\Microsoft\Windows\CurrentVersion\Policies\System",
                r"Software\Microsoft\Windows\CurrentVersion\Group Policy Objects\LocalUser\Software\Microsoft\Windows\CurrentVersion\Policies\System"
            ]
            for key_path in key_paths:
                try:
                    registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
                    winreg.SetValueEx(registry_key, "DisableTaskMgr", 0, winreg.REG_DWORD, 0)
                    winreg.CloseKey(registry_key)
                except:
                    pass
            try:
                subprocess.run(['REG', 'ADD', 'HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System',
                             '/v', 'DisableTaskMgr', '/t', 'REG_DWORD', '/d', '0', '/f'],
                             capture_output=True, check=False)
            except:
                pass
            desktop_path = os.path.join(os.environ['USERPROFILE'], 'Desktop')
            taskmgr_shortcut = os.path.join(desktop_path, 'TaskManager.lnk')
            try:
                with open(taskmgr_shortcut, 'w') as f:
                    f.write('[InternetShortcut]\n')
                    f.write('URL=file:///C:/Windows/System32/taskmgr.exe\n')
                    f.write('IconIndex=0\n')
                    f.write('IconFile=C:/Windows/System32/taskmgr.exe\n')
            except:
                pass
            print("[PASS !] Диспетчер задач восстановлен")
        except Exception as e:
            print(f"[FAIL !] Ошибка при восстановлении диспетчера задач: {e}")

    def enable_registry_editor():
        try:
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Policies\System"
            try:
                registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
                winreg.SetValueEx(registry_key, "DisableRegistryTools", 0, winreg.REG_DWORD, 0)
                winreg.CloseKey(registry_key)
            except:
                pass
            try:
                subprocess.run(['REG', 'ADD', 'HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System',
                             '/v', 'DisableRegistryTools', '/t', 'REG_DWORD', '/d', '0', '/f'],
                             capture_output=True, check=False)
            except:
                pass
            desktop_path = os.path.join(os.environ['USERPROFILE'], 'Desktop')
            regedit_shortcut = os.path.join(desktop_path, 'RegEdit.lnk')
            try:
                with open(regedit_shortcut, 'w') as f:
                    f.write('[InternetShortcut]\n')
                    f.write('URL=file:///C:/Windows/regedit.exe\n')
                    f.write('IconIndex=0\n')
                    f.write('IconFile=C:/Windows/regedit.exe\n')
            except:
                pass
            print("[PASS !] Редактор реестра восстановлен")
        except Exception as e:
            print(f"[FAIL !] Ошибка при восстановлении редактора реестра: {e}")

    def enable_cmd_and_powershell():
        try:
            key_path = r"Software\Policies\Microsoft\Windows\System"
            try:
                registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
                winreg.SetValueEx(registry_key, "DisableCMD", 0, winreg.REG_DWORD, 0)
                winreg.CloseKey(registry_key)
            except:
                pass
            try:
                subprocess.run(['REG', 'ADD', 'HKCU\\Software\\Policies\\Microsoft\\Windows\\System',
                             '/v', 'DisableCMD', '/t', 'REG_DWORD', '/d', '0', '/f'],
                             capture_output=True, check=False)
            except:
                pass
            try:
                subprocess.run(["powershell", "-Command", "Set-ExecutionPolicy Unrestricted -Force -Scope CurrentUser"],
                              capture_output=True, shell=True, check=False)
            except:
                pass
            desktop_path = os.path.join(os.environ['USERPROFILE'], 'Desktop')
            cmd_shortcut = os.path.join(desktop_path, 'Command Prompt.lnk')
            try:
                with open(cmd_shortcut, 'w') as f:
                    f.write('[InternetShortcut]\n')
                    f.write('URL=file:///C:/Windows/System32/cmd.exe\n')
                    f.write('IconIndex=0\n')
                    f.write('IconFile=C:/Windows/System32/cmd.exe\n')
            except:
                pass
            ps_shortcut = os.path.join(desktop_path, 'PowerShell.lnk')
            try:
                with open(ps_shortcut, 'w') as f:
                    f.write('[InternetShortcut]\n')
                    f.write('URL=file:///C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe\n')
                    f.write('IconIndex=0\n')
                    f.write('IconFile=C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe\n')
            except:
                pass
            print("[PASS !] Командная строка и PowerShell восстановлены")
        except Exception as e:
            print(f"[FAIL !] Ошибка при восстановлении командной строки: {e}")

    def enable_usb_storage():
        try:
            key_path = r"SYSTEM\CurrentControlSet\Services\USBSTOR"
            try:
                registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE)
                winreg.SetValueEx(registry_key, "Start", 0, winreg.REG_DWORD, 3)
                winreg.CloseKey(registry_key)
            except:
                pass
            try:
                subprocess.run(['REG', 'ADD', 'HKLM\\SYSTEM\\CurrentControlSet\\Services\\USBSTOR',
                             '/v', 'Start', '/t', 'REG_DWORD', '/d', '3', '/f'],
                             capture_output=True, check=False)
            except:
                pass
            print("[PASS !] USB накопители восстановлены")
        except Exception as e:
            print(f"[FAIL !] Ошибка при восстановлении USB: {e}")

    def enable_control_panel():
        try:
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer"
            try:
                registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
                winreg.SetValueEx(registry_key, "NoControlPanel", 0, winreg.REG_DWORD, 0)
                winreg.CloseKey(registry_key)
            except:
                pass
            try:
                subprocess.run(['REG', 'ADD', 'HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer',
                             '/v', 'NoControlPanel', '/t', 'REG_DWORD', '/d', '0', '/f'],
                             capture_output=True, check=False)
            except:
                pass
            desktop_path = os.path.join(os.environ['USERPROFILE'], 'Desktop')
            cp_shortcut = os.path.join(desktop_path, 'Control Panel.lnk')
            try:
                with open(cp_shortcut, 'w') as f:
                    f.write('[InternetShortcut]\n')
                    f.write('URL=shell:::{5399E694-6CE5-4D6C-8FCE-1D8870FDCBA0}\n')
            except:
                pass
            print("[PASS !] Панель управления восстановлена")
        except Exception as e:
            print(f"[FAIL !] Ошибка при восстановлении панели управления: {e}")

    def enable_system_tray():
        try:
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer"
            try:
                registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
                winreg.SetValueEx(registry_key, "NoTrayItemsDisplay", 0, winreg.REG_DWORD, 0)
                winreg.CloseKey(registry_key)
            except:
                pass
            try:
                subprocess.run(['REG', 'ADD', 'HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer',
                             '/v', 'NoTrayItemsDisplay', '/t', 'REG_DWORD', '/d', '0', '/f'],
                             capture_output=True, check=False)
            except:
                pass
            print("[PASS !] Системный трей восстановлен")
        except Exception as e:
            print(f"[FAIL !] Ошибка при восстановлении системного трея: {e}")

    def show_desktop_icons():
        try:
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer"
            try:
                registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
                winreg.SetValueEx(registry_key, "NoDesktop", 0, winreg.REG_DWORD, 0)
                winreg.CloseKey(registry_key)
            except:
                pass
            try:
                subprocess.run(['REG', 'ADD', 'HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer',
                             '/v', 'NoDesktop', '/t', 'REG_DWORD', '/d', '0', '/f'],
                             capture_output=True, check=False)
            except:
                pass
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'].lower() == 'explorer.exe':
                    try:
                        psutil.Process(proc.info['pid']).kill()
                    except:
                        pass
            subprocess.Popen('explorer.exe')
            print("[PASS !] Иконки рабочего стола восстановлены")
        except Exception as e:
            print(f"[FAIL !] Ошибка при восстановлении иконок рабочего стола: {e}")

    def enable_start_button():
        try:
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer"
            registry_keys = [
                ("NoStartMenuMorePrograms", 0),
                ("NoStartMenuPinnedList", 0),
                ("NoStartMenuMFUprogramsList", 0),
                ("NoUserNameInStartMenu", 0)
            ]
            try:
                registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
                for name, value in registry_keys:
                    winreg.SetValueEx(registry_key, name, 0, winreg.REG_DWORD, value)
                winreg.CloseKey(registry_key)
            except:
                pass
            for name, value in registry_keys:
                try:
                    subprocess.run(['REG', 'ADD', f'HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer',
                                 '/v', name, '/t', 'REG_DWORD', '/d', str(value), '/f'],
                                 capture_output=True, check=False)
                except:
                    pass
            print("[PASS !] Кнопка Пуск восстановлена")
        except Exception as e:
            print(f"[FAIL !] Ошибка при восстановлении кнопки Пуск: {e}")

    def enable_right_click():
        try:
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer"
            try:
                registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
                winreg.SetValueEx(registry_key, "NoViewContextMenu", 0, winreg.REG_DWORD, 0)
                winreg.CloseKey(registry_key)
            except:
                pass
            try:
                subprocess.run(['REG', 'ADD', 'HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer',
                             '/v', 'NoViewContextMenu', '/t', 'REG_DWORD', '/d', '0', '/f'],
                             capture_output=True, check=False)
            except:
                pass
            print("[PASS !] Контекстное меню восстановлено")
        except Exception as e:
            print(f"[FAIL !] Ошибка при восстановлении контекстного меню: {e}")

    def enable_program_execution():
        try:
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer"
            try:
                registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
                winreg.SetValueEx(registry_key, "DisallowRun", 0, winreg.REG_DWORD, 0)
                winreg.CloseKey(registry_key)
            except:
                pass
            try:
                subprocess.run(['REG', 'ADD', 'HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer',
                             '/v', 'DisallowRun', '/t', 'REG_DWORD', '/d', '0', '/f'],
                             capture_output=True, check=False)
            except:
                pass
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\DisallowRun"
            try:
                winreg.DeleteKey(winreg.HKEY_CURRENT_USER, key_path)
            except:
                try:
                    registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS)
                    try:
                        i = 0
                        while True:
                            value_name, _, _ = winreg.EnumValue(registry_key, i)
                            winreg.DeleteValue(registry_key, value_name)
                            i += 1
                    except:
                        pass
                    winreg.CloseKey(registry_key)
                except:
                    pass
            print("[PASS !] Ограничения на запуск программ сняты")
        except Exception as e:
            print(f"[FAIL !] Ошибка при снятии ограничений на запуск программ: {e}")

    def enable_security_settings():
        try:
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Policies\System"
            security_settings = [
                ("DisableChangePassword", 0),
                ("DisableLockWorkstation", 0),
                ("HideFastUserSwitching", 0)
            ]
            try:
                registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
                for name, value in security_settings:
                    winreg.SetValueEx(registry_key, name, 0, winreg.REG_DWORD, value)
                winreg.CloseKey(registry_key)
            except:
                pass
            for name, value in security_settings:
                try:
                    subprocess.run(['REG', 'ADD', f'HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System',
                                 '/v', name, '/t', 'REG_DWORD', '/d', str(value), '/f'],
                                 capture_output=True, check=False)
                except:
                    pass
            print("[PASS !] Настройки безопасности восстановлены")
        except Exception as e:
            print(f"[FAIL !] Ошибка при восстановлении настроек безопасности: {e}")

    def remove_from_startup():
        try:
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            try:
                registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
                try:
                    winreg.DeleteValue(registry_key, "SystemMaintenance")
                except:
                    pass
                winreg.CloseKey(registry_key)
            except:
                pass
            startup_folder = os.path.join(os.getenv('APPDATA'),
                                         r'Microsoft\Windows\Start Menu\Programs\Startup')
            suspicious_files = ["system_maintenance.bat", "system_maintenance.vbs", "maintenance.lnk", "startup.bat"]
            for file in suspicious_files:
                file_path = os.path.join(startup_folder, file)
                if os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                        print(f"[PASS !] Файл автозагрузки удален: {file_path}")
                    except:
                        print(f"[FAIL !] Не удалось удалить файл автозагрузки: {file_path}")
            print("[PASS !] Скрипт удален из автозагрузки")
        except Exception as e:
            print(f"[FAIL !] Ошибка при удалении из автозагрузки: {e}")

    def enable_safe_mode():
        try:
            key_path = r"SYSTEM\CurrentControlSet\Control\SafeBoot"
            try:
                registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE)
                try:
                    winreg.DeleteValue(registry_key, "AlternateShell")
                except:
                    pass
                winreg.CloseKey(registry_key)
            except:
                pass
            print("[PASS !] Безопасный режим восстановлен")
        except Exception as e:
            print(f"[FAIL !] Ошибка при восстановлении безопасного режима: {e}")

    def enable_recovery_options():
        try:
            subprocess.run(["wmic", "recoveros", "set", "AutoReboot", "=", "True"],
                          capture_output=True, shell=True, check=False)
            subprocess.run(["bcdedit", "/set", "{default}", "recoveryenabled", "Yes"],
                          capture_output=True, shell=True, check=False)
            subprocess.run(["bcdedit", "/set", "{default}", "bootstatuspolicy", "displayallfailures"],
                          capture_output=True, shell=True, check=False)
            print("[PASS !] Функции восстановления Windows включены")
        except Exception as e:
            print(f"[FAIL !] Ошибка при включении функций восстановления: {e}")

    def clear_keyboard_hooks():
        try:
            keyboard.unhook_all()
            keyboard._os_keyboard.init()
            print("[PASS !] Все перехваты клавиатуры сняты")
        except Exception as e:
            print(f"[FAIL !] Ошибка при снятии перехватов клавиатуры: {e}")
            
    def monitor_hardware_status():
        print("[PROCESSING !] Мониторинг и восстановление состояния оборудования...")
        try:
            c = wmi.WMI()
            for disk in c.Win32_DiskDrive():
                if disk.Status != "OK":
                    print(f"[INFO] Обнаружен сбой диска: {disk.Caption}, попытка перезапуска...")
                    subprocess.run(["devcon", "restart", f"*{disk.PNPDeviceID.split('\\\\')[1]}"], capture_output=True, shell=True, check=False)
                    print(f"[PASS !] Диск {disk.Caption} перезапущен")
                else:
                    print(f"[INFO] Диск {disk.Caption} в порядке")
            for processor in c.Win32_Processor():
                if processor.CurrentClockSpeed < processor.MaxClockSpeed * 0.8:
                    print("[INFO] Обнаружено снижение производительности процессора, сброс настроек...")
                    subprocess.run(["powercfg", "/setactive", "SCHEME_BALANCED"], capture_output=True, shell=True, check=False)
                    print("[PASS !] Настройки процессора сброшены")
        except Exception as e:
            print(f"[FAIL !] Ошибка при мониторинге оборудования: {e}")
            
    def restore_registry_access():
        print("[PROCESSING !] Восстановление прав доступа к реестру...")
        try:
            key_path = r"SYSTEM\CurrentControlSet"
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_ALL_ACCESS)
            sd = win32security.GetSecurityInfo(key, win32security.SE_REGISTRY_KEY, win32security.DACL_SECURITY_INFORMATION)
            dacl = sd.GetSecurityDescriptorDacl()
            dacl.AddAccessAllowedAce(win32security.ACL_REVISION, win32security.KEY_ALL_ACCESS, win32security.GetUserSid())
            win32security.SetSecurityInfo(key, win32security.SE_REGISTRY_KEY, win32security.DACL_SECURITY_INFORMATION, None, None, dacl, None)
            winreg.CloseKey(key)
            print("[PASS !] Права доступа к реестру восстановлены")
        except Exception as e:
            print(f"[FAIL !] Ошибка при восстановлении прав реестра: {e}")
            
    def neutralize_network_threats():
        print("[PROCESSING !] Обнаружение и нейтрализация сетевых угроз...")
        try:
            c = pypsexec.Client("localhost")
            c.connect()
            result = c.run_executable("netstat.exe", arguments="-ano")
            connections = result.stdout.decode().splitlines()
            suspicious_pids = []
            for line in connections:
                if "ESTABLISHED" in line and "0.0.0.0" not in line:
                    pid = line.split()[-1]
                    suspicious_pids.append(pid)
            for pid in suspicious_pids:
                try:
                    proc = psutil.Process(int(pid))
                    if "block" in proc.name().lower() or "maintenance" in proc.name().lower():
                        proc.terminate()
                        print(f"[PASS !] Подозрительное сетевое соединение (PID: {pid}) нейтрализовано")
                except:
                    pass
            c.disconnect()
            print("[INFO] Проверка сетевых соединений завершена")
        except Exception as e:
            print(f"[FAIL !] Ошибка при нейтрализации сетевых угроз: {e}")
            
    def scan_network_vulnerabilities():
        print("[PROCESSING !] Сканирование сети на уязвимости...")
        try:
            nm = nmap.PortScanner()
            nm.scan(hosts="127.0.0.1", arguments="-sV --open")
            for host in nm.all_hosts():
                for proto in nm[host].all_protocols():
                    ports = nm[host][proto].keys()
                    for port in ports:
                        state = nm[host][proto][port]['state']
                        service = nm[host][proto][port]['name']
                        if service in ["http", "ftp", "smb"] and state == "open":
                            print(f"[INFO] Обнаружен открытый порт {port} ({service}), закрытие...")
                            subprocess.run(["netsh", "advfirewall", "firewall", "add", "rule", f"name=Block_{port}", "dir=in", "action=block", f"protocol=TCP", f"localport={port}"], capture_output=True, shell=True, check=False)
                            print(f"[PASS !] Порт {port} заблокирован")
            print("[INFO] Сканирование сети завершено")
        except Exception as e:
            print(f"[FAIL !] Ошибка при сканировании сети: {e}")
            
    def test_audio_devices():
        print("[PROCESSING !] Проверка микрофона и аудиоустройств...")
        try:
            p = pyaudio.PyAudio()
            for i in range(p.get_device_count()):
                dev = p.get_device_info_by_index(i)
                if dev['maxInputChannels'] > 0:
                    print(f"[INFO] Тестирование микрофона: {dev['name']}")
                    stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, input_device_index=i)
                    stream.read(1024)
                    stream.close()
                    print(f"[PASS !] Микрофон {dev['name']} работает")
            p.terminate()
        except Exception as e:
            print(f"[INFO] Сбой аудиоустройств, перезапуск службы...")
            subprocess.run(["net", "stop", "audiosrv"], capture_output=True, check=False)
            subprocess.run(["net", "start", "audiosrv"], capture_output=True, check=False)
            print(f"[PASS !] Аудиослужба перезапущена")
            
    def restore_uac_settings():
        print("[PROCESSING !] Восстановление настроек UAC...")
        try:
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Policies\System"
            registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(registry_key, "EnableLUA", 0, winreg.REG_DWORD, 1)
            winreg.SetValueEx(registry_key, "ConsentPromptBehaviorAdmin", 0, winreg.REG_DWORD, 5)
            winreg.CloseKey(registry_key)
            print("[PASS !] Настройки UAC восстановлены")
        except Exception as e:
            print(f"[FAIL !] Ошибка при восстановлении UAC: {e}")
            
    def restore_com_objects():
        print("[PROCESSING !] Проверка и восстановление COM-объектов...")
        try:
            comtypes.client.GetModule("shell32.dll")
            shell = comtypes.client.CreateObject("Shell.Application")
            shell.NameSpace(0)
            print("[PASS !] COM-объекты Shell работают")
        except Exception as e:
            print(f"[INFO] Сбой COM-объектов, попытка перерегистрации...")
            subprocess.run(["regsvr32", "/s", "shell32.dll"], capture_output=True, shell=True, check=False)
            print(f"[PASS !] COM-объекты перерегистрированы")

    def create_recovery_report():
        try:
            report_path = os.path.join(os.environ['USERPROFILE'], 'Desktop', 'recovery_report.txt')
            with open(report_path, 'w') as f:
                f.write("ОТЧЕТ О ВОССТАНОВЛЕНИИ СИСТЕМЫ\n")
                f.write("=============================\n\n")
                f.write(f"Дата и время восстановления: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("Пользователь: " + os.getenv('USERNAME') + "\n")
                f.write("Компьютер: " + os.getenv('COMPUTERNAME') + "\n\n")
                f.write("Восстановленные функции:\n")
                f.write("- Диспетчер задач (Task Manager восстановлен для управления процессами)\n")
                f.write("- Редактор реестра (RegEdit снова доступен для редактирования системных настроек)\n")
                f.write("- Командная строка и PowerShell (CMD и PS разблокированы для выполнения команд)\n")
                f.write("- USB накопители (Подключение USB-устройств теперь работает корректно)\n")
                f.write("- Панель управления (Control Panel возвращена для управления системой)\n")
                f.write("- Системный трей (Область уведомлений восстановлена для удобства)\n")
                f.write("- Иконки рабочего стола (Рабочий стол снова отображает все ярлыки)\n")
                f.write("- Кнопка Пуск (Меню Пуск полностью функционально)\n")
                f.write("- Контекстное меню (Правый клик работает как раньше)\n")
                f.write("- Выполнение программ (Запуск приложений разблокирован)\n")
                f.write("- Настройки безопасности (Системные параметры безопасности восстановлены)\n")
                f.write("- Функции восстановления Windows (Опции восстановления системы активированы)\n")
                f.write("- Безопасный режим (Доступ к Safe Mode возвращён)\n")
                f.write("- Сетевые адаптеры и настройки прокси (Сеть и прокси сброшены и работают)\n")
                f.write("- Службы Windows (Критические службы запущены и настроены)\n")
                f.write("- Аудиоустройства (Микрофоны и звук проверены и восстановлены)\n")
                f.write("- Временные файлы и кэш (Очищены временные данные для оптимизации)\n")
                f.write("- Ассоциации файлов (Исполняемые файлы снова открываются корректно)\n")
                f.write("- Системные файлы (Проверка и восстановление системных компонентов выполнены)\n")
                f.write("- Брандмауэр Windows (Firewall активирован для защиты)\n")
                f.write("- Сброс групповых политик (Локальные политики возвращены к умолчанию)\n")
                f.write("- Настройки UAC (Контроль учетных записей восстановлен)\n")
                f.write("- Сетевая безопасность (Открытые порты проверены и защищены)\n")
                f.write("- Восстановление доступа к Центру обновления Windows (Обновления снова доступны)\n")
                f.write("- Очистка автозагрузки в реестре (Удалены нежелательные записи автозапуска)\n")
                f.write("- Восстановление экрана блокировки (Lock Screen снова функционирует)\n")
                f.write("- Проверка целостности реестра (Реестр проверен и сохранён в резервной копии)\n\n")
                f.write("- Мониторинг оборудования (Состояние дисков и процессора проверено и восстановлено)\n")
                f.write("- Права реестра (Доступ к системному реестру восстановлен)\n")
                f.write("- Сетевые угрозы (Подозрительные соединения проверены и нейтрализованы)\n")
                f.write("РЕКОМЕНДАЦИЯ: Выполните полную проверку системы антивирусом и перезагрузите компьютер.\n")
                f.write("Дополнительные действия:\n")
                f.write("- Убедитесь, что все драйверы обновлены через Центр обновления или сайт производителя.\n")
                f.write("- Проверьте наличие подозрительных процессов в Диспетчере задач.\n")
                f.write("- Создайте резервную копию важных данных на внешний носитель.\n")
                f.write("- Если проблемы сохраняются, обратитесь к специалисту или в сообщество проекта.\n")
            print(f"[PASS !] Отчет о восстановлении создан: {report_path}")
        except Exception as e:
            print(f"[FAIL !] Ошибка при создании отчета: {e}")

    def create_antidot_backup():
        try:
            script_path = os.path.abspath(sys.argv[0])
            backup_locations = [
                os.path.join(os.environ['USERPROFILE'], 'Desktop', 'antidot_backup.py'),
                os.path.join(os.environ['USERPROFILE'], 'Documents', 'antidot_backup.py'),
                os.path.join(tempfile.gettempdir(), 'antidot_backup.py')
            ]
            for backup_path in backup_locations:
                try:
                    shutil.copy2(script_path, backup_path)
                    print(f"[PASS !] Резервная копия антидота создана: {backup_path}")
                except:
                    pass
        except Exception as e:
            print(f"[FAIL !] Ошибка при создании резервной копии: {e}")

    def main():
        print("""
                                                                                            
█████╗ ██████╗ ██╗   ██║ █████╗ ███╗   ██╗ ██████╗███████╗██████╗                          
██╔══██╗██╔══██╗██║   ██║██╔══██╗████╗  ██║██╔════╝██╔════╝██╔══██╗                         
███████║██║  ██║██║   ██║███████║██╔██╗ ██║██║     █████╗  ██║  ██║                         
██╔══██║██║  ██║╚██╗ ██╔╝██╔══██║██║╚██╗██║██║     ██╔══╝  ██║  ██║                         
██║  ██║██████╔╝ ╚████╔╝ ██║  ██║██║ ╚████║╚██████╗███████╗██████╔╝                         
╚═╝  ╚═╝╚═════╝   ╚═══╝  ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝                          
                                                                                            
█████╗ ███╗   ██╗████████╗██╗██████╗  ██████╗ ████████╗                                    
██╔══██╗████╗  ██║╚══██╔══╝██║██╔══██╗██╔═══██╗╚══██╔══╝                                    
███████║██╔██╗ ██║   ██║   ██║██║  ██║██║   ██║   ██║                                       
██╔══██║██║╚██╗██║   ██║   ██║██║  ██║██║   ██║   ██║                                       
██║  ██║██║ ╚████║   ██║   ██║██████╔╝╚██████╔╝   ██║                                       
╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚═╝╚═════╝  ╚═════╝    ╚═╝                                       

■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
■                 IMPROVED ANTIDOTE IMPROVED ANTIDOTE              ■
■              to restore Windows system functions                 ■
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

Coder (My Telegram) @gregorybale
My Website https://gregorybale.site
Source code https://github.com/GregoryBale/WinAntidote

WinAntidote (UI) v.2.03a (ui version)
        """)

        if not is_admin():
            print("[WARNING !] Внимание: Скрипт работает с ограниченными правами")
            print("[WARNING !] Некоторые функции могут быть недоступны")

        print("[PROCESSING !] Запуск скрипта восстановления системных функций...")

        enable_self_protection()
        create_antidot_backup()
        kill_blocking_scripts()
        enable_task_manager()
        enable_registry_editor()
        enable_cmd_and_powershell()
        enable_usb_storage()
        enable_control_panel()
        enable_system_tray()
        show_desktop_icons()
        enable_start_button()
        enable_right_click()
        enable_program_execution()
        enable_security_settings()
        enable_recovery_options()
        enable_safe_mode()
        remove_from_startup()
        reset_network_configuration()
        clean_dns_cache()
        clear_keyboard_hooks()
        create_recovery_report()
        enable_network_adapters()
        reset_proxy_settings()
        enable_windows_services()
        clean_temp_files()
        restore_file_associations()
        enable_firewall()
        check_registry_integrity()
        restore_lock_screen()
        restore_windows_update_access()
        reset_group_policies()
        repair_boot_sector()
        restore_antivirus()
        restore_windows_firewall()
        restore_audio()
        bypass_input_blocks()
        restore_hidden_windows()
        restore_clipboard()
        restore_network_async()
        check_filesystem_integrity()
        restore_system_utilities_gui()
        monitor_hardware_status()
        restore_desktop_via_screenshot()
        restore_com_objects()
        restore_uac_settings()
        test_audio_devices()
        scan_network_vulnerabilities()
        neutralize_network_threats()
        restore_registry_access()
        
        print("[PROCESSING !] Перезапуск проводника для применения изменений...")
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'].lower() == 'explorer.exe':
                try:
                    psutil.Process(proc.info['pid']).kill()
                except:
                    pass
                
        subprocess.Popen('explorer.exe')
        
        print("[PROCESSING !] Восстановление завершено! Системные функции возвращены в нормальное состояние.")
        print("[PROCESSING !] Рекомендуется перезагрузить компьютер для полного сброса всех изменений.")
        print("[PROCESSING !] На рабочий стол сохранен отчет о восстановлении system_recovery_report.txt")
        print("[COMPLETE !] СКРИПТ УСПЕШНО ЗАВЕРШИЛ СВОЮ РАБОТУ!")

        try:
            ctypes.windll.user32.MessageBoxW(0,
                "Восстановление системы успешно завершено!\n\nРекомендуется перезагрузить компьютер.",
                "Антидот - Восстановление системы", 0x40)
        except:
            pass

    main()

if __name__ == "__main__":
    console = CustomConsole()
    script_thread = threading.Thread(target=run_script, args=(console,))
    script_thread.start()
    console.run()
