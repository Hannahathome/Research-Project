import serial
import threading 
from time import sleep 
from pynput import keyboard
from dataclasses import dataclass
from datetime import datetime

#Make a class to neatly contain all the data needed
@dataclass
class data:
	#Everything has default values
	thread_delay: float = 5.0
	counter: int = 0
	total_counter: int = 0
	average_counter: float = 0.0
	number_of_resets: int = 0

class myThread(threading.Thread):
	def __init__(self, threadID, name, data):
		threading.Thread.__init__(self)
		self.ser = serial.Serial('COM5', 9600)
		#self.time.sleep(2) 
		self.threadID = threadID
		self.name = name
		self.data = data
		self.filename = "Log_Data" + datetime.now().strftime('_%Y-%m-%d_%H-%M-%S') + ".txt"
		self.keep_going = False
		self.last_runtime = datetime.now()
		
	def write_to_file(self):
		self.log_file = open(self.filename, "a+")
		self.log_file.write ("====================================\n")
		self.log_file.write ("Log number: {}\n".format(self.data.number_of_resets))
		self.log_file.write ("Current keypresses before reset: {}\n".format(self.data.counter))
		self.log_file.write ("Total keypresses before reset: {}\n".format(self.data.total_counter))
		self.log_file.write ("Average keypresses in {} seconds: {}\n".format(self.data.thread_delay, self.data.average_counter))
		self.log_file.write ("====================================\n")
		print (self.data.counter)
		self.ser.write(str(self.data.counter).encode())
		self.log_file.close()
	def write_final_to_file(self):
		if self.data.number_of_resets == 0:
				self.data.average_counter = self.data.total_counter
		else:
			self.data.average_counter = self.data.total_counter / self.data.number_of_resets
		self.log_file = open(self.filename, "r+")
		old_log_file = self.log_file.read() 
		self.log_file.seek(0)
		self.log_file.write ("Final log\n")
		self.log_file.write ("Log number: {}\n".format(self.data.number_of_resets))
		self.log_file.write ("Current keypresses before reset: {}\n".format(self.data.counter))
		self.log_file.write ("Total keypresses before reset: {}\n".format(self.data.total_counter))
		self.log_file.write ("Average keypresses in {} seconds: {}\n".format(self.data.thread_delay, self.data.average_counter))	
		self.log_file.write("\n")
		self.log_file.write(old_log_file)
		self.log_file.close()
	def run(self):
		#2 is based on main thread and this thread
		self.log_file = open(self.filename, "a+")
		self.log_file.close()
		while self.keep_going == False:
			if (datetime.now() - self.last_runtime).total_seconds() > self.data.thread_delay:
                                if self.data.number_of_resets == 0:
                                        self.data.average_counter = self.data.total_counter
                                else:
                                        self.data.average_counter = self.data.total_counter / self.data.number_of_resets
                                self.write_to_file()
                                print ("====================================")
                                print ("Current keypresses before reset: {}".format(self.data.counter))
                                print ("Total keypresses before reset: {}".format(self.data.total_counter))
                                print ("Number of resets in total: {}".format(self.data.number_of_resets))
                                print ("Average keypresses in {} seconds: {}".format(self.data.thread_delay, self.data.average_counter))
                                print ("====================================")
                                print ()
                                # Reset some variables 
                                self.data.counter = 0 
                                self.data.number_of_resets += 1
                                self.last_runtime = datetime.now()
	def stop(self):
		self.keep_going = True
	
	
def on_press(key):
	global program_data 
	program_data.counter += 1
	program_data.total_counter += 1
	try:
		key_pressed = key.char    
		print('Key {0} pressed'.format(key_pressed))
		
	except AttributeError:
		key_pressed = key
		print('Key {0} pressed not send to serial'.format(key_pressed))        


def on_release(key):
	if key == keyboard.Key.esc:
		return False

#Create an instance of the dataclass. We only need to give the time of the thread delay as the otehr need to have a standard value of 0 on initialization of the program
program_data = data(300.0)
listener_thread = keyboard.Listener(on_press = on_press, on_release = on_release)
data_printer_thread = myThread(1, "Data printer thread", program_data)

#=====Main=====
#Run keyboard listener
listener_thread.start()
data_printer_thread.start()
try:
	listener_thread.wait()
	listener_thread.join()
finally:
	listener_thread.stop()
	data_printer_thread.write_final_to_file()
	data_printer_thread.stop()
