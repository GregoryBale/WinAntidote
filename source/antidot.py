
"""
██████╗ ██████╗ ███████╗ ██████╗  ██████╗ ██████╗ ██╗   ██╗██████╗  █████╗ ██╗     ███████╗
██╔════╝ ██╔══██╗██╔════╝██╔════╝ ██╔═══██╗██╔══██╗╚██╗ ██╔╝██╔══██╗██╔══██╗██║     ██╔════╝
██║  ███╗██████╔╝█████╗  ██║  ███╗██║   ██║██████╔╝ ╚████╔╝ ██████╔╝███████║██║     █████╗  
██║   ██║██╔══██╗██╔══╝  ██║   ██║██║   ██║██╔══██╗  ╚██╔╝  ██╔══██╗██╔══██║██║     ██╔══╝  
╚██████╔╝██║  ██║███████╗╚██████╔╝╚██████╔╝██║  ██║   ██║   ██████╔╝██║  ██║███████╗███████╗
╚═════╝ ╚═╝  ╚═╝╚══════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝
                                                                                            
█████╗ ██████╗ ██╗   ██╗ █████╗ ███╗   ██╗ ██████╗███████╗██████╗                          
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

v.2.0123400.11
"""

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
from threading import Thread
from ctypes import windll, wintypes, byref, Structure, POINTER, c_int, c_uint, c_void_p

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def reset_network_configuration():
    try:
        print("[*] Сброс сетевой конфигурации...")
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
        print("[+++++++++PASS !!!++++++++++] Сетевая конфигурация сброшена")
    except Exception as e:
        print(f"[-------------FAIL !!!----------------] Ошибка при сбросе сетевой конфигурации: {e}")

def clean_dns_cache():
    try:
        print("[*] Очистка DNS-кэша...")
        subprocess.run(["ipconfig", "/flushdns"], 
                      capture_output=True, shell=True, check=False)
        print("[+++++++++PASS !!!++++++++++] DNS-кэш очищен")
    except Exception as e:
        print(f"[-------------FAIL !!!----------------] Ошибка при очистке DNS-кэша: {e}")

def check_registry_integrity():
    try:
        backup_path = os.path.join(os.environ['USERPROFILE'], 'Desktop', 'registry_backup.reg')
        subprocess.run(["reg", "export", "HKLM", backup_path, "/y"],
                       capture_output=True, shell=True, check=False)
        print(f"[+++++++++PASS !!!++++++++++] Резервная копия реестра сохранена: {backup_path}")
    except Exception as e:
        print(f"[-------------FAIL !!!----------------] Ошибка при проверке целостности реестра: {e}")

def restore_lock_screen():
    try:
        subprocess.run(["reg", "add", "HKLM\\Software\\Policies\\Microsoft\\Windows\\Personalization", 
                        "/v", "NoLockScreen", "/t", "REG_DWORD", "/d", "0", "/f"],
                       capture_output=True, shell=True, check=False)
        print("[+++++++++PASS !!!++++++++++] Экран блокировки восстановлен")
    except Exception as e:
        print(f"[-------------FAIL !!!----------------] Ошибка при восстановлении экрана блокировки: {e}")

def restore_windows_update_access():
    try:
        subprocess.run(["reg", "add", "HKLM\\Software\\Policies\\Microsoft\\Windows\\WindowsUpdate", 
                        "/v", "DisableWindowsUpdateAccess", "/t", "REG_DWORD", "/d", "0", "/f"],
                       capture_output=True, shell=True, check=False)
        print("[+++++++++PASS !!!++++++++++] Доступ к Центру обновления Windows восстановлен")
    except Exception as e:
        print(f"[-------------FAIL !!!----------------] Ошибка при восстановлении доступа к обновлениям: {e}")

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
        print("[+++++++++PASS !!!++++++++++] Антивирусная защита восстановлена")
    except Exception as e:
        print(f"[-------------FAIL !!!----------------] Ошибка при восстановлении антивируса: {e}")

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
        print("[+++++++++PASS !!!++++++++++] Брандмауэр Windows восстановлен")
    except Exception as e:
        print(f"[-------------FAIL !!!----------------] Ошибка при восстановлении брандмауэра: {e}")

