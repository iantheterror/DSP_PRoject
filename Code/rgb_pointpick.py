import cv2
import numpy as np
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk

class RGBAdjustmentApp:
    def __init__(self, window, window_title):


        self.window = window
        self.window.title(window_title)
        
        self.cap = cv2.VideoCapture(0)
        
        # Initialize HSV range variables
        self.red_min = tk.DoubleVar()
        self.red_max = tk.DoubleVar()
        self.green_min = tk.DoubleVar()
        self.green_max = tk.DoubleVar()
        self.blue_min = tk.DoubleVar()
        self.blue_max = tk.DoubleVar()

        self.Rband = tk.DoubleVar()
        self.Gband = tk.DoubleVar()
        self.Bband = tk.DoubleVar()

        self.EN = tk.DoubleVar()
        self.EN.set(0)

        self.Rband.set(20)
        self.Gband.set(20)
        self.Bband.set(20)
        
        # Set default values
        self.red_min.set(0)
        self.red_max.set(255)
        self.green_min.set(0)
        self.green_max.set(255)
        self.blue_min.set(0)
        self.blue_max.set(255)
  
        self.canvas = tk.Canvas(window, width=640, height=480)




        self.click_bandwidth = np.array([int(self.Rband.get()),int(self.Gband.get()),int(self.Bband.get())])
        self.max_rgb= np.array([255,255,255])-self.click_bandwidth
        self.min_rgb = np.array([0,0,0])+self.click_bandwidth
        self.rgb_ret = np.array([255,255,255])

        self.create_widgets()
        self.update_feed()

        self.canvas.bind("<Button-1>", self.on_mouse_click)
        self.canvas.bind("<Button-3>", self.on_mouse_right)
        
        
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_mouse_right(self, event):
        self.red_min.set(0)
        self.red_max.set(255)
        self.green_min.set(0)
        self.green_max.set(255)
        self.blue_min.set(0)
        self.blue_max.set(255)  

    def on_mouse_click(self, event):
        # Handle mouse click event within the canvas
        x, y = event.x, event.y
        img_width, img_height = self.img.size
        scale_x = img_width / self.canvas.winfo_width()
        scale_y = img_height / self.canvas.winfo_height()
        img_x = int(x * scale_x)
        img_y = int(y * scale_y)
        print(img_x,img_y)
        if hasattr(self, 'img'):
            img_array = np.array(self.img)
            bgr_pixel = img_array[img_y, img_x]
            rgb_value = np.uint8([[bgr_pixel]])[0][0]
            self.rgb_ret = [rgb_value[0], rgb_value[1], rgb_value[2]]
            self.bandwidth_rgb()

    def bandwidth_rgb(self):
        self.click_bandwidth = np.array([int(self.Rband.get()),int(self.Gband.get()),int(self.Bband.get())])
        self.max_rgb= np.array([255,255,255])-self.click_bandwidth
        self.min_rgb = np.array([0,0,0])+self.click_bandwidth
        rgb_band = [0,0,0]
        for n in range(len(rgb_band)):
            if self.rgb_ret[n] >= self.max_rgb[n]:
                rgb_band[n] = self.max_rgb[n]
            elif self.rgb_ret[n] <= self.min_rgb[n]:
                rgb_band[n] = self.min_rgb[n]
            else:
                rgb_band[n] = self.rgb_ret[n]

        RGB_upper = rgb_band+self.click_bandwidth
        RGB_lower =rgb_band-self.click_bandwidth

        self.red_min.set(RGB_lower[0])
        self.red_max.set(RGB_upper[0])
        self.green_min.set(RGB_lower[1])
        self.green_max.set(RGB_upper[1])
        self.blue_min.set(RGB_lower[2])
        self.blue_max.set(RGB_upper[2])
        
    def create_widgets(self):
        # Canvas for displaying video feed
        self.canvas = tk.Canvas(self.window, width=640, height=480)
        self.canvas.pack()

        ''' self.band_window =  tk.Toplevel(self.window)
        self.band_window.title("band Sliders")


        self.hue_label = tk.Label(self.band_window, text="Hue bandwidth (1-89):")
        self.hue_label.pack()
        self.hue_slider = tk.Scale(self.band_window, from_=1, to=89, orient=tk.HORIZONTAL, variable=self.Rband, showvalue=1)
        self.hue_slider.pack()

        self.sat_label = tk.Label(self.band_window, text="Sat bandwidth (1-127):")
        self.sat_label.pack()
        self.sat_slider = tk.Scale(self.band_window, from_=1, to=127, orient=tk.HORIZONTAL, variable=self.Gband, showvalue=1)
        self.sat_slider.pack()
        
        self.val_label = tk.Label(self.band_window, text="Val bandwidth (1-127):")
        self.val_label.pack()
        self.val_slider = tk.Scale(self.band_window, from_=1, to=127, orient=tk.HORIZONTAL, variable=self.Bband, showvalue=1)
        self.val_slider.pack()'''


        

        # Create a separate window for sliders
        self.slider_window = tk.Toplevel(self.window)
        self.slider_window.title("RGB Sliders")

        # Hue min slider
        self.red_min_label = tk.Label(self.slider_window, text="Red Min (0-255):")
        self.red_min_label.pack()
        self.red_min_slider = tk.Scale(self.slider_window, from_=0, to=255, orient=tk.HORIZONTAL, variable=self.red_min, showvalue=1)
        self.red_min_slider.pack()

        # Hue max slider
        self.red_max_label = tk.Label(self.slider_window, text="Red Max (0-255):")
        self.red_max_label.pack()
        self.red_max_slider = tk.Scale(self.slider_window, from_=0, to=255, orient=tk.HORIZONTAL, variable=self.red_max, showvalue=1)
        self.red_max_slider.pack()

        # Saturation min slider
        self.green_min_label = tk.Label(self.slider_window, text="Green Min (0-255):")
        self.green_min_label.pack()
        self.green_min_slider = tk.Scale(self.slider_window, from_=0, to=255, orient=tk.HORIZONTAL, variable=self.green_min, showvalue=1)
        self.green_min_slider.pack()

        # Saturation max slider
        self.green_max_label = tk.Label(self.slider_window, text="Green Max (0-255):")
        self.green_max_label.pack()
        self.green_max_slider = tk.Scale(self.slider_window, from_=0, to=255, orient=tk.HORIZONTAL, variable=self.green_max, showvalue=1)
        self.green_max_slider.pack()

        # Value min slider
        self.blue_min_label = tk.Label(self.slider_window, text="Blue Min (0-255):")
        self.blue_min_label.pack()
        self.blue_min_slider = tk.Scale(self.slider_window, from_=0, to=255, orient=tk.HORIZONTAL, variable=self.blue_min, showvalue=1)
        self.blue_min_slider.pack()

        # Value max slider
        self.blue_max_label = tk.Label(self.slider_window, text="Blue Max (0-255):")
        self.blue_max_label.pack()
        self.blue_max_slider = tk.Scale(self.slider_window, from_=0, to=255, orient=tk.HORIZONTAL, variable=self.blue_max, showvalue=1)
        self.blue_max_slider.pack()

        self.hue_label = tk.Label(self.slider_window, text="Red bandwidth (1-89):")
        self.hue_label.pack()
        self.hue_slider = tk.Scale(self.slider_window, from_=1, to=127, orient=tk.HORIZONTAL, variable=self.Rband, showvalue=1)
        self.hue_slider.pack()

        self.sat_label = tk.Label(self.slider_window, text="Green bandwidth (1-127):")
        self.sat_label.pack()
        self.sat_slider = tk.Scale(self.slider_window, from_=1, to=127, orient=tk.HORIZONTAL, variable=self.Gband, showvalue=1)
        self.sat_slider.pack()
        
        self.val_label = tk.Label(self.slider_window, text="Blue bandwidth (1-127):")
        self.val_label.pack()
        self.val_slider = tk.Scale(self.slider_window, from_=1, to=127, orient=tk.HORIZONTAL, variable=self.Bband, showvalue=1)
        self.val_slider.pack()

        self.en_label = tk.Label(self.slider_window, text="Enable Live Bandwidth  0,1:")
        self.en_label.pack()
        self.en_slider = tk.Scale(self.slider_window, from_=0, to=1, orient=tk.HORIZONTAL, variable=self.EN, showvalue=1)
        self.en_slider.pack()


        # Update button

        # Create a separate window for HSV value entries
        self.entry_window = tk.Toplevel(self.window)
        self.entry_window.title("RGB Values")

        # Hue entry
        self.red_min_entry_label = tk.Label(self.entry_window, text="Red Min (0-255):")
        self.red_min_entry_label.grid(row=0, column=0)
        self.red_min_entry = tk.Entry(self.entry_window)
        self.red_min_entry.grid(row=0, column=1)

        self.red_max_entry_label = tk.Label(self.entry_window, text="Red Max (0-255):")
        self.red_max_entry_label.grid(row=1, column=0)
        self.red_max_entry = tk.Entry(self.entry_window)
        self.red_max_entry.grid(row=1, column=1)

        # Saturation entry
        self.green_min_entry_label = tk.Label(self.entry_window, text="Green Min (0-255):")
        self.green_min_entry_label.grid(row=2, column=0)
        self.green_min_entry = tk.Entry(self.entry_window)
        self.green_min_entry.grid(row=2, column=1)

        self.green_max_entry_label = tk.Label(self.entry_window, text="Green Max (0-255):")
        self.green_max_entry_label.grid(row=3, column=0)
        self.green_max_entry = tk.Entry(self.entry_window)
        self.green_max_entry.grid(row=3, column=1)

        # Value entry
        self.blue_min_entry_label = tk.Label(self.entry_window, text="Blue Min (0-255):")
        self.blue_min_entry_label.grid(row=4, column=0)
        self.blue_min_entry = tk.Entry(self.entry_window)
        self.blue_min_entry.grid(row=4, column=1)

        self.blue_max_entry_label = tk.Label(self.entry_window, text="Blue Max (0-255):")
        self.blue_max_entry_label.grid(row=5, column=0)
        self.blue_max_entry = tk.Entry
        self.blue_max_entry = tk.Entry(self.entry_window)
        self.blue_max_entry.grid(row=5, column=1)

    # Update button for RGB values
        self.update_entry_button = tk.Button(self.entry_window, text="Update RGB Values", command=self.update_rgb_entries)
        self.update_entry_button.grid(row=6, columnspan=2)

    def update_rgb_entries(self):
        # Get RGB values from entry fields
        red_min = int(self.red_min_entry.get())
        red_max = int(self.red_max_entry.get())
        green_min = int(self.green_min_entry.get())
        green_max = int(self.green_max_entry.get())
        blue_min = int(self.blue_min_entry.get())
        blue_max = int(self.blue_max_entry.get())

        # Update slider values
        self.red_min_slider.set(red_min)
        self.red_max_slider.set(red_max)
        self.green_min_slider.set(green_min)
        self.green_max_slider.set(green_max)
        self.blue_min_slider.set(blue_min)
        self.blue_max_slider.set(blue_max)

        # Update labels (optional)
        self.update_red_label(red_min, red_max)
        self.update_green_label(green_min, green_max)
        self.update_blue_label(blue_min, blue_max)

    def update_feed(self):
        ret, frame = self.cap.read()

        if ret:
            if int(self.EN.get())== 1:
                self.bandwidth_rgb()
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Get RGB range values from sliders
            red_min = int(self.red_min.get())
            red_max = int(self.red_max.get())
            green_min = int(self.green_min.get())
            green_max = int(self.green_max.get())
            blue_min = int(self.blue_min.get())
            blue_max = int(self.blue_max.get())
            
            # Apply RGB range filter
            lower_bound = np.array([red_min, green_min, blue_min])
            upper_bound = np.array([red_max, green_max, blue_max])
            mask = cv2.inRange(frame_rgb, lower_bound, upper_bound)
            result = cv2.bitwise_and(frame, frame, mask=mask)
            
            # Convert image format
            img = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, (640, 480))
            img = Image.fromarray(img)
            self.img = img
            imgtk = ImageTk.PhotoImage(image=img)
            
            # Update canvas with filtered image
            self.canvas.imgtk = imgtk
            self.canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)
            
        # Repeat the update process
        self.window.after(10, self.update_feed)


    def update_rgb_values(self):
        # This function updates the HSV values based on slider positions
        
        # Get HSV range values from sliders
        red_min = int(self.red_min.get())
        red_max = int(self.red_max.get())
        green_min = int(self.green_min.get())
        green_max = int(self.green_max.get())
        blue_min = int(self.blue_min.get())
        blue_max = int(self.blue_max.get())
        
        # Update sliders
        self.red_min.set(red_min)
        self.red_max.set(red_max)
        self.green_min.set(green_min)
        self.green_max.set(green_max)
        self.blue_min.set(blue_min)
        self.blue_max.set(blue_max)
        
    def on_closing(self):
        # This function is called when the window is closed
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.cap.release()
            self.window.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = RGBAdjustmentApp(root, "RGB Adjustment")
    root.mainloop()
