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

            # 設置窗口
            self.root.title("待辦事項清單")
            self.root.geometry("500x600")
            self.root.resizable(False, False)

            # 應用簡潔風格樣式
            self.style = ttk.Style()
            self.style.theme_use("clam")
            self.style.configure("TFrame", background="#f5f5f5")
            self.style.configure(
                "TLabel", background="#f5f5f5", font=("Microsoft YaHei", 12)
            )
            self.style.configure(
                "TButton",
                background="#4CAF50",
                foreground="white",
                borderwidth=0,
                focuscolor="none",
                font=("Microsoft YaHei", 10),
            )
            self.style.map("TButton", background=[("active", "#45a049")])
            self.style.configure("TEntry", font=("Microsoft YaHei", 12))
            self.style.configure(
                "Header.TLabel",
                font=("Microsoft YaHei", 16, "bold"),
                background="#f5f5f5",
                foreground="#333333",
            )

            # 創建主框架
            self.main_frame = ttk.Frame(root, padding="30")
            self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            root.columnconfigure(0, weight=1)
            root.rowconfigure(0, weight=1)

            # 設置窗口背景色
            self.root.configure(bg="#f5f5f5")

            # 綁定窗口點擊事件來清除選取
            self.root.bind("<Button-1>", self.on_window_click)

            self.create_widgets()

        def create_widgets(self):
            # 標題
            title_label = ttk.Label(
                self.main_frame, text="我的待辦清單", style="Header.TLabel"
            )
            title_label.grid(row=0, column=0, columnspan=3, pady=(0, 30), sticky=tk.W)

            # 輸入區域框架
            input_frame = ttk.Frame(self.main_frame)
            input_frame.grid(
                row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 25)
            )
            input_frame.columnconfigure(0, weight=1)

            # 任務輸入框
            self.task_entry = ttk.Entry(input_frame, width=40)
            self.task_entry.grid(row=0, column=0, padx=(0, 12), sticky=(tk.W, tk.E))
            self.task_entry.bind("<Return>", lambda e: self.add_task_input())

            # 添加按鈕
            add_button = ttk.Button(
                input_frame, text="新增任務", command=self.add_task_input
            )
            add_button.grid(row=0, column=1)

            # 分隔線
            separator = ttk.Separator(self.main_frame, orient="horizontal")
            separator.grid(
                row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15)
            )

            # 任務列表框架
            list_frame = ttk.Frame(self.main_frame)
            list_frame.grid(
                row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S)
            )
            self.main_frame.rowconfigure(3, weight=1)
            list_frame.columnconfigure(0, weight=1)
            list_frame.rowconfigure(0, weight=1)

            # 任務列表 (使用Listbox)
            self.task_listbox = tk.Listbox(
                list_frame,
                font=("Microsoft YaHei", 11),
                bd=0,
                highlightthickness=0,
                selectmode=tk.SINGLE,
                height=15,
                selectbackground="#E3F2FD",
                selectforeground="#1976D2",
                exportselection=False,
            )
            self.task_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

            # 綁定事件處理
            self.task_listbox.bind("<Button-1>", self.on_listbox_click)
            self.task_listbox.bind("<Leave>", self.clear_selection)

            # 滾動條
            scrollbar = ttk.Scrollbar(
                list_frame, orient=tk.VERTICAL, command=self.task_listbox.yview
            )
            scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
            self.task_listbox.configure(yscrollcommand=scrollbar.set)

            # 按鈕框架
            button_frame = ttk.Frame(self.main_frame)
            button_frame.grid(row=4, column=0, columnspan=3, pady=(20, 0))

            # 刪除按鈕
            delete_button = ttk.Button(
                button_frame, text="刪除選中任務", command=self.delete_selected_task
            )
            delete_button.grid(row=0, column=0, padx=(0, 10))

            # 清空按鈕
            clear_button = ttk.Button(
                button_frame, text="清空所有", command=self.clear_all_tasks
            )
            clear_button.grid(row=0, column=1)

            # 統計標籤
            self.status_label = ttk.Label(
                self.main_frame, text="共 0 項任務", font=("Microsoft YaHei", 10)
            )
            self.status_label.grid(
                row=5, column=0, columnspan=3, pady=(15, 0), sticky=tk.W
            )

        def add_task_input(self):
            task = self.task_entry.get().strip()
            if task:
                self.todolist.add_task(task)
                self.task_listbox.insert(tk.END, task)
                self.task_entry.delete(0, tk.END)
                self.update_status()
                self.task_entry.focus()

        def on_listbox_click(self, event):
            # 短暫延遲後清除選取，讓用戶看到選取效果
            self.root.after(150, self.clear_selection)

        def clear_selection(self, event=None):
            """清除列表選取狀態"""
            try:
                self.task_listbox.selection_clear(0, tk.END)
            except:
                pass

        def on_window_click(self, event):
            """處理窗口點擊事件，清除列表選取狀態"""
            # 檢查點擊是否在列表框內
            widget = event.widget
            if widget != self.task_listbox and not self.is_child_of(
                widget, self.task_listbox
            ):
                self.clear_selection()

        def is_child_of(self, widget, parent):
            """檢查widget是否是parent的子組件"""
            try:
                while widget:
                    if widget == parent:
                        return True
                    widget = widget.master
                return False
            except:
                return False

        def delete_selected_task(self):
            # 如果當前沒有選取項目，但列表中有項目，默認選中第一個
            selection = self.task_listbox.curselection()
            if not selection and self.task_listbox.size() > 0:
                selection = (0,)  # 選中第一個項目
                self.task_listbox.selection_set(0)
            elif not selection:
                messagebox.showinfo("提示", "沒有可刪除的任務")
                return

            if selection:
                index = selection[0]
                task_text = self.task_listbox.get(index)

                # 確保項目在視圖中可見
                self.task_listbox.see(index)

                # 確認對話框
                result = messagebox.askyesno(
                    "確認刪除", f"確定要刪除任務：{task_text}？"
                )
                if result:
                    self.todolist.remove_task_by_index(index)
                    self.task_listbox.delete(index)
                    self.update_status()
                    # 清除選取狀態
                    self.clear_selection()

        def clear_all_tasks(self):
            if self.task_listbox.size() > 0:
                result = messagebox.askyesno("確認", "確定要清空所有任務嗎？")
                if result:
                    self.task_listbox.delete(0, tk.END)
                    self.todolist.tasks = []
                    self.update_status()

        def update_status(self):
            count = self.task_listbox.size()
            self.status_label.config(text=f"共 {count} 項任務")

    # 創建並運行GUI
    root = tk.Tk()
    app = TodoListGUI(root)
    root.mainloop()
