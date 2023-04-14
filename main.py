#python==3.9
import os
import tkinter as tk
import time
import speech_recognition as sr
import wave
import pyaudio
import threading
from tkinter import font


class VoiceRecord:
	def __init__(self, chunk=3024, frmat=pyaudio.paInt16, channels=2, rate=44100, py=pyaudio.PyAudio()):
		self.main = tk.Tk()
		self.main.title("Speechtxt")
		self.main.iconbitmap(r'mic.ico')
		self.text = tk.Text(self.main)
		custom_font = font.Font(family="TakaoPMincho", size=18, weight="bold")
		custom_font_path = "2.ttf"
		self.text.tag_config("custom", font=custom_font)
		self.text.pack()
		self.CHUNK = chunk
		self.FORMAT = frmat
		self.CHANNELS = channels
		self.RATE = rate
		self.p = py
		self.frames = []
		self.st = 0
		self.stream = self.p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)
		self.button = tk.Button(self.main, text="🎙", font=("Arial", 15, "bold"), fg="blue", command=self.click_re)
		self.button.pack()
		self.main.mainloop()

	def click_re(self):
		if self.st:
			self.st = 0
			self.button.config(fg="blue")
			threading.Thread(target=self.pause).start()
		else:
			self.st = 1
			self.button.config(fg="red")
			threading.Thread(target=self.record).start()


	def record(self):
		self.st = 1
		self.frames = []
		stream = self.p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)
		while self.st == 1:
			data = stream.read(self.CHUNK)
			self.frames.append(data)
			print("* recording")
			self.main.update()

		stream.close()


		wf = wave.open("test2.wav", "wb")
		wf.setnchannels(self.CHANNELS)
		wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
		wf.setframerate(self.RATE)
		wf.writeframes(b''.join(self.frames))
		wf.close()

	def pause(self):
		time.sleep(0.1)
		r = sr.Recognizer()
		hello = sr.AudioFile("test2.wav")
		with hello as source:
			audio = r.record(source)
			text1 = r.recognize_google(audio, language="ja")
			self.text.insert(tk.INSERT, text1, "custom")
			threading.Thread(target=self.remove).start()

	def remove(self):
		print("Delete Record!")
		os.remove("test2.wav")


record = VoiceRecord()
