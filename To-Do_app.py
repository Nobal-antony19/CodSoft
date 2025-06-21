import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import uuid

class TodoApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Prodigy To-Do Nexus ✨")
        self.master.geometry("800x600") # Higher resolution window size.
        self.master.resizable(True, True)
        self.master.configure(bg="#121212") # Very dark black background.

        self.tasks = []
        self.style = ttk.Style()
        self._configure_styles()    
        self._create_widgets()
        self._load_tasks() # Placeholder for persistent storage.
        self._update_task_list_display()

    def _configure_styles(self):
        self.style.theme_use('clam')
        self.style.configure("TFrame", background="#121212") # Dark frame background.
        self.style.configure("TLabel", background="#121212", foreground="#DEDEFF", font=("Inter", 12)) # Light purple text.
        self.style.configure("TButton", font=("Inter", 10, "bold"), background="#5D3F6A", foreground="white", borderwidth=0, focusthickness=3, focuscolor='none') # Dark purple buttons.
        self.style.map("TButton", background=[('active', '#4D3259')]) # Even darker purple on hover.
        self.style.configure("TEntry", font=("Inter", 12), fieldbackground="#262626", foreground="#EDEDED") # Dark entry background.
        self.style.configure("Treeview", font=("Inter", 11), rowheight=28, background="#262626", foreground="#EDEDED", fieldbackground="#262626") # Dark Treeview background.
        self.style.configure("Treeview.Heading", font=("Inter", 11, "bold"), background="#704D8C", foreground="#EDEDED") # Medium dark purple headings.
        self.style.map("Treeview", background=[('selected', '#8F6BBF')]) # Brighter purple on selection.

    def _create_widgets(self):
        input_frame = ttk.Frame(self.master, padding="15 15 15 15")
        input_frame.pack(pady=10, padx=10, fill=tk.X)

        self.task_input = ttk.Entry(input_frame, width=40, font=("Inter", 12))
        self.task_input.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="ew")
        self.task_input.bind("<Return>", self._add_task_event)

        add_button = ttk.Button(input_frame, text="Add New Task ➕", command=self._add_task)
        add_button.grid(row=0, column=1, pady=5)
        input_frame.grid_columnconfigure(0, weight=1)

        task_list_frame = ttk.Frame(self.master, padding="10 10 10 10")
        task_list_frame.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)

        self.task_list = ttk.Treeview(task_list_frame, columns=("Status", "Description"), show="headings", selectmode="browse")
        self.task_list.heading("Status", text="Status", anchor=tk.CENTER)
        self.task_list.heading("Description", text="Your Daily Tasks", anchor=tk.W) # Changed to "Tasks".
        self.task_list.column("Status", width=100, anchor=tk.CENTER, stretch=tk.NO)
        self.task_list.column("Description", minwidth=200, anchor=tk.W, stretch=tk.YES)
        self.task_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        task_scrollbar = ttk.Scrollbar(task_list_frame, orient="vertical", command=self.task_list.yview)
        task_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.task_list.config(yscrollcommand=task_scrollbar.set)

        button_frame = ttk.Frame(self.master, padding="15 15 15 15")
        button_frame.pack(pady=10, padx=10, fill=tk.X)

        edit_button = ttk.Button(button_frame, text="Refine Task ✏️", command=self._edit_task)
        edit_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        complete_button = ttk.Button(button_frame, text="Mark as Conquered ✅", command=self._mark_task_complete)
        complete_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        delete_button = ttk.Button(button_frame, text="Remove Task 🗑️", command=self._delete_task)
        delete_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        button_frame.grid_columnconfigure(2, weight=1)

        self.status_label = ttk.Label(self.master, text="Ready to conquer your day! 🚀", anchor="w", font=("Inter", 10, "italic"), foreground="#BB8FCE") # Brighter purple status text.
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=(0, 10))

    def _add_task_event(self, event=None):
        self._add_task()

    def _add_task(self):
        task_description = self.task_input.get().strip()
        if task_description:
            task = {"id": str(uuid.uuid4()), "description": task_description, "completed": False}
            self.tasks.append(task)
            self.task_input.delete(0, tk.END)
            self._update_task_list_display()
            self._set_status(f"'{task_description}' added to your list! Let's do this. 💪")
        else:
            messagebox.showwarning("Input Error", "Looks like you forgot to type your task! Please enter a description. 🤔")

    def _get_selected_task_id(self):
        selected_item = self.task_list.focus()
        if selected_item:
            return self.task_list.item(selected_item, "tags")[0]
        return None

    def _get_task_by_id(self, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                return task
        return None

    def _update_task_list_display(self):
        for item in self.task_list.get_children():
            self.task_list.delete(item)

        for task in self.tasks:
            status_text = "✅ CONQUERED!" if task["completed"] else "⏳ ONGOING..."
            tag = task["id"]
            self.task_list.insert("", tk.END, tags=(tag,), values=(status_text, task["description"]))

    def _mark_task_complete(self):
        task_id = self._get_selected_task_id()
        if task_id:
            task = self._get_task_by_id(task_id)
            if task:
                task["completed"] = not task["completed"]
                self._update_task_list_display()
                status_msg = "Marked as CONQUERED! 🎉 Time for your next victory! ✨" if task["completed"] else "Marked as ONGOING again. You got this! 💪"
                self._set_status(f"'{task['description']}' {status_msg}")
        else:
            messagebox.showwarning("Selection Error", "Please select a task to mark. No magic without a choice! ☝️")

    def _edit_task(self):
        task_id = self._get_selected_task_id()
        if task_id:
            task = self._get_task_by_id(task_id)
            if task:
                new_description = simpledialog.askstring("Refine Your Task", "What's the new plan for this task?", initialvalue=task["description"])
                if new_description is not None and new_description.strip():
                    task["description"] = new_description.strip()
                    self._update_task_list_display()
                    self._set_status(f"Task updated to: '{new_description}'! Fresh start! ✨")
                elif new_description is not None:
                    messagebox.showwarning("Input Error", "A task needs a description! Please try again. 🚫")
            else:
                self._set_status("Error: Hmm, couldn't find that task. Maybe it's hiding? 🐛")
        else:
            messagebox.showwarning("Selection Error", "Please choose a task to refine. Can't edit what's not chosen! ☝️")

    def _delete_task(self):
        task_id = self._get_selected_task_id()
        if task_id:
            task_to_delete = self._get_task_by_id(task_id)
            if task_to_delete:
                if messagebox.askyesno("Confirm Deletion", f"Are you sure you want to remove '{task_to_delete['description']}'? This cannot be undone. 😬"):
                    self.tasks = [task for task in self.tasks if task["id"] != task_id]
                    self._update_task_list_display()
                    self._set_status(f"'{task_to_delete['description']}' has been removed. One less thing to worry about! 👍")
            else:
                self._set_status("Error: Hmm, couldn't find that task. Perhaps it vanished? 🐛")
        else:
            messagebox.showwarning("Selection Error", "Please select a task to remove. Can't delete air! ☝️")

    def _set_status(self, message):
        self.status_label.config(text=message)

    def _load_tasks(self):
        pass

    def _save_tasks(self):
        pass

def run_app():
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()

if __name__ == "__main__":
    run_app()