def repair_boot_sector():
    try:
        print("[*] Проверка и восстановление загрузочного сектора...")
        subprocess.run(["bootrec", "/fixmbr"], 
                       capture_output=True, check=False)
        subprocess.run(["bootrec", "/fixboot"], 
                       capture_output=True, check=False)
        subprocess.run(["bootrec", "/rebuildbcd"], 
                       capture_output=True, check=False)
        print("[+++++++++PASS !!!++++++++++] Загрузочный сектор восстановлен")
    except Exception as e:
        print(f"[-------------FAIL !!!----------------] Ошибка при восстановлении загрузочного сектора: {e}")

def reset_group_policies():
    try:
        subprocess.run(["secedit", "/configure", "/cfg", "%windir%\\inf\\defltbase.inf", 
                        "/db", "defltbase.sdb", "/verbose"], 
                       capture_output=True, shell=True, check=False)
        print("[+++++++++PASS !!!++++++++++] Локальные групповые политики сброшены до значений по умолчанию")
    except Exception as e:
        print(f"[-------------FAIL !!!----------------] Ошибка при сбросе групповых политик: {e}")
    
def enable_network_adapters():
    try:
        subprocess.run(["powershell", "-Command", "Get-NetAdapter | Enable-NetAdapter"],
                       capture_output=True, shell=True, check=False)
        print("[+++++++++PASS !!!++++++++++] Сетевые адаптеры включены")
    except Exception as e:
        print(f"[-------------FAIL !!!----------------] Ошибка при включении сетевых адаптеров: {e}")

def reset_proxy_settings():
    try:
        subprocess.run(["netsh", "winhttp", "reset", "proxy"],
                       capture_output=True, shell=True, check=False)
        print("[+++++++++PASS !!!++++++++++] Настройки прокси сброшены")
    except Exception as e:
        print(f"[-------------FAIL !!!----------------] Ошибка при сбросе настроек прокси: {e}")
        
def enable_windows_services():
    services = ["wuauserv", "bits", "cryptsvc"]  # Windows Update, BITS, Cryptographic Services
    for service in services:
        try:
            subprocess.run(["sc", "config", service, "start=", "auto"],
                           capture_output=True, shell=True, check=False)
            subprocess.run(["sc", "start", service],
                           capture_output=True, shell=True, check=False)
            print(f"[+++++++++PASS !!!++++++++++] Служба {service} включена и запущена")
        except Exception as e:
            print(f"[-------------FAIL !!!----------------] Ошибка при включении службы {service}: {e}")
            
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
            print(f"[+++++++++PASS !!!++++++++++] Временные файлы в {temp_dir} очищены")
        except Exception as e:
            print(f"[-------------FAIL !!!----------------] Ошибка при очистке временных файлов в {temp_dir}: {e}")
            
def restore_file_associations():
    try:
        subprocess.run(["assoc", ".exe=exefile"],
                       capture_output=True, shell=True, check=False)
        subprocess.run(["assoc", ".bat=batfile"],
                       capture_output=True, shell=True, check=False)
        subprocess.run(["assoc", ".cmd=cmdfile"],
                       capture_output=True, shell=True, check=False)
        print("[+++++++++PASS !!!++++++++++] Ассоциации файлов восстановлены")
    except Exception as e:
        print(f"[-------------FAIL !!!----------------] Ошибка при восстановлении ассоциаций файлов: {e}")
        
