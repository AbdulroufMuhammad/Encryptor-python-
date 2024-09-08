import PyPDF2
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class CaesarCipher:
    def __init__(, shift=3):
        self.shift = shift
    
    def encrypt_char(self, char):
        if char.isupper():  
            return chr((ord(char) + self.shift - 65) % 26 + 65)
        elif char.islower():  
            return chr((ord(char) + self.shift - 97) % 26 + 97)
        else:
            return char

    def encrypt_text(self, text):
        return ''.join([self.encrypt_char(c) for c in text])

class CaesarCipherDecryptor:
    def __init__(self, shift=3):
        self.shift = shift
    
    def decrypt_char(self, char):
        if char.isupper():  
            return chr((ord(char) - self.shift - 65) % 26 + 65)
        elif char.islower():  
            return chr((ord(char) - self.shift - 97) % 26 + 97)
        else:
            return char

    def decrypt_text(self, text):
        return ''.join([self.decrypt_char(c) for c in text])

class PDFEncryptor:
    def __init__(self, input_pdf_path, output_pdf_path):
        self.input_pdf_path = input_pdf_path
        self.output_pdf_path = output_pdf_path
        self.cipher = CaesarCipher(shift=3)

    def encrypt_pdf(self):
        with open(self.input_pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)

            encrypted_text = ""
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                page_text = page.extract_text()
                encrypted_text += self.cipher.encrypt_text(page_text)

        c = canvas.Canvas(self.output_pdf_path, pagesize=letter)

        text_lines = self.wrap_text(encrypted_text, 90)
        y_position = 750

        for line in text_lines:
            c.drawString(100, y_position, line)
            y_position -= 15

            if y_position < 50:
                c.showPage()
                y_position = 750

        c.save()

    def wrap_text(self, text, max_line_length):
        words = text.split(' ')
        lines = []
        current_line = ""

        for word in words:
            if len(current_line + word) <= max_line_length:
                current_line += word + " "
            else:
                lines.append(current_line.strip())
                current_line = word + " "

        if current_line:
            lines.append(current_line.strip())

        return lines

class PDFDecryptor:
    def __init__(self, input_pdf_path, output_pdf_path):
        self.input_pdf_path = input_pdf_path
        self.output_pdf_path = output_pdf_path
        self.cipher = CaesarCipherDecryptor(shift=3)

    def decrypt_pdf(self):
        with open(self.input_pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)

            decrypted_text = ""
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                encrypted_text = page.extract_text()
                decrypted_text += self.cipher.decrypt_text(encrypted_text)

        c = canvas.Canvas(self.output_pdf_path, pagesize=letter)

        text_lines = self.wrap_text(decrypted_text, 90)
        y_position = 750

        for line in text_lines:
            c.drawString(100, y_position, line)
            y_position -= 15

            if y_position < 50:
                c.showPage()
                y_position = 750

        c.save()

    def wrap_text(self, text, max_line_length):
        words = text.split(' ')
        lines = []
        current_line = ""

        for word in words:
            if len(current_line + word) <= max_line_length:
                current_line += word + " "
            else:
                lines.append(current_line.strip())
                current_line = word + " "

        if current_line:
            lines.append(current_line.strip())

        return lines

if __name__ == "__main__":
    encryptor = PDFEncryptor('AbdulroufmuhammadCV.pdf', 'encrypted_output.pdf')
    encryptor.encrypt_pdf()

    decryptor = PDFDecryptor('encrypted_output.pdf', 'decrypted_output.pdf')
    decryptor.decrypt_pdf()