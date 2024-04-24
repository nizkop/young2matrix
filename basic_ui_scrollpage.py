import tkinter as tk

# Erstellen des Hauptfensters
root = tk.Tk()
root.title("Scrollbare UI-Seite")

# Erstellen des Hauptframes
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)

# Erstellen des Canvas für den Inhalt
canvas = tk.Canvas(main_frame, scrollregion=(0, 0, 1000, 1000)) # Beispielgröße
canvas.pack(side="left", fill="both", expand=True)

# Erstellen des Scrollbars für das Canvas
vertical_scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
vertical_scrollbar.pack(side="right", fill="y")
horizontal_scrollbar = tk.Scrollbar(main_frame, orient="horizontal", command=canvas.xview)
horizontal_scrollbar.pack(side="bottom", fill="x")

# Konfiguration des Canvas, um die Scrollbars zu verwenden
canvas.configure(yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)

# Beispielinhalt hinzufügen (breiter Inhalt für horizontales Scrollen)
content_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=content_frame, anchor="nw")
for i in range(20):
    tk.Label(content_frame, text=f"Beispieltext {i+1}").grid(row=0, column=i, padx=10)

# Festlegen der Mindestgröße für das Scrollen
content_frame.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))

root.mainloop()
