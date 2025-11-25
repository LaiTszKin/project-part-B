# Import the necessary modules: datetime for handling dates and times, threading for concurrent operations,
# uuid for generating unique task IDs, queue for thread-safe communication, and calendar for date calculations.
import datetime as dt
import threading
import uuid
import queue
import calendar
class todolist:
    def __init__(self):
        self.tasks = []
        self.selected_index = None

    def add_task(self, task, notification_time=None):
        """
        Add a new task to the list, optionally specifying a time for a notification reminder.

        Args:
            task: The content of the task as a string.
            notification_time: An optional datetime object indicating when to trigger a notification for this task.

        Returns:
            str: A confirmation message indicating the task has been added or scheduled.
        """
        if isinstance(task, str):
            # For backward compatibility with older string-only tasks, convert the input string into a structured dictionary.
            # This dictionary stores the task text, the optional notification time, a unique ID, and the creation timestamp.
            task_dict = {
                'text': task,
                'notification_time': notification_time,
                'id': str(uuid.uuid4()),
                'created_at': dt.datetime.now()
            }
            self.tasks.append(task_dict)
        else:
            # If the input is already a dictionary (representing the newer task format), ensure it has an ID and creation time
            # if they are missing, then add it to the list.
            task['id'] = task.get('id', str(uuid.uuid4()))
            task['created_at'] = task.get('created_at', dt.datetime.now())
            self.tasks.append(task)

        if notification_time:
            return f'Scheduled task "{task}" set for {notification_time.strftime("%Y-%m-%d %H:%M")}.'
        else:
            return f'Task "{task}" added.'

    def remove_task(self, task_or_id):
        """
        Remove a task from the list using its unique ID, its text content, or the task object itself.

        Args:
            task_or_id: Can be the task's unique ID string, the task text string, or the task dictionary.

        Returns:
            str: A message confirming which task was removed, or stating that it wasn't found.
        """
        # Check if the input is a string, which could be either a task ID or the task text.
        if isinstance(task_or_id, str):
            for task in self.tasks:
                if isinstance(task, dict) and task.get('id') == task_or_id:
                    self.tasks.remove(task)
                    return f'Task "{task["text"]}" removed.'
                elif isinstance(task, str) and task == task_or_id:
                    self.tasks.remove(task)
                    return f'Task "{task}" removed.'
        # If the input is a dictionary object, try to find and remove that exact object from the list.
        elif isinstance(task_or_id, dict) and task_or_id in self.tasks:
            self.tasks.remove(task_or_id)
            return f'Task "{task_or_id["text"]}" removed.'

        return 'Task not found.'

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
            # Return a list of task descriptions. For dictionary-based tasks, extract the text;
            # for legacy string tasks, use them directly. This ensures backward compatibility.
            return [task['text'] if isinstance(task, dict) else task for task in self.tasks]

    def get_scheduled_tasks(self):
        """
        Retrieve a list of all tasks that have a scheduled notification time.

        Returns:
            list: A list containing only the task dictionaries that include a 'notification_time'.
        """
        return [task for task in self.tasks
                if isinstance(task, dict) and task.get('notification_time')]

    def get_task_by_id(self, task_id):
        """
        Search for and return a task dictionary based on its unique ID.

        Args:
            task_id: The unique identifier string of the task.

        Returns:
            dict or None: The task dictionary if found, otherwise None.
        """
        for task in self.tasks:
            if isinstance(task, dict) and task.get('id') == task_id:
                return task
        return None


