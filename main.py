# Initialise the object of the todo list
import datetime as dt
import threading
import time
import uuid
import queue
class todolist:
    def __init__(self):
        # 現在的 tasks 將儲存字典而不是字符串，保持向後兼容性
        self.tasks = []
        self.selected_index = None

    def add_task(self, task, notification_time=None):
        """
        添加任務，可選日期時間

        Args:
            task: 任務文本 (str)
            notification_time: 通知時間 (datetime, 可選)

        Returns:
            str: 確認訊息
        """
        if isinstance(task, str):
            # 為向後兼容，將字符串轉換為字典格式
            task_dict = {
                'text': task,
                'notification_time': notification_time,
                'id': str(uuid.uuid4()),
                'created_at': dt.datetime.now()
            }
            self.tasks.append(task_dict)
        else:
            # 如果是字典格式（新版本），直接添加
            task['id'] = task.get('id', str(uuid.uuid4()))
            task['created_at'] = task.get('created_at', dt.datetime.now())
            self.tasks.append(task)

        if notification_time:
            return f'Scheduled task "{task}" set for {notification_time.strftime("%Y-%m-%d %H:%M")}.'
        else:
            return f'Task "{task}" added.'

    def remove_task(self, task_or_id):
        """
        移除任務（支持字符串文本或任務 ID）

        Args:
            task_or_id: 任務文本、任務字典或任務 ID

        Returns:
            str: 確認訊息
        """
        # 嘗試按 ID 查找
        if isinstance(task_or_id, str):
            for task in self.tasks:
                if isinstance(task, dict) and task.get('id') == task_or_id:
                    self.tasks.remove(task)
                    return f'Task "{task["text"]}" removed.'
                elif isinstance(task, str) and task == task_or_id:
                    self.tasks.remove(task)
                    return f'Task "{task}" removed.'
        # 如果是字典，直接比較
        elif isinstance(task_or_id, dict) and task_or_id in self.tasks:
            self.tasks.remove(task_or_id)
            return f'Task "{task_or_id["text"]}" removed.'

        return f'Task not found.'

    def remove_task_by_index(self, index):
        if 0 <= index < len(self.tasks):
            removed_task = self.tasks.pop(index)
            if isinstance(removed_task, dict):
                return f'Task "{removed_task["text"]}" removed.'
            else:
                return f'Task "{removed_task}" removed.'
        else:
            return "Invalid task index."

    def view_tasks(self):
        if not self.tasks:
            return "No tasks in the list."
        else:
            # 為向後兼容，返回純文本列表（舊版本兼容）
            return [task['text'] if isinstance(task, dict) else task for task in self.tasks]

    def get_scheduled_tasks(self):
        """
        獲取所有預定通知的任務

        Returns:
            list: 預定任務列表
        """
        return [task for task in self.tasks
                if isinstance(task, dict) and task.get('notification_time')]

    def get_task_by_id(self, task_id):
        """
        根據 ID 獲取任務

        Args:
            task_id: 任務 ID

        Returns:
            dict or None: 任務字典或未找到時返回 None
        """
        for task in self.tasks:
            if isinstance(task, dict) and task.get('id') == task_id:
                return task
        return None


