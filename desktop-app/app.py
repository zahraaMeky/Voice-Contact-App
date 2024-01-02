import sqlite3
from kivy.uix.label import Label
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.card import MDCard
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from audio import AudioSender, AudioReceiver, ClientConnection
from kivy.core.window import Window
from kivy.uix.image import Image
from kivymd.uix.button import MDIconButton
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivymd.uix.button import MDFillRoundFlatButton,MDRaisedButton
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.uix.gridlayout import GridLayout
import arabic_reshaper
from bidi.algorithm import get_display
from kivy.properties import NumericProperty, StringProperty
from kivy.resources import resource_add_path
import threading
import nmap
from time import sleep
from kivymd.uix.spinner import MDSpinner
from re import findall
from subprocess import Popen, PIPE
from win32api import GetSystemMetrics
from kivymd.icon_definitions import md_icons
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.textfield import MDTextField
from kivy.uix.dropdown import DropDown
import os
import sys
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64
from os import getcwd
import sqlite3
import gzip

class ManageScreen(ScreenManager):
    pass

class LoginScreen(Screen):
    pass


class Client:
    def __init__(self, ip):      
        self.is_connected = False
        self.sender: AudioSender = None
        self.receiver: AudioReceiver = None
        # print('type(ip)',type(ip))

        self.HOST = ip
        self.PORT = 9999
        self.is_connected = False
        

    # def check(self,dt):
    #     if(self.sender):
    #         # print("connected : " , self.sender.connected)
    #         if (self.sender.connected):
    #             print('1')
    #         else:
    #             print('0')
    
        
    def connect(self):
        print("connect => " , self.is_connected)
        if self.is_connected:
            if self.sender:
                self.sender.stop_stream()
                self.send = None
            if self.receiver:
                self.receiver.stop_server()
                self.receiver = None
                
            return

        self.sender = AudioSender(self.HOST, self.PORT)  
        self.is_connected = True
        
    def run_stream(self):
        if (self.sender): 
            self.sender.start_stream()
        
    
    def stop_stream(self):
        if (self.sender): 
            print("stopppp streaming")
            self.sender.stop_stream()

class UserScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.call_all_added = False  


    def on_enter(self):
        self.fetch_and_display_data()
        # Clock.schedule_interval(self.check_Status,20)
        self.status_thread = threading.Thread(target=self.check_Status, daemon=True)
        self.status_thread.start()
        
    def RefreshNetwork(self,button_instance):
        # print("Refresh Network ...................")
        app = VoiceContactApp.get_running_app()
        threading.Thread(target=app.ADDScandes,daemon=True).start()  
        self.fetch_and_display_data()
        
    def fetch_and_display_data(self):
        app = VoiceContactApp.get_running_app()
        db_connection = app.open_cdb(app.dbname)
        db_cursor = db_connection.cursor()
        # conn = sqlite3.connect('voiceContact.db')
        # cursor = conn.cursor()
        db_cursor.execute('SELECT name,ip,description FROM rooms')
        rows = db_cursor.fetchall()
        db_connection.commit()

        layout = self.ids.user_rooms_layout
        Hlayout = self.ids.btns_Hulayout
        layout.clear_widgets()
                
        self.cnt_btns = []
        self.st_lbls = []
        self.st_IMG = []
        self.st_bluth =[]
        i = 0
        app = VoiceContactApp.get_running_app()
        if not self.call_all_added:
            self.call_all = CallAll()
            refresh_net = AddRoomButton(text="تحديث الشبكة")
            self.call_all.st = 0
            Hlayout.add_widget(refresh_net)
            Hlayout.add_widget(self.call_all)

            self.call_all.bind(on_press=self.callAllfunc)
            refresh_net.bind(on_press=self.RefreshNetwork)
            self.call_all_added = True

        for row in rows:
            card = CustomCard()  
            card.update_size(400,470)          
            room_name = row[0]
            room_ip = row[1]
            room_desc = row[2]
            ip_label = Label(text=app.arabicText(room_ip), color=(0.909, 0.667, 0.259, 1))
            card.add_widget(ip_label)
            name_label = Label(text=app.arabicText(room_name) ,halign='right'  , color=(0.909, 0.667, 0.259, 1),font_size="16sp", font_name='resources/JannaLTBold.ttf')
            card.add_widget(name_label)
            desc_label = Label(text=app.arabicText(room_desc),text_size=(200,None), size_hint_y=None,valign='top',halign='right',color=(242 / 255, 194 / 255, 114 / 255, 1),font_size="14sp", font_name='resources/JannaLTBold.ttf')
            card.add_widget(desc_label)
            status_image = Image(source="resources/waveMute.png",size_hint=(None, None),size=(400,150))
            status_image.i=i
            status_image.ip=f'{room_ip}'
            self.st_IMG.append(status_image)
            connect_button = ConnectButton()
            connect_button.room_ip = f'{room_ip}'  # Assign a custom property
            connect_button.room_name = f'{room_name}'  # Assign a custom property
            connect_button.i = i
            connect_button.st = 0
            connect_button.ip = room_ip
            self.cnt_btns.append(connect_button)
            connect_button.bind(on_press=self.connect_room)
            card.add_widget(status_image)
            card.add_widget(connect_button)
            btn_layout =  BoxLayout()
            card.add_widget(btn_layout)
            speaker, connected = ClientConnection(room_ip, 7777).check()
            # print('checkStatus',speaker,connected)
            status_layout = StatusLayout()
            if connected:
                status_conn = ConnectionStatusButton(icon="access-point-network")
                status_conn.text_color =  (10 / 255, 16 / 255, 37 / 255, 1) 
            else:
                status_conn = ConnectionStatusButton(icon="access-point-network-off")
                status_conn.text_color = (183, 183, 183)
            status_conn.i = i
            status_conn.ip = room_ip
            self.st_lbls.append(status_conn)
            status_layout.add_widget(status_conn)
            if speaker:
                status_blutooth = ConnectionStatusButton(icon="headphones")
                status_blutooth.text_color =  (10 / 255, 16 / 255, 37 / 255, 1) 
            else:
                status_blutooth = ConnectionStatusButton(icon="headphones-off")
                status_blutooth.text_color = (183, 183, 183)
            status_blutooth.i = i
            status_blutooth.ip = room_ip
            self.st_bluth.append(status_blutooth)
            status_layout.add_widget(status_blutooth)
            card.add_widget(status_layout)
            layout.add_widget(card)
            i += 1

        db_cursor.close()
        # Clock.schedule_interval(self.check_Status,5)
        

        
    def check_Status(self):
        while True:
            try:
                for room in self.st_lbls:
                    # print(room.ip)
                    speaker, connected = ClientConnection(room.ip, 7777).check()
                    # print('speaker', speaker,'connected',connected,"=====================")
                    connect_status = self.st_lbls[room.i]
                    bluetooth_status =self.st_bluth[room.i]
                    if connected:
                        connect_status.icon ="access-point-network"
                        connect_status.text_color =  (10 / 255, 16 / 255, 37 / 255, 1) 
                    
                    else:
                        connect_status.icon ="access-point-network-off"
                        connect_status.text_color = (183, 183, 183)
                        
                    if speaker:
                        bluetooth_status.icon ="headphones"
                        bluetooth_status.text_color =  (10 / 255, 16 / 255, 37 / 255, 1) 
                    else:
                        bluetooth_status.icon ="headphones-off"
                        bluetooth_status.text_color = (183, 183, 183)
            
                # is_connected = self.client.sender.connected
                # print('is_connected',is_connected,'connected',connected)

                # if  is_connected:
                #     self.st_IMG[self.i].source="resources/wave2.gif"
                # else:
                #     self.st_IMG[self.i].source="resources/waveMute.png"
            except Exception as e:
                print("check Exception : ", e)
            sleep(5)

    
    def check_Status2(self,dt):
        for room in self.st_lbls:
            # print(room.ip)
            speaker, connected = ClientConnection(room.ip, 7777).check()
            # print('speaker', speaker,'connected',connected,"=====================")
            connect_status = self.st_lbls[room.i]
            bluetooth_status =self.st_bluth[room.i]
            if connected:
                connect_status.icon ="access-point-network"
                connect_status.text_color =  (10 / 255, 16 / 255, 37 / 255, 1) 
              
            else:
                connect_status.icon ="access-point-network-off"
                connect_status.text_color = (183, 183, 183)
                
            if speaker:
                bluetooth_status.icon ="headphones"
                bluetooth_status.text_color =  (10 / 255, 16 / 255, 37 / 255, 1) 
            else:
                bluetooth_status.icon ="headphones-off"
                bluetooth_status.text_color = (183, 183, 183)

    
    def connect_room(self,instance):
        app = VoiceContactApp.get_running_app()
        self.i  =  instance.i
        self.ip = instance.room_ip
        connect_button = self.cnt_btns[self.i]
        status_image = self.st_IMG[self.i]
        speaker,connected = ClientConnection(self.ip , 7777).check()
        # print(speaker , "   " , connected)
        if connect_button.st == 1:
            self.cnt_btns[self.i].st = 0
            connect_button.text =app.arabicText("إتصال بالغرفة")
            connect_button.md_bg_color =  (242 / 255, 194 / 255, 114 / 255, 1)
            self.client.stop_stream()
            Clock.schedule_once(self.StopStream,3)
            # Clock.schedule_interval(self.check_Status,2)
        else:
            if speaker and connected:
                self.cnt_btns[self.i].st = 1
                connect_button.text =app.arabicText("قطع الإتصال")
                # connect_button.md_bg_color =  (210/255, 141/255, 26/255, 1)
                connect_button.md_bg_color =  (236/255, 112/255, 99/255, 1)
                self.client = Client(ip=self.ip) 
                self.client.connect()
                Clock.schedule_once(self.runStream,2)
                Clock.schedule_once(self.runSound,3)
                Clock.schedule_interval(self.check,1)

            elif connected == False:
                message = app.arabicText('الجهاز غير متصل')
                popup = userAlert(message)
                popup.open()

            elif speaker == False:
                message = app.arabicText('السماعة غير متصلة')
                popup = userAlert(message)
                popup.open()
       
            
   
    def runStream(self,dt):
        self.client.run_stream()
        
    def runSound(self,dt):
        is_connected = self.client.sender.connected
        if is_connected:
            sound = SoundLoader.load('resources/sound.wav')
            if sound:
                # print("Sound play")
                sound.play()    
                
    def StopStream(self,dt):
        self.client.stop_stream()
        Clock.unschedule(self.check)
        
    def uncheckAll2Connect(self,dt):
        Clock.unschedule(self.checkAll2Connect)
                  
    def check(self,dt):
        speaker,connected = ClientConnection(self.ip, 7777).check()
        is_connected = self.client.sender.connected
        if  is_connected:
            self.st_IMG[self.i].source='resources/wave2.gif'
        else:
            self.st_IMG[self.i].source="resources/waveMute.png"

            
    def check2(self,dt):
        app = VoiceContactApp.get_running_app()
        connect_button = self.cnt_btns[self.i]
        status_label = self.st_lbls[self.i]
        status_Img = self.st_IMG [self.i]
        speaker,connected = ClientConnection(self.ip, 7777).check()
        is_connected = self.client.sender.connected
        # print('is_connected',is_connected,'connected',connected)

        if  is_connected:
            self.st_IMG[self.i].source="resources/wave2.gif"
        else:
            self.st_IMG[self.i].source="resources/waveMute.png"


    def callAllfunc(self,instance):
        # print('instance.st  from callAllfunc',instance.st)
        app = VoiceContactApp.get_running_app()
        if instance.st == 0 :
            instance.st = 1
            # print('instance.st ',instance.st )
            
            self.connected_rooms = []
            self.connected_clients = []
            # conn = sqlite3.connect('voiceContact.db')
            db_connection = app.open_cdb(app.dbname)
            db_cursor = db_connection.cursor()
            # cursor = conn.cursor()
            db_cursor.execute('SELECT ip FROM rooms')
            rows = db_cursor.fetchall()
            for i, row in enumerate(rows):
                ip_address = row[0]
                # print(f"Index: {i}, IP Address: {ip_address}")
                speaker,connected = ClientConnection(ip_address , 7777).check()
                if speaker and connected:
                    self.connected_rooms.append(ip_address)
            print("connected_rooms",self.connected_rooms)
            
            db_cursor.close()
            # conn.close()
            # app.db_connection.close()
            
            for ip_address in self.connected_rooms:
                client = Client(ip=ip_address)
                client.connect()
                client.run_stream()
                self.connected_clients.append(client)

            if (len(self.connected_rooms)>0):
                instance.text = app.arabicText('قطع الإتصال بالكل')
                # instance.md_bg_color =  (236/255, 112/255, 99/255, 1)
                Clock.schedule_once(self.play,2)
                # Clock.unschedule(self.check_Status)
                Clock.schedule_interval(self.checkAll2Connect,5)
            else:
                print("no client")
                instance.st = 0
                instance.text = app.arabicText('الإتصال بالكل')
                # instance.md_bg_color =  (242 / 255, 194 / 255, 114 / 255, 1)
                # Clock.schedule_once(self.stop_stream_all_rooms,1)
                Clock.schedule_once(self.uncheckAll2Connect,2)

        else:
            print("close all")
            instance.st = 0
            instance.text = app.arabicText('الإتصال بالكل')
            # instance.md_bg_color =  (242 / 255, 194 / 255, 114 / 255, 1)
            Clock.schedule_once(self.stop_stream_all_rooms,1)
            Clock.schedule_once(self.uncheckAll2Connect,2)
            # Clock.schedule_interval(self.check_Status,20)
                
    def stop_stream_all_rooms(self,dt):
        for client in self.connected_clients:
            client.stop_stream()
            
    def play(self,dt) :  
        Clock.schedule_once(self.Sound4All,1)

        
    def Sound4All(self,dt):
        count = 0 
        for client in self.connected_clients:
            is_connected = client.sender.connected
            if is_connected:
                count += 1 
            # print(" is_connected:", is_connected,"count", count, 'len(self.connected_clients)', len(self.connected_clients))

        # Now you can access the updated count outside the loop
        if count == len(self.connected_clients):
            sound = SoundLoader.load('resources/sound.wav')
            if sound:
                # print("Sound play")
                sound.play()

                    
    def checkAll2Connect(self,instance):
        print("checkAll2Connect")
        app = VoiceContactApp.get_running_app()
        live = False
        for client in self.connected_clients:
            is_connected = client.sender.connected
            client_ip = client.HOST
            if is_connected:
                live = True
                for status_image in self.st_IMG:
                    ip_address = status_image.ip
                    index =  status_image.i
                    if  ip_address ==client_ip:
                        img = self.st_IMG[index]
                        btn = self.cnt_btns[index]
                        img.source="resources/wave2.gif"
                        btn.text =app.arabicText('قطع الإنصال')
                        btn.md_bg_color =  (236/255, 112/255, 99/255, 1)

            else:
                    for status_image in self.st_IMG:
                        ip_address = status_image.ip
                        index =  status_image.i
                        if  ip_address ==client_ip:
                            img = self.st_IMG[index]
                            btn = self.cnt_btns[index]
                            # print('from else',is_connected)
                            img.source="resources/waveMute.png"
                            btn.text =app.arabicText('الإتصال بالغرفة')
                            btn.md_bg_color =  (242 / 255, 194 / 255, 114 / 255, 1)
        
        if not live:
            # instance.st = 0
            print("no live")
            self.call_all.text = app.arabicText('الإتصال بالكل')
            # Clock.schedule_once(self.stop_stream_all_rooms,1)
            Clock.schedule_once(self.uncheckAll2Connect,1)

                
    def uncheckAll2Connect(self,dt):
        app = VoiceContactApp.get_running_app()
        for ip_address in self.connected_rooms:
            client = Client(ip=ip_address)
            client.stop_stream()
            for status_image in self.st_IMG:
                        ip_address = status_image.ip
                        index =  status_image.i
                        if  ip_address ==ip_address:
                            img = self.st_IMG[index]
                            btn = self.cnt_btns[index]
                            # print('from else',is_connected)
                            img.source="resources/waveMute.png"
                            btn.text =app.arabicText('الإتصال بالغرفة')
                            btn.md_bg_color =  (242 / 255, 194 / 255, 114 / 255, 1)
        Clock.unschedule(self.checkAll2Connect)

