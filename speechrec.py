import pyaudio
import wave
import sys

chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()

stream = p.open(format = FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = True,
                frames_per_buffer = chunk)

print "* recording"
frames = []
for i in range(0, RATE / chunk * RECORD_SECONDS):
    data = stream.read(chunk, exception_on_overflow = False)
    frames.append(data)
print "* done recording"

stream.close()
p.terminate()

wf = wave.open("/Users/jayesh/Desktop/"+WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()



########################################################################################################################



from wit import Wit

access_token = 'DHOSKLQAXGNVVPCC3UGXAPZJRCPVTHAY'

client = Wit(access_token)


filepath = '/Users/jayesh/Desktop/output.wav'

resp = None
with open(filepath, 'rb') as f:
    
    resp = client.speech(f, None, {'Content-Type': 'audio/wav'})


print resp