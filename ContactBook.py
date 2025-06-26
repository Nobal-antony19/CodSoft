import tkinter as tk
from tkinter import messagebox

class ContactBookApp:

    def __init__(self, master):
        self.master = master
        master.title("My Contact Book")
        master.geometry("800x600")
        master.configure(bg='#8A2BE2') # Violet background

        self.contacts = []
        self._setup_ui() # Consolidate UI creation
        self._refresh_list()

    def _setup_ui(self):
        # Input fields and labels
        input_frame = tk.Frame(self.master, bg='#FFFFFF', bd=2, relief='groove'); input_frame.pack(pady=10, padx=10, fill='x')
        self.entries = {}; labels = ["Name:", "Phone:", "Email:", "Address:"]
        for i, text in enumerate(labels):
            tk.Label(input_frame, text=text, bg='#FFFFFF', fg='#8A2BE2', font=('Arial', 12, 'bold')).grid(row=i, column=0, sticky='w', padx=5, pady=2)
            entry = tk.Entry(input_frame, width=40, bd=2, relief='solid', font=('Arial', 11)); entry.grid(row=i, column=1, padx=5, pady=2)
            self.entries[text.replace(":", "").lower()] = entry

        # Buttons for actions
        btn_frame = tk.Frame(self.master, bg='#8A2BE2'); btn_frame.pack(pady=5, padx=10, fill='x')
        btn_s = {'bg': '#FFFFFF', 'fg': '#8A2BE2', 'font': ('Arial', 10, 'bold'), 'width': 12, 'bd': 2, 'relief': 'raised'}
        tk.Button(btn_frame, text="Add", command=self._add, **btn_s).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Update", command=self._update, **btn_s).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(btn_frame, text="Delete", command=self._delete, **btn_s).grid(row=0, column=2, padx=5, pady=5)
        tk.Button(btn_frame, text="Clear", command=self._clear_fields, **btn_s).grid(row=0, column=3, padx=5, pady=5)

        # Search bar and button
        srch_frame = tk.Frame(self.master, bg='#8A2BE2'); srch_frame.pack(pady=5, padx=10, fill='x')
        tk.Label(srch_frame, text="Search:", bg='#8A2BE2', fg='#FFFFFF', font=('Arial', 12, 'bold')).pack(side='left', padx=5)
        self.search_entry = tk.Entry(srch_frame, width=30, bd=2, relief='solid', font=('Arial', 11)); self.search_entry.pack(side='left', padx=5)
        tk.Button(srch_frame, text="Search", command=self._search, **btn_s).pack(side='left', padx=5)
        tk.Button(srch_frame, text="View All", command=self._refresh_list, **btn_s).pack(side='left', padx=5)

        # Contact list display
        list_frame = tk.Frame(self.master, bg='#FFFFFF', bd=2, relief='groove'); list_frame.pack(pady=10, padx=10, expand=True, fill='both')
        self.contact_listbox = tk.Listbox(list_frame, height=10, bd=2, relief='solid', font=('Arial', 11), selectbackground='#8A2BE2', selectforeground='#FFFFFF')
        self.contact_listbox.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        self.contact_listbox.bind('<<ListboxSelect>>', self._load_selected)
        scrollbar = tk.Scrollbar(list_frame, command=self.contact_listbox.yview); scrollbar.pack(side='right', fill='y')
        self.contact_listbox.config(yscrollcommand=scrollbar.set)

    def _get_fields_data(self):
        return {k: v.get().strip() for k, v in self.entries.items()}

    def _clear_fields(self):
        for entry in self.entries.values(): entry.delete(0, tk.END)

    def _add(self):
        data = self._get_fields_data()
        if not data['name'] or not data['phone']: messagebox.showwarning("Input Error", "Name and Phone are required!"); return
        self.contacts.append(data); messagebox.showinfo("Success", "Contact added!"); self._clear_fields(); self._refresh_list()

    def _refresh_list(self, display_contacts=None):
        self.contact_listbox.delete(0, tk.END)
        to_display = display_contacts if display_contacts is not None else self.contacts
        if not to_display: self.contact_listbox.insert(tk.END, "No contacts yet!"); return
        for c in to_display: self.contact_listbox.insert(tk.END, f"{c['name']} - {c['phone']}")

    def _load_selected(self, event=None):
        idx = self.contact_listbox.curselection()
        if not idx: return
        displayed_txt = self.contact_listbox.get(idx[0])
        sel_c = next((c for c in self.contacts if f"{c['name']} - {c['phone']}" == displayed_txt), None)
        if sel_c:
            self._clear_fields()
            for k, entry_w in self.entries.items(): entry_w.insert(0, sel_c.get(k, ''))

    def _update(self):
        idx = self.contact_listbox.curselection()
        if not idx: messagebox.showwarning("Error", "Select contact to update."); return
        displayed_txt = self.contact_listbox.get(idx[0])
        orig_c = next((c for c in self.contacts if f"{c['name']} - {c['phone']}" == displayed_txt), None)
        if orig_c:
            new_data = self._get_fields_data()
            if not new_data['name'] or not new_data['phone']: messagebox.showwarning("Error", "Name/Phone required for update!"); return
            orig_c.update(new_data); messagebox.showinfo("Success", "Contact updated!"); self._clear_fields(); self._refresh_list()

    def _delete(self):
        idx = self.contact_listbox.curselection()
        if not idx: messagebox.showwarning("Error", "Select contact to delete."); return
        displayed_txt = self.contact_listbox.get(idx[0])
        del_c = next((c for c in self.contacts if f"{c['name']} - {c['phone']}" == displayed_txt), None)
        if del_c and messagebox.askyesno("Confirm", f"Delete {del_c['name']}?"):
            self.contacts.remove(del_c); messagebox.showinfo("Success", "Contact deleted!"); self._clear_fields(); self._refresh_list()
        elif not del_c: messagebox.showerror("Error", "Could not find contact for deletion.")

    def _search(self):
        q = self.search_entry.get().strip().lower()
        if not q: self._refresh_list(); messagebox.showinfo("Info", "Showing all contacts."); return
        found = [c for c in self.contacts if q in c['name'].lower() or q in c['phone'].lower()]
        self._refresh_list(found)
        if not found: messagebox.showinfo("Result", "No matching contacts.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactBookApp(root)
    root.mainloop()