class UserControlScreen(Screen):
    def __init__(self, **kwargs):
        super(UserControlScreen, self).__init__(**kwargs)
        self.uRole = None
        self.btn_added = False
        
    def on_enter(self):
        self.fetch_and_display_users()

    def convertRole(self,selected_role):
        app = VoiceContactApp.get_running_app()
        selected_role = selected_role.strip()
        print("Selected Role:", selected_role)  
        if selected_role == app.arabicText("مسئول"):
            print('مسئول')
            self.uRole = 1
        if selected_role == app.arabicText("مستخدم"):
            print('مستخدم')
            self.uRole = 0
        print("uRole after conversion:", self.uRole)  
         
    
    def fetch_and_display_users(self):
        # print("Fetch data from class")
        app = VoiceContactApp.get_running_app()
        db_connection = app.open_cdb(app.dbname)
        db_cursor = db_connection.cursor()
        # conn = sqlite3.connect('voiceContact.db')
        # cursor = conn.cursor()
        db_cursor.execute('SELECT username,role,id FROM users')
        rows = db_cursor.fetchall()
        db_connection.commit()

        layout = self.ids.users_layout

        Hlayout = self.ids.userbtns_Hlayout
        layout.clear_widgets()
    
        app = VoiceContactApp.get_running_app()
        if not self.btn_added:
            addUsers = AddRoomButton(text="إضافة مستخدم")
            backScreen = AddRoomButton(text="رجوع للخلف")
            Hlayout.add_widget(addUsers)
            Hlayout.add_widget(backScreen)

            addUsers.bind(on_press=self.add_user)
            backScreen.bind(on_press=self.ReturnBack)
            self.btn_added = True

        print("users: " , rows)
        for row in rows:
            card = CustomCard() 
            card.update_size(300,200)           
            user_name = row[0]
            user_role = row[1]
            user_id = row[2]
            user_namelb = Label(text=app.arabicText(user_name), color=(0.909, 0.667, 0.259, 1))
            card.add_widget(user_namelb)
            if user_role == 1:
                user_rolelb = Label(text=app.arabicText("مسئول") ,color=(0.909, 0.667, 0.259, 1),font_size="16sp", font_name='resources/JannaLTBold.ttf')
            if user_role == 0:
                user_rolelb = Label(text=app.arabicText("مستخدم"),color=(0.909, 0.667, 0.259, 1),font_size="16sp", font_name='resources/JannaLTBold.ttf')
            card.add_widget(user_rolelb)
          
            btn_layout =  GridLayout(cols=1,spacing=180)
            delete_button = Button(text=app.arabicText('حذف'))
            delete_button.background_normal=''
            delete_button.color = (10 / 255, 16 / 255, 37 / 255, 1)
            delete_button.background_color =(210 / 255, 141 / 255, 26 / 255, 1)
            delete_button.font_name='resources/JannaLTBold.ttf'
            delete_button.font_size='16sp'
            delete_button.user_id = user_id
            delete_button.user_name = user_name
            # delete_button.bind(on_press=lambda instance:self.set_flag(room_name))
            delete_button.bind(on_press=self.set_flag)
            btn_layout.add_widget(delete_button)
            # edit_button = EditButton()
            # edit_button.user_id = user_id
            # edit_button.user_name = user_name
            # # edit_button.bind(on_press=self.edit_room)
            # btn_layout.add_widget(edit_button)
            card.add_widget(btn_layout)
            layout.add_widget(card)
        
        db_cursor.close()
        
      
    def set_flag(self, instance):
        self.flag = 1
        app = VoiceContactApp.get_running_app()
        self.confirmpopup = Popup(title=app.arabicText('تأكيد الحذف'), size_hint=(0.5, 0.5))
        user_id = instance.user_id
        user_name = instance.user_name
        # print("request to remove room :" , room_ip)
        # app = VoiceContactApp.get_running_app()
        popup_content_confirm = boxColor()
        layout = BoxLayout(orientation='vertical')
        save_button = Button(text=app.arabicText('نعم'), on_press=self.delete_room(user_id))
        save_button.background_normal=''
        save_button.background_color = (210 / 255, 141 / 255, 26 / 255, 1)
        save_button.color = (10 / 255, 16 / 255, 37 / 255, 1) 
        save_button.font_name='resources/JannaLTBold.ttf'
        save_button.font_size='16sp'
        close_button = Button(text=app.arabicText('إغلاق'), on_press=self.confirmpopup.dismiss)
        close_button.background_normal=''
        close_button.background_color = (10 / 255, 16 / 255, 37 / 255, 1) 
        close_button.color = (210 / 255, 141 / 255, 26 / 255, 1)
        close_button.font_name='resources/JannaLTBold.ttf'
        close_button.font_size='16sp'
        popup_content_confirm.add_widget(Label(text=app.arabicText(' هل أنت متأكد من حذف ' + str(user_name) + "؟"), color=(210 / 255, 141 / 255, 26 / 255, 1), font_size="16sp", font_name='resources/JannaLTBold.ttf'))
        layout.add_widget(save_button)
        layout.add_widget(close_button)
        popup_content_confirm.add_widget(layout)
        # self.confirmpopup = Popup(title=app.arabicText('تأكيد الحذف'), content=popup_content_confirm, size_hint=(0.5, 0.5))
        self.confirmpopup.content = popup_content_confirm
        self.confirmpopup.title_color =  (210 / 255, 141 / 255, 26 / 255, 1)
        self.confirmpopup.title_font = "resources/JannaLTBold.ttf"
        self.confirmpopup.open()
        
    def delete_room(self, user_id):
        def delete_room_button(instance):
            self.confirmpopup.dismiss() 
            app = VoiceContactApp.get_running_app()
            db_connection = app.open_cdb(app.dbname)
            db_cursor = db_connection.cursor()
            # print("from delete",room_ip)
            # cursor = conn.cursor()
            db_cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
            db_connection.commit()
            rows_affected = db_cursor.rowcount
            if rows_affected > 0:
                # print('rows_affected',rows_affected)
                app.save_cdb(db_connection,app.dbname)
                popup_content = boxColor()
                popup_content.add_widget(Label(text=app.arabicText('تم الحذف بنجاح'),color=(210 / 255, 141 / 255, 26 / 255, 1),font_size="16sp", font_name='resources/JannaLTBold.ttf'))
                self.sucesspopup = Popup(title=app.arabicText('حالة الحذف'), content=popup_content, size_hint=(0.5, 0.5))
                self.sucesspopup.title_color =  (210 / 255, 141 / 255, 26 / 255, 1)
                self.sucesspopup.title_font = "resources/JannaLTBold.ttf"
                self.sucesspopup.open()
                Clock.schedule_once(self.dismiss_popup,0.2)
            db_cursor.close()


        return delete_room_button
   
    def dismiss_popup(self,dt):
        self.sucesspopup.dismiss() 
        self.fetch_and_display_users() 
    
    def add_user(self,instance):
        app = VoiceContactApp.get_running_app()
        popup_content = boxColor()
        room_name_input = Ar_text(maxchar=100, multiline=False,background_color=(69/255, 69/255, 69/255,1),
                        foreground_color=(210 / 255, 141 / 255, 26 / 255, 1),font_size="16sp",font_name='resources/JannaLTBold.ttf' )
        userpassword_input = Ar_text(maxchar=20, multiline=False,background_color=(69/255, 69/255, 69/255,1),foreground_color=(210 / 255, 141 / 255, 26 / 255, 1),font_size="16sp", font_name='resources/JannaLTBold.ttf')
        userRole_input = Button(text=app.arabicText('النوع'),font_size="16sp",font_name='resources/JannaLTBold.ttf',color=(210 / 255, 141 / 255, 26 / 255, 1) )
        user_role_dropdown = DropDown()
        role1=app.arabicText("مسئول")
        role2=app.arabicText("مستخدم")
        for role in [role1, role2]:
            role_button = Button(text=role, size_hint_y=None, height=44,font_size="16sp", font_name='resources/JannaLTBold.ttf', color=(210 / 255, 141 / 255, 26 / 255, 1))
            role_button.bind(on_release=lambda btn, role=role: user_role_dropdown.select(role))  
            user_role_dropdown.add_widget(role_button)

        def userRole_input_set_role(selected_role):
            userRole_input.text = selected_role
            self.convertRole(selected_role)
            user_role_dropdown.dismiss()
           

        userRole_input.bind(on_release=user_role_dropdown.open)
        user_role_dropdown.bind(on_select=lambda instance, x: userRole_input_set_role(x))

        save_button = Button(text=app.arabicText('حفظ'), on_press=self.save_new_room(room_name_input, userpassword_input))
        save_button.background_normal=''
        save_button.background_color = (210 / 255, 141 / 255, 26 / 255, 1)
        save_button.color = (10 / 255, 16 / 255, 37 / 255, 1) 
        save_button.font_name='resources/JannaLTBold.ttf'
        save_button.font_size='16sp'
        close_button = Button(text=app.arabicText('إغلاق'), on_press=self.close_popup)
        close_button.background_normal=''
        close_button.background_color = (10 / 255, 16 / 255, 37 / 255, 1) 
        close_button.color = (210 / 255, 141 / 255, 26 / 255, 1)
        close_button.font_name='resources/JannaLTBold.ttf'
        close_button.font_size='16sp'
        popup_content.add_widget(Label (text=app.arabicText('اسم المستخدم'),color=(210 / 255, 141 / 255, 26 / 255, 1),font_size="16sp", font_name='resources/JannaLTBold.ttf'))
        popup_content.add_widget(room_name_input)
        popup_content.add_widget(Label (text=app.arabicText('كلمة المرور'),color=(210 / 255, 141 / 255, 26 / 255, 1),font_size="16sp", font_name='resources/JannaLTBold.ttf'))
        popup_content.add_widget(userpassword_input)
        popup_content.add_widget(Label(text=app.arabicText('صلاحية المسخدم'),color=(210 / 255, 141 / 255, 26 / 255, 1),font_size="16sp", font_name='resources/JannaLTBold.ttf'))
        popup_content.add_widget(userRole_input)
        popup_content.add_widget(save_button)
        popup_content.add_widget(close_button)
        title= app.arabicText('إضافة مستخدم')
        self.popup = Popup(title=title,content=popup_content, size_hint=(0.5, 0.5))
        self.popup.title_color =  (210 / 255, 141 / 255, 26 / 255, 1)
        self.popup.title_font = "resources/JannaLTBold.ttf"
        self.popup.open()
            
    def close_popup(self, instance):
        self.popup.dismiss()
        
    def check_user_existence(self,username):
        app = VoiceContactApp.get_running_app()
        db_connection = app.open_cdb(app.dbname)
        db_cursor = db_connection.cursor()
        # room_name = app.arabicText(room_name)
        # room_name = room_name.strip()
        # room_ip = room_ip.strip()
        # query = "SELECT * FROM rooms WHERE name = ? OR ip = ?"
        query = "SELECT * FROM users WHERE username = ?"
        # db_cursor.execute(query, (room_name,room_ip))
        db_cursor.execute(query, (username,))
        result = db_cursor.fetchall()
        db_connection.commit()
        db_cursor.close()
        print("result",len(result))
        if len(result) > 0 :return True
        else:return False
        
    def save_new_room(self, username, pasword):
        def save_new_room_button(instance):
            app = VoiceContactApp.get_running_app()
            new_username = app.arabicText(username.text)
            new_username = new_username.strip()
            new_password = app.arabicText(pasword.text)
            new_password = new_password.strip()
            new_role = self.uRole
            print('new_role',new_role,new_username,new_password)
            new_username = new_username.strip()
            new_password = new_password.strip()
            check = self.check_user_existence(new_username)
            print("check",check)
            if check == False:
                if new_username !="" and new_password!="" and new_role!="" :
                    # conn = sqlite3.connect('voiceContact.db')
                    db_connection = app.open_cdb(app.dbname)
                    db_cursor = db_connection.cursor()
                    app.save_cdb(db_connection,app.dbname) 
                    # cursor = conn.cursor()
                    db_cursor.execute('INSERT INTO users (username,password,role) VALUES (?, ?,?)', (new_username, new_password,new_role))
                    db_connection.commit() 
                    self.popup.dismiss() 
                    db_cursor.close()
                    app.save_cdb(db_connection,app.dbname) 
                    popup_content = boxColor()
                    popup_content.add_widget(Label(text=app.arabicText('تم إضافة المستخدم بنجاح'),color=(210 / 255, 141 / 255, 26 / 255, 1),font_size="16sp", font_name='resources/JannaLTBold.ttf'))
                    self.sucesspopup = Popup(title=app.arabicText('حالة المستخدم'), content=popup_content, size_hint=(0.5, 0.5))
                    self.sucesspopup.title_color =  (210 / 255, 141 / 255, 26 / 255, 1)
                    self.sucesspopup.title_font = "resources/JannaLTBold.ttf"
                    self.sucesspopup.open()
                    Clock.schedule_once(self.dismiss_popup,0.2)
            if check == True:
                popup_content = boxColor()
                popup_content.add_widget(Label(text=app.arabicText('المستخدم موجود بالفعل'),color=(210 / 255, 141 / 255, 26 / 255, 1),font_size="16sp", font_name='resources/JannaLTBold.ttf'))
                self.sucesspopup = Popup(title=app.arabicText('حالة المستخدم'), content=popup_content, size_hint=(0.5, 0.5))
                self.sucesspopup.title_color =  (210 / 255, 141 / 255, 26 / 255, 1)
                self.sucesspopup.title_font = "resources/JannaLTBold.ttf"
                self.sucesspopup.open()
                Clock.schedule_once(self.dismiss_popup,0.2)
                # self.fetch_and_display_users()  

        return save_new_room_button
  
    
    
    def ReturnBack(self,instance):
        app = VoiceContactApp.get_running_app()
        screen_manager = app.root
        # user_screen = screen_manager.get_screen("users")  
        # room_screen.create_widget(ip,name)
        screen_manager.current = "admin"
        
    def addusers(self,instance):
        pass   

class AdminScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.call_all_added = False 
        self.checkifFetch = False
        self.done =False
        self.progress_bar = False

    def on_enter(self):
        self.Check_If_Rrooms()
        self.status_thread = threading.Thread(target=self.check_Status,daemon=True)
        self.status_thread.start()
        
    def Check_If_Rrooms(self):
        # print('global_conn',global_conn)
        app = VoiceContactApp.get_running_app()
        db_connection = app.open_cdb(app.dbname)
        db_cursor = db_connection.cursor()
        # conn = sqlite3.connect('voiceContact.db')
        # cursor =global_conn.cursor()
        db_cursor.execute('SELECT * FROM rooms')
        rows = db_cursor.fetchall()
        db_connection.commit()
        row_count = len(rows)
        db_cursor.close()
        # print('row_count',row_count)
        if row_count == 0:
            threading.Thread(target=self.ADDScandes,daemon=True).start()
            Clock.schedule_interval(self.checkdone,0.1)
        else:
            self.fetch_and_display_data()
            
    def checkIP(self, ip):
      count = 2
      output = Popen(f"ping {ip} -n {count}", stdout=PIPE, encoding="utf-8")
      data = ""
      for line in output.stdout:
            data = data + line

      result = findall("TTL", data)
      if (result):
            return True
      else:
            return False
      
    def scan_ips(self,target):
        nm = nmap.PortScanner()
        nm.scan(hosts=target, arguments='-sn')
        
        active_ips = []
        for ip in nm.all_hosts():
            if(self.checkIP(ip)):
                active_ips.append(ip)
        return active_ips
    

            
    def checkdone(self,dt):
        if self.done == True:
            self.fetch_and_display_data()  
            

                  
    #check and Add to database
    def ADDScandes(self):
        target_range = '100.100.1.1/24'  # Replace with your desired IP range
        active_ips = self.scan_ips(target_range)
        countRows = self.countRows()
        for ip in active_ips:
            if (ip.split(".")[3]!="0" and ip.split(".")[3]!="1" and ip.split(".")[3]!="10"):
                checkip = self.CheckIPINDATAbase(ip)
                if checkip == 0:
                    self.ADD2Database(ip)
                    # print("IP already not exists:", ip)
        # print('ADDScandes', active_ips, 'countRows', countRows)
        self.done = True
        # self.fetch_and_display_data()
        
    def countRows(self):
        # conn = sqlite3.connect('voiceContact.db')
        app = VoiceContactApp.get_running_app()
        db_connection = app.open_cdb(app.dbname)
        db_cursor = db_connection.cursor()
        # cursor = conn.cursor()
        db_cursor.execute('SELECT * FROM rooms')
        rows = db_cursor.fetchall()
        db_connection.commit()
        db_cursor.close()
        row_count = len(rows)
        return row_count
    
    def CheckIPINDATAbase(self, ip):
        # conn = sqlite3.connect('voiceContact.db')
        app = VoiceContactApp.get_running_app()
        db_connection = app.open_cdb(app.dbname)
        db_cursor = db_connection.cursor()
        # cursor = conn.cursor()
        query = "SELECT * FROM rooms WHERE ip = ? "
        db_cursor.execute(query, (ip,))
        rows = db_cursor.fetchall()
        db_connection.commit()
        db_cursor.close()
        row_count = len(rows)
        return row_count
    
    def ADD2Database(self,ip):
        countRows = self.countRows()
        # conn = sqlite3.connect('voiceContact.db')
        app = VoiceContactApp.get_running_app()
        db_connection = app.open_cdb(app.dbname)
        db_cursor = db_connection.cursor()
        # cursor = conn.cursor()
        new_name = "room"+str(countRows)
        new_IP =ip
        db_cursor.execute('INSERT INTO rooms (name, ip) VALUES (?, ?)', (new_name, new_IP))
        db_connection.commit()
        db_cursor.close()
        app.save_cdb(db_connection,app.dbname) 
        
        
        
    def RefreshNetwork(self,button_instance):
        # print("Refresh Network ...................")
        # app = VoiceContactApp.get_running_app()
        # # threading.Thread(target=app.ADDScandes,daemon=True).start()
        # app.ADDScandes()  
        # self.fetch_and_display_data()
        self.done = False
        threading.Thread(target=self.ADDScandes,daemon=True).start()
        Clock.schedule_interval(self.checkdone,0.1)
        
 
        
    def drawProgress(self,dt):
        if  self.checkifFetch == False :
            Playout = self.ids.prog
            progress_bar = CustomProgressBar()
            Playout.add_widget(progress_bar)


        
        
    def clearProgress(self):
        Playout = self.ids.prog
        progress_bar = CustomProgressBar()
        if self.checkifFetch == True :
            Playout.remove_widget(progress_bar)
     
      
    def fetch_and_display_data(self):
        # print("Fetch data from class")
        # conn = sqlite3.connect('voiceContact.db')
        app = VoiceContactApp.get_running_app()
        db_connection = app.open_cdb(app.dbname)
        db_cursor = db_connection.cursor()
        # cursor = conn.cursor()
        db_cursor.execute('SELECT name,ip,description FROM rooms')
        rows = db_cursor.fetchall()
        db_connection.commit()
        db_cursor.close()

        layout = self.ids.rooms_layout
        Hlayout = self.ids.btns_Hlayout
        layout.clear_widgets()
    
        self.cnt_btns = []
        self.st_lbls = []
        self.st_IMG = []
        self.st_bluth =[]
        i = 0
        app = VoiceContactApp.get_running_app()
        if not self.call_all_added:
            self.call_all = CallAll()
            refresh_net = AddRoomButton(text="تحديث الشبكة")
            users = AddRoomButton(text="المستخدمين")
            self.call_all.st = 0
            Hlayout.add_widget(refresh_net)
            Hlayout.add_widget(users)
            Hlayout.add_widget(self.call_all)

            self.call_all.bind(on_press=self.callAllfunc)
            refresh_net.bind(on_press=self.RefreshNetwork)
            users.bind(on_press=self.change_screen)
            self.call_all_added = True

        for row in rows:
            card = CustomCard()
            card.update_size(350,470)
            room_name = row[0]
            room_ip = row[1]
            room_desc = row[2]
            ip_layout = GridLayout(cols=1, padding=(0, "40dp"), spacing=10) 
            ip_label = Label(text=app.arabicText(room_ip),color=(0.909, 0.667, 0.259, 1))
            ip_layout.add_widget(ip_label)
            card.add_widget(ip_layout)
            # ip_label = Label(text=app.arabicText(room_ip),color=(0.909, 0.667, 0.259, 1))
            # card.add_widget(ip_label)
            name_layout = GridLayout(cols=1, padding=(0,"10dp"))
            name_label = Label(text=app.arabicText(room_name) , color=(0.909, 0.667, 0.259, 1),font_size="16sp", font_name='resources/JannaLTBold.ttf')
            name_layout.add_widget(name_label)
            card.add_widget(name_layout)
            desc_layout = GridLayout(cols=1)
            # text_size=(250,None), size_hint_y=None
            desc_label = Label(text=app.arabicText(room_desc),text_size=(250,None), size_hint_y=None,halign='right',color=(242 / 255, 194 / 255, 114 / 255, 1),font_size="14sp", font_name='resources/JannaLTBold.ttf')
            desc_layout.add_widget(desc_label)
            card.add_widget(desc_layout)
            space_layout =  GridLayout(cols=1)
            # connect_layout = GridLayout(cols=1, padding=(0,"50dp"), spacing=20)  # Horizontal layout for connection elements
            card.add_widget(space_layout)
            image_layout = GridLayout(cols=1,padding=(0,"20dp"),spacing=20,pos_hint={"center_x":0.3},size_hint=(None, None))
            status_image = Image(source="resources/waveMute.png",size_hint=(None, None), size=(250,120))
            image_layout.add_widget(status_image)
            card.add_widget(image_layout)
            status_image.i=i
            status_image.ip=f'{room_ip}'
            self.st_IMG.append(status_image)
            connect_layout =  GridLayout(cols=1)
            connect_button = ConnectButton()
            connect_button.room_ip = f'{room_ip}' 
            connect_button.room_name = f'{room_name}' 
            connect_button.i = i
            connect_button.st = 0
            connect_button.ip = room_ip
            self.cnt_btns.append(connect_button)
            connect_button.bind(on_press=self.connect_room)
            # image_layout.add_widget(status_image)
            # connect_layout = GridLayout(cols=1,pos_hint={"center_x":0.5},size_hint=(None, None))
            card.add_widget(connect_layout)
            card.add_widget(connect_button)
            btn_layout =  GridLayout(cols=2,spacing=250)
            delete_button = DeleteButton()
            delete_button.room_ip = room_ip
            delete_button.room_name = room_name
            # delete_button.bind(on_press=lambda instance:self.set_flag(room_name))
            delete_button.bind(on_press=self.set_flag)
            btn_layout.add_widget(delete_button)
            edit_button = EditButton()
            edit_button.room_ip = room_ip
            edit_button.bind(on_press=self.edit_room)
            btn_layout.add_widget(edit_button)
            card.add_widget(btn_layout)
            speaker, connected = ClientConnection(room_ip, 7777).check()
            # print('checkStatus',speaker,connected)
            status_layout = StatusLayout()
            if connected:
                status_conn = ConnectionStatusButton(icon="access-point-network")
                status_conn.text_color =  (10 / 255, 16 / 255, 37 / 255, 1) 
            else:
                status_conn = ConnectionStatusButton(icon="access-point-network-off")
                status_conn.text_color = (183, 183, 183)
            status_conn.i = i
            status_conn.ip = room_ip
            self.st_lbls.append(status_conn)
            status_layout.add_widget(status_conn)
            if speaker:
                status_blutooth = ConnectionStatusButton(icon="headphones")
                status_blutooth.text_color =  (10 / 255, 16 / 255, 37 / 255, 1) 
            else:
                status_blutooth = ConnectionStatusButton(icon="headphones-off")
                status_blutooth.text_color = (183, 183, 183)
            status_blutooth.i = i
            status_blutooth.ip = room_ip
            self.st_bluth.append(status_blutooth)
            status_layout.add_widget(status_blutooth)
            card.add_widget(status_layout)
            layout.add_widget(card)
            i += 1
        self.done = False
        self.checkifFetch = True
        Clock.unschedule(self.checkdone)
        

    def set_flag(self, instance):
        self.flag = 1
        app = VoiceContactApp.get_running_app()
        self.confirmpopup = Popup(title=app.arabicText('تأكيد الحذف'), size_hint=(0.5, 0.5))
        room_ip = instance.room_ip
        room_name = instance.room_name
        # print("request to remove room :" , room_ip)
        # app = VoiceContactApp.get_running_app()
        popup_content_confirm = boxColor()
        layout = BoxLayout(orientation='vertical')
        save_button = Button(text=app.arabicText('نعم'), on_press=self.delete_room(room_ip))
        save_button.background_normal=''
        save_button.background_color = (210 / 255, 141 / 255, 26 / 255, 1)
        save_button.color = (10 / 255, 16 / 255, 37 / 255, 1) 
        save_button.font_name='resources/JannaLTBold.ttf'
        save_button.font_size='16sp'
        close_button = Button(text=app.arabicText('إغلاق'), on_press=self.confirmpopup.dismiss)
        close_button.background_normal=''
        close_button.background_color = (10 / 255, 16 / 255, 37 / 255, 1) 
        close_button.color = (210 / 255, 141 / 255, 26 / 255, 1)
        close_button.font_name='resources/JannaLTBold.ttf'
        close_button.font_size='16sp'
        popup_content_confirm.add_widget(Label(text=app.arabicText(' هل أنت متأكد من حذف ' + room_name + " (" + room_ip + ") ؟"),color=(210 / 255, 141 / 255, 26 / 255, 1),font_size="16sp", font_name='resources/JannaLTBold.ttf'))
        layout.add_widget(save_button)
        layout.add_widget(close_button)
        popup_content_confirm.add_widget(layout)
        # self.confirmpopup = Popup(title=app.arabicText('تأكيد الحذف'), content=popup_content_confirm, size_hint=(0.5, 0.5))
        self.confirmpopup.content = popup_content_confirm
        self.confirmpopup.title_color =  (210 / 255, 141 / 255, 26 / 255, 1)
        self.confirmpopup.title_font = "resources/JannaLTBold.ttf"
        self.confirmpopup.open()
        
        # print('self.flag',self.flag)
        
             
    def check_Status(self):
        while True:
            try:
                for room in self.st_lbls:
                    # print(room.ip)
                    speaker, connected = ClientConnection(room.ip, 7777).check()
                    # print('speaker', speaker,'connected',connected,"=====================")
                    connect_status = self.st_lbls[room.i]
                    bluetooth_status =self.st_bluth[room.i]
                    if connected:
                        connect_status.icon ="access-point-network"
                        connect_status.text_color =  (10 / 255, 16 / 255, 37 / 255, 1) 
                    
                    else:
                        connect_status.icon ="access-point-network-off"
                        connect_status.text_color = (183, 183, 183)
                        
                    if speaker:
                        bluetooth_status.icon ="headphones"
                        bluetooth_status.text_color =  (10 / 255, 16 / 255, 37 / 255, 1) 
                    else:
                        bluetooth_status.icon ="headphones-off"
                        bluetooth_status.text_color = (183, 183, 183)
            
            except Exception as e:
                print("check Exception : ", e)
            sleep(5)

    
    def check_Status2(self,dt):
        for room in self.st_lbls:
            # print(room.ip)
            speaker, connected = ClientConnection(room.ip, 7777).check()
            # print('speaker', speaker,'connected',connected,"=====================")
            connect_status = self.st_lbls[room.i]
            bluetooth_status =self.st_bluth[room.i]
            if connected:
                connect_status.icon ="access-point-network"
                connect_status.text_color =  (10 / 255, 16 / 255, 37 / 255, 1) 
              
            else:
                connect_status.icon ="access-point-network-off"
                connect_status.text_color = (183, 183, 183)
                
            if speaker:
                bluetooth_status.icon ="headphones"
                bluetooth_status.text_color =  (10 / 255, 16 / 255, 37 / 255, 1) 
            else:
                bluetooth_status.icon ="headphones-off"
                bluetooth_status.text_color = (183, 183, 183)

    
                
    def connect_room(self,instance):
        app = VoiceContactApp.get_running_app()
        self.i  =  instance.i
        self.ip = instance.room_ip
        connect_button = self.cnt_btns[self.i]
        status_image = self.st_IMG[self.i]
        speaker,connected = ClientConnection(self.ip , 7777).check()
        if connect_button.st == 1:
            self.cnt_btns[self.i].st = 0
            connect_button.text =app.arabicText("إتصال بالغرفة")
            connect_button.md_bg_color =  (242 / 255, 194 / 255, 114 / 255, 1)
            self.client.stop_stream()
            Clock.schedule_once(self.StopStream,3)
            # Clock.schedule_interval(self.check_Status,2)
        else:
            if speaker and connected:
                # if connect_button.st == 0:
                self.cnt_btns[self.i].st = 1
                connect_button.text =app.arabicText("قطع الإتصال")
                # connect_button.md_bg_color =  (210/255, 141/255, 26/255, 1)
                connect_button.md_bg_color =  (236/255, 112/255, 99/255, 1)
                self.client = Client(ip=self.ip) 
                self.client.connect()
                Clock.schedule_once(self.runStream,2)
                Clock.schedule_once(self.runSound,3)
                # print('self.client.sender.connected',self.client.sender.connected)
                # Clock.unschedule(self.check_Status)
                
                # self.ch_th = threading.Thread(target=self.check, daemon=True)
                # self.ch_th.start()

                Clock.schedule_interval(self.check,1)
                # else:
                #     self.cnt_btns[self.i].st = 0
                #     connect_button.text =app.arabicText("إتصال بالغرفة")
                #     self.client.stop_stream()
                #     Clock.schedule_once(self.StopStream,3)
                #     Clock.schedule_interval(self.check_Status,20)
            
            elif connected == False:
                message = app.arabicText('الجهاز غير متصل')
                popup = userAlert(message)
                popup.open()

            elif speaker == False:
                message = app.arabicText('السماعة غير متصلة')
                popup = userAlert(message)
                popup.open()
       
            
   
    def runStream(self,dt):
        self.client.run_stream()
        
    def runSound(self,dt):
        is_connected = self.client.sender.connected
        if is_connected:
            sound = SoundLoader.load('resources/sound.wav')
            if sound:
                # print("Sound play")
                sound.play()    
                
    def StopStream(self,dt):
        self.client.stop_stream()
        Clock.unschedule(self.check)
        
    def uncheckAll2Connect(self,dt):
        Clock.unschedule(self.checkAll2Connect)
                  
    def check(self,dt):
        # app = VoiceContactApp.get_running_app()
        # connect_button = self.cnt_btns[self.i]
        # status_label = self.st_lbls[self.i]
        # status_Img = self.st_IMG [self.i]
   
        speaker,connected = ClientConnection(self.ip, 7777).check()
        is_connected = self.client.sender.connected
        # print('is_connected',is_connected,'connected',connected)

        if  is_connected:
            self.st_IMG[self.i].source='resources/wave2.gif'
        else:
            self.st_IMG[self.i].source="resources/waveMute.png"

            
    def check2(self,dt):
        app = VoiceContactApp.get_running_app()
        connect_button = self.cnt_btns[self.i]
        status_label = self.st_lbls[self.i]
        status_Img = self.st_IMG [self.i]
        speaker,connected = ClientConnection(self.ip, 7777).check()
        is_connected = self.client.sender.connected
        # print('is_connected',is_connected,'connected',connected)

        if  is_connected:
            self.st_IMG[self.i].source="resources/wave2.gif"
        else:
            self.st_IMG[self.i].source="resources/waveMute.png"


    def callAllfunc(self,instance):
        # print('instance.st  from callAllfunc',instance.st)
        app = VoiceContactApp.get_running_app()
        db_connection = app.open_cdb(app.dbname)
        db_cursor = db_connection.cursor()
        if instance.st == 0 :
            instance.st = 1
            # print('instance.st ',instance.st )
            
            self.connected_rooms = []
            self.connected_clients = []
            # conn = sqlite3.connect('voiceContact.db')
            # cursor = conn.cursor()
            db_cursor.execute('SELECT ip FROM rooms')
            rows = db_cursor.fetchall()
            for i, row in enumerate(rows):
                ip_address = row[0]
                # print(f"Index: {i}, IP Address: {ip_address}")
                speaker,connected = ClientConnection(ip_address , 7777).check()
                if speaker and connected:
                    self.connected_rooms.append(ip_address)
                # print("connected_rooms",self.connected_rooms)
            
            db_connection.commit()
            db_cursor.close()
    
            
            for ip_address in self.connected_rooms:
                client = Client(ip=ip_address)
                client.connect()
                client.run_stream()
                self.connected_clients.append(client)
            instance.text = app.arabicText('قطع الإتصال بالكل')
            Clock.schedule_once(self.play,3)
            # Clock.unschedule(self.check_Status)
            Clock.schedule_interval(self.checkAll2Connect,2)

        else:
            instance.st = 0
            instance.text = app.arabicText('الإتصال بالكل')
            Clock.schedule_once(self.stop_stream_all_rooms,1)
            Clock.schedule_once(self.uncheckAll2Connect,3)
            # Clock.schedule_interval(self.check_Status,20)
                
    def stop_stream_all_rooms(self,dt):
        for client in self.connected_clients:
            client.stop_stream()
            
    def play(self,dt) :  
        Clock.schedule_once(self.Sound4All,1)

        
    def Sound4All(self,dt):
        count = 0 
        for client in self.connected_clients:
            is_connected = client.sender.connected
            if is_connected:
                count += 1 
            # print(" is_connected:", is_connected,"count", count, 'len(self.connected_clients)', len(self.connected_clients))

        # Now you can access the updated count outside the loop
        if count == len(self.connected_clients):
            sound = SoundLoader.load('resources/sound.wav')
            if sound:
                # print("Sound play")
                sound.play()

                    
    def checkAll2Connect(self,dt):
        app = VoiceContactApp.get_running_app()
        for client in self.connected_clients:
            is_connected = client.sender.connected
            client_ip = client.HOST
            # print('self.connected_clients:',self.connected_clients,is_connected)
            if is_connected:
                for status_image in self.st_IMG:
                    ip_address = status_image.ip
                    index =  status_image.i
                    if  ip_address ==client_ip:
                        img = self.st_IMG[index]
                        btn = self.cnt_btns[index]
                        img.source="resources/wave2.gif"
                        btn.text =app.arabicText('قطع الإنصال')
            else:
                    for status_image in self.st_IMG:
                        ip_address = status_image.ip
                        index =  status_image.i
                        if  ip_address ==client_ip:
                            img = self.st_IMG[index]
                            btn = self.cnt_btns[index]
                            # print('from else',is_connected)
                            img.source="resources/waveMute.png"
                            btn.text =app.arabicText('الإتصال بالغرفة')
              
                     
                        

               
                
    def uncheckAll2Connect(self,dt):
        app = VoiceContactApp.get_running_app()
        for ip_address in self.connected_rooms:
            client = Client(ip=ip_address)
            client.stop_stream()
            # self.connected_clients.append(client)
            Clock.unschedule(self.checkAll2Connect)


            
    def change_screen(self,instance):
        app = VoiceContactApp.get_running_app()
        screen_manager = app.root
        # user_screen = screen_manager.get_screen("users")  
        # room_screen.create_widget(ip,name)
        screen_manager.current = "users"
        

            
    def delete_room(self, room_ip):
        def delete_room_button(instance):
            self.confirmpopup.dismiss() 
            app = VoiceContactApp.get_running_app()
            db_connection = app.open_cdb(app.dbname)
            db_cursor = db_connection.cursor()
            # conn = sqlite3.connect('voiceContact.db')
            # # print("from delete",room_ip)
            # cursor = conn.cursor()
            db_cursor.execute('DELETE FROM rooms WHERE ip = ?', (room_ip,))
            rows_affected = db_cursor.rowcount
            db_connection.commit()
            db_cursor.close()
            app.save_cdb(db_connection,app.dbname) 

            if rows_affected > 0:
                # print('rows_affected',rows_affected)
                popup_content = boxColor()
                popup_content.add_widget(Label(text=app.arabicText('تم الحذف بنجاح'),color=(210 / 255, 141 / 255, 26 / 255, 1),font_size="16sp", font_name='resources/JannaLTBold.ttf'))
                self.sucesspopup = Popup(title=app.arabicText('حالة الحذف'), content=popup_content, size_hint=(0.5, 0.5))
                self.sucesspopup.title_color =  (210 / 255, 141 / 255, 26 / 255, 1)
                self.sucesspopup.title_font = "resources/JannaLTBold.ttf"
                self.sucesspopup.open()
                Clock.schedule_once(self.dismiss_popup,0.2)


        return delete_room_button
   
    def dismiss_popup(self,dt):
        self.sucesspopup.dismiss() 
        self.fetch_and_display_data() 
  
           
    def edit_room(self, instance):
            room_ip = instance.room_ip
        # def edit_room_button(instance):
            app = VoiceContactApp.get_running_app()
            db_connection = app.open_cdb(app.dbname)
            db_cursor = db_connection.cursor()
            name =''
            ip=''
            desc=''
            # conn = sqlite3.connect('voiceContact.db')
            # cursor = conn.cursor()
            db_cursor.execute('SELECT name, ip, description FROM rooms WHERE ip = ?', (room_ip,))
            rows = db_cursor.fetchall()
            db_connection.commit()
            db_cursor.close()
            for row in rows:
                name = row[0]
                ip = row[1]
                desc = row[2]
            # print('name',name)
            # Create a popup for editing the room details
            popup_content = boxColor()
            room_name_input = Ar_text(maxchar=80, text=app.arabicText(name),multiline=False,background_color=(69/255, 69/255, 69/255,1),foreground_color=(210 / 255, 141 / 255, 26 / 255, 1),font_size="16sp", font_name='resources/JannaLTBold.ttf')
            room_IP_input = Ar_text(maxchar=20, text=app.arabicText(ip),multiline=False,background_color=(69/255, 69/255, 69/255,1),foreground_color=(210 / 255, 141 / 255, 26 / 255, 1),font_size="16sp", font_name='resources/JannaLTBold.ttf')
            room_Dec_input = Ar_text(maxchar=140, text=app.arabicText(desc),multiline=True,background_color=(69/255, 69/255, 69/255,1),foreground_color=(210 / 255, 141 / 255, 26 / 255, 1),font_size="16sp", font_name='resources/JannaLTBold.ttf')
            save_button = Button(text=app.arabicText('حفظ'), on_press=self.save_room(room_ip, room_name_input, room_IP_input,room_Dec_input))
            save_button.background_normal=''
            save_button.background_color = (210 / 255, 141 / 255, 26 / 255, 1)
            save_button.color = (10 / 255, 16 / 255, 37 / 255, 1) 
            save_button.font_name='resources/JannaLTBold.ttf'
            save_button.font_size='16sp'
            close_button = Button(text=app.arabicText('إغلاق'), on_press=self.close_popup)
            close_button.background_normal=''
            close_button.background_color = (10 / 255, 16 / 255, 37 / 255, 1) 
            close_button.color = (210 / 255, 141 / 255, 26 / 255, 1)
            close_button.font_name='resources/JannaLTBold.ttf'
            close_button.font_size='16sp'
            popup_content.add_widget(Label(text=app.arabicText('اسم الغرفة'),color=(210 / 255, 141 / 255, 26 / 255, 1),font_size="16sp", font_name='resources/JannaLTBold.ttf'))
            popup_content.add_widget(room_name_input)
            popup_content.add_widget(Label(text=app.arabicText('رقم الغرفة'),color=(210 / 255, 141 / 255, 26 / 255, 1),font_size="16sp", font_name='resources/JannaLTBold.ttf'))
            popup_content.add_widget(room_IP_input)
            popup_content.add_widget(Label(text=app.arabicText('وصف الغرفة'),color=(210 / 255, 141 / 255, 26 / 255, 1),font_size="16sp", font_name='resources/JannaLTBold.ttf'))
            popup_content.add_widget(room_Dec_input)
            popup_content.add_widget(save_button)
            popup_content.add_widget(close_button)
            self.popup = Popup(title=app.arabicText('تحديث الغرفة'), content=popup_content, size_hint=(0.5, 0.5))
            self.popup.title_color =  (210 / 255, 141 / 255, 26 / 255, 1)
            self.popup.title_font = "resources/JannaLTBold.ttf"
            self.popup.open()
            
        # return edit_room_button

    def save_room(self, room_ip, name_input, IP_input,Des_input):
        def save_room_button(instance):
            app = VoiceContactApp.get_running_app()
            db_connection = app.open_cdb(app.dbname)
            db_cursor = db_connection.cursor()
            new_name = app.arabicText(name_input.text)
            new_IP = app.arabicText(IP_input.text)
            new_des = app.arabicText(Des_input.text)
            new_name = new_name.strip()
            new_IP = new_IP.strip()
            new_des = new_des.strip()
            if new_name !="" and new_IP!="":
                # conn = sqlite3.connect('voiceContact.db')
                # cursor = conn.cursor()
                db_cursor.execute('UPDATE rooms SET name = ?, ip = ?, description = ? WHERE ip = ?', (new_name, new_IP, new_des, room_ip))
                db_connection.commit()
                db_cursor.close()
                app.save_cdb(db_connection,app.dbname) 
                self.popup.dismiss()  # Close the popup after saving
                self.fetch_and_display_data()  # Refresh the data after editing

        return save_room_button

    def add_room(self):
        app = VoiceContactApp.get_running_app()
        # popup_content = BoxLayout(orientation='vertical')
        popup_content = boxColor()
        room_name_input = Ar_text(maxchar=80, multiline=False,background_color=(69/255, 69/255, 69/255,1),
                        foreground_color=(210 / 255, 141 / 255, 26 / 255, 1),font_size="16sp",font_name='resources/JannaLTBold.ttf' 
                        )
    

        room_IP_input = Ar_text(maxchar=20, multiline=False,background_color=(69/255, 69/255, 69/255,1),foreground_color=(210 / 255, 141 / 255, 26 / 255, 1),font_size="16sp", font_name='resources/JannaLTBold.ttf')
        room_des_inp = Ar_text(maxchar=120, multiline=True,background_color=(69/255, 69/255, 69/255,1),foreground_color=(210 / 255, 141 / 255, 26 / 255, 1),font_size="16sp", font_name='resources/JannaLTBold.ttf')
        save_button = Button(text=app.arabicText('حفظ'), on_press=self.save_new_room(room_name_input, room_IP_input,room_des_inp))
        save_button.background_normal=''
        save_button.background_color = (210 / 255, 141 / 255, 26 / 255, 1)
        save_button.color = (10 / 255, 16 / 255, 37 / 255, 1) 
        save_button.font_name='resources/JannaLTBold.ttf'
        save_button.font_size='16sp'
        close_button = Button(text=app.arabicText('إغلاق'), on_press=self.close_popup)
        close_button.background_normal=''
        close_button.background_color = (10 / 255, 16 / 255, 37 / 255, 1) 
        close_button.color = (210 / 255, 141 / 255, 26 / 255, 1)
        close_button.font_name='resources/JannaLTBold.ttf'
        close_button.font_size='16sp'
        popup_content.add_widget(Label (text=app.arabicText('اسم الغرفة'),color=(210 / 255, 141 / 255, 26 / 255, 1),font_size="16sp", font_name='resources/JannaLTBold.ttf'))
        popup_content.add_widget(room_name_input)
        popup_content.add_widget(Label(text=app.arabicText('رقم الغرفة'),color=(210 / 255, 141 / 255, 26 / 255, 1),font_size="16sp", font_name='resources/JannaLTBold.ttf'))
        popup_content.add_widget(room_IP_input)
        popup_content.add_widget(Label(text=app.arabicText('وصف الغرفة'),color=(210 / 255, 141 / 255, 26 / 255, 1),font_size="16sp", font_name='resources/JannaLTBold.ttf'))
        popup_content.add_widget(room_des_inp)
        popup_content.add_widget(save_button)
        popup_content.add_widget(close_button)
        title= app.arabicText('إضافة غرفة')
        self.popup = Popup(title=title,content=popup_content, size_hint=(0.5, 0.5))
        self.popup.title_color =  (210 / 255, 141 / 255, 26 / 255, 1)
        self.popup.title_font = "resources/JannaLTBold.ttf"
        self.popup.open()
            
    def close_popup(self, instance):
        self.popup.dismiss()
        
    def check_room_existence(self,room_name, room_ip):
        app = VoiceContactApp.get_running_app()
        db_connection = app.open_cdb(app.dbname)
        db_cursor = db_connection.cursor()
        # room_name = app.arabicText(room_name)
        # room_name = room_name.strip()
        # room_ip = room_ip.strip()
        # query = "SELECT * FROM rooms WHERE name = ? OR ip = ?"
        query = "SELECT * FROM rooms WHERE ip = ?"
        # db_cursor.execute(query, (room_name,room_ip))
        db_cursor.execute(query, (room_ip,))
        result = db_cursor.fetchall()
        db_connection.commit()
        db_cursor.close()
        print("result",len(result))
        if len(result) > 0 :return True
        else:return False
    
    def save_new_room(self, name_input, IP_input,Des_input):
        def save_new_room_button(instance):
            app = VoiceContactApp.get_running_app()
            db_connection = app.open_cdb(app.dbname)
            db_cursor = db_connection.cursor()
            new_name = app.arabicText(name_input.text)
            new_IP = app.arabicText(IP_input.text)
            new_Des = app.arabicText(Des_input.text)
            new_name = new_name.strip()
            new_IP = new_IP.strip()
            new_Des = new_Des.strip()
            check = self.check_room_existence(new_name,new_IP)
            print("check",check)
            if check == False:
                if new_name !="" and new_IP!="" and len(new_IP.split("."))==4 and new_Des!="":
                    # conn = sqlite3.connect('voiceContact.db')
                    # cursor = conn.cursor()
                    db_cursor.execute('INSERT INTO rooms (name, ip,description) VALUES (?, ?,?)', (new_name, new_IP,new_Des))
                    db_connection.commit()
                    db_cursor.close()
                    app.save_cdb(db_connection,app.dbname) 
                    self.popup.dismiss() 
                    #show msg if save
                    popup_content = boxColor()
                    popup_content.add_widget(Label(text=app.arabicText('تم إضافة الغرفة بنجاح'),color=(210 / 255, 141 / 255, 26 / 255, 1),font_size="16sp", font_name='resources/JannaLTBold.ttf'))
                    self.sucesspopup = Popup(title=app.arabicText('حالة الغرفة'), content=popup_content, size_hint=(0.5, 0.5))
                    self.sucesspopup.title_color =  (210 / 255, 141 / 255, 26 / 255, 1)
                    self.sucesspopup.title_font = "resources/JannaLTBold.ttf"
                    self.sucesspopup.open()
                    Clock.schedule_once(self.dismiss_popup,0.2)
            if check == True:
                popup_content = boxColor()
                popup_content.add_widget(Label(text=app.arabicText('الغرفة موجودة بالفعل'),color=(210 / 255, 141 / 255, 26 / 255, 1),font_size="16sp", font_name='resources/JannaLTBold.ttf'))
                self.sucesspopup = Popup(title=app.arabicText('حالة الغرفة'), content=popup_content, size_hint=(0.5, 0.5))
                self.sucesspopup.title_color =  (210 / 255, 141 / 255, 26 / 255, 1)
                self.sucesspopup.title_font = "resources/JannaLTBold.ttf"
                self.sucesspopup.open()
                Clock.schedule_once(self.dismiss_popup,0.2)

        return save_new_room_button

        
        
        
