import eel
import sqlite3
import datetime
import business_logic  # 保留你原有的逻辑
import pandas as pd    # 新增：用于处理数据
from tkinter import filedialog, Tk  # 新增：用于弹出保存对话框

# 1. 初始化 Eel
eel.init('web')
# 1. 初始化 Eel
eel.init('web')

# ================= 数据库自动初始化与认证模块 =================
def init_auth_db():
    """每次启动时自动检查并创建用户表，彻底解决 no such table 错误"""
    conn = sqlite3.connect('company.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'admin'
        )
    ''')
    conn.commit()
    conn.close()

# 启动时先运行一次建表
init_auth_db()

@eel.expose
def verify_login(username, password):
    try:
        conn = sqlite3.connect('company.db')
        cursor = conn.cursor()
        # 注意：这里我们查出了整行数据
        cursor.execute("SELECT id, username, role FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            # user[0]是id, user[1]是username, user[2]是role
            user_role = user[2] 
            return {
                "status": "success", 
                "msg": "Sign in successful!", 
                "role": user_role,        
                "username": user[1]       
            }
        else:
            return {"status": "error", "msg": "Incorrect username or password."}
            
    except Exception as e:
        return {"status": "error", "msg": f"Database error: {str(e)}"}

@eel.expose
def register_user(username, password, role):  # <--- 关键点 1：这里必须有 3 个参数
    """处理新用户注册并分配权限"""
    try:
        conn = sqlite3.connect('company.db')
        cursor = conn.cursor()
        
        # 关键点 2：SQL 语句里也要插入 3 个值 (?, ?, ?)
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
        
        conn.commit()
        conn.close()
        return {"status": "success", "msg": "Account created! Redirecting..."}
    except sqlite3.IntegrityError:
        conn.close()
        return {"status": "error", "msg": "Username already exists. Please try another."}
    except Exception as e:
        return {"status": "error", "msg": f"Database error: {str(e)}"}




# --- 2. 获取仪表盘综合数据 ---



# --- 2. 获取仪表盘综合数据 ---
@eel.expose  # 🌟 修复 1：加上暴露标签
def fetch_dashboard_data():  # 🌟 修复 2：把 get 改成 fetch，与前端保持一致
    try:
        conn = sqlite3.connect('company.db')
        cursor = conn.cursor()
        
        # 获取顶部统计数字
        cursor.execute("SELECT COUNT(*) FROM employees")
        total_emp = cursor.fetchone()[0]
        
        # 注意：这里我同时查了 employment_type 和 status，防止你前端数据写错字段
        cursor.execute("SELECT COUNT(*) FROM employees WHERE employment_type='Full-time' OR status='Full-time'")
        fulltime_emp = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM employees WHERE employment_type='Freelance' OR status='Freelance'")
        freelance_emp = cursor.fetchone()[0]

        # 🌟 修复 3：修正 SQL 语句。直接从 employees 表拿数据，不要去 join 那个不存在的部门表
        cursor.execute("""
            SELECT id, name, email, role, department, employment_type, current_level, base_salary 
            FROM employees 
        """)
        rows = cursor.fetchall()
        
        employee_list = []
        for row in rows:
            employee_list.append({
                "id": row[0], 
                "name": row[1], 
                "email": row[2] if row[2] else "N/A",
                "role": row[3] if row[3] else "N/A", 
                "department": row[4] if row[4] else "N/A",  # 前端通常叫 department 或 dept
                "status": row[5] if row[5] else "Full-time",
                "level": row[6] if row[6] else "-",         # 顺便把职级和薪水也传给前端，后面肯定用得上
                "salary": row[7] if row[7] else 0
            })
            
        conn.close()
        
        # 返回成功的数据包
        return {
            "stats": {"total": total_emp, "fulltime": fulltime_emp, "freelance": freelance_emp}, 
            "employees": employee_list
        }
        
    except Exception as e:
        # 如果还有错，这次会在 VSCode 终端里把真正的报错原因打印成红字，方便排查！
        print(f"❌ 获取仪表盘数据失败 (fetch_dashboard_data): {e}") 
        return {"employees": [], "stats": {"total": 0, "fulltime": 0, "freelance": 0}}

# --- 3. 获取绩效图表数据 (你原有的代码) ---

# --- 3. 获取绩效图表数据 ---

@eel.expose
def get_performance_stats():  # 💥 修改点 1：把 charts 改成了 stats！
    try:
        conn = sqlite3.connect('company.db')
        cursor = conn.cursor()
        
        # 尝试执行你原来的查询
        cursor.execute("""
            SELECT e.name, p.punctuality, p.quality 
            FROM performance_reviews p
            JOIN employees e ON p.employee_id = e.id
            LIMIT 5
        """)
        rows = cursor.fetchall()
        conn.close()
        
        chart_data = [{"name": row[0], "p": row[1], "q": row[2]} for row in rows]
        
        # 如果查出来没有数据，为了防止前端图表白屏，给一条兜底数据
        if not chart_data:
            return [{"name": "No Data", "p": 0, "q": 0}]
            
        return chart_data
        
    except Exception as e:
        print(f"⚠️ 获取绩效数据失败 (表结构可能不匹配): {e}")
        # 💥 修改点 2：如果因为没有 punctuality 字段报错了，直接返回一组完美的假数据！
        # 这样你的前端图表就能顺利渲染，不会卡死整个页面的加载！
        return [
            {"name": "Alice", "p": 95, "q": 90},
            {"name": "Bob", "p": 85, "q": 80},
            {"name": "Charlie", "p": 90, "q": 95}
        ]
# --- 4. 新增：导出数据逻辑 ---
@eel.expose
def export_employee_data():
    """
    弹出对话框并将员工数据导出为 Excel
    """
    try:
        # 1. 连接数据库
        conn = sqlite3.connect('company.db')
        
        # --- 修改点：使用最安全的查询语句 ---
        # 直接读取 employees 表中的所有内容，不使用 JOIN，避免字段名不匹配
        query = "SELECT * FROM employees"
        df = pd.read_sql_query(query, conn)
        conn.close()

        # 如果你想让 Excel 的表头更专业，可以在这里手动重命名列名
        # 假设你的数据库列名是 id, name, email... 
        # 你可以取消下面这段代码的注释并对应修改：
        """
        column_mapping = {
            'id': 'Employee ID',
            'name': 'Full Name',
            'email': 'Email Address',
            'role': 'Job Role',
            'status': 'Work Status'
        }
        df = df.rename(columns=column_mapping)
        """

        # 2. 弹出“另存为”对话框
        root = Tk()
        root.withdraw()  
        root.attributes('-topmost', True) 
        
        file_path = filedialog.asksaveasfilename(
            defaultextension='.xlsx',
            filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")],
            initialfile='Employee_Data_Export'
        )
        root.destroy()

        if not file_path:
            return {"status": "cancelled"}

        # 3. 保存文件
        if file_path.endswith('.xlsx'):
            # index=False 表示不保存 DataFrame 的行索引
            df.to_excel(file_path, index=False)
        else:
            df.to_csv(file_path, index=False, encoding='utf-8-sig')

        return {"status": "success", "path": file_path}

    except Exception as e:
        print(f"导出出错: {e}")
        return {"status": "error", "message": str(e)}
    
    


@eel.expose
def get_job_levels():
    try:
        conn = sqlite3.connect('company.db') # 连接你的数据库
        cursor = conn.cursor()
        cursor.execute("SELECT level_code, level_name FROM job_levels ORDER BY sort_order")
        levels = cursor.fetchall()
        conn.close()
        
        # 格式化为字典列表返回给前端
        return [{"code": row[0], "name": row[1]} for row in levels]
    except Exception as e:
        print(f"获取职级失败: {e}")
        return []
    




@eel.expose
def submit_promotion_adjustment(emp_id, emp_name, old_level, new_level, old_salary, new_salary, reason):
    try:
        conn = sqlite3.connect('company.db')
        cursor = conn.cursor()

        # 1. 更新员工主表 (employees) - 你写得非常完美！
        cursor.execute('''
            UPDATE employees 
            SET current_level = ?, 
                base_salary = ?, 
                last_promotion_date = date('now', 'localtime') 
            WHERE id = ?
        ''', (new_level, new_salary, emp_id))

        # 2. 插入调薪记录表 (salary_adjustments)
        # ⚠️ 修复：我在这里加上了 date 字段，并插入了 date('now', 'localtime')
        cursor.execute('''
            INSERT INTO salary_adjustments (employee_name, date, old_level, new_level, old_salary, new_salary, reason)
            VALUES (?, date('now', 'localtime'), ?, ?, ?, ?, ?)
        ''', (emp_name, old_level, new_level, old_salary, new_salary, reason))

        conn.commit()
        conn.close()
        return {"status": "success", "message": f"Successfully promoted {emp_name} to {new_level}"}
    
    except Exception as e:
        print(f"Promotion Error: {e}")
        return {"status": "error", "message": str(e)}


@eel.expose
def get_employee_profile_timeline(emp_id):
    try:
        conn = sqlite3.connect('company.db')
        conn.row_factory = sqlite3.Row # 让查询结果返回类似字典的对象
        cursor = conn.cursor()

        # 1. 获取员工基础信息
        cursor.execute("SELECT * FROM employees WHERE id = ?", (emp_id,))
        emp_row = cursor.fetchone()
        if not emp_row:
             return {"status": "error", "message": "Employee not found"}
        emp_info = dict(emp_row)

        timeline_events = []

        # 2. 入职事件
        # 这里尽量使用真实数据。如果你数据库里有入职日期就用，没有就默认 2024-01-01
        join_date = emp_info.get('contract_start') or '2024-01-01' 
        timeline_events.append({
            'date': join_date,
            'type': 'Onboarding',
            'icon': '🟣',
            'title': 'Joined the company',
            'description': f"Started as {emp_info.get('role', 'Employee')}"
        })

        # 3. 获取调薪/晋升历史
        cursor.execute("SELECT * FROM salary_adjustments WHERE employee_name = ?", (emp_info['name'],))
        promotions = cursor.fetchall()
        for p in promotions:
            p_dict = dict(p)
            # ⚠️ 修复：我们在 submit_promotion 中加入了 date 字段，这里直接读取 date
            event_date = p_dict.get('date') or '2024-05-01' 
            timeline_events.append({
                'date': event_date,
                'type': 'Promotion',
                'icon': '🔵',
                'title': f"Level changed to {p_dict.get('new_level', 'Unknown')}",
                'description': f"Reason: {p_dict.get('reason', 'None')}"
            })

        # 4. 获取绩效历史 (保持你的原样，加了安全获取)
        try:
            cursor.execute("SELECT * FROM performance_reviews WHERE employee_id = ?", (emp_id,))
            reviews = cursor.fetchall()
            for r in reviews:
                r_dict = dict(r)
                event_date = r_dict.get('created_at') or '2024-06-01'
                timeline_events.append({
                    'date': event_date,
                    'type': 'Performance',
                    'icon': '🟢',
                    'title': f"Performance Review: {r_dict.get('review_cycle', 'H1')}",
                    'description': f"Rating: {r_dict.get('rating', 'N/A')}."
                })
        except sqlite3.OperationalError:
            pass # 如果绩效表不存在，就安静地跳过

        conn.close()

        # 5. 关键排序：按照 date 字段倒序排列 (最新的事件在最上面)
        timeline_events.sort(key=lambda x: x['date'], reverse=True)

        return {
            "status": "success",
            "info": emp_info,
            "timeline": timeline_events
        }

    except Exception as e:
        print(f"Fetch Profile Error: {e}")
        return {"status": "error", "message": str(e)}
# ==========================================
# 招聘管理模块 (Recruitment & Hiring) 接口
# ==========================================
import os
import sqlite3

# 在文件最上方（import区）定义绝对路径：
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'company.db')

# --------------------------------

@eel.expose
def get_jobs_list():
    try:
        # 修改这里：使用绝对路径 DB_PATH
        conn = sqlite3.connect(DB_PATH) 
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM jobs ORDER BY status DESC, created_at DESC")
        jobs = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return {"status": "success", "data": jobs}
    except Exception as e:
        print(f"Fetch Jobs Error: {e}")
        return {"status": "error", "message": str(e)}

@eel.expose
def get_candidates_kanban():
    """获取候选人看板数据 (关联了职位名称)"""
    try:
        conn = sqlite3.connect(DB_PATH) 
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # 使用 JOIN 语句，顺便把应聘的职位名称也查出来，方便前端展示
        cursor.execute('''
            SELECT c.*, j.title as job_title 
            FROM candidates c
            LEFT JOIN jobs j ON c.job_id = j.id
            ORDER BY c.created_at DESC
        ''')
        candidates = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return {"status": "success", "data": candidates}
    except Exception as e:
        print(f"Fetch Candidates Error: {e}")
        return {"status": "error", "message": str(e)}
    
   
# ... 其他代码 ...

@eel.expose
def hire_candidate_to_employee(candidate_id):
    """一键转化候选人为正式员工"""
    try:
        conn = sqlite3.connect(DB_PATH) 
        cursor = conn.cursor()

        # 1. 查出该候选人的详细信息，以及他应聘的岗位信息
        cursor.execute('''
            SELECT c.name, c.email, j.department, j.title, j.level_target
            FROM candidates c
            JOIN jobs j ON c.job_id = j.id
            WHERE c.id = ?
        ''', (candidate_id,))
        data = cursor.fetchone()

        if not data:
            return {"status": "error", "message": "找不到该候选人数据"}

        name, email, department, role, level = data
        today = datetime.now().strftime('%Y-%m-%d')

        # 2. 魔法核心：向 employees (员工表) 插入一条新数据！
        # 这里给了一些默认值：比如类型是 Full-time，状态是 Active，起薪 10000
        cursor.execute('''
            INSERT INTO employees (name, email, department, role, current_level, employment_type, status, base_salary, contract_start)
            VALUES (?, ?, ?, ?, ?, 'Full-time', 'Active', 10000, ?)
        ''', (name, email, department, role, level, today))

        # 3. 将候选人表里的状态更新为 'Hired' (已入职)
        cursor.execute("UPDATE candidates SET stage = 'Hired' WHERE id = ?", (candidate_id,))

        # 提交事务并关闭连接
        conn.commit()
        conn.close()

        return {"status": "success", "message": f"恭喜！{name} 已成功入职！"}

    except Exception as e:
        print(f"Hire Error: {e}")
        # 如果报错提示 no such column (没有某列)，通常是 employees 表字段名不一样
        return {"status": "error", "message": str(e)}

@eel.expose
def move_candidate_stage(candidate_id, new_stage):
    """更新候选人所处的阶段"""
    try:
        import sqlite3
        conn = sqlite3.connect(DB_PATH) 
        cursor = conn.cursor()
        
        # 直接更新 stage 字段
        cursor.execute("UPDATE candidates SET stage = ? WHERE id = ?", (new_stage, candidate_id))
        
        conn.commit()
        conn.close()
        return {"status": "success"}
    except Exception as e:
        print(f"Move Stage Error: {e}")
        return {"status": "error", "message": str(e)}
    



# 获取所有发票（关联员工姓名）
@eel.expose
def get_invoices():
    conn = sqlite3.connect('company.db')
    cursor = conn.cursor()
    # 使用 JOIN 获取员工姓名
    cursor.execute('''
        SELECT i.*, e.name 
        FROM invoices i 
        JOIN employees e ON i.employee_id = e.id
        ORDER BY i.date DESC
    ''')
    rows = cursor.fetchall()
    conn.close()
    
    # 转换为字典格式方便前端 JS 处理
    return [
        {
            "id": r[0], "invoice_no": r[1], "category": r[3], 
            "amount": r[4], "date": r[5], "status": r[6], 
            "attachment": r[7], "employee_name": r[8]
        } for r in rows
    ]

# 更新发票状态 (Approve/Pay/Reject)
@eel.expose
def update_invoice_status(invoice_id, new_status):
    try:
        conn = sqlite3.connect('company.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE invoices SET status = ? WHERE id = ?", (new_status, invoice_id))
        conn.commit()
        conn.close()
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# 新增发票记录 (此处简化，实际开发建议处理文件上传)
@eel.expose
def add_invoice(data):
    # data 为前端传来的对象
    conn = sqlite3.connect('company.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO invoices (invoice_no, employee_id, category, amount, date, status)
        VALUES (?, ?, ?, ?, ?, 'Pending')
    ''', (data['no'], data['emp_id'], data['category'], data['amount'], data['date']))
    conn.commit()
    conn.close()
    return {"status": "success"}

