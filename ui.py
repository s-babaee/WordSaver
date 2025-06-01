import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import pandas as pd

FILENAME = "words.csv"


class CSVEditorApp(tk.Tk):
    def __init__(self, csv_path=FILENAME):
        super().__init__()

        self.csv_path = csv_path
        self.df = pd.DataFrame()  # دیتافریم برای ذخیره داده‌های CSV
        self.title("CSV Viewer - Excel Lookalike")
        self.geometry("1200x600")

        # ایجاد فریم برای Treeview
        self.frame = ttk.Frame(self)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # استایل دهی به Treeview
        style = ttk.Style(self)
        style.configure("Treeview",
                        background="#D1D1D2",
                        fieldbackground="#D1D1D2",
                        rowheight=25)
        style.map('Treeview',
                  background=[('selected', '#4a6984')])

        # استایل اسکرول‌بار
        style.configure("Vertical.TScrollbar", background='#9b9d9d', troughcolor='#5b5e5e')

        # ویجت Treeview (جدول داده‌ها)
        self.tree = ttk.Treeview(self.frame, columns=[], show="headings", selectmode="browse", style="Treeview")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # پیکربندی رنگ ردیف‌های جدول
        self.tree.tag_configure('odd', background='#E5E5E5')
        self.tree.tag_configure('even', background='#D1D1D2')

        # اسکرول‌بار برای جدول
        self.scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.tree.yview, style="Vertical.TScrollbar")
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # دکمه‌های عملیات
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(fill=tk.X, pady=10)

        self.load_button = tk.Button(self.button_frame, text="Load CSV", command=self.load_csv)
        self.load_button.pack(side=tk.LEFT, padx=10)

        self.save_button = tk.Button(self.button_frame, text="Save Changes", command=self.save_csv)
        self.save_button.pack(side=tk.LEFT, padx=10)

        self.delete_button = tk.Button(self.button_frame, text="Delete Selected Row", command=self.delete_row)
        self.delete_button.pack(side=tk.LEFT, padx=10)

        self.edit_button = tk.Button(self.button_frame, text="Edit Cell", command=self.edit_cell)
        self.edit_button.pack(side=tk.LEFT, padx=10)

        # بارگذاری اولیه داده‌ها
        self.load_csv()

    def load_csv(self):
        """لود کردن CSV و نمایش در Treeview"""
        try:
            self.df = pd.read_csv(self.csv_path, encoding='utf-8')
            self.populate_treeview()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load CSV file: {e}")

    def populate_treeview(self):
        """به‌روزرسانی داده‌های جدول"""
        self.tree.delete(*self.tree.get_children())  # پاک کردن داده‌های قبلی
        self.tree["columns"] = self.df.columns.tolist()

        # تنظیم عناوین ستون‌ها
        for col in self.df.columns:
            self.tree.heading(col, text=col)

        # درج داده‌ها در Treeview
        for index, row in self.df.iterrows():
            tag = 'odd' if index % 2 == 0 else 'even'
            self.tree.insert("", "end", values=row.tolist(), tags=(tag,))

    def save_csv(self):
        """ذخیره تغییرات در فایل CSV"""
        if not self.df.empty:
            file_path = "./words.csv"
            if file_path:
                try:
                    self.df.to_csv(file_path, index=False, encoding='utf-8')
                    messagebox.showinfo("Saved", "The changes have been saved successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save CSV file: {e}")
        else:
            messagebox.showwarning("No Data", "No data to save!")

    def delete_row(self):
        """حذف ردیف انتخاب‌شده"""
        selected_item = self.tree.selection()
        if selected_item:
            response = messagebox.askyesno("Delete Row", "Are you sure you want to delete this row?")
            if response:
                item_values = self.tree.item(selected_item)["values"]
                matching_rows = self.df[self.df.apply(lambda row: row.tolist() == item_values, axis=1)]

                if not matching_rows.empty:
                    index_to_delete = matching_rows.index[0]
                    self.df.drop(index_to_delete, inplace=True)
                    self.df.reset_index(drop=True, inplace=True)
                    self.populate_treeview()
                    messagebox.showinfo("Deleted", "The row has been deleted successfully!")
                else:
                    messagebox.showwarning("No Match", "No matching row found to delete.")
        else:
            messagebox.showwarning("Select Row", "Please select a row to delete.")

    def edit_cell(self):
        """ویرایش مقدار سلول انتخابی"""
        selected_item = self.tree.selection()
        if selected_item:
            col_index = self.tree.identify_column(self.tree.winfo_pointerx())
            col_index = int(col_index.replace("#", "")) - 1
            old_value = self.tree.item(selected_item)["values"][col_index]

            new_value = simpledialog.askstring("Edit Cell", f"Edit value for {self.df.columns[col_index]}", initialvalue=old_value)
            if new_value is not None:
                row_index = self.df.index[self.df.isin([old_value]).any(axis=1)].tolist()[0]
                self.df.iloc[row_index, col_index] = new_value
                self.populate_treeview()
                messagebox.showinfo("Edited", "The cell has been edited successfully!")
        else:
            messagebox.showwarning("Select Row", "Please select a row to edit.")


if __name__ == "__main__":
    app = CSVEditorApp()
    app.mainloop()
