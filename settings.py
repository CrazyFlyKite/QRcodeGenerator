from tkinter.messagebox import showinfo

# Window settings
title: str = 'QRcode Generator'
icon: str = 'QR code.ico'
width: int = 500
height: int = 300
resizable: bool = False

# Default values
default_format: str = '.jpg'
default_size: int = 500
default_foreground_color: str = 'black'
default_background_color: str = 'white'

# Instructions
instructions = '''
        Instructions:
        - Enter the data to encode in the QR code.
        - Select the desired file format.
        - Enter the size for the QR code image.
        - Click the 'Generate' to generate and save the QR code.

        Some color combinations can alter the appearance of a QR code significantly.
        Please choose FG and BG colors carefully.

        Supported file formats:
        - PNG, JPG, JPEG, GIF, BMP
        '''

def display_instructions():
    showinfo('Instructions', instructions)