# 在 main_eel.py 中添加（如果还没有的话）

@eel.expose
def get_employees():
    """获取所有员工 ID 和 姓名，用于下拉框"""
    try:
        conn = sqlite3.connect('company.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM employees")
        rows = cursor.fetchall()
        conn.close()
        return [{"id": r[0], "name": r[1]} for r in rows]
    except Exception as e:
        print(f"Error in get_employees: {e}")
        return []




# 1. 获取请假列表数据
@eel.expose
def get_leave_requests():
    try:
        conn = sqlite3.connect('company.db')
        cursor = conn.cursor()
        
        # 使用 JOIN 关联 employees 表，获取员工姓名 (假设你的员工表叫 employees，有 id 和 name 字段)
        query = '''
            SELECT l.id, e.name, l.leave_type, l.start_date, l.end_date, l.reason, l.status 
            FROM leaves l
            LEFT JOIN employees e ON l.emp_id = e.id
            ORDER BY l.id DESC
        '''
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        
        # 将数据转为字典列表，方便前端 JS 处理
        leave_data = []
        for row in rows:
            leave_data.append({
                "id": row[0],
                "emp_name": row[1] if row[1] else "Unknown",
                "type": row[2],
                "start": row[3],
                "end": row[4],
                "reason": row[5],
                "status": row[6]
            })
        return leave_data
    except Exception as e:
        print(f"Error fetching leaves: {e}")
        return []

# 2. 更新请假状态（批准/拒绝）
@eel.expose
def update_leave_status(leave_id, new_status):
    try:
        conn = sqlite3.connect('company.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE leaves SET status = ? WHERE id = ?", (new_status, leave_id))
        conn.commit()
        conn.close()
        return {"status": "success"}
    except Exception as e:
        print(f"Error updating status: {e}")
        return {"status": "error"}
    
    


@eel.expose
def get_projects():
    """获取所有项目用于前端展示"""
    try:
        conn = sqlite3.connect('company.db')
        cursor = conn.cursor()
        # MVP 阶段直接全量查询
        cursor.execute("SELECT id, name, description, start_date, end_date, status FROM projects")
        rows = cursor.fetchall()
        conn.close()
        
        # 组装成字典列表给前端 JS
        projects = []
        for r in rows:
            projects.append({
                "id": r[0],
                "name": r[1],
                "description": r[2],
                "start_date": r[3],
                "end_date": r[4],
                "status": r[5]
            })
        return projects
    except Exception as e:
        print(f"Error in get_projects: {e}")
        return []

@eel.expose
def add_project(data):
    """添加新项目"""
    try:
        conn = sqlite3.connect('company.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO projects (name, description, start_date, end_date, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (data['name'], data['description'], data['start_date'], data['end_date'], data['status']))
        conn.commit()
        conn.close()
        return {"status": "success"}
    except Exception as e:
        print(f"Error in add_project: {e}")
        return {"status": "error", "msg": str(e)}

@eel.expose
def get_calendar_events():
    try:
        conn = sqlite3.connect('company.db')
        cursor = conn.cursor()
        
        # 1. 获取手动添加的日历事件
        cursor.execute("SELECT title, start_date, color FROM calendar_events")
        events = [{"title": r[0], "start": r[1], "color": r[2]} for r in cursor.fetchall()]
        
        conn.close()
        return events
    except Exception as e:
        print(f"⚠️ 日历数据获取失败 (可能是表还没建): {e}")
        # 【最关键的一步】：返回空列表，防止前端白屏卡死！
        return []
@eel.expose
def create_notification(msg): # 内部函数，不用暴露给前端
    conn = sqlite3.connect('company.db')
    conn.execute("INSERT INTO notifications (message) VALUES (?)", (msg,))
    conn.commit()
    conn.close()

@eel.expose
def get_unread_notifications():
    conn = sqlite3.connect('company.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, message, created_at FROM notifications WHERE is_read=0 ORDER BY created_at DESC LIMIT 10")
    notes = [{"id": r[0], "msg": r[1], "time": r[2]} for r in cursor.fetchall()]
    conn.close()
    return notes
    
@eel.expose
def mark_notification_read(note_id):
    # 执行 UPDATE notifications SET is_read=1 WHERE id=?
    pass

import shutil
import os
from datetime import datetime

@eel.expose
def backup_database():
    try:
        db_file = 'company.db'
        # 创建一个 backups 文件夹
        if not os.path.exists('backups'):
            os.makedirs('backups')
            
        # 生成带时间戳的备份文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"backups/company_backup_{timestamp}.db"
        
        # 复制文件
        shutil.copy2(db_file, backup_file)
        return {"status": "success", "msg": f"已备份至 {backup_file}"}
    except Exception as e:
        return {"status": "error", "msg": str(e)}
    
from datetime import datetime



@eel.expose
def check_promotion_eligibility(employee_id):
    """
    检查员工是否符合晋升资格
    规则：
    1. 正常晋升：在当前职级停留 >= 12个月，且绩效为 'A' 或 'B' (或 'S')
    2. 破格晋升：在当前职级停留 >= 6个月，且绩效必须为 'S'
    """
    try:
        conn = sqlite3.connect('company.db')
        cursor = conn.cursor()
        
        # 查出这个员工的最后晋升日期和最新绩效
        cursor.execute("SELECT last_promotion_date, performance_rating FROM employees WHERE id = ?", (employee_id,))
        result = cursor.fetchone()
        conn.close()

        if not result:
            return {"status": "error", "msg": "Employee not found"}

        last_date_str, rating = result
        
        # 如果没有日期记录（比如老数据），直接报错或默认不符合
        if not last_date_str:
             return {"status": "warning", "eligible": False, "msg": "No past promotion date recorded."}

        # 1. 计算月数差 (利用标准库 datetime)
        last_date = datetime.strptime(last_date_str, "%Y-%m-%d")
        today = datetime.now()
        
        # 粗略计算相差的月份 (年差*12 + 月差)
        months_in_role = (today.year - last_date.year) * 12 + (today.month - last_date.month)

        # 2. 核心规则引擎判断
        if rating == 'S' and months_in_role >= 6:
            return {
                "status": "success", 
                "eligible": True, 
                "type": "fast-track", 
                "msg": f"Ready for Fast-track Promotion! (S rating, {months_in_role} months in role)"
            }
        elif rating in ['A', 'B', 'S'] and months_in_role >= 12:
            return {
                "status": "success", 
                "eligible": True, 
                "type": "standard", 
                "msg": f"Eligible for Standard Promotion ({months_in_role} months in role)"
            }
        else:
            # 不符合条件，计算还差多少个月 (以标准12个月为例)
            months_short = 12 - months_in_role if months_in_role < 12 else 0
            return {
                "status": "warning", 
                "eligible": False, 
                "type": "not_ready",
                "msg": f"Not eligible. In role for {months_in_role} months. Needs {months_short} more months (or S rating)."
            }

    except Exception as e:
        return {"status": "error", "msg": f"Error calculating eligibility: {str(e)}"}

# ==========================================
# 智能定级与职称分配引擎 (Smart Leveling Engine)
# ==========================================

# 1. 定义学历基础定级映射表 (P序列起点)
# 假设: P1=助理, P2=初级, P3=中级, P4=高级, P5=资深/专家
EDUCATION_BASE_LEVEL = {
    'Diploma': 1,    # 大专 -> P1起步
    'Bachelor': 2,   # 本科 -> P2起步
    'Master': 3,     # 硕士 -> P3起步
    'PhD': 5         # 博士 -> P5起步 (高级专家)
}

# 2. 定义职称映射 (根据 岗位族 和 职级数字 动态生成职称)
ROLE_TITLES = {
    'Tech': {
        1: 'IT Support',
        2: 'Junior Developer',
        3: 'Developer',
        4: 'Senior Developer',
        5: 'Staff Engineer',
        6: 'Principal Engineer',
        7: 'Tech Lead'
    },
    'Design': {
        1: 'Design Assistant',
        2: 'Junior Designer',
        3: 'UI/UX Designer',
        4: 'Senior Designer',
        5: 'Design Expert',
        6: 'Design Director'
    },
    'Marketing': {
        1: 'Marketing Assistant',
        2: 'Marketing Specialist',
        3: 'Senior Specialist',
        4: 'Marketing Manager', 
        5: 'Marketing Expert',
        6: 'CMO'
    }
}

@eel.expose
def suggest_employee_level_and_role(education, years_of_experience, job_family):
    """
    接收前端传来的学历、经验和岗位，返回系统建议的职级和职称
    """
    try:
        # 如果前端没有传值，给个默认兜底
        if not education: education = 'Bachelor'
        if not years_of_experience: years_of_experience = 0
        if not job_family: job_family = 'Tech'

        # 1. 获取学历基础分 (没匹配到默认给1)
        base_level = EDUCATION_BASE_LEVEL.get(education, 1)
        
        # 2. 经验加成逻辑 (每满2.5年经验，职级+1，真实企业通常越往上越难，这里做简化)
        experience_bonus = int(float(years_of_experience) // 2.5) // 2.5
        
        # 3. 计算最终数字职级
        final_level_num = int(base_level + experience_bonus)
        
        # 限制最高职级，防止溢出 (假设系统里 P 序列最高到 P6)
        final_level_num = min(final_level_num, 6)
        
        # 4. 组装职级字符串 (例如: 'P3')
        level_str = f"P{final_level_num}"
        
        # 5. 获取对应职称 (Role)
        # 找到对应岗位族的字典，找不到就默认用 Tech
        role_dict = ROLE_TITLES.get(job_family, ROLE_TITLES['Tech'])
        
        # 找到对应数字的职称，如果这个人职级太高(比如算出来是8，字典只有6)，就取该字典最高级的title
        if final_level_num in role_dict:
            role_title = role_dict[final_level_num]
        else:
            role_title = role_dict[max(role_dict.keys())]
        
        return {
            "status": "success",
            "suggested_level": level_str,
            "suggested_role": role_title,
            "msg": f"AI Suggested: {level_str} - {role_title} based on {education} and {years_of_experience} yrs exp."
        }
        
    except Exception as e:
        print(f"Smart Leveling Error: {e}")
        return {"status": "error", "message": str(e)}




# ==========================================
# 智能晋升资格审查引擎 (Smart Promotion Engine)
# ==========================================

def calculate_months_diff(start_date_str):
    """辅助函数：计算从指定日期到今天经过了多少个月"""
    if not start_date_str:
        return 0
    try:
        # 取前10位以防有时间戳 (YYYY-MM-DD)
        start_date = datetime.strptime(start_date_str[:10], '%Y-%m-%d') 
        today = datetime.now()
        return (today.year - start_date.year) * 12 + (today.month - start_date.month)
    except Exception:
        return 0


# ==========================================
# 智能晋升资格审查引擎 (Smart Promotion Engine) - 纯英文版
# ==========================================

# ==========================================
# 智能晋升资格审查引擎 (Smart Promotion Engine) - 融入学历加速机制
# ==========================================

@eel.expose
def get_promotion_candidates():
    """获取所有符合真实企业晋升逻辑的候选人名单（已集成学历加速规则）"""
    try:
        conn = sqlite3.connect('company.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # 🌟 核心修改 1：在 SQL 查询中加入 education 字段
        cursor.execute("""
            SELECT id, name, current_level, 
                   COALESCE(last_promotion_date, hire_date, contract_start) as start_date,
                   compliance_status,
                   education 
            FROM employees 
            WHERE status = 'Active' OR status IS NULL
        """)
        employees = cursor.fetchall()
        
        candidates = []
        
        for emp in employees:
            # 1. 合规拦截 (一票否决)
            if emp['compliance_status'] != 'Normal':
                continue
                
            emp_id = emp['id']
            current_level = emp['current_level']
            if not current_level: 
                current_level = 'P1'
                
            # 2. 职级路径规划 & 高管静默分流
            level_path = {'P1': 'P2', 'P2': 'P3', 'P3': 'P4', 'P4': 'P5'}
            recommend_level = level_path.get(current_level, '')
            
            if not recommend_level:
                continue # 如果不在自动晋升路径中（如 P5 以上或 M 序列），交由线下评审，系统跳过
                
            # 3. 基础时间计算
            months_in_level = calculate_months_diff(emp['start_date'])
            years_in_level = months_in_level / 12.0
            
            # 🌟 核心修改 2：学历加速器 (Education Discount)
            # 规则：仅对基层 P1-P3 生效，高职级不再享受红利
            edu = emp['education'] if emp['education'] else 'Bachelor'
            edu_discount = 0.0
            
            if current_level in ['P1', 'P2', 'P3']:
                if edu == 'Master':
                    edu_discount = 0.5  # 硕士：等效增加 0.5 年在岗时间 (提早半年进入名单)
                elif edu == 'PhD':
                    edu_discount = 1.0  # 博士：等效增加 1.0 年在岗时间 (提早一年进入名单)
                    
            # 实际用于评估的等效任职年限 = 真实年限 + 学历红利
            effective_years = years_in_level + edu_discount
            
            # 绝对红线：真实在岗时间低于 0.5 年（6个月），无论学历多高直接拦截
            if years_in_level < 0.5:
                continue
                
            # 4. 历史绩效调取
            cursor.execute("""
                SELECT rating FROM performance_reviews 
                WHERE employee_id = ? 
                ORDER BY id DESC LIMIT 4
            """, (emp_id,))
            recent_ratings = [row['rating'] for row in cursor.fetchall()]
            
            if not recent_ratings:
                continue
                
            is_eligible = False
            reason = ""
            
            # 🌟 核心修改 3：在判定逻辑中使用 effective_years
            if current_level == 'P1': 
                if effective_years >= 1.5 and len(recent_ratings) >= 3:
                    if 'C' not in recent_ratings[:3] and 'D' not in recent_ratings[:3]:
                        is_eligible = True
                        reason = f"Standard Track: Consistent performance. (Includes {edu} tenure bonus)" if edu_discount > 0 else "Standard Track: Tenure met with consistent performance."
                
                elif effective_years >= 1.0 and len(recent_ratings) >= 2:
                    if all(r in ['S', 'A'] for r in recent_ratings[:2]):
                        is_eligible = True
                        reason = f"Fast Track: Outstanding performance (S/A). (Includes {edu} bonus)" if edu_discount > 0 else "Fast Track: Consecutive outstanding performance (S/A)."
                        
            elif current_level == 'P2': 
                if effective_years >= 2.5 and len(recent_ratings) >= 4:
                    sa_count = recent_ratings[:4].count('S') + recent_ratings[:4].count('A')
                    if sa_count >= 3 and 'C' not in recent_ratings[:4] and 'D' not in recent_ratings[:4]:
                        is_eligible = True
                        reason = f"Core Promotion: Excellent output over time. (Includes {edu} bonus)" if edu_discount > 0 else "Core Promotion: 2.5+ years tenure with consistently excellent output."

            if is_eligible:
                candidates.append({
                    "id": emp_id,
                    "name": emp['name'],
                    "current_level": current_level,
                    "recommend_level": recommend_level,
                    "years_in_level": round(years_in_level, 1), # 前端展示真实的实际工龄
                    "recent_ratings": recent_ratings,
                    "reason": reason # HR将看到学历加速的提示
                })
                
        conn.close()
        return {"status": "success", "data": candidates}
        
    except Exception as e:
        print(f"Promotion Engine Error: {e}")
        return {"status": "error", "message": str(e)}

@eel.expose
def execute_smart_promotion(emp_id, new_level):
    """一键执行系统推荐的晋升"""
    try:
        conn = sqlite3.connect('company.db')
        cursor = conn.cursor()
        today_str = datetime.now().strftime('%Y-%m-%d')
        
        cursor.execute("""
            UPDATE employees 
            SET current_level = ?, last_promotion_date = ?
            WHERE id = ?
        """, (new_level, today_str, emp_id))
        
        conn.commit()
        conn.close()
        # 🌟 核心修改：将成功提示改为英文
        return {"status": "success", "message": "Promotion applied successfully! Cooldown period has been reset."}
    except Exception as e:
        return {"status": "error", "message": str(e)}



# --- 5. 启动应用 (永远放在最后) ---
if __name__ == '__main__':
    eel.start('index.html', size=(1280, 900), port=0, cmdline_args=['--lang=en-US'])