import GPUtil
import time
import pygame
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
import threading

def get_gpu_temp():
    try:
        gpus = GPUtil.getGPUs()
        if not gpus:
            return "No GPU found"
        return gpus[0].temperature
    except Exception as e:
        return str(e)

def play_alert_sound():
    pygame.mixer.music.load('alert.mp3')
    pygame.mixer.music.play()

pygame.mixer.init()


fig, ax = plt.subplots()
x_data = deque(maxlen=100)  # Store up to 100 data points
y_data = deque(maxlen=100)
line, = ax.plot([], [], lw=2)
ax.set_ylim(0, 100)  # Set y-axis range based on temperature


alert_threshold = 73

def init():
    ax.set_xlim(0, 100)  # Adjust as needed
    line.set_data(x_data, y_data)
    return line,

def update(frame):
    time.sleep(3)  # Wait 5 seconds before each check
    gpu_temp = get_gpu_temp()
    
    if isinstance(gpu_temp, (int, float)):
        print(f"GPU Temperature: {gpu_temp}°C")
        x_data.append(frame)
        y_data.append(gpu_temp)
        
        if gpu_temp >= alert_threshold:
            print("GPU temperature too high! Playing alert sound.")
            threading.Thread(target=play_alert_sound).start()
    
    line.set_data(x_data, y_data)
    return line,

ani = animation.FuncAnimation(fig, update, init_func=init, interval=1000, blit=True)

plt.xlabel('Time (s)')
plt.ylabel('GPU Temperature (°C)')
plt.title('Real-time GPU Temperature Monitoring')
plt.show()
