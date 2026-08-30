import tkinter as tk
from tkinter import messagebox
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ==========================================
# Project: Solar Tracking System
# Student:  Shanzay Mujeeb Khan (285)
# Session: 2025-EE (Section A)
# ==========================================

def get_solar_elevation():
    """
    This function calculates the Sun's position based on inputs.
    It uses standard Solar Geometry formulas.
    """
    try:
       lat_text = entry_lat.get()  #Getting input from GUI
       day_text = entry_day.get()
       
       if not lat_text or not day_text:  #checking box
             messagebox.showwarning("Input Error", "Please fill all fields!")
             return
       latitude = float(lat_text)
       day_number = int(day_text)
 
       if day_number < 1 or day_number > 365:  #setting range
           messagebox.showerror("Error", "Day number must be between 1 and 365.")
           return
 
       lat_rad = math.radians(latitude)  #Latitude conversion
       
#Declination Angle (delta)
# Formula: 23.45 * sin(360/365 * (n - 81))        
       inner_angle = (360 / 365) * (day_number - 81)
       delta = 23.45 * math.sin(math.radians(inner_angle))
       delta_rad = math.radians(delta)
             
       
#Elevation/Altitude Angle (Beta)
#Formula: sin(beta) = cos(L)cos(d) + sin(L)sin(d)        
       H=0
       sin_beta = (math.cos(lat_rad) * math.cos(delta_rad) * math.cos(H)) + \
                  (math.sin(lat_rad) * math.sin(delta_rad))
       elevation_angle=math.degrees(math.asin(sin_beta))              
       optimal_tilt = 90 - elevation_angle  
       results=(f"--- Calculation Results ---\n"
                         f"Day Number: {day_number}\n"
                         f"Sun Declination: {delta:.2f}°\n"
                         f"Sun Elevation: {elevation_angle:.2f}°\n"
                         f"Optimal Panel Tilt: {optimal_tilt:.2f}°")
       result_var.set(results)
       update_graph(elevation_angle)
 
    except ValueError:
      messagebox.showerror("Type Error", "Please enter valid numeric values.")
     
def update_graph(angle_deg):
        """
        Visualizes the ground, the sun, and the tracking angle.
        """
        ax.clear() #Clearing plot
        
        angle_rad = math.radians(angle_deg)  #Angle to radian conversion
     
        line_length = 10  #Coordiantes on axis for Sun
        sun_x = line_length * math.cos(angle_rad)  # Base
        sun_y = line_length * math.sin(angle_rad)  # Height
     
        ax.plot([-12, 12], [0, 0], color='brown', linewidth=3, label='Ground')  #Plotting ground
        ax.plot([0, sun_x], [0, sun_y], color='orange', linestyle='--', label='Sun Ray')  #Plotting Sun's Ray
     
        ax.plot(sun_x, sun_y, marker='o', markersize=18, color='yellow',  #Plotting Sun 
         markeredgecolor='orange', label='Sun Position')
     
        panel_size = 2  #Plotting Solar Panel for tracking
        px = panel_size * math.sin(angle_rad)
        py = panel_size * math.cos(angle_rad)
        ax.plot([-px, px], [py, -py], color='blue', linewidth=4, label='Tracker Panel')

        ax.set_title(f"Solar Tracking Visualization (Angle: {angle_deg:.1f}°)")  #Format of Graph
        ax.set_xlim(-12, 12)
        ax.set_ylim(0, 12)
        ax.grid(True, linestyle=':', alpha=0.5)
        ax.legend(loc='upper left', fontsize='small')
        canvas.draw()          
     
# ==========================================
# Main GUI Application Setup
# ==========================================

root = tk.Tk()  #Window
root.title("Solar Tracking System ")
root.geometry("600x650")
root.configure(bg="#f0f0f0")

lbl_title = tk.Label(root, text="Solar Elevation & Tracking System", #Title
                     font=("Helvetica", 16, "bold"), bg="#f0f0f0", fg="#333")
lbl_title.pack(pady=15)

#ALL INPUTS 
input_frame = tk.Frame(root, bg="#f0f0f0")
input_frame.pack(pady=10)

tk.Label(input_frame, text="Latitude (deg):", bg="#f0f0f0", font=("Arial", 11)).grid(row=0, column=0, padx=5) #Latitude
entry_lat = tk.Entry(input_frame, width=12, font=("Arial", 11))
entry_lat.insert(0, "31.55")   #Default:Lahore
entry_lat.grid(row=0, column=1, padx=5)

tk.Label(input_frame, text="Day (1-365):", bg="#f0f0f0", font=("Arial", 11)).grid(row=0, column=2, padx=5)  #Day
entry_day = tk.Entry(input_frame, width=12, font=("Arial", 11))
entry_day.insert(0, "172")   #Default:June 21
entry_day.grid(row=0, column=3, padx=5)

btn_calculate = tk.Button(root, text="Track Sun Position", command=get_solar_elevation,  #Button 
                          bg="#28a745", fg="white", font=("Arial", 12, "bold"), padx=15, pady=5)
btn_calculate.pack(pady=10)

result_var = tk.StringVar()  #RESULT
result_var.set("Enter data and click button...")
lbl_result = tk.Label(root, textvariable=result_var, bg="white", relief="solid", 
                      width=50, height=5, font=("Consolas", 10), justify="left")
lbl_result.pack(pady=10)

fig = plt.Figure(figsize=(5, 4), dpi=100)  #Graphical Figure(matplotlib)
ax = fig.add_subplot(111)

canvas = FigureCanvasTkAgg(fig, root)  #Graphical Figure (tkinter)
canvas.get_tk_widget().pack(pady=5)
root.mainloop()   #keeps window open









