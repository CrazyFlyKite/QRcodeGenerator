import qrcode
import tkinter as tk
from tkinter.ttk import Combobox
from tkinter import messagebox, filedialog
from PIL import Image
import pickle
from settings import *

class QRcodeGenerator:
    def __init__(self):
        # Initialize variables
        self.root = tk.Tk()
        self.foreground_color = default_foreground_color
        self.background_color = default_background_color
        self.history = list()

        # Initialize UI elements
        self.data_label = tk.Label()
        self.format_label = tk.Label()
        self.size_label = tk.Label()
        self.background_label = tk.Label()
        self.foreground_label = tk.Label()
        self.generate_button = tk.Button()
        self.instructions_button = tk.Button()
        self.clear_button = tk.Button()
        self.data_entry = tk.Entry()
        self.size_entry = tk.Entry()
        self.file_format = Combobox()
        self.history_listbox = tk.Listbox()
        self.history_frame = tk.LabelFrame()
        self.generator_frame = tk.LabelFrame()

    def setup_UI(self):
        # Setup Window
        self.root.title(title)
        self.root.geometry(f'{width}x{height}')
        self.root.resizable(resizable, resizable)
        self.root.iconbitmap(icon)

        # Setup UI elements
        self.history_frame = tk.LabelFrame(self.root, text='History', width=30)
        self.generator_frame = tk.LabelFrame(self.root, text='Generator')

        self.data_label = tk.Label(self.generator_frame, text='Data')
        self.format_label = tk.Label(self.generator_frame, text='Format')
        self.size_label = tk.Label(self.generator_frame, text='Size')
        self.background_label = tk.Label(self.generator_frame, text='Background', bg='white', padx=10, pady=5)
        self.foreground_label = tk.Label(self.generator_frame, text='Foreground', bg='black', fg='white', padx=10, pady=5)
        self.generate_button = tk.Button(self.generator_frame, text='Generate', command=self.generate_qrcode)
        self.instructions_button = tk.Button(self.generator_frame, text='Instructions', command=display_instructions)
        self.clear_button = tk.Button(self.history_frame, text='Clear all', command=self.clear_history)
        self.data_entry = tk.Entry(self.generator_frame)
        self.size_entry = tk.Entry(self.generator_frame)
        self.file_format = Combobox(self.generator_frame, values=['.png', '.jpg', '.jpeg', '.gif', '.bmp'], state='readonly')
        self.history_listbox = tk.Listbox(self.history_frame)

        # Bind and set UI elements
        self.file_format.set(default_format)
        self.size_entry.insert(0, default_size)
        self.history_listbox.bind('<Double-Button-1>', self.select_history_item)
        self.background_label.bind('<Button-1>', lambda event: self.choose_background_color())
        self.foreground_label.bind('<Button-1>', lambda event: self.choose_foreground_color())

        # Pack UI elements
        self.generator_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.history_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.history_listbox.pack(pady=10)
        self.clear_button.pack(pady=10)

        self.data_label.grid(row=0, column=0, sticky='w', padx=10, pady=3)
        self.data_entry.grid(row=0, column=1, padx=10, pady=3)
        self.format_label.grid(row=1, column=0, sticky='w', padx=10, pady=3)
        self.file_format.grid(row=1, column=1, padx=10, pady=3)
        self.size_label.grid(row=2, column=0, sticky='w', padx=10, pady=3)
        self.size_entry.grid(row=2, column=1, padx=10, pady=3)
        self.background_label.grid(row=3, column=1, padx=10, pady=6)
        self.foreground_label.grid(row=4, column=1, padx=10, pady=6)
        self.generate_button.grid(row=5, column=1, pady=3)
        self.instructions_button.grid(row=6, column=1, pady=4)

        # Load History
        self.load_history()

    def generate_qrcode(self):
        data = self.data_entry.get()
        file_format_selected = self.file_format.get()

        # Set size of the QR code
        try:
            size = int(self.size_entry.get())
            if size <= 0:
                messagebox.showwarning('Error', 'Please enter a valid size (positive integer).')
                return
        except ValueError:
            messagebox.showwarning('Error', 'Please enter a valid size.')
            return

        if not data:
            messagebox.showwarning('Error', 'Data field is empty.')
            return

        if not file_format_selected:
            messagebox.showwarning('Error', 'Please select a file format.')
            return

        try:
            # Generating the QR code
            code = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_Q, box_size=10, border=1)
            code.add_data(data)
            code.make(fit=True)
            image = code.make_image(fill_color=self.foreground_color, back_color=self.background_color)

            qr_image = image.resize((int(size), int(size)))

            canvas = Image.new('RGB', (int(size), int(size)), 'white')
            canvas.paste(qr_image)

            file_path = filedialog.asksaveasfilename(defaultextension=file_format_selected, filetypes=[('Image Files', '*' + file_format_selected)])
            if not file_path:
                return

            canvas.save(file_path)

            messagebox.showinfo('Success', f'QR code saved as {file_path}')

            self.history.append(data)
            self.history_listbox.insert(tk.END, data)
            self.save_history()
        except Exception as exception:
            messagebox.showerror('Error', f'Something went wrong: {str(exception)}')

    def choose_background_color(self):
        # Ask for background color of the QR code
        color = colorchooser.askcolor()[1]
        if color:
            self.background_label.configure(bg=color)
            self.background_color = color

    def choose_foreground_color(self):
        # Ask for foreground color of the QR code
        color = colorchooser.askcolor()[1]
        if color:
            self.foreground_label.configure(bg=color)
            self.foreground_color = color

    def select_history_item(self, event):
        selected_index = self.history_listbox.curselection()
        if selected_index:
            data = self.history[selected_index[0]]
            response = messagebox.askquestion('Confirm', f"Do you want to enter \"{data}\" to the Generator?")
            if response == 'yes':
                self.data_entry.delete(0, tk.END)
                self.data_entry.insert(tk.END, data)

    def save_history(self):
        # Save History to "history.pickle"
        with open('history.pickle', 'wb') as file:
            pickle.dump(self.history, file)

    def load_history(self):
        # Load History to "history.pickle"
        try:
            with open('history.pickle', 'rb') as file:
                self.history = pickle.load(file)
                self.history_listbox.delete(0, tk.END)
                for item in self.history:
                    self.history_listbox.insert(tk.END, item)
        except FileNotFoundError:
            return

    def clear_history(self):
        # Clear History
        self.history = []
        self.history_listbox.delete(0, tk.END)
        self.save_history()

    def run(self):
        self.setup_UI()
        self.root.mainloop()

# Running the App
if __name__ == '__main__':
    generator = QRcodeGenerator()
    generator.run()
