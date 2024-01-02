# from vidstream import AudioReceiver, AudioSender
from audio import AudioReceiver, AudioSender

HOST = '0.0.0.0'
PORT = 9999

print('Host:', HOST)

receiver = AudioReceiver(HOST, PORT, 100)
receiver.start_server()
 
# while True:
#     print(receiver.getRunning())
#input('press enter to stop')
#receiver.stop_server()
