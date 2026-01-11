import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3

DB_FILE = "tpop_favorites.db"

class TPopFavoritesSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("T-pop Favorites Record System")
        self.root.geometry("1100x700")
        self.root.resizable(True, True)

        image_path = "bg.png"
        img = Image.open(image_path)
        background_image = ImageTk.PhotoImage(img)

        background_label = tk.Label(root, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        background_label.image = background_image

        self.colors = {
                'header': '#465187',
                'bg_white': '#a37dc2',
                'btn_green': '#c2a3db',
                'btn_blue': '#c2a3db',
                'btn_red': '#c2a3db',
                'btn_orange': '#c2a3db',
                'btn_gray': '#c2a3db',
                'status_bg': '#465187',
                'status_fg': '#465187'
            }

        self.selected_id = None
        self.initialize_database()
        self.create_widgets()
        self.refresh_table()

    def create_connection(self):
        return sqlite3.connect(DB_FILE)

    def initialize_database(self):
        with self.create_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS favorites (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    fav_group TEXT NOT NULL,
                    bias TEXT NOT NULL,
                    bias_wrecker TEXT NOT NULL,
                    song_count INTEGER NOT NULL,
                    fav_song TEXT NOT NULL,
                    fav_album TEXT NOT NULL
                )
            """)

    def create_widgets(self):
        header_frame = tk.Frame(self.root, bg=self.colors['header'], height=60)
        header_frame.pack(fill='x')

        tk.Label(
            header_frame,
            text="T-pop Favorites Record System",
            font=('Arial', 20, 'bold'),
            bg=self.colors['header'],
            fg='white',
            pady=15
        ).pack()

        input_frame = tk.Frame(self.root, bg=self.colors['bg_white'], pady=20)
        input_frame.pack(fill='x', padx=20, pady=15)

        for i in range(6):
            input_frame.columnconfigure(i, weight=1)

        self.name_var = tk.StringVar()
        self.group_var = tk.StringVar()
        self.bias_var = tk.StringVar()
        self.wrecker_var = tk.StringVar()
        self.song_count_var = tk.StringVar()
        self.song_var = tk.StringVar()
        self.album_var = tk.StringVar()

        self.create_input_field(input_frame, "Your Name:", self.name_var, 0, 0)
        self.create_input_field(input_frame, "Favorite Group/Artist:", self.group_var, 0, 2)
        self.create_input_field(input_frame, "Your Bias:", self.bias_var, 1, 0)
        self.create_input_field(input_frame, "Bias Wrecker:", self.wrecker_var, 1, 2)
        self.create_input_field(input_frame, "Song Count:", self.song_count_var, 2, 0)
        self.create_input_field(input_frame, "Favorite Song:", self.song_var, 2, 2)
        self.create_input_field(input_frame, "Favorite Album:", self.album_var, 3, 0)

        button_frame = tk.Frame(self.root, bg='#465187', pady=10)
        button_frame.pack(fill='x', padx=20)

        buttons = [
            ("Add Entry", self.add_entry, self.colors['btn_green']),
            ("Update Entry", self.update_entry, self.colors['btn_blue']),
            ("Delete Entry", self.delete_entry, self.colors['btn_red']),
            ("View All", self.refresh_table, self.colors['btn_orange']),
            ("Clear Fields", self.clear_fields, self.colors['btn_gray'])
        ]

        for i, (text, cmd, color) in enumerate(buttons):
            tk.Button(
                button_frame,
                text=text,
                font=('Canva Sans', 11, 'bold'),
                bg=color,
                fg='black',
                width=15,
                command=cmd
            ).grid(row=0, column=i, padx=8)

        table_frame = tk.Frame(self.root, bg=self.colors['bg_white'])
        table_frame.pack(fill='both', expand=True, padx=20, pady=(5, 10))

        self.tree = ttk.Treeview(
            table_frame,
            columns=("ID", "Name", "Group", "Bias", "Wrecker", "Songs", "Song", "Album"),
            show='headings'
        )

        for col in ("ID", "Name", "Group", "Bias", "Wrecker", "Songs", "Song", "Album"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=140)

        self.tree.pack(fill='both', expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.select_row)

        status_frame = tk.Frame(self.root, bg=self.colors['status_bg'], height=30)
        status_frame.pack(fill='x')

        self.status_label = tk.Label(
            status_frame,
            text=f"Ready | Database: {DB_FILE}",
            bg=self.colors['status_bg'],
            fg=self.colors['status_fg']
        )
        self.status_label.pack(anchor='w', padx=10)

    def create_input_field(self, parent, label, var, r, c):
        tk.Label(parent, text=label, bg='#a37dc2', fg='white', font=('Arial', 11)).grid(row=r, column=c, sticky='w')
        tk.Entry(parent, textvariable=var, font=('Arial', 11)).grid(row=r, column=c + 1, sticky='ew', padx=5)

    def refresh_table(self):
        self.tree.delete(*self.tree.get_children())
        with self.create_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM favorites")
            for row in cur.fetchall():
                self.tree.insert("", "end", values=row)

    def clear_fields(self):
        self.selected_id = None
        for var in (
            self.name_var, self.group_var, self.bias_var,
            self.wrecker_var, self.song_count_var,
            self.song_var, self.album_var
        ):
            var.set("")

    def select_row(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        vals = self.tree.item(sel[0], "values")
        self.selected_id = vals[0]
        self.name_var.set(vals[1])
        self.group_var.set(vals[2])
        self.bias_var.set(vals[3])
        self.wrecker_var.set(vals[4])
        self.song_count_var.set(vals[5])
        self.song_var.set(vals[6])
        self.album_var.set(vals[7])

    def add_entry(self):
        with self.create_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO favorites
                (name, fav_group, bias, bias_wrecker, song_count, fav_song, fav_album)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                self.name_var.get(),
                self.group_var.get(),
                self.bias_var.get(),
                self.wrecker_var.get(),
                int(self.song_count_var.get()),
                self.song_var.get(),
                self.album_var.get()
            ))
        self.clear_fields()
        self.refresh_table()

    def update_entry(self):
        if not self.selected_id:
            messagebox.showwarning("Selection Required", "Please select a record first.")
            return

        confirm = messagebox.askyesno(
            "Confirm Update",
            "Are you sure you want to update this entry?"
        )
        if not confirm:
            return

        with self.create_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                UPDATE favorites SET
                name=?, fav_group=?, bias=?, bias_wrecker=?,
                song_count=?, fav_song=?, fav_album=?
                WHERE id=?
            """, (
                self.name_var.get(),
                self.group_var.get(),
                self.bias_var.get(),
                self.wrecker_var.get(),
                int(self.song_count_var.get()),
                self.song_var.get(),
                self.album_var.get(),
                self.selected_id
            ))

        messagebox.showinfo("Updated", "Entry updated successfully.")
        self.clear_fields()
        self.refresh_table()

    def delete_entry(self):
        if not self.selected_id:
            messagebox.showwarning("Selection Required", "Please select a record first.")
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this entry?\n\nThis action cannot be undone."
        )
        if not confirm:
            return

        with self.create_connection() as conn:
            conn.execute("DELETE FROM favorites WHERE id=?", (self.selected_id,))

        messagebox.showinfo("Deleted", "Entry deleted successfully.")
        self.clear_fields()
        self.refresh_table()


def main():
    root = tk.Tk()
    TPopFavoritesSystem(root)
    root.mainloop()


if __name__ == "__main__":
    main()