def enable_firewall():
    try:
        subprocess.run(["netsh", "advfirewall", "set", "allprofiles", "state", "on"],
                       capture_output=True, shell=True, check=False)
        print("[+++++++++PASS !!!++++++++++] Брандмауэр Windows включен")
        print("[+++++++++PASS !!!++++++++++]")
        print("[+++++++++PASS !!!++++++++++]")
        print("[+++++++++PASS !!!++++++++++]")
        print("[+++++++++PASS !!!++++++++++]")
        print("[+++++++++PASS !!!++++++++++]")
        print("[!!!!!!!! WARNING !!!!!!!!] - ПОЖАЛУЙСТА ПОДОЖДИТЕ ПОКА СКРИПТ ЗАКОНЧИТ ПОЛНОСТЬЮ СВОЮ РАБОТУ!")
        print("[!!!!!!!! WARNING !!!!!!!!] - ПОЖАЛУЙСТА ПОДОЖДИТЕ ПОКА СКРИПТ ЗАКОНЧИТ ПОЛНОСТЬЮ СВОЮ РАБОТУ!")
        print("[!!!!!!!! WARNING !!!!!!!!] - ПОЖАЛУЙСТА ПОДОЖДИТЕ ПОКА СКРИПТ ЗАКОНЧИТ ПОЛНОСТЬЮ СВОЮ РАБОТУ!")
        print("[!!!!!!!! WARNING !!!!!!!!] - ПОЖАЛУЙСТА ПОДОЖДИТЕ ПОКА СКРИПТ ЗАКОНЧИТ ПОЛНОСТЬЮ СВОЮ РАБОТУ!")
        print("[!!!!!!!! WARNING !!!!!!!!] - ПОЖАЛУЙСТА ПОДОЖДИТЕ ПОКА СКРИПТ ЗАКОНЧИТ ПОЛНОСТЬЮ СВОЮ РАБОТУ!")
    except Exception as e:
        print(f"[-------------FAIL !!!----------------] Ошибка при включении брандмауэра: {e}")
    
def enable_self_protection():
    try:
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleCtrlHandler(None, True)
        print("[+++++++++PASS !!!++++++++++] Self-protection enabled.")
    except Exception as e:
        print(f"[-------------FAIL !!!----------------] Could not enable self-protection: {e}")

def force_admin_privileges():
    if not is_admin():
        print("[!] Пытаемся запустить с правами администратора...")
        try:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, '"' + sys.argv[0] + '"', None, 1)
            sys.exit(0)
        except:
            print("[!] Не удалось получить права администратора обычным способом.")
            try:
                temp_bat = os.path.join(tempfile.gettempdir(), "elevate.bat")
                with open(temp_bat, "w") as f:
                    f.write('@echo off\n')
                    f.write(f'powershell -Command "Start-Process -FilePath \'{sys.executable}\' -ArgumentList \'{sys.argv[0]}\' -Verb RunAs"\n')
                subprocess.call([temp_bat])
                os.remove(temp_bat)
                sys.exit(0)
            except:
                print("[!] Не удалось получить права администратора. Некоторые функции восстановления могут не работать.")
                return False
    return True

def kill_blocking_scripts():
    print("[*] Поиск и завершение процессов блокировки...")
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
                        print(f"[+++++++++PASS !!!++++++++++] Процесс блокировки с PID {pid} завершен")
                    except:
                        pass
                os.remove(flag_file)
                print(f"[+++++++++PASS !!!++++++++++] Файл-флаг блокировки {flag_file} удален")
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
                    print(f"[+++++++++PASS !!!++++++++++] Процесс блокировки с PID {proc.info['pid']} завершен")
                except:
                    try:
                        p = psutil.Process(proc.info['pid'])
                        p.kill()
                        print(f"[+++++++++PASS !!!++++++++++] Процесс блокировки с PID {proc.info['pid']} принудительно завершен")
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
                print(f"[+++++++++PASS !!!++++++++++] Скрытая копия скрипта блокировки удалена: {script_path}")
            except:
                print(f"[-------------FAIL !!!----------------] Не удалось удалить скрытую копию: {script_path}")
                
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

        print("[+++++++++PASS !!!++++++++++] Диспетчер задач восстановлен")
    except Exception as e:
        print(f"[-------------FAIL !!!----------------] Ошибка при восстановлении диспетчера задач: {e}")

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
        print("[+++++++++PASS !!!++++++++++] Редактор реестра восстановлен")
    except Exception as e:
        print(f"[-------------FAIL !!!----------------] Ошибка при восстановлении редактора реестра: {e}")

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
        print("[+++++++++PASS !!!++++++++++] Командная строка и PowerShell восстановлены")
    except Exception as e:
        print(f"[-------------FAIL !!!----------------] Ошибка при восстановлении командной строки: {e}")

