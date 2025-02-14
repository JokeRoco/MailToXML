import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
import main
import extract_msg
import os

emailpath = ""
OrderID = ""

def on_drop(event):
    global emailpath
    emailpath = event.data.strip('{}')  # Pfad bereinigen
    process_email(emailpath)



def process_email(file_path):
    global OrderID
    msg = extract_msg.Message(file_path)
    body = msg.body.split('{message}')[1]
    offer = main.OfferRequest(body)
    OrderID = offer.order_id
    xml = offer.get_xml()
    email_text = xml
    text_box.delete("1.0", tk.END)
    text_box.insert(tk.END, email_text)


def save_as_xml():
    global emailpath
    xml_text = text_box.get("1.0", tk.END).strip()  # Inhalt aus dem Textfeld holen
    emailpath = emailpath.rsplit("/", 1)[0]
    print(emailpath)
    f = open(emailpath + "/" + OrderID + ".xml", "wb")  # öffnen/erstellen einer xml-Datei
    f.write(bytes(xml_text, 'utf-8'))  # xml-Datei mit Inhalt füllen
    f.close()


# Tkinter GUI einrichten
root = TkinterDnD.Tk()
root.title("Email to XML")
root.geometry("600x440")

label = tk.Label(root, text="Ziehe eine Outlook-E-Mail (.msg) hierher:", font=("Arial", 12))
label.pack(pady=10)

frame = tk.Frame(root, width=500, height=50, bg="lightgray")
frame.pack(pady=10)
frame.drop_target_register(DND_FILES)
frame.dnd_bind('<<Drop>>', on_drop)

text_box = tk.Text(root, wrap="word", height=15, width=70)
text_box.pack(pady=10)

save_button = tk.Button(root, text="Speichern als XML", command=save_as_xml, bg="lightblue", font=("Arial", 10))
save_button.pack(pady=5)


root.mainloop()
