import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import sqlite3
import csv  # 新增：用于导出CSV
from datetime import datetime
from business_logic import (
    evaluate_promotion, 
    calculate_allowance, 
    add_employee, 
    add_admin_record, # 新增导入
    get_db_connection
)

class EmployeeSystemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BME Project: Employee Management System v2.1")
        self.root.geometry("1000x650")
        
        # --- 1. 顶部标题 ---
        tk.Label(root, text="Standalone Employee Management System", 
                 font=("Arial", 20, "bold"), pady=15).pack()

        # --- 2. 录入面板 (录入员工) ---
        input_frame = tk.LabelFrame(root, text=" 1. Quick Registration ", padx=15, pady=10)
        input_frame.pack(padx=20, pady=5, fill="x")

        tk.Label(input_frame, text="Name:").grid(row=0, column=0, sticky="w")
        self.ent_name = tk.Entry(input_frame, width=15)
        self.ent_name.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Hire Year:").grid(row=0, column=2, sticky="w", padx=10)
        self.ent_year = tk.Entry(input_frame, width=10)
        self.ent_year.grid(row=0, column=3, padx=5)

        tk.Label(input_frame, text="Grade:").grid(row=0, column=4, sticky="w", padx=10)
        self.ent_grade = ttk.Spinbox(input_frame, from_=1, to=10, width=5)
        self.ent_grade.set(1)
        self.ent_grade.grid(row=0, column=5, padx=5)

        tk.Button(input_frame, text="Register Employee", command=self.save_employee, 
                  bg="#4CAF50", fg="white").grid(row=0, column=6, padx=20)

        # --- 3. 核心显示区：表格 ---
        list_frame = tk.LabelFrame(root, text=" 2. Employee Overview (Double-click for details) ", padx=10, pady=10)
        list_frame.pack(padx=20, pady=10, fill="both", expand=True)

        columns = ("id", "name", "grade", "status", "next_year", "allowance")
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings')

        headers = ["ID", "Full Name", "Grade", "Promo Status", "Est. Promotion", "Annual Allowance"]
        for col, head in zip(columns, headers):
            self.tree.heading(col, text=head)
            self.tree.column(col, anchor="center" if col != "name" else "w")

        self.tree.column("id", width=40)
        self.tree.column("allowance", anchor="e")

        self.tree.bind("<Double-1>", self.on_item_double_click)
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # --- 4. 功能控制区 ---
        ctrl_frame = tk.LabelFrame(root, text=" 3. Actions ", padx=15, pady=10)
        ctrl_frame.pack(padx=20, pady=10, fill="x")

        # 功能按钮一排开
        tk.Button(ctrl_frame, text="🔄 Refresh List", command=self.load_data, width=15).pack(side="left", padx=5)
        
        # 新增按钮：录入奖惩记录
        tk.Button(ctrl_frame, text="➕ Add Record", command=self.open_add_record_window, 
                  bg="#FF9800", fg="white", width=15).pack(side="left", padx=5)
        
        # 新增按钮：导出 CSV
        tk.Button(ctrl_frame, text="📥 Export to CSV", command=self.export_csv, 
                  bg="#2196F3", fg="white", width=15).pack(side="left", padx=5)

        tk.Button(ctrl_frame, text="❌ Exit", command=root.quit, width=10).pack(side="right", padx=5)

        self.load_data()

    # --- 功能 1: 刷新数据 ---
    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, grade FROM employees")
        rows = cursor.fetchall()
        conn.close()

        for eid, name, grade in rows:
            promo_res = evaluate_promotion(eid)
            money = calculate_allowance(eid)
            
            status_text = promo_res['status']
            icon = "✅" if status_text == "ELIGIBLE" else "🚫" if status_text == "FORBIDDEN" else "⏳"

            self.tree.insert("", tk.END, iid=eid, values=(
                eid, name, grade, f"{icon} {status_text}", promo_res['next_year'], f"${money:,.2f}"
            ))

    # --- 功能 2: 导出 CSV ---
    def export_csv(self):
        # 弹出文件保存对话框
        file_path = filedialog.asksaveasfilename(
            defaultextension='.csv',
            filetypes=[("CSV files", "*.csv")],
            title="Export Employee Report"
        )
        
        if not file_path:
            return

        try:
            with open(file_path, mode='w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                # 写入表头
                writer.writerow(["ID", "Name", "Grade", "Status", "Promotion Year", "Allowance"])
                
                # 写入表格中的每一行数据
                for row_id in self.tree.get_children():
                    row_data = self.tree.item(row_id)['values']
                    writer.writerow(row_data)
            
            messagebox.showinfo("Export Success", f"Report saved to:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to save file: {e}")

    # --- 功能 3: 录入奖惩记录窗口 ---
    def open_add_record_window(self):
        # 检查是否选中了员工
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Required", "Please select an employee from the list first.")
            return
        
        emp_id = selected[0]
        emp_name = self.tree.item(emp_id)['values'][1]

        # 创建录入窗口
        rec_win = tk.Toplevel(self.root)
        rec_win.title(f"Add Record for {emp_name}")
        rec_win.geometry("350x400")

        tk.Label(rec_win, text=f"New Record for {emp_name}", font=("Arial", 12, "bold"), pady=10).pack()

        # 类型选择
        tk.Label(rec_win, text="Type:").pack(anchor="w", padx=30)
        type_var = tk.StringVar(value="Commendation")
        type_cb = ttk.Combobox(rec_win, textvariable=type_var, values=["Commendation", "Sanction"], state="readonly")
        type_cb.pack(fill="x", padx=30, pady=5)

        # 描述
        tk.Label(rec_win, text="Description:").pack(anchor="w", padx=30)
        ent_desc = tk.Entry(rec_win)
        ent_desc.pack(fill="x", padx=30, pady=5)

        # 日期 (默认今天)
        tk.Label(rec_win, text="Date (YYYY-MM-DD):").pack(anchor="w", padx=30)
        ent_date = tk.Entry(rec_win)
        ent_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        ent_date.pack(fill="x", padx=30, pady=5)

        # 时长 (仅对处分有效)
        tk.Label(rec_win, text="Duration (Months, for Sanctions):").pack(anchor="w", padx=30)
        ent_dur = tk.Entry(rec_win)
        ent_dur.insert(0, "0")
        ent_dur.pack(fill="x", padx=30, pady=5)

        def submit_record():
            r_type = type_var.get()
            desc = ent_desc.get().strip()
            date = ent_date.get().strip()
            dur = ent_dur.get().strip()

            if not desc or not date:
                messagebox.showerror("Input Error", "Please fill in all fields.")
                return

            try:
                add_admin_record(emp_id, r_type, desc, date, int(dur))
                messagebox.showinfo("Success", "Administrative record added.")
                rec_win.destroy()
                self.load_data() # 关键：刷新主界面，因为奖惩会影响晋升和津贴！
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(rec_win, text="Save Record", command=submit_record, bg="#FF9800", fg="white", pady=10).pack(pady=20)

    # --- 其余原有功能 (双击查看等) ---
    def save_employee(self):
        name, year, grade = self.ent_name.get().strip(), self.ent_year.get().strip(), self.ent_grade.get()
        if not name or not year: return
        add_employee(name, int(year), int(grade))
        self.load_data()
        self.ent_name.delete(0, tk.END); self.ent_year.delete(0, tk.END)

    def on_item_double_click(self, event):
        selected = self.tree.selection()
        if selected: self.show_history_window(selected[0])

    def show_history_window(self, emp_id):
        detail_win = tk.Toplevel(self.root); detail_win.title("Employee History"); detail_win.geometry("450x350")
        conn = get_db_connection(); cursor = conn.cursor()
        cursor.execute("SELECT name FROM employees WHERE id = ?", (emp_id,)); name = cursor.fetchone()[0]
        cursor.execute("SELECT type, description, date_issued, duration_months FROM records WHERE emp_id = ?", (emp_id,))
        history = cursor.fetchall(); conn.close()
        tk.Label(detail_win, text=f"Records for {name}", font=("Arial", 12, "bold")).pack(pady=10)
        for r_type, desc, date, dur in history:
            color = "green" if r_type == "Commendation" else "red"
            tk.Label(detail_win, text=f"[{date}] {r_type}: {desc} ({dur} mo)", fg=color).pack(anchor="w", padx=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeSystemApp(root)
    root.mainloop()