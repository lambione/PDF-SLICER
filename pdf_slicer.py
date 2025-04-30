from PyPDF2 import PdfReader, PdfWriter
import tkinter as tk
from tkinter import filedialog, messagebox

# NOTE: Remember to pip install the following! 
# pip install PyPDF2
# pip install pypdf

def parse_page_range(pages_range):
    # NOTE:  range_str is of the form i.e 1-5,6-7
    pages = set()
    for range_set in pages_range.split(','):
        # NOTE: If there is a '-' it means it is a range of pages
        if '-' in range_set:
            # NOTE: simply transforms the two str numbers into int
            start,end = map(int,range_set.split('-'))
            # NOTE: adds multiple elements to the set i.e range(3,6) adds 3,4,5
            pages.update(range(start,end+1))
        else :
            pages.add(int(range_set))
    # NOTE: return a list of pages
    return sorted(pages)

def select_pdf():

    # NOTE: THE DIALOG IS THE POPUPPP!!
    filepath = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if filepath:
        # NOTE: set the path in thinker 
        pdf_path.set(filepath)

def slice_pdf():
    try:
        # NOTE: get pages to attach together and the pdf and instantiate a new pdf instance
        pages = parse_page_range(page_range.get())
        reader = PdfReader(pdf_path.get())
        writer = PdfWriter()

        # NOTE: Add the selected pages to the output pdf
        for p in pages:
            # NOTE: if that page is in the pdf then add it to the output one
            if p-1 < len(reader.pages):
                writer.add_page(reader.pages[p-1])
        
        # NOTE: THE DIALOG IS THE POPUPPP!! -> used to ask the user where he wants to save it 
        output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if output_path:
            # NOTE: save the pdf
            with open(output_path, "wb") as f:
                writer.write(f)
            # NOTE: warn user that the process was successfull!!
            messagebox.showinfo("Success", "PDF sliced and saved!")
            # NOTE: Close the pop-up
            root.destroy()
    except Exception as e:
        messagebox.showerror("Something went wrong", str(e))



# === GUI Setup ===

# NOTE: create the GUI instance, give it a title and measures
root = tk.Tk()
root.title("PDF Slicer FINALLYYY")
root.geometry("400x200")

# NOTE: STringVar is a wrapper for a string variable
# NOTE: Lets you get and set values through .get() and .set()
# NOTE: it is basically a state, everytime user inputs something they get automatically updated!!
pdf_path = tk.StringVar()
page_range = tk.StringVar()


# NOTE: the pack() is used to place stuff into the window pop-up

## BROWSING FILES
# NOTE: simply create a label,entry and button that says what is written in TEXT
tk.Label(root, text="PDF File:").pack()
tk.Entry(root, textvariable=pdf_path, width=30).pack()
tk.Button(root, text="Browse", command=select_pdf).pack()

## PAGE RANGE SECTION
# NOTE: create another label and an entry 
tk.Label(root, text="Page Range (e.g., 1-3,5):").pack()
tk.Entry(root, textvariable=page_range).pack()

# SAVE BUTTON -> pady=10 means vertical padding 
tk.Button(root, text="Slice and Save", command=slice_pdf).pack(pady=10)

# START EVERYTHING!
root.mainloop()