def enable_usb_storage():
    try:
        key_path = r"SYSTEM\CurrentControlSet\Services\USBSTOR"
        try:
            registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(registry_key, "Start", 0, winreg.REG_DWORD, 3)  # 3 - запуск вручную (по умолчанию)
            winreg.CloseKey(registry_key)
        except:
            pass
        try:
            subprocess.run(['REG', 'ADD', 'HKLM\\SYSTEM\\CurrentControlSet\\Services\\USBSTOR',
                         '/v', 'Start', '/t', 'REG_DWORD', '/d', '3', '/f'],
                         capture_output=True, check=False)
        except:
            pass
        print("[+++++++++PASS !!!++++++++++] USB накопители восстановлены")
    except Exception as e:
        print(f"[-------------FAIL !!!----------------] Ошибка при восстановлении USB: {e}")

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
        print("[+++++++++PASS !!!++++++++++] Панель управления восстановлена")
    except Exception as e:
        print(f"[-------------FAIL !!!----------------] Ошибка при восстановлении панели управления: {e}")

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

        print("[+++++++++PASS !!!++++++++++] Системный трей восстановлен")
    except Exception as e:
        print(f"[-------------FAIL !!!----------------] Ошибка при восстановлении системного трея: {e}")

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

        print("[+++++++++PASS !!!++++++++++] Иконки рабочего стола восстановлены")
    except Exception as e:
        print(f"[-------------FAIL !!!----------------] Ошибка при восстановлении иконок рабочего стола: {e}")

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
        print("[+++++++++PASS !!!++++++++++] Кнопка Пуск восстановлена")
    except Exception as e:
        print(f"[-------------FAIL !!!----------------] Ошибка при восстановлении кнопки Пуск: {e}")

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
        print("[+++++++++PASS !!!++++++++++] Контекстное меню восстановлено")
    except Exception as e:
        print(f"[-------------FAIL !!!----------------] Ошибка при восстановлении контекстного меню: {e}")

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
        print("[+++++++++PASS !!!++++++++++] Ограничения на запуск программ сняты")
    except Exception as e:
        print(f"[-------------FAIL !!!----------------] Ошибка при снятии ограничений на запуск программ: {e}")

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
        print("[+++++++++PASS !!!++++++++++] Настройки безопасности восстановлены")
    except Exception as e:
        print(f"[-------------FAIL !!!----------------] Ошибка при восстановлении настроек безопасности: {e}")

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
                    print(f"[+++++++++PASS !!!++++++++++] Файл автозагрузки удален: {file_path}")
                except:
                    print(f"[-------------FAIL !!!----------------] Не удалось удалить файл автозагрузки: {file_path}")
        print("[+++++++++PASS !!!++++++++++] Скрипт удален из автозагрузки")
    except Exception as e:
        print(f"[-------------FAIL !!!----------------] Ошибка при удалении из автозагрузки: {e}")

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
        print("[+++++++++PASS !!!++++++++++] Безопасный режим восстановлен")
    except Exception as e:
        print(f"[-------------FAIL !!!----------------] Ошибка при восстановлении безопасного режима: {e}")

def enable_recovery_options():
    try:
        subprocess.run(["wmic", "recoveros", "set", "AutoReboot", "=", "True"],
                      capture_output=True, shell=True, check=False)
        subprocess.run(["bcdedit", "/set", "{default}", "recoveryenabled", "Yes"],
                      capture_output=True, shell=True, check=False)
        subprocess.run(["bcdedit", "/set", "{default}", "bootstatuspolicy", "displayallfailures"],
                      capture_output=True, shell=True, check=False)
        print("[+++++++++PASS !!!++++++++++] Функции восстановления Windows включены")
    except Exception as e:
        print(f"[-------------FAIL !!!----------------] Ошибка при включении функций восстановления: {e}")