class NotificationScheduler:
    """
    通知調度器 - 負責管理和觸發定時通知
    單例模式實現，確保全局只有一個調度器實例
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.scheduled_notifications = {}  # {task_id: (threading.Timer, task)}
            self.notification_queue = queue.Queue()
            self.running = True
            self.daemon_thread = threading.Thread(target=self._notification_daemon, daemon=True)
            self.daemon_thread.start()
            self.initialized = True

    def schedule_notification(self, task_id, notification_time, task_text):
        """
        調度通知

        Args:
            task_id: 任務 ID
            notification_time: 通知時間 (datetime)
            task_text: 任務文本

        Returns:
            bool: 是否成功調度
        """
        if task_id in self.scheduled_notifications:
            # 如果已經存在，先取消舊的通知
            self.cancel_notification(task_id)

        # 計算延遲時間
        now = dt.datetime.now()
        if notification_time <= now:
            # 如果通知時間已過，立即觸發
            self._trigger_notification(task_id, task_text)
            return True

        delay = (notification_time - now).total_seconds()

        # 創建定時器
        timer = threading.Timer(delay, self._trigger_notification, args=[task_id, task_text])
        timer.daemon = True
        timer.start()

        # 儲存調度信息
        self.scheduled_notifications[task_id] = (timer, task_text)
        return True

    def cancel_notification(self, task_id):
        """
        取消通知

        Args:
            task_id: 任務 ID

        Returns:
            bool: 是否成功取消
        """
        if task_id in self.scheduled_notifications:
            timer, task_text = self.scheduled_notifications[task_id]
            timer.cancel()
            del self.scheduled_notifications[task_id]
            return True
        return False

    def _trigger_notification(self, task_id, task_text):
        """
        觸發通知的內部方法

        Args:
            task_id: 任務 ID
            task_text: 任務文本
        """
        # 將通知放入佇列，由守護線程處理
        self.notification_queue.put({
            'task_id': task_id,
            'task_text': task_text,
            'timestamp': dt.datetime.now()
        })

        # 清理已觸發的通知
        if task_id in self.scheduled_notifications:
            del self.scheduled_notifications[task_id]

    def _notification_daemon(self):
        """
        通知守護線程 - 負責顯示通知
        """
        while self.running:
            try:
                # 等待通知，超時 1 秒檢查 running 狀態
                notification = self.notification_queue.get(timeout=1)
                self._show_notification(notification)
                self.notification_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                print(f"通知錯誤: {e}")

    def _show_notification(self, notification):
        """
        顯示 Apple 風格的通知

        Args:
            notification: 通知字典
        """
        try:
            # 在 macOS 上使用 osascript 發送系統通知
            import subprocess
            import platform

            if platform.system() == "Darwin":  # macOS
                title = "備忘錄提醒"
                message = f"提醒：{notification['task_text']}"
                sound = "Glass"  # Apple 系統音效

                script = f'''
                display notification "{message}" with title "{title}" subtitle "定時提醒" sound name "{sound}"
                '''

                result = subprocess.run(
                    ['osascript', '-e', script],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode != 0:
                    # 降級到 tkMessageBox
                    self._fallback_notification(notification)
            else:
                # 其他平台使用備用方案
                self._fallback_notification(notification)

        except Exception as e:
            print(f"通知發送失敗: {e}")
            # 最終備用方案
            self._fallback_notification(notification)

    def _fallback_notification(self, notification):
        """
        備用通知方案（使用 messagebox）

        Args:
            notification: 通知字典
        """
        # 檢查是否有 tkinter root 實例
        try:
            import tkinter as tk
            from tkinter import messagebox

            # 嘗試找到現有的 root 窗口
            for widget in tk._default_root.winfo_children():
                if isinstance(widget, tk.Tk):
                    root = widget
                    break
            else:
                # 如果找不到，創建一個临時窗口
                root = tk.Tk()
                root.withdraw()  # 隱藏窗口
                cleanup_root = True

            messagebox.showinfo(
                "備忘錄提醒",
                f"提醒：{notification['task_text']}",
                parent=root if not cleanup_root else None
            )

            if cleanup_root:
                root.destroy()

        except Exception:
            # 最終備用 - 控制台輸出
            print(f"=== 備忘錄提醒 ===")
            print(f"提醒：{notification['task_text']}")
            print(f"時間：{notification['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
            print("=" * 20)

    def get_scheduled_count(self):
        """
        獲取已調度的通知數量

        Returns:
            int: 調度中的通知數量
        """
        return len(self.scheduled_notifications)

    def get_all_scheduled(self):
        """
        獲取所有已調度的通知信息

        Returns:
            list: 調度信息列表
        """
        result = []
        for task_id, (timer, task_text) in self.scheduled_notifications.items():
            # 獲取剩餘時間
            try:
                remaining_time = timer.interval - timer.finished.wait(0)
                remaining_time = max(0, remaining_time)
                result.append({
                    'task_id': task_id,
                    'task_text': task_text,
                    'remaining_seconds': remaining_time
                })
            except:
                # 如果計時器已經完成，跳過
                continue
        return result

    def shutdown(self):
        """
        關閉調度器
        """
        self.running = False

        # 取消所有調度的通知
        for task_id in list(self.scheduled_notifications.keys()):
            self.cancel_notification(task_id)

        # 等待守護線程結束
        if self.daemon_thread.is_alive():
            self.daemon_thread.join(timeout=2)


if __name__ == "__main__":
    import tkinter as tk
    from tkinter import ttk, messagebox

    class TodoListGUI:
        def __init__(self, root):
            self.root = root
            self.todolist = todolist()
            # 初始化通知調度器
            self.notification_scheduler = NotificationScheduler()

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
                font=("SF Pro Text", 13)  # Prefer SF Pro if available, fallback to Helvetica Neue
            )

            # 標題樣式
            self.style.configure(
                "Header.TLabel",
                font=("SF Pro Display", 28, "bold"),
                background=self.colors['bg'],
                foreground=self.colors['text']
            )

            # 次要文字樣式
            self.style.configure(
                "Secondary.TLabel",
                font=("SF Pro Text", 11),
                background=self.colors['bg'],
                foreground=self.colors['secondary_text']
            )

            # 卡片樣式
            self.style.configure(
                "Card.TFrame",
                background=self.colors['card']
            )

            # 主要按鈕樣式 - Apple風格
            self.style.configure(
                "Primary.TButton",
                background=self.colors['primary'],
                foreground="white",
                borderwidth=0,
                focuscolor="none",
                font=("SF Pro Text", 13, "bold"),
                padding=(20, 10)
            )
            self.style.map(
                "Primary.TButton",
                background=[("active", "#0051D5"), ("pressed", "#0047B9")]
            )

            # 次要按鈕樣式
            self.style.configure(
                "Secondary.TButton",
                background=self.colors['card'],
                foreground=self.colors['primary'], # Secondary actions often use Primary color in iOS
                borderwidth=0,
                font=("SF Pro Text", 13),
                padding=(16, 8)
            )
            self.style.map(
                "Secondary.TButton",
                background=[("active", self.colors['hover'])],
                foreground=[("active", self.colors['primary'])]
            )

            # 輸入框樣式
            self.style.configure(
                "TEntry",
                font=("SF Pro Text", 15),
                padding=(12, 12),
                borderwidth=0
            )

            # 創建主框架 - Apple風格的內邊距
            self.main_frame = ttk.Frame(root, padding="24")
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
            title_label.grid(row=0, column=0, columnspan=3, pady=(0, 32), sticky=tk.W)

            # 輸入區域框架
            input_frame = ttk.Frame(self.main_frame)
            input_frame.grid(
                row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N), pady=(0, 24)
            )
            input_frame.columnconfigure(0, weight=1)

            # 任務輸入框 - Apple風格的圓角
            self.task_entry = ttk.Entry(input_frame, style="TEntry")
            self.task_entry.grid(row=0, column=0, columnspan=2, padx=(0, 12), sticky=(tk.W, tk.E, tk.N))
            self.task_entry.bind("<Return>", lambda e: self.add_task_input())

            # 定時通知按鈕
            self.schedule_button = ttk.Button(
                input_frame, text="⏰", command=self.show_datetime_picker, width=3, style="Secondary.TButton"
            )
            self.schedule_button.grid(row=0, column=2, sticky=(tk.N, tk.E), padx=(0, 8))

            # 添加按鈕
            add_button = ttk.Button(
                input_frame, text="新增", command=self.add_task_input, style="Primary.TButton"
            )
            add_button.grid(row=0, column=3, sticky=(tk.N, tk.E))

            # 日期時間選擇框架（隱藏預設）
            self.datetime_frame = ttk.Frame(self.main_frame)
            self.datetime_frame.grid(
                row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 24)
            )
            self.datetime_frame.columnconfigure(1, weight=1)
            self.datetime_frame.grid_remove()  # 初始隱藏

            # 日期選擇標籤
            date_label = ttk.Label(self.datetime_frame, text="提醒日期時間:", style="Secondary.TLabel")
            date_label.grid(row=0, column=0, padx=(0, 8), sticky=tk.W)

            # 日期時間輸入框
            self.datetime_var = tk.StringVar(value="")
            self.datetime_entry = ttk.Entry(self.datetime_frame, textvariable=self.datetime_var, width=25)
            self.datetime_entry.grid(row=0, column=1, padx=(0, 8), sticky=(tk.W, tk.E))
            self.datetime_entry.bind("<KeyRelease>", self.validate_datetime_input)
            self.datetime_entry.bind("<FocusOut>", self.parse_datetime)

            # 清除按鈕
            clear_datetime_button = ttk.Button(
                self.datetime_frame, text="✖", command=self.clear_datetime, width=3
            )
            clear_datetime_button.grid(row=0, column=2)

            # 選定的日期時間
            self.selected_datetime = None

            # 任務列表框架 - Apple風格的卡片
            # Use Card.TFrame for white background
            list_frame = ttk.Frame(self.main_frame, style="Card.TFrame", padding=10)
            list_frame.grid(
                row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 24)
            )
            self.main_frame.rowconfigure(3, weight=1)  # 列表框架可以擴展
            self.main_frame.columnconfigure(0, weight=1)  # 確保主框架可以擴展
            list_frame.columnconfigure(0, weight=1)
            list_frame.rowconfigure(0, weight=1)

            # 任務列表 (自定義樣式的Listbox)
            self.task_listbox = tk.Listbox(
                list_frame,
                font=("SF Pro Text", 15),
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
            button_frame.grid(row=4, column=0, columnspan=3, pady=(0, 16))

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
            clear_button.grid(row=0, column=1, padx=(0, 10))

            # 通知管理按鈕
            notification_button = ttk.Button(
                button_frame,
                text="📅 通知管理",
                command=self.show_notification_manager,
                style="Secondary.TButton"
            )
            notification_button.grid(row=0, column=2)

            # 統計標籤
            self.status_label = ttk.Label(
                self.main_frame, text="共 0 項備忘", style="Secondary.TLabel"
            )
            self.status_label.grid(
                row=5, column=0, columnspan=3, pady=(12, 0), sticky=tk.W
            )

        def add_task_input(self):
            task = self.task_entry.get().strip()
            if task:
                # 添加任務，如果設定了通知時間則一併傳遞
                message = self.todolist.add_task(task, self.selected_datetime)

                # 如果有通知時間，調度通知
                if self.selected_datetime:
                    task_dict = self.todolist.tasks[-1]  # 獲取剛才添加的任務
                    self.notification_scheduler.schedule_notification(
                        task_dict['id'],
                        self.selected_datetime,
                        task
                    )

                # 顯示在列表中
                self.display_task_in_list(task, self.selected_datetime)

                # 清空輸入和重置狀態
                self.task_entry.delete(0, tk.END)
                self.clear_datetime()
                self.datetime_frame.grid_remove()
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

        def show_datetime_picker(self):
            """顯示/隱藏日期時間選擇器"""
            if self.datetime_frame.winfo_ismapped():
                self.datetime_frame.grid_remove()
            else:
                self.datetime_frame.grid()
                self.datetime_entry.focus()

        def clear_datetime(self):
            """清除選定的日期時間"""
            self.selected_datetime = None
            self.datetime_var.set("")

        def display_task_in_list(self, task_text, notification_time=None):
            """在列表中顯示任務，支持顯示通知時間"""
            if notification_time:
                time_str = notification_time.strftime("%m/%d %H:%M")
                display_text = f"  ⏰ {task_text} ({time_str})"
            else:
                display_text = f"  {task_text}"

            self.task_listbox.insert(tk.END, display_text)

        def validate_datetime_input(self, event):
            """驗證日期時間輸入格式即時提示"""
            input_text = self.datetime_var.get().strip()

            if not input_text:
                self.datetime_entry.config(foreground=self.colors['text'])
                return

            # 簡單的格式提示 (支持 MM/DD HH:MM 或 YYYY/MM/DD HH:MM)
            patterns = [
                r'\d{1,2}/\d{1,2} \d{1,2}:\d{2}$',      # MM/DD HH:MM
                r'\d{4}/\d{1,2}/\d{1,2} \d{1,2}:\d{2}$', # YYYY/MM/DD HH:MM
            ]

            import re
            if any(re.match(pattern, input_text) for pattern in patterns):
                self.datetime_entry.config(foreground=self.colors['success'])
            else:
                self.datetime_entry.config(foreground=self.colors['delete'])

        def parse_datetime(self, event=None):
            """解析日期時間輸入並設定為選定時間"""
            input_text = self.datetime_var.get().strip()

            if not input_text:
                self.selected_datetime = None
                return

            try:
                # 嘗試不同的日期時間格式
                formats = [
                    "%m/%d %H:%M",
                    "%m/%d %H:%M:%S",
                    "%Y/%m/%d %H:%M",
                    "%Y/%m/%d %H:%M:%S",
                    "%m-%d %H:%M",
                    "%m-%d %H:%M:%S",
                    "%Y-%m-%d %H:%M",
                    "%Y-%m-%d %H:%M:%S"
                ]

                for fmt in formats:
                    try:
                        parsed_datetime = dt.datetime.strptime(input_text, fmt)

                        # 如果沒有年份，使用當前年份
                        if fmt.startswith("%m/"):
                            parsed_datetime = parsed_datetime.replace(year=dt.datetime.now().year)

                        # 驗證日期時間是否在未來
                        if parsed_datetime <= dt.datetime.now():
                            # 如果是過去的時間，自動加一天
                            if parsed_datetime.time() != dt.datetime.now().time():
                                parsed_datetime = parsed_datetime.replace(day=parsed_datetime.day + 1)

                        self.selected_datetime = parsed_datetime
                        self.datetime_entry.config(foreground=self.colors['success'])
                        return

                    except ValueError:
                        continue

                # 如果所有格式都失敗
                self.selected_datetime = None
                self.datetime_entry.config(foreground=self.colors['delete'])

            except Exception:
                self.selected_datetime = None
                self.datetime_entry.config(foreground=self.colors['delete'])

        def show_notification_manager(self):
            """顯示通知管理對話框"""
            # 創建通知管理窗口
            manager_window = tk.Toplevel(self.root)
            manager_window.title("通知管理")
            manager_window.geometry("600x400")
            manager_window.resizable(True, True)
            manager_window.transient(self.root)
            manager_window.grab_set()

            # 設置 Apple 風格樣式
            manager_frame = ttk.Frame(manager_window, padding="20")
            manager_frame.pack(fill=tk.BOTH, expand=True)

            # 標題
            title_label = ttk.Label(
                manager_frame, text="預定通知管理", style="Header.TLabel"
            )
            title_label.pack(pady=(0, 20))

            # 通知列表框架
            list_frame = ttk.Frame(manager_frame)
            list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

            # 列表框和滾動條
            notification_listbox = tk.Listbox(list_frame, font=("SF Pro Text", 12))
            scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=notification_listbox.yview)
            notification_listbox.configure(yscrollcommand=scrollbar.set)

            notification_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            # 按鈕框架
            button_frame = ttk.Frame(manager_frame)
            button_frame.pack(fill=tk.X)

            # 刷新按鈕
            refresh_button = ttk.Button(
                button_frame, text="🔄 刷新", command=lambda: self.refresh_notification_list(notification_listbox)
            )
            refresh_button.pack(side=tk.LEFT, padx=(0, 10))

            # 取消選中通知按鈕
            cancel_button = ttk.Button(
                button_frame, text="❌ 取消選中", command=lambda: self.cancel_selected_notification(notification_listbox, manager_window)
            )
            cancel_button.pack(side=tk.LEFT, padx=(0, 10))

            # 關閉按鈕
            close_button = ttk.Button(
                button_frame, text="關閉", command=manager_window.destroy
            )
            close_button.pack(side=tk.RIGHT)

            # 初始加載通知列表
            self.refresh_notification_list(notification_listbox)

        def refresh_notification_list(self, listbox):
            """刷新通知列表顯示"""
            # 清空現有列表
            listbox.delete(0, tk.END)

            # 獲取所有預定的通知
            scheduled_notifications = self.notification_scheduler.get_all_scheduled()
            scheduled_tasks = self.todolist.get_scheduled_tasks()

            if not scheduled_notifications and not scheduled_tasks:
                listbox.insert(tk.END, "  沒有預定的通知")
                return

            # 顯示調度器中的通知
            if scheduled_notifications:
                listbox.insert(tk.END, "  活躍通知:")
                for i, notification in enumerate(scheduled_notifications):
                    remaining_time = notification['remaining_seconds']
                    hours = int(remaining_time // 3600)
                    minutes = int((remaining_time % 3600) // 60)
                    time_str = f"{hours:02d}:{minutes:02d}"
                    listbox.insert(tk.END, f"    ⏰ {notification['task_text']} - 剩餘 {time_str}")

            # 顯示帶通知時間的任務
            if scheduled_tasks:
                if scheduled_notifications:
                    listbox.insert(tk.END, "")  # 分隔線
                listbox.insert(tk.END, "  帶通知的任務:")
                for task in scheduled_tasks:
                    time_str = task['notification_time'].strftime("%m/%d %H:%M")
                    listbox.insert(tk.END, f"    📌 {task['text']} - {time_str}")

        def cancel_selected_notification(self, listbox, parent_window):
            """取消選中的通知"""
            selection = listbox.curselection()
            if not selection:
                messagebox.showinfo("提示", "請先選擇要取消的通知", parent=parent_window)
                return

            selected_index = selection[0]
            selected_text = listbox.get(selected_index)

            # 解析選中的項目
            if "📌" in selected_text:
                # 這是一個任務項，需要從 todolist 中移除
                task_text = selected_text.split("📌 ")[1].split(" -")[0].strip()
                # 找到對應的任務並取消通知
                for task in self.todolist.get_scheduled_tasks():
                    if task['text'] == task_text:
                        self.notification_scheduler.cancel_notification(task['id'])
                        # 移除通知時間，轉為普通任務
                        task['notification_time'] = None
                        break
            elif "⏰" in selected_text:
                # 這是一個活躍通知
                task_text = selected_text.split("⏰ ")[1].split(" -")[0].strip()
                # 找到對應的任務並移除
                for task in self.todolist.get_scheduled_tasks():
                    if task['text'] == task_text:
                        self.todolist.remove_task(task['id'])
                        break

            # 刷新列表
            self.refresh_notification_list(listbox)
            messagebox.showinfo("成功", "通知已取消", parent=parent_window)

    # 創建並運行GUI
    root = tk.Tk()
    app = TodoListGUI(root)
    root.mainloop()
