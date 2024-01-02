import socket
import pyaudio
import select
import threading

speaking = 0

class AudioSender:
    def __init__(self, host, port, audio_format=pyaudio.paInt32, channels=1, rate=44100, frame_chunk=800):
        self.__host = host
        self.__port = port

        self.__audio_format = audio_format
        self.__channels = channels
        self.__rate = rate
        self.__frame_chunk = frame_chunk

        self.__sending_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__audio = pyaudio.PyAudio()

        self.__running = False
        self.connected = False

    def start_stream(self, tone):
        self.tone = tone
        if self.__running:
            print("Already streaming")
        else:
            # try:
            #     self.__sending_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #     self.__sending_socket.connect((self.__host, self.__port))
            #     self.__stream = self.__audio.open(format=self.__audio_format, channels=self.__channels, rate=self.__rate, input=True, frames_per_buffer=self.__frame_chunk)
            #     self.connected = True
            # except: pass
            print("Start streaming ...")
            # speaker,connected = ClientConnection(self.__host , 7777).check("-", 0)
            thread = threading.Thread(target=self.__client_streaming)
            thread.start()

    def stop_stream(self):
        if self.__running:
            self.__running = False
            self.connected = False
            # self.__sending_socket.close()
        else:
            print("Client not streaming")
        self.connected = False
        print("streaming stop ")

    def __client_streaming(self):
        try:
            speaker,connected = ClientConnection(self.__host , 7777).check("-", 0)
            self.__sending_socket.connect((self.__host, self.__port))
            self.__stream = self.__audio.open(format=self.__audio_format, channels=self.__channels, rate=self.__rate, input=True, frames_per_buffer=self.__frame_chunk)
            self.connected = True
            self.__running = True
            if(self.tone!=0): self.__sending_socket.send("#".encode())
            else : self.__sending_socket.send("$".encode())

            while self.__running:
                try:
                    voice = self.__stream.read(self.__frame_chunk)
                    if (voice): self.__sending_socket.send(voice)
                except Exception as e: 
                    print("Exception 1 : " , e)
                    self.__running = False
                    self.connected = False

        except Exception as e:
            print("Exception_ : " , e)
            self.connected = False
            self.__running = False


class AudioReceiver:
    def __init__(self, host, port, slots=8, audio_format=pyaudio.paInt32, channels=1, rate=44100, frame_chunk=800):
        self.__host = host
        self.__port = port

        self.__slots = slots
        self.__used_slots = 0

        self.__audio_format = audio_format
        self.__channels = channels
        self.__rate = rate
        self.__frame_chunk = frame_chunk

        self.__audio = pyaudio.PyAudio()

        self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__server_socket.bind((self.__host, self.__port))
        
        self.__block = threading.Lock()
        self.__running = False

        self.__client = None

    def check_client(self) -> bool:
        if(self.__client):
            try:
                self.__client.settimeout(3)
                data = self.__client.send("1".encode())
                return True
            except Exception as e:
                return False
        return False
    
    def is_socket_closed(self) -> bool:
        try:
            data = self.__server_socket.recv(16, socket.MSG_DONTWAIT | socket.MSG_PEEK)
            if len(data) == 0:
                return True
        except BlockingIOError:
            return False  # socket is open and reading from it would block
        except ConnectionResetError:
            return True  # socket was closed for some other reason
        except Exception as e:
            return False
        return False

    def isRunning(self):
        return self.__running

    def start_server(self):
        if self.__running:
            print("Audio server is running already")
        else:
            self.__running = True
            self.__stream = self.__audio.open(format=self.__audio_format, channels=self.__channels, rate=self.__rate, output=True, frames_per_buffer=self.__frame_chunk)
            thread = threading.Thread(target=self.__server_listening)
            thread.start()

    def getRunning(self):
        return self.__running

    def __server_listening(self):
        self.__server_socket.listen()
        while self.__running:
            print("waiting for client")
            self.__block.acquire()
            connection, address = self.__server_socket.accept()
            self.__client = connection
            print("connected === " + str(address))
            self.__block.release()
            thread = threading.Thread(target=self.__client_connection, args=(connection, address,))
            thread.start()

    def __client_connection(self, connection, address):
        while self.__running:
            try:
                if (connection):
                    data = connection.recv(self.__frame_chunk)
                    self.__stream.write(data)
            except Exception as e: 
                print("__client_connection | Exception : " , str(e))
                self.__client = None

    def stop_server(self):
        if self.__running:
            self.__running = False
            closing_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            closing_connection.connect((self.__host, self.__port))
            closing_connection.close()
            self.__block.acquire()
            self.__server_socket.close()
            self.__block.release()
        else:
            print("Server not running!")


class ServerConnection:

    def __init__(self, host, port):
        self.__host = host
        self.__port = port

        self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__server_socket.bind((self.__host, self.__port))
        
        self.__block = threading.Lock()
        self.__running = False
        self.__client = None
        self.__speaker = 0

    def start_server(self):
        self.__server_socket.listen()
        while True:
            print("waiting for client")
            self.__block.acquire()
            connection, address = self.__server_socket.accept()

            print("connected === " + str(address))

            self.__block.release()

            if (connection):
                data = str(self.__speaker).encode()
                connection.send(data)
                connection.close()


class ClientConnection:
    def __init__(self, host, port):
        self.__host = host
        self.__port = port

    def check(self, room_name, tone_enable):
            data = "0"
            # print("host: ", self.__host)
            # print(room_name)
            # print("enable tone : ", tone_enable)
            try:
                # print("start")
                self.__client_socket = socket.socket()
                self.__client_socket.settimeout(2)
                self.__client_socket.connect((self.__host, self.__port))
                data_to_send = str(room_name) + ":" + str(tone_enable)
                # print(data_to_send)
                self.__client_socket.sendall(data_to_send.encode())
                # print("sent!")
                data = self.__client_socket.recv(1024).decode()
                # print("receive : " , data)
                self.__client_socket.close() 
                connected = True
            except Exception as e:
                print("ClientConnection check | Exception : " , e)
                data = "0"
                connected = False
            
            if (data=="1"): speaker = True
            else: speaker = False

            return speaker, connected 