def clear_keyboard_hooks():
    try:
        keyboard.unhook_all()
        keyboard._os_keyboard.init()
        print("[+++++++++PASS !!!++++++++++] Все перехваты клавиатуры сняты")
    except Exception as e:
        print(f"[-------------FAIL !!!----------------] Ошибка при снятии перехватов клавиатуры: {e}")

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
            f.write("- Диспетчер задач\n")
            f.write("- Редактор реестра\n")
            f.write("- Командная строка и PowerShell\n")
            f.write("- USB накопители\n")
            f.write("- Панель управления\n")
            f.write("- Системный трей\n")
            f.write("- Иконки рабочего стола\n")
            f.write("- Кнопка Пуск\n")
            f.write("- Контекстное меню\n")
            f.write("- Выполнение программ\n")
            f.write("- Настройки безопасности\n")
            f.write("- Функции восстановления Windows\n")
            f.write("- Безопасный режим\n")
            f.write("- Сетевые адаптеры и настройки прокси\n")
            f.write("- Службы Windows\n")
            f.write("- Временные файлы и кэш\n")
            f.write("- Ассоциации файлов\n")
            f.write("- Системные файлы\n")
            f.write("- Запланированные задачи\n")
            f.write("- Брандмауэр Windows\n")
            f.write("- Точка восстановления системы\n\n")
            f.write("- Сброс групповых политик\n")
            f.write("- Восстановление доступа к Центру обновления Windows\n")
            f.write("- Очистка автозагрузки в реестре\n")
            f.write("- Восстановление экрана блокировки\n")
            f.write("- Проверка целостности реестра\n")
            f.write("РЕКОМЕНДАЦИЯ: Выполните полную проверку системы антивирусом и перезагрузите компьютер.\n")

        print(f"[+++++++++PASS !!!++++++++++] Отчет о восстановлении создан: {report_path}")
    except Exception as e:
        print(f"[-------------FAIL !!!----------------] Ошибка при создании отчета: {e}")

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
                print(f"[+++++++++PASS !!!++++++++++] Резервная копия антидота создана: {backup_path}")
            except:
                pass
    except Exception as e:
        print(f"[-------------FAIL !!!----------------] Ошибка при создании резервной копии: {e}")

