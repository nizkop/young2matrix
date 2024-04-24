import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


class MainApplication(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Hauptstartseite")
        self.geometry("400x300")  # Breite des Fensters festlegen

        self.canvas = tk.Canvas(self)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.create_widgets()

    def create_widgets(self):
        input_label = ttk.Label(self.scrollable_frame, text="Bitte eine Zahl eingeben:")
        input_label.grid(row=0, column=0, pady=10)

        input_entry = ttk.Entry(self.scrollable_frame)
        input_entry.grid(row=0, column=1, pady=10)

        button1 = ttk.Button(self.scrollable_frame, text="Seite 1", command=self.open_page1)
        button1.grid(row=1, column=0, pady=5)

        button2 = ttk.Button(self.scrollable_frame, text="Seite 2", command=self.open_page2)
        button2.grid(row=1, column=1, pady=5)

        button3 = ttk.Button(self.scrollable_frame, text="Seite 3", command=self.open_page3)
        button3.grid(row=2, column=0, pady=5)

        button4 = ttk.Button(self.scrollable_frame, text="Seite 4", command=self.open_page4)
        button4.grid(row=2, column=1, pady=5)

        # Beispiel für LaTeX-Formel
        figure, ax = plt.subplots(figsize=(4, 3))
        ax.text(0.05, 0.5, r"$\sum_{i=1}^{n} i^2$", horizontalalignment='left', verticalalignment='center', fontsize=20)
        ax.axis('off')
        figure.patch.set_facecolor('none')  # Hintergrundfarbe der Figur auf "none" setzen
        plt.tight_layout(pad=0.2)

        canvas = FigureCanvasTkAgg(figure, master=self.scrollable_frame)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.configure(highlightthickness=0, borderwidth=0)
        canvas_widget.grid(row=2, columnspan=2, pady=10)

    def open_page1(self):
        # Hier implementiere die Logik für die erste Unterseite
        pass

    def open_page2(self):
        # Hier implementiere die Logik für die zweite Unterseite
        pass

    def open_page3(self):
        # Hier implementiere die Logik für die dritte Unterseite
        pass

    def open_page4(self):
        # Hier implementiere die Logik für die vierte Unterseite
        pass


if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