class CustomProgressBar(MDSpinner):
    def __init__(self, **kwargs):
        super(CustomProgressBar, self).__init__(**kwargs)
        self.size_hint=None, None
        self.size=60,60
        self.pos_hint={'center_x': .5, 'center_y': .5}
        self.active = True
        self.color = 210 / 255, 141 / 255, 26 / 255, 1
        # self.size_hint = (0.9, None)
        # self.pos_hint = {"center_x": 0.5}
        # self.type= "determinate"
        # self.running_duration= 1
        # self.catching_duration= 1.5
        # self.md_bg_color= 0.909, 0.667, 0.259, 1
        # self.min=0
        # self.max=100

    # def update_progress(self,dt):
    #     if self.value < 100:
    #         self.value += 10
    #     else:
    #         self.value = 0
            
    # def loader(self):
    #     try:
    #         self.i =+10
    #         self.ids.progress.value = self.i
    #     except:
    #         Clock.unschedule(self.loader)
        


# Define the CallAll button class
class CallAll(MDRaisedButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.app = VoiceContactApp.get_running_app()  
        self.text = self.app.arabicText('الإتصال بالكل')
        self.size_hint = (None, None)
        self.size = (500, 5)
        self.md_bg_color = (10 / 255, 16 / 255, 37 / 255, 1)
        self.text_color = (0.909, 0.667, 0.259, 1)
        self.font_size = "15sp"
        self.font_name = 'resources/JannaLTBold.ttf'

        
 

       
class Ar_text(TextInput):
    max_chars = NumericProperty(20)  # maximum character allowed
    str = StringProperty()

    def __init__(self, maxchar ,**kwargs):
        super(Ar_text, self).__init__(**kwargs)
        # print('self.text',self.text)
        # self.str = self.text
        self.max_chars = maxchar
        self.str = get_display(arabic_reshaper.reshape(self.text))
        # self.text = get_display(arabic_reshaper.reshape(" اكتب.. "))


    def insert_text(self, substring, from_undo=False):
        if not from_undo and (len(self.text) + len(substring) > self.max_chars):
            return
        self.str = self.str+substring
        self.text = get_display(arabic_reshaper.reshape(self.str))
        substring = ""
        super(Ar_text, self).insert_text(substring, from_undo)

    def do_backspace(self, from_undo=False, mode='bkspc'):
        self.str = self.str[0:len(self.str)-1]
        self.text = get_display(arabic_reshaper.reshape(self.str))

    
class boxColor(BoxLayout):
    def __init__(self):
        super(boxColor, self).__init__()
        self.orientation = 'vertical'

        with self.canvas.before:
            Color(10 / 255, 16 / 255, 37 / 255, 1)  
            self.rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
   
        
class userAlert(Popup):
    def __init__(self, message,show_ok_button=False,roomName=""):
        super(userAlert, self).__init__()
        # print('from userAlert show_ok_button',show_ok_button)
        self.roomName = roomName  
        self.app = VoiceContactApp.get_running_app()
        layout = BoxLayout(orientation='vertical')
        label = Label(text=message, color=(210 / 255, 141 / 255, 26 / 255, 1),font_name='resources/JannaLTBold.ttf')
        closebutton = Button(text=self.app.arabicText('إغلاق'), size_hint=(1, 0.2),font_name='resources/JannaLTBold.ttf')
        closebutton.background_normal=''
        closebutton.background_color = (10 / 255, 16 / 255, 37 / 255, 1)
        closebutton.color =  (210 / 255, 141 / 255, 26 / 255, 1)
        closebutton.bind(on_press=self.dismiss)
        layout.add_widget(label)
        self.title =  self.app.arabicText('خطأ')
        self.title_font = "resources/JannaLTBold.ttf"
        self.title_color = (210 / 255, 141 / 255, 26 / 255, 1)
        self.content = layout
        self.size_hint = (0.3, 0.3)
        self.color =  (210 / 255, 141 / 255, 26 / 255, 1)
        if show_ok_button:
            yesbutton = Button(text=self.app.arabicText('نعم'), size_hint=(1, 0.2), font_name='resources/JannaLTBold.ttf')
            yesbutton.background_normal = ''
            yesbutton.background_color = (210 / 255, 141 / 255, 26 / 255, 1)
            yesbutton.color = (10 / 255, 16 / 255, 37 / 255, 1)
            yesbutton.bind(on_press=lambda instance: self.callDelete())
            layout.add_widget(yesbutton)
        layout.add_widget(closebutton)
        with layout.canvas.before:
            Color(10 / 255, 16 / 255, 37 / 255, 1)  
            self.rect = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class StatusLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(StatusLayout, self).__init__(**kwargs)
        self.orientation = 'horizontal'

        with self.canvas.before:
            Color(210 / 255, 141 / 255, 26 / 255, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(minimum_size=self._update_rect, size=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
        
class userLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(userLayout, self).__init__(**kwargs)
        self.orientation = 'vertical' 

        with self.canvas.before:
            Color(210 / 255, 141 / 255, 26 / 255, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(minimum_size=self._update_rect, size=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos


class Header(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        txt = "نظــام التواصــل الصوتــي"
        reshaped_text = arabic_reshaper.reshape(txt)   
        bidi_text = get_display(reshaped_text)  
        # Create the Image widget
        # image = Image(source='resources/voice-message.png',size_hint=(None, None), size=(120,120),pos_hint={"center_x": 0.5})  
        # image = Image(source='resources/voice-message.png',size_hint=(None, None), size=(120,120),pos_hint={"center_x": 0.5, "center_y": 0.75})  
        # self.add_widget(image)
        self.text=bidi_text
        self.color=(0.909, 0.667, 0.259, 1) 
        self.font_size="20sp"
        self.font_name='resources/JannaLTBold.ttf'
        self.size_hint_y= None


class ColoredBoxLayout(BoxLayout):
    background_color = (10 / 255, 16 / 255, 37 / 255, 1)  # Default background color (white)

    def __init__(self, **kwargs):
        super(ColoredBoxLayout, self).__init__(**kwargs)
        self.bind(size=self._update_background)

    def _update_background(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.background_color)
            Rectangle(pos=self.pos, size=self.size)

class RoomInterance(Screen):
    def create_widget(self,ip,name):
        Clock.schedule_interval(self.check,1)
        self.client = Client(ip=ip) 
        self.client.connect()
        Clock.schedule_once(self.runStream,2)
        Clock.schedule_once(self.runSound,3)
   
        is_connected = self.client.sender.connected
        # print("is_connected from create_widget",is_connected)
        head = Header()
        image = Image(source="resources/waveMute.png")
        
        center_layout = BoxLayout(orientation='vertical',pos_hint={'center_x': 0.5},spacing=15, padding=15)
        h_layout = BoxLayout(orientation='horizontal',spacing= 10,size_hint=(None, None),pos_hint={'center_x': 0.45})
        
        center_layout.add_widget(head)  
        center_layout.add_widget(image)
        
        back_button = BackButton(on_release=self.previous_screen)
        h_layout.add_widget(back_button)
        toggle_button = StopButton(text='Stop')
        toggle_button.bind(on_press=lambda instance: self.on_button_press(instance, ip))
        h_layout.add_widget(toggle_button)    
        box = ColoredBoxLayout(orientation='horizontal', pos_hint={'center_x': 0.5}, size_hint=(0.5, 0.2), size=(500, 300),spacing=10)
        room_label = Label(text=f"Name: {name}",color=(0.909, 0.667, 0.259, 1),font_name='resources/Poppins-SemiBold.ttf')
        ip_label = Label(text=f"IP: {ip}",color=(0.909, 0.667, 0.259, 1),font_name='resources/Poppins-SemiBold.ttf')
        status_label = Label(text="Disconnected", color=(0.909, 0.667, 0.259, 1),
                             font_name='resources/Poppins-SemiBold.ttf')
        self.status_label = status_label  # Assign label to self.status_label
        self.image = image  

        box.add_widget(room_label)
        box.add_widget(ip_label)
        box.add_widget(status_label)
        center_layout.add_widget(h_layout)
        center_layout.add_widget(box)
        self.add_widget(center_layout)
        
    def runStream(self, dt):
        self.client.run_stream()
    def runSound(self,dt):
        is_connected = self.client.sender.connected
        if is_connected:
            sound = SoundLoader.load('resources/sound.wav')
            if sound:
                # print("Sound play")
                sound.play()
       
         
    def check(self,dt):
        if self.client.sender.connected:
            self.status_label.text = "Connected"
            # Update the image source if needed
            self.image.source = "resources/wave2.gif"
           
        else:
            self.status_label.text = "Disconnected"
            self.image.source = "resources/waveMute.png"
           
        
    def on_button_press(self, instance, ip):
        # print('ip from button:', ip)
        if instance.text == 'Stop':
            instance.text = 'On'
            self.client.stop_stream()
        else:
            instance.text = 'Stop'
            Clock.schedule_once(self.runStream,2)
            Clock.schedule_once(self.runSound,3)
              
    def access_user(self):
        app = VoiceContactApp.get_running_app()
        current_user = app.current_user 
        return  current_user
      
    def previous_screen(self, *args):
        self.client.stop_stream()
        current_user = self.access_user()
        # print('current_user',current_user)
        screen_manager = self.manager
        admin_screen = screen_manager.get_screen("admin")
        user_screen = screen_manager.get_screen("user")
        getRole= current_user['is_admin']
        if getRole:
            screen_manager.current = "admin"
            admin_screen.fetch_and_display_data() 
        else:
            screen_manager.current = "user"
            user_screen.fetch_and_display_data() 
            
                
class DeleteButton(MDIconButton):
    def __init__(self, **kwargs):
        super(DeleteButton, self).__init__(**kwargs)
        self.icon = "delete"  # Set the icon name here
        self.theme_text_color = "Custom"
        self.text_color = (210 / 255, 141 / 255, 26 / 255, 1)
        # self.md_bg_color = (0.235, 0.282, 0.420, 1)

class EditButton(MDIconButton):
    def __init__(self, **kwargs):
        super(EditButton, self).__init__(**kwargs)
        self.icon = "application-edit"  # Set the icon name here
        self.theme_text_color = "Custom"
        self.text_color = (210 / 255, 141 / 255, 26 / 255, 1)
        # self.md_bg_color = (0.235, 0.282, 0.420, 1)

class ConnectionStatusButton(MDIconButton):
    def __init__(self, **kwargs):
        super(ConnectionStatusButton, self).__init__(**kwargs)
        self.background_normal=''
        # self.md_bg_color= (0.909, 0.667, 0.259, 1)
        self.size_hint=(0.5, 1)
        self.theme_text_color = "Custom"
        self.text_color = (183, 183, 183)
        
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            return True
        return super(ConnectionStatusButton, self).on_touch_down(touch)
    def on_release(self):
        pass

        
                
class ConnectButton(MDFillRoundFlatButton):
    def __init__(self, **kwargs):
        super(ConnectButton, self).__init__(**kwargs)
        app = VoiceContactApp.get_running_app()
        self.background_normal=''
        self.md_bg_color= (242 / 255, 194 / 255, 114 / 255, 1)
        self.color =(10 / 255, 16 / 255, 37 / 255, 1)
        self.text_color = (10 / 255, 16 / 255, 37 / 255, 1)
        self.font_size="15sp" 
        self.font_name='resources/JannaLTBold.ttf'
        self.text=app.arabicText('إتصال بالغرفة')
        self.size_hint = (None,None)
        # self.size = (900,10)
        self.spacing = "50dp"
        self.padding = ["40dp", "10dp"]
        self.pos_hint ={'center_x': 0.5, 'center_y': 0.5}
        
class StopButton(Button):
    def __init__(self, **kwargs):
        super(StopButton, self).__init__(**kwargs)
        self.background_normal=''
        self.background_color =(10 / 255, 16 / 255, 37 / 255, 1)
        self.color = (0.909, 0.667, 0.259, 1)
        self.font_size="15sp" 
        self.font_name='resources/Poppins-SemiBold.ttf'
        self.text="Stop" 
        self.size_hint = (None, None)  # Disable size_hint
        self.size = (110, 50)  # Set the size (width, height)
         
 #0.909, 0.667, 0.259, 1 yellow  
class CustomCard(MDCard):
    def __init__(self,**kwargs):
        super(CustomCard, self).__init__(**kwargs)
        self.md_bg_color= (0, 0, 0, 0)
        self.md_bg_color=(10 / 255, 16 / 255, 37 / 255, 1)
        self.text_color = (0.909, 0.667, 0.259, 1)
        self.size_hint = (None, None)
        self.size = (300,370)
        # self.padding_top = "50dp"
        self.spacing= 10
        self.orientation = 'vertical'
        
    def update_size(self, width, height):
        self.size = (width, height)
   
  
                   
class LogoutButton(MDRaisedButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal=''
        app = VoiceContactApp.get_running_app()
        self.text = app.arabicText('تسجيل خروج')
        self.on_press = self.logout
        self.size_hint = (None, None)  # Disable size_hint
        self.size = (500, 5) # Set the size (width, height)
        self.md_bg_color =(10 / 255, 16 / 255, 37 / 255, 1)
        self.text_color = (0.909, 0.667, 0.259, 1)
        self.font_size="15sp" 
        self.font_name='resources/JannaLTBold.ttf'
        
    def logout(self, *args):
        app = VoiceContactApp.get_running_app()
        app.logout()  
        
class AddRoomButton(MDRaisedButton):
    def __init__(self,text = "إضافة غرفة",**kwargs):
        super().__init__(**kwargs)
        reshaped_text = arabic_reshaper.reshape(text)    
        bidi_text = get_display(reshaped_text)  
        self.text = bidi_text
        self.background_normal=''
        self.md_bg_color =(210 / 255, 141 / 255, 26 / 255, 1)
        self.color =(10 / 255, 16 / 255, 37 / 255, 1)
        self.text_color = (10 / 255, 16 / 255, 37 / 255, 1)
        self.size_hint = (None, None)  # Disable size_hint
        self.size = (110, 30)  # Set the size (width, height)
        self.font_size="15sp" 
        self.font_name='resources/JannaLTBold.ttf'

class BackButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = 'Back'
        self.background_normal=''
        self.background_color =(210 / 255, 141 / 255, 26 / 255, 1)
        self.color =(0.235, 0.282, 0.420, 1) 
        self.text_color = (0.909, 0.667, 0.259, 1)
        self.size_hint = (None, None)  # Disable size_hint
        self.size = (110, 50)  # Set the size (width, height)
        self.font_size="15sp" 
        self.font_name='resources/Poppins-SemiBold.ttf'


                      
class VoiceContactApp(MDApp):
    def build(self):
        kv= Builder.load_file("kv.kv")
        return kv
    
    def on_start(self):
        print("start")
        self.password=b'WeAreTheBest'
        self.dbname='VOICE_DB'
        self.resources = self.resource_path("resources")
        # self.db_connection = self.open_cdb(self.dbname)
        
    def login(self):
        login_screen = self.root.get_screen('login')
        username = login_screen.ids.username.text
        password = login_screen.ids.password.text
        # conn = sqlite3.connect('resources/voiceContact.db')
        # cursor = global_conn.cursor()
        db_connection = self.open_cdb(self.dbname)
        db_cursor = db_connection.cursor()
        query = "SELECT * FROM users WHERE username = ? AND password = ?"
        db_cursor.execute(query, (username, password))
        result = db_cursor.fetchone()
        if result:
            user_info = {
                'username': result[0],
                'is_admin': bool(result[3])
            }
            self.current_user = user_info  # Store the current user information

            if user_info['is_admin']:
                # print("user_info['is_admin']",user_info['is_admin'])
                self.root.current = "admin"
            else:
                # print("user_info['is_admin']",user_info['is_admin'])
                self.root.current = "user"       
            
        db_cursor.close()

    def logout(self):
        self.current_user = None  # Clear the current user information
        self.root.current = "login"
        
    def resource_path(self, relative_path):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)
    
    def arabicText(self,text):
        reshaped_text = arabic_reshaper.reshape(text)    
        bidi_text = get_display(reshaped_text)  
        return bidi_text   
    def close_button(self):
        app = VoiceContactApp.get_running_app()
        app.stop()
        
    def key_creation(self, password):
        kdf=PBKDF2HMAC(algorithm = hashes.SHA256(), salt=b'\xfaz\xb5\xf2|\xa1z\xa9\xfe\xd1F@1\xaa\x8a\xc2', iterations=1024, length=32, backend=default_backend())
        key=Fernet(base64.urlsafe_b64encode(kdf.derive(password)))
        return key

    def encryption(self, b, password):
        f=self.key_creation(password)
        safe=f.encrypt(b)
        return safe

    def decryption(self, safe, password):
        f=self.key_creation(password)
        b=f.decrypt(safe)
        return b

    def open_cdb(self, name):
        global dir
        # f=gzip.open(getcwd()+name+'_crypted.sql.gz','rb')
        # f=gzip.open(dir + "/" + name + '_crypted.sql.gz','rb')
        f=gzip.open(name + '_crypted.sql.gz','rb')
        safe=f.read()
        f.close()
        content=self.decryption(safe,self.password)
        content=content.decode('utf-8')
        con=sqlite3.connect(':memory:')
        con.executescript(content)
        return con

    def save_cdb(self, con,name):
        # fp=gzip.open(getcwd()+name+'_crypted.sql.gz','wb')
        # fp=gzip.open(dir + "/" + name + '_crypted.sql.gz','wb')
        fp=gzip.open(name + '_crypted.sql.gz','wb')
        b=b''
        for line in con.iterdump():
            b+=bytes('%s\n','utf8') % bytes(line,'utf8')
        b=self.encryption(b,self.password)
        fp.write(b)
        fp.close()     

        
if __name__ == '__main__':
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
   
    # set fullscreen
    width = GetSystemMetrics(0)
    height = GetSystemMetrics(1)
    Window.size = (width, height)
    Window.top = 30
    Window.left = 0
    # Window.fullscreen = True

    # run app
    VoiceContactApp().run()