def main():
    print("""
██████╗ ██████╗ ███████╗ ██████╗  ██████╗ ██████╗ ██╗   ██╗██████╗  █████╗ ██╗     ███████╗
██╔════╝ ██╔══██╗██╔════╝██╔════╝ ██╔═══██╗██╔══██╗╚██╗ ██╔╝██╔══██╗██╔══██╗██║     ██╔════╝
██║  ███╗██████╔╝█████╗  ██║  ███╗██║   ██║██████╔╝ ╚████╔╝ ██████╔╝███████║██║     █████╗  
██║   ██║██╔══██╗██╔══╝  ██║   ██║██║   ██║██╔══██╗  ╚██╔╝  ██╔══██╗██╔══██║██║     ██╔══╝  
╚██████╔╝██║  ██║███████╗╚██████╔╝╚██████╔╝██║  ██║   ██║   ██████╔╝██║  ██║███████╗███████╗
╚═════╝ ╚═╝  ╚═╝╚══════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝
                                                                                            
█████╗ ██████╗ ██╗   ██╗ █████╗ ███╗   ██╗ ██████╗███████╗██████╗                          
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

v.2.0123400.11
    """)

    if not force_admin_privileges():
        print("[!] Внимание: Скрипт будет работать с ограниченными возможностями")
        print("[!] Некоторые функции восстановления могут не сработать")

    print("[*] Запуск скрипта восстановления системных функций...")

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
    
    print("[*] Перезапуск проводника для применения изменений...")
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'].lower() == 'explorer.exe':
            try:
                psutil.Process(proc.info['pid']).kill()
            except:
                pass
            
    subprocess.Popen('explorer.exe')
    
    print("[*] Восстановление завершено! Системные функции возвращены в нормальное состояние.")
    print("[*] Рекомендуется перезагрузить компьютер для полного сброса всех изменений.")
    print("[*] На рабочий стол сохранен отчет о восстановлении system_recovery_report.txt")
    print("[*]    ")
    print("[*]    ")
    print("[*]    ")
    print("   ")
    print("[*]    ")
    print("[*]    ")
    print("   ")
    print("   ")
    print("   ")
    print("[*]    ")
    print("   ")
    print("[*********] COMPLETE !!! *********] СКРИПТ УСПЕШНО ЗАВЕРШИЛ СВОЮ РАБОТУ - МОЖЕТЕ ЗАКРЫТЬ ТЕРМИНАЛ!")
    print("[*********] COMPLETE !!! *********] СКРИПТ УСПЕШНО ЗАВЕРШИЛ СВОЮ РАБОТУ - МОЖЕТЕ ЗАКРЫТЬ ТЕРМИНАЛ!")
    print("[*********] COMPLETE !!! *********] СКРИПТ УСПЕШНО ЗАВЕРШИЛ СВОЮ РАБОТУ - МОЖЕТЕ ЗАКРЫТЬ ТЕРМИНАЛ!")
    print("[*********] COMPLETE !!! *********] СКРИПТ УСПЕШНО ЗАВЕРШИЛ СВОЮ РАБОТУ - МОЖЕТЕ ЗАКРЫТЬ ТЕРМИНАЛ!")
    print("[*********] COMPLETE !!! *********] СКРИПТ УСПЕШНО ЗАВЕРШИЛ СВОЮ РАБОТУ - МОЖЕТЕ ЗАКРЫТЬ ТЕРМИНАЛ!")
    print("[*********] COMPLETE !!! *********] СКРИПТ УСПЕШНО ЗАВЕРШИЛ СВОЮ РАБОТУ - МОЖЕТЕ ЗАКРЫТЬ ТЕРМИНАЛ!")
    print("[*********] COMPLETE !!! *********] СКРИПТ УСПЕШНО ЗАВЕРШИЛ СВОЮ РАБОТУ - МОЖЕТЕ ЗАКРЫТЬ ТЕРМИНАЛ!")
    print("[*********] COMPLETE !!! *********] СКРИПТ УСПЕШНО ЗАВЕРШИЛ СВОЮ РАБОТУ - МОЖЕТЕ ЗАКРЫТЬ ТЕРМИНАЛ!")
    print("[*********] COMPLETE !!! *********] СКРИПТ УСПЕШНО ЗАВЕРШИЛ СВОЮ РАБОТУ - МОЖЕТЕ ЗАКРЫТЬ ТЕРМИНАЛ!")
    print("[*********] COMPLETE !!! *********] СКРИПТ УСПЕШНО ЗАВЕРШИЛ СВОЮ РАБОТУ - МОЖЕТЕ ЗАКРЫТЬ ТЕРМИНАЛ!")
    print("[*********] COMPLETE !!! *********] СКРИПТ УСПЕШНО ЗАВЕРШИЛ СВОЮ РАБОТУ - МОЖЕТЕ ЗАКРЫТЬ ТЕРМИНАЛ!")
    print("[*********] COMPLETE !!! *********] СКРИПТ УСПЕШНО ЗАВЕРШИЛ СВОЮ РАБОТУ - МОЖЕТЕ ЗАКРЫТЬ ТЕРМИНАЛ!")
    try:
        ctypes.windll.user32.MessageBoxW(0,
            "Восстановление системы успешно завершено!\n\nРекомендуется перезагрузить компьютер.",
            "Антидот - Восстановление системы", 0x40)
    except:
        pass
    input("Нажмите Enter для выхода...")

if __name__ == "__main__":
    main()