class NotificationScheduler:
    """
    Notification Scheduler - Responsible for managing and triggering scheduled notifications.
    This class is implemented as a Singleton to ensure only one scheduler instance exists globally within the application.
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
            # A dictionary to store active scheduled notifications, mapping task IDs to a tuple of (timer object, task text).
            self.scheduled_notifications = {}
            self.notification_queue = queue.Queue()
            self.fallback_handler = None
            self.running = True
            self.daemon_thread = threading.Thread(target=self._notification_daemon, daemon=True)
            self.daemon_thread.start()
            self.initialized = True

    def set_fallback_handler(self, handler):
        """
        Set a fallback handler function for notifications.
        This is primarily used to handle UI-related callbacks in the main GUI thread, ensuring thread safety when updating the interface.
        """
        self.fallback_handler = handler

    def schedule_notification(self, task_id, notification_time, task_text):
        """
        Schedule a notification for a specific task at a given time.

        Args:
            task_id: The unique identifier of the task.
            notification_time: The datetime object representing when the notification should occur.
            task_text: The text content of the task to be displayed in the notification.

        Returns:
            bool: True if the scheduling was successful.
        """
        if task_id in self.scheduled_notifications:
            # If a notification is already scheduled for this task, cancel the old one before setting the new one.
            self.cancel_notification(task_id)

        # Calculate the time delay until the notification should fire.
        now = dt.datetime.now()
        if notification_time <= now:
            # If the scheduled time is in the past, trigger the notification immediately.
            self._trigger_notification(task_id, task_text)
            return True

        delay = (notification_time - now).total_seconds()

        # Create a background timer thread that will call the trigger function after the calculated delay.
        timer = threading.Timer(delay, self._trigger_notification, args=[task_id, task_text])
        timer.daemon = True
        timer.start()

        # Store the timer and task details in the dictionary for future reference or cancellation.
        self.scheduled_notifications[task_id] = (timer, task_text)
        return True

    def cancel_notification(self, task_id):
        """
        Cancel a currently scheduled notification for a specific task.

        Args:
            task_id: The unique identifier of the task whose notification should be cancelled.

        Returns:
            bool: True if a notification was found and cancelled, False otherwise.
        """
        if task_id in self.scheduled_notifications:
            timer, task_text = self.scheduled_notifications[task_id]
            timer.cancel()
            del self.scheduled_notifications[task_id]
            return True
        return False

    def _trigger_notification(self, task_id, task_text):
        """
        Internal method called when the timer expires to trigger the notification.

        Args:
            task_id: The unique identifier of the task.
            task_text: The text content of the task.
        """
        # Place the notification details into a thread-safe queue.
        # The daemon thread will pick this up and handle the actual display of the notification.
        self.notification_queue.put({
            'task_id': task_id,
            'task_text': task_text,
            'timestamp': dt.datetime.now()
        })

        # Remove the task from the list of active scheduled notifications as it has now been triggered.
        if task_id in self.scheduled_notifications:
            del self.scheduled_notifications[task_id]

    def _notification_daemon(self):
        """
        Background daemon thread function that continuously monitors the queue for pending notifications.
        It is responsible for displaying notifications as they arrive.
        """
        while self.running:
            try:
                # Wait for a new notification item in the queue. Use a 1-second timeout to allow periodic checking of the 'running' flag.
                notification = self.notification_queue.get(timeout=1)
                self._show_notification(notification)
                self.notification_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Notification error: {e}")

    def _show_notification(self, notification):
        """
        Display the notification to the user. On macOS, it attempts to use native system notifications.

        Args:
            notification: A dictionary containing details of the notification to display.
        """
        try:
            # Import necessary modules for running system commands and checking the OS platform.
            import subprocess
            import platform

            if platform.system() == "Darwin":  # macOS
                title = "Reminder"
                message = f"Reminder: {notification['task_text']}"
                sound = "Glass"  # Default Apple system sound

                # AppleScript command to display a native notification.
                script = f'''
                display notification "{message}" with title "{title}" subtitle "Scheduled Reminder" sound name "{sound}"
                '''

                result = subprocess.run(
                    ['osascript', '-e', script],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                # Even if the system notification is sent, also show the in-app GUI notification as a fallback/confirmation.
                self._fallback_notification(notification)
            else:
                # For non-macOS platforms, strictly use the fallback (GUI) notification method.
                self._fallback_notification(notification)

        except Exception as e:
            print(f"Failed to send notification: {e}")
            # If an error occurs (e.g., osascript fails), default to the fallback method.
            self._fallback_notification(notification)

    def _fallback_notification(self, notification):
        """
        Fallback notification method using a Tkinter message box or console output.
        This is used when system notifications are unavailable or fail.

        Args:
            notification: A dictionary containing details of the notification.
        """
        # If an external handler is provided (e.g., to handle UI updates on the main thread), use it first.
        # This helps avoid thread-safety issues with Tkinter.
        if self.fallback_handler:
            try:
                self.fallback_handler(notification)
                return
            except Exception as e:
                print(f"External notification handler failed: {e}")

        # If no handler or it failed, try to use Tkinter directly.
        try:
            import tkinter as tk
            from tkinter import messagebox

            # Attempt to find an existing Tkinter root window.
            for widget in tk._default_root.winfo_children():
                if isinstance(widget, tk.Tk):
                    root = widget
                    break
            else:
                # If no root window exists, create a temporary one for the message box.
                root = tk.Tk()
                root.withdraw()  # Hide the temporary window.
                cleanup_root = True

            messagebox.showinfo(
                "Reminder",
                f"Reminder: {notification['task_text']}",
                parent=root if not cleanup_root else None
            )

            if cleanup_root:
                root.destroy()

        except Exception:
            # Ultimate fallback: print the notification to the console if all else fails.
            print("=== Reminder ===")
            print(f"Message: {notification['task_text']}")
            print(f"Time: {notification['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
            print("=" * 20)

    def get_scheduled_count(self):
        """
        Get the total number of currently scheduled notifications.

        Returns:
            int: The count of active scheduled notifications.
        """
        return len(self.scheduled_notifications)

    def get_all_scheduled(self):
        """
        Retrieve detailed information about all currently scheduled notifications.

        Returns:
            list: A list of dictionaries, each containing the task ID, text, and remaining time in seconds.
        """
        result = []
        for task_id, (timer, task_text) in self.scheduled_notifications.items():
            # Calculate the remaining time until the notification triggers.
            try:
                remaining_time = timer.interval - timer.finished.wait(0)
                remaining_time = max(0, remaining_time)
                result.append({
                    'task_id': task_id,
                    'task_text': task_text,
                    'remaining_seconds': remaining_time
                })
            except:
                # If the timer has finished or an error occurs, skip this item.
                continue
        return result

    def shutdown(self):
        """
        Gracefully shut down the scheduler.
        Stops the daemon thread and cancels all pending notifications.
        """
        self.running = False

        # Cancel all currently scheduled notifications.
        for task_id in list(self.scheduled_notifications.keys()):
            self.cancel_notification(task_id)

        # Wait for the daemon thread to finish execution, with a timeout to prevent hanging.
        if self.daemon_thread.is_alive():
            self.daemon_thread.join(timeout=2)


if __name__ == "__main__":
    import tkinter as tk
    from tkinter import ttk, messagebox

    class ScrollableFrame(ttk.Frame):
        """
        A custom scrollable container that supports complex widgets within rows.
        This component replaces the standard Listbox, allowing for more flexible layouts and richer content.
        """
        def __init__(self, container, *args, **kwargs):
            # Initialize the frame. If a style dictionary is provided, extract the background color
            # to apply it to the underlying canvas, ensuring a consistent look.
            bg_color = '#FFFFFF'
            if 'style' in kwargs and isinstance(kwargs['style'], dict):
                style_config = kwargs.pop('style')
                bg_color = style_config.get('background', '#FFFFFF')
            
            super().__init__(container, *args, **kwargs)
            
            # Create a Canvas to hold the content and a vertical Scrollbar for navigation.
            self.canvas = tk.Canvas(self, highlightthickness=0, bg=bg_color)
            self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
            self.scrollable_frame = ttk.Frame(self.canvas)

            # Configure the scroll region whenever the inner frame size changes (e.g., adding/removing tasks).
            self.scrollable_frame.bind(
                "<Configure>",
                lambda e: self.canvas.configure(
                    scrollregion=self.canvas.bbox("all")
                )
            )

            # Embed the scrollable frame inside the canvas.
            self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

            # Link the canvas scrolling to the scrollbar.
            self.canvas.configure(yscrollcommand=self.scrollbar.set)

            # Layout the canvas and scrollbar using pack geometry manager.
            self.canvas.pack(side="left", fill="both", expand=True)
            self.scrollbar.pack(side="right", fill="y")
            
            # Bind mouse wheel events for intuitive scrolling.
            self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
            
        def _on_mousewheel(self, event):
            # Handle mouse wheel scrolling, but only if the canvas is currently visible on screen.
            if self.canvas.winfo_ismapped():
                self.canvas.yview_scroll(int(-1*(event.delta)), "units")

    class TodoListGUI:
        def __init__(self, root):
            self.root = root
            self.todolist = todolist()
            # Initialize the notification scheduler and set up the thread-safe fallback handler
            self.notification_scheduler = NotificationScheduler()
            self.notification_scheduler.set_fallback_handler(self.handle_fallback_notification)

            # Define a color palette inspired by Apple's Human Interface Guidelines
            self.colors = {
                'bg': '#F2F2F7',          # Light gray system background
                'card': '#FFFFFF',        # Pure white for card-like elements
                'primary': '#007AFF',     # Standard Apple Blue
                'text': '#1D1D1F',        # Dark gray for primary text
                'secondary_text': '#8E8E93', # Lighter gray for secondary text
                'border': '#C6C6C8',      # Gray for borders
                'hover': '#E5E5EA',       # Light gray for hover states
                'selected': '#E5F2FF',    # Very light blue for selection
                'delete': '#FF3B30',      # System Red for destructive actions
                'success': '#34C759'      # System Green for success actions
            }

            # Configure the main application window
            self.root.title("Reminders")
            self.root.geometry("600x640")
            self.root.minsize(550, 480)  # Set minimum window dimensions
            self.root.resizable(True, True)  # Allow the user to resize the window

            # Configure ttk styles to match the Apple aesthetic
            self.style = ttk.Style()
            self.style.theme_use("clam")

            # Configure rounded button elements for softer interface
            # The clam theme supports element options including roundness
            self.style.element_create("RoundedButton.border", "from", "clam")
            
            # Define a custom layout for rounded buttons using the roundness option
            self.style.layout("Rounded.TButton", [
                ("Button.border", {
                    "sticky": "nswe",
                    "border": "1",
                    "children": [
                        ("Button.focus", {
                            "sticky": "nswe",
                            "children": [
                                ("Button.padding", {
                                    "sticky": "nswe",
                                    "children": [
                                        ("Button.label", {"sticky": "nswe"})
                                    ]
                                })
                            ]
                        })
                    ]
                })
            ])

            # Frame Styles
            self.style.configure("TFrame", background=self.colors['bg'])

            # Label Styles - Using SF Pro Text if available
            self.style.configure(
                "TLabel",
                background=self.colors['bg'],
                foreground=self.colors['text'],
                font=("SF Pro Text", 13)  # Fallback to system default if SF Pro is missing
            )

            # Header Label Style
            self.style.configure(
                "Header.TLabel",
                font=("SF Pro Display", 28, "bold"),
                background=self.colors['bg'],
                foreground=self.colors['text']
            )

            # Secondary Text Style
            self.style.configure(
                "Secondary.TLabel",
                font=("SF Pro Text", 11),
                background=self.colors['bg'],
                foreground=self.colors['secondary_text']
            )

            # Card Style for container elements
            self.style.configure(
                "Card.TFrame",
                background=self.colors['card']
            )

            # Primary Button Style - Bold white text on blue background with rounded corners
            self.style.configure(
                "Primary.TButton",
                background=self.colors['primary'],
                foreground="white",
                borderwidth=0,
                focuscolor="none",
                font=("SF Pro Text", 13, "bold"),
                padding=(20, 10),
                relief="flat"
            )
            # Configure element options for rounded appearance
            self.style.configure("Primary.TButton", borderradius=12)
            self.style.map(
                "Primary.TButton",
                background=[("active", "#0051D5"), ("pressed", "#0047B9")],
                relief=[("pressed", "sunken"), ("!pressed", "flat")]
            )

            # Secondary Button Style - Blue text on white/clear background with rounded corners
            self.style.configure(
                "Secondary.TButton",
                background=self.colors['card'],
                foreground=self.colors['primary'], # Mimics iOS secondary action buttons
                borderwidth=0,
                font=("SF Pro Text", 13),
                padding=(16, 8),
                relief="flat"
            )
            # Configure element options for rounded appearance
            self.style.configure("Secondary.TButton", borderradius=10)
            self.style.map(
                "Secondary.TButton",
                background=[("active", self.colors['hover'])],
                foreground=[("active", self.colors['primary'])],
                relief=[("pressed", "sunken"), ("!pressed", "flat")]
            )

            # Success Button Style (Checkmark) with rounded corners
            self.style.configure(
                "Success.TButton",
                background=self.colors['success'],
                foreground="white",
                borderwidth=0,
                font=("SF Pro Text", 13, "bold"),
                padding=(8, 4),
                relief="flat"
            )
            # Configure element options for rounded appearance
            self.style.configure("Success.TButton", borderradius=8)
            self.style.map(
                "Success.TButton",
                background=[("active", "#28a745"), ("pressed", "#218838")],
                relief=[("pressed", "sunken"), ("!pressed", "flat")]
            )

            # Entry Field Style
            self.style.configure(
                "TEntry",
                font=("SF Pro Text", 15),
                padding=(12, 12),
                borderwidth=0
            )
            
            # Combobox Style
            self.style.configure(
                "TCombobox",
                font=("SF Pro Text", 15),
                padding=(12, 12),
                borderwidth=0
            )

            # Create the main container frame with generous padding
            self.main_frame = ttk.Frame(root, padding="24")
            self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            root.columnconfigure(0, weight=1)
            root.rowconfigure(0, weight=1)

            # Set the root window background color
            self.root.configure(bg=self.colors['bg'])

            self.create_widgets()

        def handle_fallback_notification(self, notification):
            """
            Handle fallback notifications by scheduling them to run on the main GUI thread.
            This ensures thread safety when showing message boxes from background threads.
            """
            self.root.after(0, lambda: self._show_safe_messagebox(notification))

        def _show_safe_messagebox(self, notification):
            # Display the message box. This method is designed to be called via root.after from the main thread.
            messagebox.showinfo(
                "Reminder",
                f"Reminder: {notification['task_text']}"
            )

        def create_widgets(self):
            # Header Title
            title_label = ttk.Label(
                self.main_frame, text="My Reminders", style="Header.TLabel"
            )
            title_label.grid(row=0, column=0, columnspan=3, pady=(0, 32), sticky=tk.W)

            # Input Area Container
            input_frame = ttk.Frame(self.main_frame)
            input_frame.grid(
                row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N), pady=(0, 24)
            )
            input_frame.columnconfigure(0, weight=1)

            # Task Entry Field - Styled with rounded corners (via style configuration)
            self.task_entry = ttk.Entry(input_frame, style="TEntry")
            self.task_entry.grid(row=0, column=0, columnspan=2, padx=(0, 12), sticky=(tk.W, tk.E, tk.N))
            self.task_entry.bind("<Return>", lambda e: self.add_task_input())

            # Schedule Button (Alarm Clock Icon)
            self.schedule_button = ttk.Button(
                input_frame, text="⏰", command=self.show_datetime_picker, width=3, style="Secondary.TButton"
            )
            self.schedule_button.grid(row=0, column=2, sticky=(tk.N, tk.E), padx=(0, 8))

            # Add Button
            add_button = ttk.Button(
                input_frame, text="Add", command=self.add_task_input, style="Primary.TButton"
            )
            add_button.grid(row=0, column=3, sticky=(tk.N, tk.E))

            # DateTime Picker Container (Initially hidden)
            self.datetime_frame = ttk.Frame(self.main_frame)
            self.datetime_frame.grid(
                row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 24)
            )
            self.datetime_frame.columnconfigure(1, weight=1)
            self.datetime_frame.grid_remove()  # Start hidden

            # Date Picker Label
            date_label = ttk.Label(self.datetime_frame, text="Reminder Time:", style="Secondary.TLabel")
            date_label.grid(row=0, column=0, padx=(0, 8), sticky=tk.W)

            # Selection Controls - 5 Comboboxes for Year, Month, Day, Hour, Minute
            self.selection_frame = ttk.Frame(self.datetime_frame)
            self.selection_frame.grid(row=0, column=1, padx=(0, 8), sticky=(tk.W, tk.E))
            
            # Initialize Time Variables
            current_dt = dt.datetime.now()
            self.year_var = tk.StringVar(value=str(current_dt.year))
            self.month_var = tk.StringVar(value=f"{current_dt.month:02d}")
            self.day_var = tk.StringVar(value=f"{current_dt.day:02d}")
            self.hour_var = tk.StringVar(value=f"{current_dt.hour:02d}")
            self.minute_var = tk.StringVar(value=f"{current_dt.minute:02d}")
            
            # Year Selector
            self.year_cb = ttk.Combobox(self.selection_frame, textvariable=self.year_var, width=5, state="readonly")
            self.year_cb['values'] = [str(y) for y in range(current_dt.year, current_dt.year + 11)]
            self.year_cb.grid(row=0, column=0)
            self.year_cb.bind("<<ComboboxSelected>>", self.update_days)
            
            ttk.Label(self.selection_frame, text="/", style="Secondary.TLabel").grid(row=0, column=1, padx=2)
            
            # Month Selector
            self.month_cb = ttk.Combobox(self.selection_frame, textvariable=self.month_var, width=3, state="readonly")
            self.month_cb['values'] = [f"{m:02d}" for m in range(1, 13)]
            self.month_cb.grid(row=0, column=2)
            self.month_cb.bind("<<ComboboxSelected>>", self.update_days)
            
            ttk.Label(self.selection_frame, text="/", style="Secondary.TLabel").grid(row=0, column=3, padx=2)

            # Day Selector
            self.day_cb = ttk.Combobox(self.selection_frame, textvariable=self.day_var, width=3, state="readonly")
            self.day_cb.grid(row=0, column=4)
            # Note: Day values are populated dynamically by update_days()
            
            # Spacer
            ttk.Label(self.selection_frame, text="  ", style="Secondary.TLabel").grid(row=0, column=5)
            
            # Hour Selector
            self.hour_cb = ttk.Combobox(self.selection_frame, textvariable=self.hour_var, width=3, state="readonly")
            self.hour_cb['values'] = [f"{h:02d}" for h in range(24)]
            self.hour_cb.grid(row=0, column=6)
            
            # Separator
            ttk.Label(self.selection_frame, text=":", style="Secondary.TLabel").grid(row=0, column=7, padx=2)
            
            # Minute Selector
            self.minute_cb = ttk.Combobox(self.selection_frame, textvariable=self.minute_var, width=3, state="readonly")
            self.minute_cb['values'] = [f"{m:02d}" for m in range(60)]
            self.minute_cb.grid(row=0, column=8)
            
            # Reset Button
            reset_btn = ttk.Button(
                self.selection_frame, 
                text="↺", 
                width=3, 
                command=self.clear_datetime, 
                style="Secondary.TButton"
            )
            reset_btn.grid(row=0, column=9, padx=(12, 0))
            
            # Populate days for the initial selection
            self.update_days()

            # Variable to store the final selected datetime object
            self.selected_datetime = None

            # Task List Container - Styled as a card with white background
            list_frame = ttk.Frame(self.main_frame, style="Card.TFrame", padding=10)
            list_frame.grid(
                row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 24)
            )
            self.main_frame.rowconfigure(3, weight=1)  # Allow the list area to expand vertically
            self.main_frame.columnconfigure(0, weight=1)  # Allow the list area to expand horizontally
            list_frame.columnconfigure(0, weight=1)
            list_frame.rowconfigure(0, weight=1)

            # Custom Scrollable List Component
            self.task_list = ScrollableFrame(list_frame, style={'background': self.colors['card']})
            self.task_list.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            
            # Bottom Action Button Frame
            button_frame = ttk.Frame(self.main_frame)
            button_frame.grid(row=4, column=0, columnspan=3, pady=(0, 16))

            # Clear All Button
            clear_button = ttk.Button(
                button_frame,
                text="Clear All",
                command=self.clear_all_tasks,
                style="Secondary.TButton"
            )
            clear_button.grid(row=0, column=1, padx=(0, 10))


            # Status Bar Label
            self.status_label = ttk.Label(
                self.main_frame, text="0 Reminders", style="Secondary.TLabel"
            )
            self.status_label.grid(
                row=5, column=0, columnspan=3, pady=(12, 0), sticky=tk.W
            )
            
            # Perform initial data load
            self.refresh_task_list()

        def refresh_task_list(self):
            """Refresh the task list view"""
            # Clear existing widgets in scrollable frame
            for widget in self.task_list.scrollable_frame.winfo_children():
                widget.destroy()
                
            # Re-populate
            for task in self.todolist.tasks:
                self.create_task_row(task)
                
            self.update_status()

        def create_task_row(self, task):
            """Render a single task row in the list."""
            # Normalize the task data: if it's a legacy string task, convert it to a dictionary format on the fly.
            if isinstance(task, str):
                task_data = {'text': task, 'id': str(uuid.uuid4()), 'notification_time': None}
            else:
                task_data = task
            
            row_frame = ttk.Frame(self.task_list.scrollable_frame, style="Card.TFrame")
            row_frame.pack(fill="x", expand=True, pady=2)
            
            # Prepare display text
            text = task_data['text']
            notif_time = task_data.get('notification_time')
            
            # Check if the task is overdue
            is_overdue = False
            if notif_time and notif_time < dt.datetime.now():
                is_overdue = True
                
            if notif_time:
                time_str = notif_time.strftime("%m/%d %H:%M")
                text = f"{text} (⏰ {time_str})"
                
            # Use a content frame to manage layout margins
            content_frame = ttk.Frame(row_frame, style="Card.TFrame")
            content_frame.pack(side="left", fill="both", expand=True, padx=5)
            
            # Use a standard tk.Label for specific text coloring (red if overdue)
            task_label = tk.Label(
                content_frame, 
                text=text, 
                bg=self.colors['card'],
                fg=self.colors['delete'] if is_overdue else self.colors['text'],
                font=("SF Pro Text", 15),
                anchor="w",
                justify="left"
            )
            task_label.pack(side="left", fill="x", expand=True)
            
            # Complete Button (Checkmark)
            complete_btn = ttk.Button(
                row_frame,
                text="✓",
                width=3,
                style="Success.TButton",
                command=lambda t=task_data: self.complete_task(t)
            )
            complete_btn.pack(side="right", padx=5)

        def complete_task(self, task):
            """
            Mark a task as completed.
            This removes the task from the list and cancels any associated notifications.
            """
            task_id = task.get('id')
            if task_id:
                # Cancel any scheduled notification for this task
                self.notification_scheduler.cancel_notification(task_id)
                # Remove the task data from the model
                self.todolist.remove_task(task)
                # Refresh the UI to reflect changes
                self.refresh_task_list()

        def add_task_input(self):
            task = self.task_entry.get().strip()
            if task:
                # Check if the date picker is visible and retrieve the scheduled time if so.
                notification_time = None
                if self.datetime_frame.winfo_ismapped():
                    notification_time = self.get_selected_datetime()

                # Add the task to the logic model
                self.todolist.add_task(task, notification_time)

                # If a notification time was set, schedule the notification via the scheduler
                if notification_time:
                    task_dict = self.todolist.tasks[-1]  # Get the newly added task dictionary
                    self.notification_scheduler.schedule_notification(
                        task_dict['id'],
                        notification_time,
                        task
                    )

                # Update the display
                self.refresh_task_list()

                # Reset the input fields and UI state
                self.task_entry.delete(0, tk.END)
                self.clear_datetime()
                self.datetime_frame.grid_remove()
                self.update_status()
                self.task_entry.focus()

        def clear_all_tasks(self):
            if len(self.todolist.tasks) > 0:
                # Ask for user confirmation before clearing everything
                result = messagebox.askyesno("Confirm", "Are you sure you want to clear all reminders?")
                if result:
                    # Cancel all scheduled notifications first
                    for task in self.todolist.tasks:
                        if isinstance(task, dict) and task.get('id'):
                            self.notification_scheduler.cancel_notification(task['id'])

                    # Clear the data model
                    self.todolist.tasks = []
                    # Refresh the UI
                    self.refresh_task_list()

        def update_status(self):
            count = len(self.todolist.tasks)
            self.status_label.config(text=f"{count} Reminders")

        def show_datetime_picker(self):
            """Toggle the visibility of the date/time picker panel."""
            if self.datetime_frame.winfo_ismapped():
                self.datetime_frame.grid_remove()
            else:
                self.datetime_frame.grid()
                self.year_cb.focus()

        def clear_datetime(self):
            """Reset the date/time picker variables to the current time."""
            now = dt.datetime.now()
            self.year_var.set(str(now.year))
            self.month_var.set(f"{now.month:02d}")
            self.day_var.set(f"{now.day:02d}")
            self.hour_var.set(f"{now.hour:02d}")
            self.minute_var.set(f"{now.minute:02d}")
            self.update_days()

        def update_days(self, event=None):
            """Dynamically update the 'Day' dropdown options based on the selected Year and Month."""
            try:
                year = int(self.year_var.get())
                month = int(self.month_var.get())
                
                # Calculate the number of days in the selected month/year
                _, num_days = calendar.monthrange(year, month)
                
                # Update the values in the day combobox
                days = [f"{d:02d}" for d in range(1, num_days + 1)]
                self.day_cb['values'] = days
                
                # If the currently selected day is invalid for the new month (e.g., 31st in Feb), adjust it.
                current_day = self.day_var.get()
                if current_day:
                    if int(current_day) > num_days:
                        self.day_var.set(days[-1])
                else:
                    self.day_var.set("01")
                    
            except ValueError:
                # Ignore errors during initialization or partial input
                pass

        def get_selected_datetime(self):
            """Construct and return a datetime object from the picker's current values."""
            try:
                year = int(self.year_var.get())
                month = int(self.month_var.get())
                day = int(self.day_var.get())
                hour = int(self.hour_var.get())
                minute = int(self.minute_var.get())
                return dt.datetime(year, month, day, hour, minute)
            except ValueError:
                return None


    # Initialize and run the main application
    root = tk.Tk()
    app = TodoListGUI(root)
    root.mainloop()
