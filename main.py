import tkinter as tk
from tkinter import filedialog, messagebox
import PyPDF2
import os

class PDFEditorApp:
    def __init__(self, master):
        self.master = master
        master.title("PDF Page Editor")
        master.geometry("400x400")
        master.config(bg="#f0f0f0")  # Light grey background

        self.label = tk.Label(master, text="Select a PDF file:", bg="#f0f0f0", font=("Arial", 14))
        self.label.pack(pady=10)

        self.select_button = tk.Button(master, text="Browse", command=self.load_pdf, bg="#4CAF50", fg="white", font=("Arial", 12))
        self.select_button.pack(pady=5)

        self.file_display = tk.Label(master, text="", wraplength=350, bg="#f0f0f0", font=("Arial", 10))
        self.file_display.pack(pady=10)

        self.page_label = tk.Label(master, text="Page numbers to delete (comma-separated):", bg="#f0f0f0", font=("Arial", 12))
        self.page_label.pack(pady=10)

        self.page_entry = tk.Entry(master, font=("Arial", 12))
        self.page_entry.pack(pady=5)

        self.delete_button = tk.Button(master, text="Delete Pages", command=self.delete_pages, bg="#FF5722", fg="white", font=("Arial", 12))
        self.delete_button.pack(pady=10)

        self.extract_label = tk.Label(master, text="Page numbers to extract (comma-separated):", bg="#f0f0f0", font=("Arial", 12))
        self.extract_label.pack(pady=10)

        self.extract_entry = tk.Entry(master, font=("Arial", 12))
        self.extract_entry.pack(pady=5)

        self.extract_button = tk.Button(master, text="Extract Pages", command=self.extract_pages, bg="#2196F3", fg="white", font=("Arial", 12))
        self.extract_button.pack(pady=5)

        self.file_path = None
        self.extracted_file_path = None  # Variable to hold the extracted file path
        self.deleted_pdf_counter = 1  # Counter for deleted PDF naming
        self.extracted_pdf_counter = 1  # Counter for extracted PDF naming

    def load_pdf(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if self.file_path:
            file_name = os.path.basename(self.file_path)  # Get the file name from the full path
            self.file_display.config(text=f"Selected File: {file_name}")  # Display only the file name

    def delete_pages(self):
        if not self.file_path:
            messagebox.showwarning("No File", "Please select a PDF file first.")
            return

        try:
            page_numbers = self.page_entry.get().split(',')
            page_numbers = [int(num.strip()) for num in page_numbers if num.strip().isdigit()]

            if any(num < 1 for num in page_numbers):
                raise ValueError("Page numbers must be positive.")

            pdf_reader = PyPDF2.PdfReader(self.file_path)
            total_pages = len(pdf_reader.pages)

            if any(num > total_pages for num in page_numbers):
                raise ValueError("One or more page numbers exceed total pages.")

            pdf_writer = PyPDF2.PdfWriter()

            for i in range(total_pages):
                if i + 1 not in page_numbers:  # Skip the pages to delete
                    pdf_writer.add_page(pdf_reader.pages[i])

            # Generate a unique file name for the deleted PDF
            base_filename = "deleted"
            self.deleted_pdf_counter = 1  # Reset counter for new naming
            deleted_file_path = f"{base_filename}_{self.deleted_pdf_counter}.pdf"

            # Ensure the file name is unique
            while os.path.exists(deleted_file_path):
                self.deleted_pdf_counter += 1
                deleted_file_path = f"{base_filename}_{self.deleted_pdf_counter}.pdf"

            # Save the modified PDF to a new location
            with open(deleted_file_path, 'wb') as output_pdf:
                pdf_writer.write(output_pdf)

            messagebox.showinfo("Success", "Pages deleted successfully!")
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def extract_pages(self):
        if not self.file_path:
            messagebox.showwarning("No File", "Please select a PDF file first.")
            return

        try:
            page_numbers = self.extract_entry.get().split(',')
            page_numbers = [int(num.strip()) for num in page_numbers if num.strip().isdigit()]

            if any(num < 1 for num in page_numbers):
                raise ValueError("Page numbers must be positive.")

            pdf_reader = PyPDF2.PdfReader(self.file_path)
            total_pages = len(pdf_reader.pages)

            if any(num > total_pages for num in page_numbers):
                raise ValueError("One or more page numbers exceed total pages.")

            pdf_writer = PyPDF2.PdfWriter()

            # Loop through the page numbers to extract the specified pages
            for num in page_numbers:
                pdf_writer.add_page(pdf_reader.pages[num - 1])  # Convert to 0-based index

            # Generate a unique file name for the extracted PDF
            base_filename = "extracted"
            self.extracted_pdf_counter = 1  # Reset counter for new naming
            extracted_file_path = f"{base_filename}_{self.extracted_pdf_counter}.pdf"

            # Ensure the file name is unique
            while os.path.exists(extracted_file_path):
                self.extracted_pdf_counter += 1
                extracted_file_path = f"{base_filename}_{self.extracted_pdf_counter}.pdf"

            # Save the extracted pages to a new PDF
            with open(extracted_file_path, 'wb') as output_pdf:
                pdf_writer.write(output_pdf)

            messagebox.showinfo("Success", "Pages extracted successfully!")
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFEditorApp(root)
    root.mainloop()