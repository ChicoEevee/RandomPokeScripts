import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
import json, os, time

class ColorEditorApp:
    def __init__(self, root):
        self.root = root
        root.title("JSON Color Editor")

        self.data = None
        self.current_file_path = None
        self.current_material_index = None
        self.current_param_index = None

        # Left: Materials
        left_frame = tk.Frame(root)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        tk.Label(left_frame, text="Materials").pack()
        self.material_listbox = tk.Listbox(left_frame, height=15)
        self.material_listbox.pack(fill=tk.Y)
        self.material_listbox.bind("<<ListboxSelect>>", self.on_material_select)

        # Middle: Parameters
        middle_frame = tk.Frame(root)
        middle_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        tk.Label(middle_frame, text="Float4 Parameters").pack()
        self.param_listbox = tk.Listbox(middle_frame, height=15)
        self.param_listbox.pack(fill=tk.Y)
        self.param_listbox.bind("<<ListboxSelect>>", self.on_param_select)

        # Right: RGBA
        right_frame = tk.Frame(root)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        tk.Label(right_frame, text="Edit Color (RGBA)").pack()

        self.r_var = tk.StringVar()
        self.g_var = tk.StringVar()
        self.b_var = tk.StringVar()
        self.a_var = tk.StringVar()

        # Trigger preview update when RGB changes
        self.r_var.trace_add("write", lambda *args: self.update_color_preview())
        self.g_var.trace_add("write", lambda *args: self.update_color_preview())
        self.b_var.trace_add("write", lambda *args: self.update_color_preview())

        def make_labeled_entry(parent, label, var):
            row = tk.Frame(parent)
            row.pack(anchor="w", pady=2)
            tk.Label(row, text=label, width=5).pack(side=tk.LEFT)
            entry = tk.Entry(row, textvariable=var, width=10)
            entry.pack(side=tk.LEFT)
            return entry

        self.r_entry = make_labeled_entry(right_frame, "R:", self.r_var)
        self.g_entry = make_labeled_entry(right_frame, "G:", self.g_var)
        self.b_entry = make_labeled_entry(right_frame, "B:", self.b_var)
        self.a_entry = make_labeled_entry(right_frame, "A:", self.a_var)

        # Color Preview
        self.preview_canvas = tk.Canvas(right_frame, width=60, height=30, bg="#000000", highlightthickness=1, highlightbackground="black")
        self.preview_canvas.pack(pady=5)
        self.preview_rect = self.preview_canvas.create_rectangle(0, 0, 60, 30, fill="#000000", outline="black")

        # Color Picker Button
        color_btn = tk.Button(right_frame, text="Pick Color", command=self.pick_color)
        color_btn.pack(pady=5)

        # Buttons
        btn_frame = tk.Frame(right_frame)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Load TRMTR", command=self.load_json).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Save TRMTR", command=self.save_json).pack(side=tk.LEFT, padx=5)

    def pick_color(self):
        rgb, hex_color = colorchooser.askcolor()
        if rgb:
            r, g, b = [round(v / 255.0, 6) for v in rgb]
            self.r_var.set(str(r))
            self.g_var.set(str(g))
            self.b_var.set(str(b))

    def update_color_preview(self):
        try:
            r = float(self.r_var.get())
            g = float(self.g_var.get())
            b = float(self.b_var.get())
            r = min(max(r, 0), 1)
            g = min(max(g, 0), 1)
            b = min(max(b, 0), 1)
            hex_color = "#{:02x}{:02x}{:02x}".format(int(r * 255), int(g * 255), int(b * 255))
            self.preview_canvas.itemconfig(self.preview_rect, fill=hex_color)
        except ValueError:
            pass  # Ignore invalid input

    def load_json(self):
        path = filedialog.askopenfilename(filetypes=[("TRMTR files", "*.trmtr")])
        os.system(f'flatc --raw-binary --strict-json -o . -t trmtr.fbs --allow-non-utf8 -- "{path}"')
        if not path:
            return
        with open(path.replace(".trmtr",".json"), 'r') as f:
            self.data = json.load(f)
        self.current_file_path = path.replace(".trmtr",".json")  # Save loaded file path
        self.populate_materials()

    def populate_materials(self):
        self.material_listbox.delete(0, tk.END)
        if not self.data or "materials" not in self.data:
            return

        for mat in self.data["materials"]:
            self.material_listbox.insert(tk.END, mat.get("name", "<no name>"))

        self.current_material_index = None
        self.current_param_index = None
        self.param_listbox.delete(0, tk.END)
        self.clear_color_entries()

    def on_material_select(self, event):
        if not self.save_current_param_values():
            self.material_listbox.selection_clear(0, tk.END)
            if self.current_material_index is not None:
                self.material_listbox.selection_set(self.current_material_index)
            return

        sel = self.material_listbox.curselection()
        if not sel:
            return
        self.current_material_index = sel[0]

        material = self.data["materials"][self.current_material_index]

        self.param_listbox.delete(0, tk.END)
        for param in material.get("float4_parameter", []):
            self.param_listbox.insert(tk.END, param.get("color_name", "<no name>"))

        self.current_param_index = None
        self.clear_color_entries()

    def on_param_select(self, event):
        if not self.save_current_param_values():
            self.param_listbox.selection_clear(0, tk.END)
            if self.current_param_index is not None:
                self.param_listbox.selection_set(self.current_param_index)
            return

        sel = self.param_listbox.curselection()
        if not sel:
            return
        self.current_param_index = sel[0]

        param = self.data["materials"][self.current_material_index]["float4_parameter"][self.current_param_index]
        rgba = param.get("color_value", {"r":0,"g":0,"b":0,"a":0})

        self.r_var.set(str(rgba.get("r", 0)))
        self.g_var.set(str(rgba.get("g", 0)))
        self.b_var.set(str(rgba.get("b", 0)))
        self.a_var.set(str(rgba.get("a", 0)))

    def clear_color_entries(self):
        self.r_var.set("")
        self.g_var.set("")
        self.b_var.set("")
        self.a_var.set("")

    def save_current_param_values(self):
        if (self.data is None or
            self.current_material_index is None or
            self.current_param_index is None):
            return True

        try:
            r = float(self.r_var.get())
            g = float(self.g_var.get())
            b = float(self.b_var.get())
            a = float(self.a_var.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "RGBA values must be valid numbers.")
            return False

        param = self.data["materials"][self.current_material_index]["float4_parameter"][self.current_param_index]
        param["color_value"] = {"r": r, "g": g, "b": b, "a": a}
        return True
        
    def save_json(self):
        # Save current edits first
        if not self.save_current_param_values():
            return

        if not self.current_file_path:
            path = filedialog.asksaveasfilename(defaultextension=".json",
                                                filetypes=[("JSON files", "*.json")])
            if not path:
                return
            self.current_file_path = path

        try:
            with open(self.current_file_path, "w") as f:
                json.dump(self.data, f, indent=1)
                time.sleep(3)
            
            messagebox.showinfo("Saved", f"JSON saved successfully:\n{os.path.basename(self.current_file_path)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save JSON:\n{e}")
        os.system(f'flatc -b trmtr.fbs "{self.current_file_path}"')

if __name__ == "__main__":
    root = tk.Tk()
    app = ColorEditorApp(root)
    root.mainloop()
