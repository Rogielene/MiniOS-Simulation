import tkinter as tk
import random
from tkinter import ttk, messagebox
from auth_system import login, register
from file_system import create_file, read_file, delete_file, list_files, get_directory_structure
from scheduler import ProcessScheduler

class MiniOS:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini OS Simulator")
        self.root.geometry("500x600")
        self.root.minsize(500, 600) 
        self.root.configure(bg="#f0f2f5")
        self.current_user = None
        self.file_content = tk.StringVar()
        self.memory_blocks = [None] * 100
        self.alloc_method = tk.StringVar(value="First-Fit")
        self.memory_allocations = []  # Stores dicts: {'pid': str, 'start': int, 'size': int, 'color': str}
        self.color_pool = ["#FF9999", "#99CCFF", "#99FF99", "#FFCC99", "#CCCCFF", "#FFFF99"]
        self.color_index = 0

        # Custom colors and fonts
        self.bg_color = "#f0f2f5"
        self.primary_color = "#1877f2"
        self.secondary_color = "#42b72a"
        self.text_color = "#1c1e21"
        self.box_color = "#ffffff"
        self.font_primary = ("Segoe UI", 12)
        self.font_secondary = ("Segoe UI", 10)
        self.font_title = ("Segoe UI", 16, "bold")
        
        # Configure grid for responsive layout
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        self.setup_ui()
        
    def setup_ui(self):
        self.main_frame = tk.Frame(self.root, bg=self.bg_color)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=0)
        self.main_frame.grid_rowconfigure(2, weight=0)
        self.main_frame.grid_rowconfigure(3, weight=0)
        self.main_frame.grid_rowconfigure(4, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Logo/Title
        self.logo_label = tk.Label(
            self.main_frame,
            text="MiniOS",
            font=self.font_title,
            fg=self.primary_color,
            bg=self.bg_color
        )
        self.logo_label.grid(row=0, column=0, pady=(0, 20), sticky="s")
        
        # Login box
        self.login_box = tk.Frame(
            self.main_frame,
            bg=self.box_color,
            padx=20,
            pady=20,
            highlightbackground="#dddfe2",
            highlightthickness=1
        )
        self.login_box.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        
        # Username field
        self.username_label = tk.Label(
            self.login_box,
            text="Username",
            font=self.font_secondary,
            fg=self.text_color,
            bg=self.box_color,
            anchor="w"
        )
        self.username_label.pack(fill=tk.X, pady=(0, 5))
        
        self.username_entry = ttk.Entry(
            self.login_box,
            font=self.font_primary
        )
        self.username_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Password field
        self.password_label = tk.Label(
            self.login_box,
            text="Password",
            font=self.font_secondary,
            fg=self.text_color,
            bg=self.box_color,
            anchor="w"
        )
        self.password_label.pack(fill=tk.X, pady=(0, 5))
        
        self.password_entry = ttk.Entry(
            self.login_box,
            font=self.font_primary,
            show="•"
        )
        self.password_entry.pack(fill=tk.X, pady=(0, 20))
        
        # Login button
        self.login_button = tk.Button(
            self.login_box,
            text="Log In",
            font=self.font_primary,
            bg=self.primary_color,
            fg="white",
            activebackground="#166fe5",
            activeforeground="white",
            relief=tk.FLAT,
            command=self.handle_login,
            cursor="hand2"
        )
        self.login_button.pack(fill=tk.X, pady=(0, 10))
        
        # Forgot password link
        self.forgot_link = tk.Label(
            self.login_box,
            text="Forgot password?",
            font=self.font_secondary,
            fg=self.primary_color,
            bg=self.box_color,
            cursor="hand2"
        )
        self.forgot_link.pack()
        self.forgot_link.bind("<Button-1>", lambda e: messagebox.showinfo("Info", "Contact your system administrator"))
        
        # Divider
        self.divider = tk.Frame(
            self.main_frame,
            height=1,
            bg="#dddfe2"
        )
        self.divider.grid(row=2, column=0, sticky="ew", pady=15)
        
        # Register button
        self.register_button = tk.Button(
            self.main_frame,
            text="Create New Account",
            font=self.font_primary,
            bg=self.secondary_color,
            fg="white",
            activebackground="#36a420",
            activeforeground="white",
            relief=tk.FLAT,
            command=self.show_register,
            cursor="hand2"
        )
        self.register_button.grid(row=3, column=0, sticky="ew", ipady=10)
        
        # Footer
        self.footer = tk.Label(
            self.main_frame,
            text="© 2025 MiniOS",
            font=("Segoe UI", 8),
            fg="#65676b",
            bg=self.bg_color
        )
        self.footer.grid(row=4, column=0, pady=(20, 0), sticky="n")
        
        # Bind window resize event
        self.root.bind("<Configure>", self.on_window_resize)
        
        # Center the window initially
        self.center_window()
        
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def on_window_resize(self, event):
        window_width = self.root.winfo_width()
        base_size = min(window_width / 25, 16)
        
        # Update font sizes
        self.font_primary = ("Segoe UI", int(base_size))
        self.font_secondary = ("Segoe UI", int(base_size * 0.83))
        self.font_title = ("Segoe UI", int(base_size * 1.33), "bold")
        
        # Apply new fonts to widgets
        self.logo_label.config(font=self.font_title)
        self.username_label.config(font=self.font_secondary)
        self.password_label.config(font=self.font_secondary)
        self.username_entry.config(font=self.font_primary)
        self.password_entry.config(font=self.font_primary)
        self.login_button.config(font=self.font_primary)
        self.forgot_link.config(font=self.font_secondary)
        self.register_button.config(font=self.font_primary)
        
    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
            
        if login(username, password):
            messagebox.showinfo("Success", f"Welcome, {username}!")
            # Here you would typically proceed to the main application
            self.root.destroy()
        else:
            messagebox.showerror("Error", "Invalid username or password")
            self.password_entry.delete(0, tk.END)
            
    def show_register(self):
        # Create registration window
        register_window = tk.Toplevel(self.root)
        register_window.title("Create Account")
        register_window.geometry("400x450")
        register_window.minsize(400, 450)
        register_window.configure(bg=self.bg_color)
        register_window.grab_set()
        
        # Configure grid for responsive layout
        register_window.grid_rowconfigure(0, weight=1)
        register_window.grid_columnconfigure(0, weight=1)
        
        # Registration form
        main_frame = tk.Frame(register_window, bg=self.bg_color)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        tk.Label(
            main_frame,
            text="Sign Up",
            font=self.font_title,
            fg=self.primary_color,
            bg=self.bg_color
        ).pack(pady=(20, 10))
        
        reg_box = tk.Frame(
            main_frame,
            bg=self.box_color,
            padx=20,
            pady=20,
            highlightbackground="#dddfe2",
            highlightthickness=1
        )
        reg_box.pack(fill=tk.BOTH, expand=True)
        
        # Username field
        tk.Label(
            reg_box,
            text="Username",
            font=self.font_secondary,
            fg=self.text_color,
            bg=self.box_color,
            anchor="w"
        ).pack(fill=tk.X, pady=(0, 5))
        
        reg_username = ttk.Entry(
            reg_box,
            font=self.font_primary
        )
        reg_username.pack(fill=tk.X, pady=(0, 15))
        
        # Password field
        tk.Label(
            reg_box,
            text="Password",
            font=self.font_secondary,
            fg=self.text_color,
            bg=self.box_color,
            anchor="w"
        ).pack(fill=tk.X, pady=(0, 5))
        
        reg_password = ttk.Entry(
            reg_box,
            font=self.font_primary,
            show="•"
        )
        reg_password.pack(fill=tk.X, pady=(0, 15))
        
        # Confirm Password field
        tk.Label(
            reg_box,
            text="Confirm Password",
            font=self.font_secondary,
            fg=self.text_color,
            bg=self.box_color,
            anchor="w"
        ).pack(fill=tk.X, pady=(0, 5))
        
        reg_confirm = ttk.Entry(
            reg_box,
            font=self.font_primary,
            show="•"
        )
        reg_confirm.pack(fill=tk.X, pady=(0, 20))
        
        # Register button
        tk.Button(
            reg_box,
            text="Sign Up",
            font=self.font_primary,
            bg=self.secondary_color,
            fg="white",
            activebackground="#36a420",
            activeforeground="white",
            relief=tk.FLAT,
            command=lambda: self.handle_register(reg_username.get(), reg_password.get(), reg_confirm.get(), register_window),
            cursor="hand2"
        ).pack(fill=tk.X)
        
        # Bind resize event to the registration window
        register_window.bind("<Configure>", lambda e: self.on_window_resize(e))
        
    def handle_register(self, username, password, confirm, window):
        if not username or not password or not confirm:
            messagebox.showerror("Error", "All fields are required", parent=window)
            return
            
        if password != confirm:
            messagebox.showerror("Error", "Passwords don't match", parent=window)
            return
            
        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters", parent=window)
            return
            
        result = register(username, password)
        messagebox.showinfo("Success", result, parent=window)
        window.destroy()

    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
            
        if login(username, password):
            self.current_user = username
            self.show_main_interface()
        else:
            messagebox.showerror("Error", "Invalid username or password")
            self.password_entry.delete(0, tk.END)
            
    def show_main_interface(self):
        self.clear_window()
        
        # Create notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create frames for each tab
        self.file_frame = ttk.Frame(self.notebook)
        self.memory_frame = ttk.Frame(self.notebook)
        self.process_frame = ttk.Frame(self.notebook)
        
        # Add tabs to notebook
        self.notebook.add(self.file_frame, text="File Management")
        self.notebook.add(self.memory_frame, text="Memory Management")
        self.notebook.add(self.process_frame, text="Process Scheduling")
        
        # Setup each tab's content
        self.setup_file_management()
        self.setup_memory_management()
        self.setup_process_scheduling()

    # File Management System 
    def setup_file_management(self):
        container = tk.Frame(self.file_frame, bg=self.bg_color)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title
        title = tk.Label(
            container,
            text="File Management System",
            font=self.font_title,
            fg=self.primary_color,
            bg=self.bg_color
        )
        title.pack(pady=(0, 10))

        # File Operations Frame
        ops_frame = tk.Frame(container, bg=self.box_color, bd=1, relief="solid", padx=10, pady=10)
        ops_frame.pack(fill=tk.X, pady=10)

        # Filename
        tk.Label(
            ops_frame, text="Filename:",
            font=self.font_secondary,
            fg=self.text_color,
            bg=self.box_color
        ).grid(row=0, column=0, sticky="w", pady=2)
        self.file_name = ttk.Entry(ops_frame, font=self.font_primary)
        self.file_name.grid(row=0, column=1, sticky="ew", padx=5, pady=2)

        # Content
        tk.Label(
            ops_frame, text="Content:",
            font=self.font_secondary,
            fg=self.text_color,
            bg=self.box_color
        ).grid(row=1, column=0, sticky="w", pady=2)
        self.file_content_entry = ttk.Entry(ops_frame, textvariable=self.file_content, font=self.font_primary)
        self.file_content_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=2)

        ops_frame.grid_columnconfigure(1, weight=1)

        # Buttons
        btn_frame = tk.Frame(ops_frame, bg=self.box_color)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0))

        for text, command, color in [
            ("Create", self.create_file, self.primary_color),
            ("View", self.view_file, "#28a745"),
            ("Delete", self.delete_file, "#dc3545"),
            ("List", self.refresh_all_views, "#6c757d")
        ]:
            tk.Button(
                btn_frame,
                text=text,
                font=self.font_secondary,
                bg=color,
                fg="white",
                activebackground=color,
                activeforeground="white",
                relief=tk.FLAT,
                padx=10,
                command=command,
                cursor="hand2"
            ).pack(side=tk.LEFT, padx=5)

        # File List
        list_frame = tk.LabelFrame(container, text="File List", font=self.font_secondary, bg=self.bg_color, fg=self.text_color)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.file_tree = ttk.Treeview(
            list_frame,
            columns=("name", "owner", "size", "created"),
            show="headings"
        )
        for col, title in zip(["name", "owner", "size", "created"], ["File Name", "Owner", "Size (bytes)", "Created"]):
            self.file_tree.heading(col, text=title)
            self.file_tree.column(col, width=100 if col != "name" else 150)
        self.file_tree.pack(fill=tk.BOTH, expand=True, pady=5)

        # Directory View
        dir_frame = tk.LabelFrame(container, text="Directory Structure", font=self.font_secondary, bg=self.bg_color, fg=self.text_color)
        dir_frame.pack(fill=tk.BOTH, expand=True)

        # Add scrollbars
        self.dir_canvas = tk.Canvas(dir_frame, bg=self.bg_color, highlightthickness=0)
        v_scroll = ttk.Scrollbar(dir_frame, orient="vertical", command=self.dir_canvas.yview)
        h_scroll = ttk.Scrollbar(dir_frame, orient="horizontal", command=self.dir_canvas.xview)
        
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.dir_canvas.pack(fill=tk.BOTH, expand=True)
        
        self.dir_canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        self.dir_canvas.bind("<Configure>", lambda e: self.dir_canvas.configure(scrollregion=self.dir_canvas.bbox("all")))

        # Initial Load
        self.refresh_files()
        self.refresh_directory_structure()

    def refresh_directory_structure(self):
        self.dir_canvas.delete("all")
        
        # Get file list
        files = list_files()
        if not files:
            return
        
        # Color palette for file boxes
        file_colors = ["#FF9999", "#99CCFF", "#99FF99",  # red, blue, green
                    "#FFCC99", "#CCCCFF", "#FFFF99"]  # orange, lavender, yellow
        
        # Set dimensions and spacing
        box_width = 100
        box_height = 40
        h_spacing = 120  # horizontal spacing between boxes
        start_x = 50     # starting x position
        start_y = 50     # y position for all boxes
        
        # Draw Root box
        self.dir_canvas.create_rectangle(
            start_x, start_y,
            start_x + box_width, start_y + box_height,
            outline=self.text_color,
            fill="#DDDDDD",
            width=2
        )
        self.dir_canvas.create_text(
            start_x + box_width/2, start_y + box_height/2,
            text="📁 Root",
            fill=self.text_color,
            font=self.font_secondary
        )
        
        # Draw files connected horizontally
        prev_x = start_x + box_width
        for i, file in enumerate(files):
            file_x = prev_x + h_spacing - box_width
            file_y = start_y
            
            # Draw connecting arrow
            self.dir_canvas.create_line(
                prev_x, start_y + box_height/2,
                file_x, start_y + box_height/2,
                arrow=tk.LAST,
                fill=self.text_color,
                width=1.5
            )
            
            file_color = file_colors[i % len(file_colors)]
            
            self.dir_canvas.create_rectangle(
                file_x, file_y,
                file_x + box_width, file_y + box_height,
                outline=self.text_color,
                fill=file_color,
                width=2
            )
            
            # Draw file name
            display_name = file['name'][:8] + "..." if len(file['name']) > 8 else file['name']
            self.dir_canvas.create_text(
                file_x + box_width/2, file_y + box_height/2,
                text=f"📄 {display_name}",
                fill=self.text_color,
                font=self.font_secondary
            )
            
            prev_x = file_x + box_width
        
        # Update scroll region
        self.dir_canvas.configure(scrollregion=self.dir_canvas.bbox("all"))
        
    def draw_directory_node(self, nodes, x, y, parent_x, parent_y):
        box_width = 120
        box_height = 40
        h_spacing = 150
        v_spacing = 80
        
        if not isinstance(nodes, list):
            nodes = [nodes]
            
        for i, node in enumerate(nodes):
            # Calculate position
            current_x = x + i * h_spacing
            current_y = y
            
            # Draw connecting line from parent
            if parent_x is not None and parent_y is not None:
                self.dir_canvas.create_line(
                    parent_x, parent_y + box_height,
                    current_x + box_width/2, current_y,
                    arrow=tk.LAST,
                    fill=self.text_color,
                    width=1.5
                )
            
            # Draw the box
            self.dir_canvas.create_rectangle(
                current_x, current_y,
                current_x + box_width, current_y + box_height,
                outline=self.text_color,
                fill=self.box_color,
                width=2
            )
            
            # Draw icon and name
            icon = "📁" if node.get("type") == "directory" else "📄"
            self.dir_canvas.create_text(
                current_x + box_width/2, current_y + box_height/2,
                text=f"{icon} {node['name']}",
                fill=self.text_color,
                font=self.font_secondary
            )
            
            if node.get("type") == "directory" and "contents" in node:
                num_children = len(node["contents"])
                if num_children > 0:
                    child_x = current_x - ((num_children - 1) * h_spacing) / 2
                    self.draw_directory_node(
                        node["contents"],
                        x=child_x,
                        y=current_y + v_spacing,
                        parent_x=current_x + box_width/2,
                        parent_y=current_y + box_height
                    )

    def create_file(self):
        filename = self.file_name.get()
        content = self.file_content.get()
        
        if not filename:
            messagebox.showerror("Error", "Filename cannot be empty")
            return
            
        try:
            create_file(filename, content, self.current_user)
            self.refresh_files()
            self.refresh_directory_structure()
            messagebox.showinfo("Success", f"File '{filename}' created successfully.")
            self.file_name.delete(0, tk.END)
            self.file_content.set("")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        
    def view_file(self):
        selected = self.file_tree.selection()
        if not selected:
            messagebox.showerror("Error", "No file selected")
            return

        filename = self.file_tree.item(selected[0])['values'][0]
        try:
            content = read_file(filename)
            messagebox.showinfo("File Content", f"Content of '{filename}':\n\n{content}")
        except FileNotFoundError as e:
            messagebox.showerror("Error", str(e))

    def delete_file(self):
        selected = self.file_tree.selection()
        if not selected:
            messagebox.showerror("Error", "No file selected")
            return
            
        filename = self.file_tree.item(selected[0])['values'][0]
        if delete_file(filename):
            messagebox.showinfo("Success", f"Deleted '{filename}'")
            self.refresh_files()
            self.refresh_directory_structure()
        else:
            messagebox.showerror("Error", f"File '{filename}' not found")

    def refresh_files(self):
        for item in self.file_tree.get_children():
            self.file_tree.delete(item)
            
        for file in list_files():
            self.file_tree.insert("", tk.END, values=(
                file['name'],
                file['owner'],
                file['size'],
                file['created']
            ))

    def refresh_all_views(self):
        self.refresh_files()
        self.refresh_directory_structure()

    # Memory Management
    def setup_memory_management(self):
        container = tk.Frame(self.memory_frame, bg=self.bg_color)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        title = tk.Label(
            container,
            text="Memory Management",
            font=self.font_title,
            fg=self.primary_color,
            bg=self.bg_color
        )
        title.pack(pady=(0, 10))

        method_frame = tk.LabelFrame(
            container,
            text="Allocation Method",
            font=self.font_secondary,
            bg=self.bg_color,
            fg=self.text_color
        )
        method_frame.pack(fill=tk.X, pady=5)

        self.alloc_method = tk.StringVar(value="First-Fit")
        self.dealloc_pid = tk.StringVar()

        ttk.Combobox(method_frame, textvariable=self.alloc_method, values=["First-Fit", "Best-Fit"], state="readonly", width=10).pack(side=tk.LEFT, padx=10)

        ttk.Button(method_frame, text="Allocate Memory", command=self.allocate_memory).pack(side=tk.LEFT, padx=5)

        self.dealloc_dropdown = ttk.Combobox(method_frame, textvariable=self.dealloc_pid, state="readonly", width=10)
        self.dealloc_dropdown.pack(side=tk.LEFT, padx=5)

        ttk.Button(method_frame, text="Release Memory", command=self.deallocate_memory).pack(side=tk.LEFT, padx=5)
        ttk.Button(method_frame, text="Compact Memory", command=self.compact_memory).pack(side=tk.LEFT, padx=5)

        blocks_frame = tk.LabelFrame(
            container,
            text="Memory Blocks (100 blocks)",
            font=self.font_secondary,
            bg=self.bg_color,
            fg=self.text_color
        )
        blocks_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.mem_canvas = tk.Canvas(blocks_frame, bg="white", highlightthickness=0)
        self.mem_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        input_frame = tk.Frame(container, bg=self.bg_color)
        input_frame.pack(fill=tk.X, pady=5)

        tk.Label(input_frame, text="Process ID:", font=self.font_secondary, bg=self.bg_color).pack(side=tk.LEFT, padx=5)
        self.mem_pid = ttk.Entry(input_frame, width=10)
        self.mem_pid.pack(side=tk.LEFT, padx=5)

        tk.Label(input_frame, text="Size (blocks):", font=self.font_secondary, bg=self.bg_color).pack(side=tk.LEFT, padx=5)
        self.mem_size = ttk.Entry(input_frame, width=10)
        self.mem_size.pack(side=tk.LEFT, padx=5)

        table_frame = tk.LabelFrame(
            container,
            text="Process Memory Allocation",
            font=self.font_secondary,
            bg=self.bg_color,
            fg=self.text_color
        )
        table_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.mem_log_table = ttk.Treeview(
            table_frame,
            columns=("pid", "start", "size", "status"),
            show="headings"
        )

        for col in ("pid", "start", "size", "status"):
            self.mem_log_table.heading(col, text=col.title())
            self.mem_log_table.column(col, width=100, anchor="center")

        self.mem_log_table.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.refresh_memory_blocks()

    def refresh_memory_blocks(self):
        self.mem_canvas.delete("all")
        block_width = 60
        block_height = 30
        margin = 10
        spacing = 5
        blocks_per_row = 10

        canvas_width = margin * 2 + (block_width + spacing) * blocks_per_row - spacing
        canvas_height = margin * 2 + (block_height + spacing) * 10 - spacing
        self.mem_canvas.config(width=canvas_width, height=canvas_height)

        seen_pids = set()
        for i in range(100):
            row = i // blocks_per_row
            col = i % blocks_per_row
            x = margin + col * (block_width + spacing)
            y = margin + row * (block_height + spacing)
            block = self.memory_blocks[i]
            if block is None:
                fill_color = "white"
                text = str(i)
            else:
                pid, fill_color = block
                text = f"P{pid}"
                seen_pids.add(str(pid))
            self.mem_canvas.create_rectangle(x, y, x + block_width, y + block_height, fill=fill_color, outline="black")
            self.mem_canvas.create_text(x + block_width / 2, y + block_height / 2, text=text, font=("Segoe UI", 8))

        self.dealloc_dropdown["values"] = sorted(list(seen_pids))

    def allocate_memory(self):
        try:
            pid = int(self.mem_pid.get())
            size = int(self.mem_size.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter numeric values.")
            return

        if size <= 0 or size > 100:
            messagebox.showerror("Invalid Size", "Size must be between 1 and 100 blocks.")
            return

        if any(block and block[0] == pid for block in self.memory_blocks):
            messagebox.showerror("Duplicate PID", f"P{pid} is already allocated.")
            return

        color = self.color_pool[self.color_index % len(self.color_pool)]
        self.color_index += 1

        method = self.alloc_method.get()

        def find_fit():
            best_start = -1
            best_size = 101
            current_start = -1
            current_len = 0
            for i in range(100):
                if self.memory_blocks[i] is None:
                    if current_start == -1:
                        current_start = i
                    current_len += 1
                else:
                    if method == "First-Fit" and current_len >= size:
                        return current_start
                    if method == "Best-Fit" and current_len >= size and current_len < best_size:
                        best_start = current_start
                        best_size = current_len
                    current_start = -1
                    current_len = 0
            if method == "First-Fit" and current_len >= size:
                return current_start
            if method == "Best-Fit" and current_len >= size and current_len < best_size:
                return best_start if best_start != -1 else current_start
            return -1

        start = find_fit()
        if start == -1:
            messagebox.showwarning("Allocation Failed", "No suitable space available.")
            return

        for i in range(start, start + size):
            self.memory_blocks[i] = (pid, color)
        
        self.memory_allocations.append({
            "pid": pid,
            "start": start,
            "size": size,
            "color": color,
            "status": "Allocated"
        })
        
        self.mem_log_table.insert("", tk.END, values=(pid, start, size, "Allocated"))
        self.refresh_memory_blocks()
        self.mem_pid.delete(0, tk.END)
        self.mem_size.delete(0, tk.END)
        
    def deallocate_memory(self):
        selected_pid = self.dealloc_pid.get()
        if not selected_pid:
            messagebox.showwarning("No Selection", "Please select a process to release.")
            return

        try:
            pid = int(selected_pid)  # Ensure numeric comparison
        except ValueError:
            messagebox.showerror("Invalid PID", "Please select a valid process ID.")
            return

        # Find all allocations for this PID
        allocations_to_remove = []
        blocks_freed = 0

        # First pass: Identify allocations to remove and free blocks
        for i, block in enumerate(self.memory_blocks):
            if block is not None and block[0] == pid:
                self.memory_blocks[i] = None  # Free the block
                blocks_freed += 1

        # Second pass: Update allocations list and table
        updated_allocations = []
        for alloc in self.memory_allocations:
            if alloc["pid"] == pid:
                # Update table entry if found
                for item in self.mem_log_table.get_children():
                    values = self.mem_log_table.item(item)["values"]
                    if values[0] == pid and values[3] == "Allocated":
                        self.mem_log_table.delete(item)
                        break
            else:
                updated_allocations.append(alloc)
        self.memory_allocations = updated_allocations

        # Update UI
        self.refresh_memory_blocks()
        
        if blocks_freed > 0:
            messagebox.showinfo("Success", 
                            f"Released {blocks_freed} blocks for Process P{pid}")
        else:
            messagebox.showwarning("Not Found", 
                                f"No allocated memory found for Process P{pid}")
            
    def compact_memory(self):
        allocated = [block for block in self.memory_blocks if block is not None]
        self.memory_blocks = [None] * 100
        for i, block in enumerate(allocated):
            self.memory_blocks[i] = block
        for alloc in self.memory_allocations:
            if alloc["status"] == "Allocated":
                alloc["start"] = self.memory_blocks.index((alloc['pid'], alloc['color']))
        self.refresh_memory_blocks()
        messagebox.showinfo("Success", "Memory compaction completed")


    # File Management Tab
    def create_file(self):
        filename = self.file_name.get()
        content = self.file_content.get()
        
        if not filename:
            messagebox.showerror("Error", "Filename cannot be empty")
            return
            
        try:
            create_file(filename, content, self.current_user)
            self.refresh_files()
            self.refresh_directory_structure()
            messagebox.showinfo("Success", f"File '{filename}' created successfully.")
            self.file_name.delete(0, tk.END)
            self.file_content.set("")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        
    def view_file(self):
        selected = self.file_tree.selection()
        if not selected:
            messagebox.showerror("Error", "No file selected")
            return

        filename = self.file_tree.item(selected[0])['values'][0]
        try:
            content = read_file(filename)
            messagebox.showinfo("File Content", f"Content of '{filename}':\n\n{content}")
        except FileNotFoundError as e:
            messagebox.showerror("Error", str(e))

    def delete_file(self):
        selected = self.file_tree.selection()
        if not selected:
            messagebox.showerror("Error", "No file selected")
            return
            
        filename = self.file_tree.item(selected[0])['values'][0]
        if delete_file(filename):
            messagebox.showinfo("Success", f"Deleted '{filename}'")
            self.refresh_files()
            self.refresh_directory_structure()
        else:
            messagebox.showerror("Error", f"File '{filename}' not found")
    
    def refresh_files(self):
        for item in self.file_tree.get_children():
            self.file_tree.delete(item)
            
        for file in list_files():
            self.file_tree.insert("", tk.END, values=(
                file['name'],
                file['owner'],
                file['size'],
                file['created']
            ))
    

    # Process Scheduling Tab
    def setup_process_scheduling(self):
        container = tk.Frame(self.process_frame, bg=self.bg_color)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Title
        title = tk.Label(
            container,
            text="Process Scheduling",
            font=self.font_title,
            fg=self.primary_color,
            bg=self.bg_color,
            anchor="center",
            justify="center"
        )
        title.pack(pady=(0, 10), fill=tk.X)

        self.scheduler = ProcessScheduler()
        self.current_running = None
        self.running = False
        self.time_quantum = 100
        self.gantt_blocks = []

        # Top Controls
        controls = tk.LabelFrame(container, text="Process Scheduling", font=self.font_secondary, bg=self.bg_color, fg=self.text_color)
        controls.pack(fill=tk.X, pady=5)

        # Process Name
        tk.Label(controls, text="Process Name:", font=self.font_secondary, bg=self.bg_color).grid(row=0, column=0, padx=5, pady=2)
        self.proc_name = ttk.Entry(controls)
        self.proc_name.grid(row=0, column=1, padx=5)

        # Burst Time
        tk.Label(controls, text="Burst Time (ms):", font=self.font_secondary, bg=self.bg_color).grid(row=1, column=0, padx=5, pady=2)
        self.proc_burst = ttk.Entry(controls)
        self.proc_burst.grid(row=1, column=1, padx=5)

        # Algorithm selector
        tk.Label(controls, text="Select Algorithm:", font=self.font_secondary, bg=self.bg_color).grid(row=2, column=0, padx=5, pady=2)
        self.algorithm = ttk.Combobox(controls, values=["First-Come, First-Served (FCFS)", "Round Robin"], state="readonly")
        self.algorithm.current(0)
        self.algorithm.grid(row=2, column=1, padx=5)

        # Quantum for Round Robin
        tk.Label(controls, text="Quantum (ms):", font=self.font_secondary, bg=self.bg_color).grid(row=3, column=0, padx=5, pady=2)
        self.quantum_entry = ttk.Entry(controls)
        self.quantum_entry.insert(0, "100")
        self.quantum_entry.grid(row=3, column=1, padx=5)

        # Buttons
        ttk.Button(controls, text="Add Process", command=self.add_process).grid(row=0, column=2, padx=10)
        ttk.Button(controls, text="Run Scheduler", command=self.run_scheduler).grid(row=1, column=2, padx=10)
        ttk.Button(controls, text="Stop Scheduler", command=self.stop_scheduler).grid(row=2, column=2, padx=10)

        # Ready Queue & Current
        status_frame = tk.Frame(container, bg=self.bg_color)
        status_frame.pack(fill=tk.X, pady=5)

        ready_box = tk.LabelFrame(status_frame, text="Ready Queue", font=self.font_secondary, bg=self.bg_color, fg=self.text_color)
        ready_box.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5)
        self.ready_text = tk.Label(ready_box, text="Queue is empty.", bg="white", font=self.font_secondary, anchor="w", width=40)
        self.ready_text.pack(fill=tk.BOTH)

        running_box = tk.LabelFrame(status_frame, text="Currently Running", font=self.font_secondary, bg=self.bg_color, fg=self.text_color)
        running_box.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5)
        self.running_label = tk.Label(running_box, text="No process running.", bg="white", font=self.font_secondary, anchor="w", width=40)
        self.running_label.pack(fill=tk.BOTH)

        # Gantt Chart
        gantt_box = tk.LabelFrame(container, text="Gantt Chart", font=self.font_secondary, bg=self.bg_color, fg=self.text_color)
        gantt_box.pack(fill=tk.X, pady=5)

        self.gantt_canvas = tk.Canvas(gantt_box, height=50, bg="white", scrollregion=(0, 0, 1000, 50))
        self.gantt_canvas.pack(side=tk.LEFT, fill=tk.X, expand=True)

        scrollbar = tk.Scrollbar(gantt_box, orient=tk.HORIZONTAL, command=self.gantt_canvas.xview)
        scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.gantt_canvas.configure(xscrollcommand=scrollbar.set)

        # Results Table
        result_frame = tk.LabelFrame(container, text="Process Results", font=self.font_secondary, bg=self.bg_color, fg=self.text_color)
        result_frame.pack(fill=tk.BOTH, expand=True)

        self.result_table = ttk.Treeview(result_frame, columns=("pid", "name", "burst", "arrival", "completion", "waiting", "turnaround"), show="headings")
        for col in ["pid", "name", "burst", "arrival", "completion", "waiting", "turnaround"]:
            self.result_table.heading(col, text=col.capitalize())
            self.result_table.column(col, anchor="center", width=80)
        self.result_table.pack(fill=tk.BOTH, expand=True)

        # Process Data Store
        self.proc_list = []
        self.gantt_time = 0
        self.pid_counter = 1

    def add_process(self):
        name = self.proc_name.get()
        try:
            burst = int(self.proc_burst.get())
        except ValueError:
            messagebox.showerror("Error", "Burst time must be an integer")
            return

        if not name or burst <= 0:
            messagebox.showerror("Error", "Please enter a valid name and burst time")
            return

        process = {
            "pid": self.pid_counter,
            "name": name,
            "burst": burst,
            "arrival": self.gantt_time,
            "remaining": burst,
            "completion": None,
            "waiting": 0,
            "turnaround": 0,
            "status": "Ready"
        }
        self.proc_list.append(process)
        self.pid_counter += 1
        self.update_ready_queue()
        self.proc_name.delete(0, tk.END)
        self.proc_burst.delete(0, tk.END)

    def update_ready_queue(self):
        names = [f"P{p['pid']} ({p['name']})" for p in self.proc_list if p["status"] == "Ready"]
        self.ready_text.config(text=", ".join(names) if names else "Queue is empty.")

    def run_scheduler(self):
        algo = self.algorithm.get()
        try:
            quantum = int(self.quantum_entry.get())
        except ValueError:
            quantum = 100
            
        # Reset state when starting scheduler
        self.clear_gantt_chart()
        
        self.running = True
        if algo == "First-Come, First-Served (FCFS)":
            self.schedule_fcfs()
        else:
            self.schedule_rr(quantum)

    def stop_scheduler(self):
        self.running = False
        self.clear_gantt_chart()
        self.running_label.config(text="No process running.")  

    def schedule_fcfs(self):
        if not self.proc_list or not self.running:
            return

        ready = [p for p in self.proc_list if p["status"] == "Ready"]
        if not ready:
            return

        process = ready[0]
        process["status"] = "Running"
        self.update_ready_queue()
        self.running_label.config(text=f"Running: P{process['pid']} ({process['name']}) for {process['burst']}ms")
        duration = process["burst"]

        # Assign unique color if not already set
        if "color" not in process:
            process["color"] = f"#{random.randint(100,255):02x}{random.randint(100,255):02x}{random.randint(100,255):02x}"

        self.root.after(duration, lambda: self.finish_process(process))

        x = len(self.gantt_blocks) * 80
        self.gantt_canvas.create_rectangle(x, 0, x+80, 50, fill=process["color"])
        self.gantt_canvas.create_text(x+40, 25, text=f"P{process['pid']}", font=("Segoe UI", 10))
        self.gantt_blocks.append(process)
        self.gantt_time += duration

    def schedule_rr(self, quantum):
        if not self.running:
            return

        # Get all ready processes (ensure no starvation by rotating the queue)
        ready = [p for p in self.proc_list if p["status"] == "Ready"]
        if not ready:
            if all(p["status"] == "Completed" for p in self.proc_list):
                self.running_label.config(text="All processes completed!")
            return

        # Pick the next process from the ready queue
        process = ready[0]
        process["status"] = "Running"
        self.update_ready_queue()

        # Calculate time slice
        slice_time = min(quantum, process["remaining"])
        self.running_label.config(
            text=f"Running: P{process['pid']} ({process['name']}) | Slice: {slice_time}ms | Remaining: {process['remaining']}ms"
        )

        if "color" not in process:
            process["color"] = f"#{random.randint(100, 255):02x}{random.randint(100, 255):02x}{random.randint(100, 255):02x}"

        # Add block to Gantt chart
        x_start = sum(block["slice_time"] for block in self.gantt_blocks)
        x_end = x_start + slice_time
        block = {
            "pid": process["pid"],
            "slice_time": slice_time,
            "color": process["color"]
        }
        self.gantt_blocks.append(block)

        # Draw the block
        pixel_width = slice_time
        self.gantt_canvas.create_rectangle(
            x_start, 0, x_start + pixel_width, 50,
            fill=process["color"], outline="black"
        )
        self.gantt_canvas.create_text(
            x_start + pixel_width // 2, 25,
            text=f"P{process['pid']}", font=("Arial", 8)
        )

        # Update scroll region
        self.gantt_canvas.config(scrollregion=(0, 0, x_end + 100, 50))

        # Update process state
        process["remaining"] -= slice_time
        self.gantt_time += slice_time

        def next_step():
            if process["remaining"] <= 0:
                process["status"] = "Completed"
                process["completion"] = self.gantt_time
                process["turnaround"] = process["completion"] - process["arrival"]
                process["waiting"] = process["turnaround"] - process["burst"]
                self.refresh_results()
            else:
                # Move the process to the end of the ready queue
                process["status"] = "Ready"
                self.proc_list.remove(process)  # Remove from current position
                self.proc_list.append(process)  # Add to end (simulate queue rotation)

            # Continue scheduling
            if self.running:
                self.schedule_rr(quantum)

        # Schedule the next step after the current slice
        self.root.after(slice_time, next_step)

    def finish_process(self, process):
        process["status"] = "Completed"
        process["completion"] = self.gantt_time
        process["turnaround"] = process["completion"] - process["arrival"]
        process["waiting"] = process["turnaround"] - process["burst"]
        self.running_label.config(text="All processes completed!")
        self.update_ready_queue()
        self.refresh_results()
        if self.algorithm.get() == "First-Come, First-Served (FCFS)" and self.running:
            self.schedule_fcfs()

    def refresh_results(self):
        for item in self.result_table.get_children():
            self.result_table.delete(item)
        for p in self.proc_list:
            if p["status"] in ["Completed"]:
                self.result_table.insert("", tk.END, values=(
                    p["pid"], p["name"], p["burst"], p["arrival"],
                    p["completion"], p["waiting"], p["turnaround"]
                ))
    
    def clear_gantt_chart(self):
        self.gantt_canvas.delete("all")
        self.gantt_blocks = []
        self.gantt_time = 0
        
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
            
if __name__ == "__main__":
    root = tk.Tk()
    app = MiniOS(root)
    root.mainloop()