import qrcode
import qrcode.image.svg
from tkinter import Tk, Label, Entry, Button, LabelFrame, filedialog, colorchooser, Listbox, messagebox
from tkinter.ttk import Combobox
from PIL import Image
import pickle

class QRcodeGenerator:
    def __init__(self):
        # Initialize variables
        self.root = Tk()
        self.foreground_color = 'black'
        self.background_color = 'white'
        self.history = []

        # Initialize UI elements
        self.data_label = Label()
        self.format_label = Label()
        self.size_label = Label()
        self.background_label = Label()
        self.foreground_label = Label()
        self.generate_button = Button()
        self.instructions_button = Button()
        self.clear_button = Button()
        self.data_entry = Entry()
        self.size_entry = Entry()
        self.file_format = Combobox()
        self.history_listbox = Listbox()
        self.history_frame = LabelFrame()
        self.generator_frame = LabelFrame()

        # Setup UI
        self.setup_UI()

    def setup_UI(self):         # Function for setuping Window and UI elements
        # Setup Window
        self.root.title('QRcode Generator')
        self.root.geometry('500x300')
        self.root.resizable(False, False)
        self.root.iconbitmap("QR code.ico")

        # Setup UI elements
        self.history_frame = LabelFrame(self.root, text='History', width=30)
        self.generator_frame = LabelFrame(self.root, text='Generator')

        self.data_label = Label(self.generator_frame, text='Data')
        self.format_label = Label(self.generator_frame, text='Format')
        self.size_label = Label(self.generator_frame, text='Size')

        self.background_label = Label(self.generator_frame, text='Background', bg='white', padx=10, pady=5)
        self.foreground_label = Label(self.generator_frame, text='Foreground', bg='black', fg='white', padx=10, pady=5)
        self.background_label.bind('<Button-1>', lambda event: self.choose_background_color())
        self.foreground_label.bind('<Button-1>', lambda event: self.choose_foreground_color())

        self.generate_button = Button(self.generator_frame, text='Generate', command=self.generate_qrcode)
        self.instructions_button = Button(self.generator_frame, text='Instructions', command=self.display_instructions)
        self.clear_button = Button(self.history_frame, text='Clear All', command=self.clear_history)

        self.data_entry = Entry(self.generator_frame)
        self.size_entry = Entry(self.generator_frame)
        self.size_entry.insert(0, '250')

        self.file_format = Combobox(self.generator_frame, values=['.png', '.jpg', '.jpeg', '.gif', '.bmp'], state='readonly')
        self.file_format.set('.jpg')

        self.history_listbox = Listbox(self.history_frame)
        self.history_listbox.bind('<Double-Button-1>', self.select_history_item)

        # Pack UI elements
        self.generator_frame.pack(side='left', padx=10, pady=10, fill='both', expand=True)
        self.history_frame.pack(side='right', padx=10, pady=10, fill='both', expand=True)

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

    def generate_qrcode(self):      # Function for generating QR codes
        data = self.data_entry.get()
        file_format_selected = self.file_format.get()

        try:
            size = int(self.size_entry.get())
            if size <= 0:
                messagebox.showwarning('Error', 'Please enter a valid size (positive integer).')
                return
        except ValueError:
            messagebox.showwarning('Error', 'Please enter a valid size (positive integer).')
            return

        if not data:
            messagebox.showwarning('Error', 'Please enter data.')
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
            self.history_listbox.insert('end', data)
            self.save_history()
        except Exception as exception:
            messagebox.showerror('Error', f'Something went wrong: {str(exception)}')

    @staticmethod
    def display_instructions():         # Function for displaying instructions
        instructions = """
        Instructions:
        - Enter the data to encode in the QR code.
        - Select the desired file format.
        - Enter the size for the QR code image.
        - Click the 'Generate' to generate and save the QR code.

        Some color combinations can alter the appearance of a QR code significantly.
        Please choose FG and BG colors carefully.

        Supported file formats:
        - PNG, JPG, JPEG, GIF, BMP
        """

        messagebox.showinfo('Instructions', instructions)

    def choose_background_color(self):          # Function for choosing the background color of the QR code
        color = colorchooser.askcolor()[1]
        if color:
            self.background_label.configure(bg=color)
            self.background_color = color

    def choose_foreground_color(self):          # Function for choosing the foreground color of the QR code
        color = colorchooser.askcolor()[1]
        if color:
            self.foreground_label.configure(bg=color)
            self.foreground_color = color

    def select_history_item(self, event):        # Function for selecting items from the History
        selected_index = self.history_listbox.curselection()
        if selected_index:
            data = self.history[selected_index[0]]
            response = messagebox.askquestion('Confirm', f"Do you want to enter this data: {data}, to the Generator?")
            if response == 'yes':
                self.data_entry.delete(0, 'end')
                self.data_entry.insert('end', data)

    def save_history(self):         # Function for saving the History to "history.pickle"
        with open('history.pickle', 'wb') as file:
            pickle.dump(self.history, file)

    def load_history(self):         # Function for loading History from "history.pickle"
        try:
            with open('history.pickle', 'rb') as file:
                self.history = pickle.load(file)
                self.history_listbox.delete(0, 'end')
                for item in self.history:
                    self.history_listbox.insert('end', item)
        except FileNotFoundError:
            return

    def clear_history(self):            # Function for clearing all from the History
        self.history = []
        self.history_listbox.delete(0, 'end')
        self.save_history()

    def run(self):       # Function for running the App
        self.root.mainloop()

# Running the App
if __name__ == '__main__':
    generator = QRcodeGenerator()
    generator.run()
