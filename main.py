# Initialise the object of the todo list
class todolist:
    def __init__(self):
        self.tasks = []
        self.selected_index = None

    def add_task(self, task):
        self.tasks.append(task)
        return f'Task "{task}" added.'

    def remove_task(self, task):
        if task in self.tasks:
            self.tasks.remove(task)
            return f'Task "{task}" removed.'
        else:
            return f'Task "{task}" not found.'

    def remove_task_by_index(self, index):
        if 0 <= index < len(self.tasks):
            removed_task = self.tasks.pop(index)
            return f'Task "{removed_task}" removed.'
        else:
            return "Invalid task index."

    def view_tasks(self):
        if not self.tasks:
            return "No tasks in the list."
        else:
            return self.tasks


if __name__ == "__main__":
    import tkinter as tk
    from tkinter import ttk, messagebox

    class TodoListGUI:
        def __init__(self, root):
            self.root = root
            self.todolist = todolist()

            # 定義Apple風格的色彩系統
            self.colors = {
                'bg': '#F2F2F7',          # 淺灰背景 (Apple系統灰)
                'card': '#FFFFFF',        # 卡片白
                'primary': '#007AFF',     # Apple藍
                'text': '#1D1D1F',        # 深灰文字 (Apple常用)
                'secondary_text': '#8E8E93', # 次要文字
                'border': '#C6C6C8',      # 邊框灰
                'hover': '#E5E5EA',       # 懸停灰
                'selected': '#E5F2FF',    # 選中藍
                'delete': '#FF3B30',      # 刪除紅 (Apple紅)
                'success': '#34C759'      # 成功綠 (Apple綠)
            }

            # 設置窗口
            self.root.title("備忘錄")
            self.root.geometry("480x640")
            self.root.minsize(320, 480)  # 設置最小尺寸
            self.root.resizable(True, True)  # 允許調整窗口大小

            # 應用Apple風格樣式
            self.style = ttk.Style()
            self.style.theme_use("clam")

            # 框架樣式
            self.style.configure("TFrame", background=self.colors['bg'])

            # 標籤樣式 - Apple字體風格
            self.style.configure(
                "TLabel",
                background=self.colors['bg'],
                foreground=self.colors['text'],
                font=("Helvetica Neue", 13)
            )

            # 標題樣式
            self.style.configure(
                "Header.TLabel",
                font=("Helvetica Neue", 26, "bold"),
                background=self.colors['bg'],
                foreground=self.colors['text']
            )

            # 次要文字樣式
            self.style.configure(
                "Secondary.TLabel",
                font=("Helvetica Neue", 11),
                background=self.colors['bg'],
                foreground=self.colors['secondary_text']
            )

            # 主要按鈕樣式 - Apple風格
            self.style.configure(
                "Primary.TButton",
                background=self.colors['primary'],
                foreground="white",
                borderwidth=0,
                focuscolor="none",
                font=("Helvetica Neue", 13),
                padding=(16, 8)
            )
            self.style.map(
                "Primary.TButton",
                background=[("active", "#0051D5"), ("pressed", "#0047B9")]
            )

            # 次要按鈕樣式
            self.style.configure(
                "Secondary.TButton",
                background=self.colors['card'],
                foreground=self.colors['delete'],
                borderwidth=1,
                font=("Helvetica Neue", 13),
                padding=(16, 8)
            )
            self.style.map(
                "Secondary.TButton",
                background=[("active", self.colors['hover'])],
                foreground=[("active", self.colors['delete'])]
            )

            # 輸入框樣式
            self.style.configure(
                "TEntry",
                font=("Helvetica Neue", 15),
                padding=(12, 10)
            )

            # 創建主框架 - Apple風格的內邊距
            self.main_frame = ttk.Frame(root, padding="24 28 24 28")
            self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            root.columnconfigure(0, weight=1)
            root.rowconfigure(0, weight=1)

            # 設置窗口背景色
            self.root.configure(bg=self.colors['bg'])

            # 綁定點擊事件來清除選取 - 點擊主框架空白區域時觸發
            self.main_frame.bind("<Button-1>", self.on_window_click)

            self.create_widgets()

        def create_widgets(self):
            # 標題
            title_label = ttk.Label(
                self.main_frame, text="我的備忘錄", style="Header.TLabel"
            )
            title_label.grid(row=0, column=0, columnspan=3, pady=(0, 24), sticky=tk.W)

            # 輸入區域框架
            input_frame = ttk.Frame(self.main_frame)
            input_frame.grid(
                row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N), pady=(0, 20)
            )
            input_frame.columnconfigure(0, weight=1)

            # 任務輸入框 - Apple風格的圓角
            self.task_entry = ttk.Entry(input_frame)
            self.task_entry.grid(row=0, column=0, padx=(0, 12), sticky=(tk.W, tk.E, tk.N))
            self.task_entry.bind("<Return>", lambda e: self.add_task_input())

            # 添加按鈕
            add_button = ttk.Button(
                input_frame, text="新增", command=self.add_task_input, style="Primary.TButton"
            )
            add_button.grid(row=0, column=1, sticky=(tk.N, tk.E))

            # 任務列表框架 - Apple風格的卡片
            list_frame = ttk.Frame(self.main_frame, style="TFrame")
            list_frame.grid(
                row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20)
            )
            self.main_frame.rowconfigure(2, weight=1)  # 列表框架可以擴展
            self.main_frame.columnconfigure(0, weight=1)  # 確保主框架可以擴展
            list_frame.columnconfigure(0, weight=1)
            list_frame.rowconfigure(0, weight=1)

            # 任務列表 (自定義樣式的Listbox)
            self.task_listbox = tk.Listbox(
                list_frame,
                font=("Helvetica Neue", 15),
                bd=0,
                highlightthickness=0,
                selectmode=tk.SINGLE,
                bg=self.colors['card'],
                fg=self.colors['text'],
                selectbackground=self.colors['selected'],
                selectforeground=self.colors['primary'],
                activestyle='none',
                relief='flat',
                exportselection=False,
            )
            self.task_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            # 確保列表框可以擴展
            self.task_listbox.config(width=0)  # 讓寬度自動適應

            # 滾動條 - Apple風格
            scrollbar = ttk.Scrollbar(
                list_frame, orient=tk.VERTICAL, command=self.task_listbox.yview
            )
            scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
            self.task_listbox.configure(yscrollcommand=scrollbar.set)

            # 按鈕框架
            button_frame = ttk.Frame(self.main_frame)
            button_frame.grid(row=3, column=0, columnspan=3)

            # 刪除按鈕
            delete_button = ttk.Button(
                button_frame, text="刪除選中備忘", command=self.delete_selected_task, style="Secondary.TButton"
            )
            delete_button.grid(row=0, column=0, padx=(0, 10))

            # 清空按鈕
            clear_button = ttk.Button(
                button_frame,
                text="清空所有",
                command=self.clear_all_tasks,
                style="Secondary.TButton"
            )
            clear_button.grid(row=0, column=1)

            # 統計標籤
            self.status_label = ttk.Label(
                self.main_frame, text="共 0 項備忘", style="Secondary.TLabel"
            )
            self.status_label.grid(
                row=4, column=0, columnspan=3, pady=(12, 0), sticky=tk.W
            )

        def add_task_input(self):
            task = self.task_entry.get().strip()
            if task:
                self.todolist.add_task(task)
                self.task_listbox.insert(tk.END, f"  {task}")  # 添加左邊距
                self.task_entry.delete(0, tk.END)
                self.update_status()
                self.task_entry.focus()

        def clear_selection(self, event=None):
            """清除列表選取狀態"""
            try:
                self.task_listbox.selection_clear(0, tk.END)
            except:
                pass

        def on_window_click(self, event):
            """點擊主框架空白區域時清除選取"""
            # 如果直接點擊在主框架上（空白區域），清除選取
            if event.widget == self.main_frame:
                self.clear_selection()

        def delete_selected_task(self):
            # 如果當前沒有選取項目，但列表中有項目，默認選中第一個
            selection = self.task_listbox.curselection()
            if not selection and self.task_listbox.size() > 0:
                selection = (0,)  # 選中第一個項目
                self.task_listbox.selection_set(0)
            elif not selection:
                messagebox.showinfo("提示", "沒有可刪除的備忘")
                return

            if selection:
                index = selection[0]
                task_text = self.task_listbox.get(index).strip()

                # 確保項目在視圖中可見
                self.task_listbox.see(index)

                # 確認對話框
                result = messagebox.askyesno(
                    "確認刪除", f"確定要刪除此備忘嗎？\n\n{task_text}"
                )
                if result:
                    self.todolist.remove_task_by_index(index)
                    self.task_listbox.delete(index)
                    self.update_status()
                    # 清除選取狀態
                    self.clear_selection()

        def clear_all_tasks(self):
            if self.task_listbox.size() > 0:
                result = messagebox.askyesno("確認", "確定要清空所有備忘嗎？")
                if result:
                    self.task_listbox.delete(0, tk.END)
                    self.todolist.tasks = []
                    self.update_status()

        def update_status(self):
            count = self.task_listbox.size()
            self.status_label.config(text=f"共 {count} 項備忘")

    # 創建並運行GUI
    root = tk.Tk()
    app = TodoListGUI(root)
    root.mainloop()
