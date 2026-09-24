import sqlite3

def init_db():
    conn = sqlite3.connect('company.db')
    cursor = conn.cursor()

    print("开始构建及升级数据库结构...")

    # 0. 部门表
    cursor.execute('''CREATE TABLE IF NOT EXISTS departments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    )''')

    # ==========================================
    # 1. 员工信息表 (修改这里：加入了 education, years_of_experience, job_family)
    # ==========================================
    cursor.execute('''CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL, email TEXT, phone TEXT,
        department TEXT NOT NULL, role TEXT, employment_type TEXT,
        status TEXT DEFAULT 'Active', base_salary REAL,
        
        hire_date DATE,                 -- ✅ 新增：专门的入职日期，用于精确计算工龄
        
        contract_start DATE, contract_end DATE,
        emergency_contact TEXT, notes TEXT,
        current_level TEXT, career_track TEXT,
        last_promotion_date DATE, salary_band INTEGER,
        performance_rating TEXT,
        
        compliance_status TEXT DEFAULT 'Normal', -- ✅ 新增：合规状态 (Normal/Warning)，用于一票否决制
        
        -- 👇👇👇 新增的智能定级相关字段 👇👇👇
        education TEXT,                      -- 学历 (例如: Bachelor, Master, PhD)
        years_of_experience INTEGER DEFAULT 0, -- 入职前的工作经验年限
        job_family TEXT                      -- 岗位族/职能线 (例如: Tech, Design, Marketing)
        -- 👆👆👆 新增的智能定级相关字段 👆👆👆
    )''')

    # 🌟🌟🌟 动态升级已有数据库的代码块 (ALTER TABLE) 🌟🌟🌟
    # 作用：如果你的 company.db 已经存在，上面的 CREATE 语句不会执行，
    # 我们通过读取表结构，如果发现没有这三个新字段，就自动加上去！
    cursor.execute("PRAGMA table_info(employees)")
    existing_columns = [col[1] for col in cursor.fetchall()]
    
    if 'education' not in existing_columns:
        cursor.execute("ALTER TABLE employees ADD COLUMN education TEXT")
        print("🔧 已向已有的 employees 表添加 'education' 字段")
        
    if 'years_of_experience' not in existing_columns:
        cursor.execute("ALTER TABLE employees ADD COLUMN years_of_experience INTEGER DEFAULT 0")
        print("🔧 已向已有的 employees 表添加 'years_of_experience' 字段")
        
    if 'job_family' not in existing_columns:
        cursor.execute("ALTER TABLE employees ADD COLUMN job_family TEXT")
        print("🔧 已向已有的 employees 表添加 'job_family' 字段")
    # 🌟🌟🌟 动态升级代码结束 🌟🌟🌟

    # 2. 晋升记录表
    cursor.execute('''CREATE TABLE IF NOT EXISTS promotion_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        emp_id INTEGER, old_level TEXT, new_level TEXT,
        status TEXT DEFAULT 'Pending', apply_date DATE,
        approve_date DATE, reviewer_id INTEGER, reason TEXT,
        FOREIGN KEY(emp_id) REFERENCES employees(id)
    )''')

    # 3. 绩效考核表
    cursor.execute('''CREATE TABLE IF NOT EXISTS performance_reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER, review_cycle TEXT, rating TEXT,
        comments TEXT, evaluator TEXT, evaluator_name TEXT,
        created_at DATE DEFAULT (date('now','localtime')),
        punctuality INTEGER DEFAULT 100, quality INTEGER DEFAULT 100,
        FOREIGN KEY (employee_id) REFERENCES employees (id)
    )''')

    # 4. 调薪记录表
    cursor.execute('''CREATE TABLE IF NOT EXISTS salary_adjustments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_name TEXT, old_level TEXT, new_level TEXT,
        old_salary REAL, new_salary REAL, reason TEXT,
        adjustment_date DATE DEFAULT (date('now','localtime'))
    )''')

    # 5. 职级字典表
    # 注意：为了保护现有数据，这里去掉了 DROP TABLE 操作。
    # 否则每次运行 init_db 都会清空你已经录入的职级数据！
    cursor.execute('''CREATE TABLE IF NOT EXISTS job_levels (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        level_code TEXT UNIQUE NOT NULL, level_name TEXT NOT NULL,         
        career_track TEXT, min_salary REAL, max_salary REAL, sort_order INTEGER                
    )''')

    # 插入默认职级 (只在表为空时插入)
    cursor.execute("SELECT COUNT(*) FROM job_levels")
    if cursor.fetchone()[0] == 0:
        default_levels = [
            ('P1', 'P1 - Junior Specialist', 10), ('P2', 'P2 - Specialist', 20),
            ('P3', 'P3 - Senior Specialist', 30), ('P4', 'P4 - Expert / Lead', 40),
            ('P5', 'P5 - Senior Expert', 50), ('P6', 'P6 - Principal', 60),
            ('M1', 'M1 - Team Leader', 100), ('M2', 'M2 - Manager', 110),
            ('M3', 'M3 - Senior Manager', 120), ('M4', 'M4 - Director', 130),
            ('M5', 'M5 - VP', 140)
        ]
        cursor.executemany("INSERT INTO job_levels (level_code, level_name, sort_order) VALUES (?, ?, ?)", default_levels)

    # 6. 招聘相关表
    cursor.execute('''CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, department TEXT,
        level_target TEXT, headcount INTEGER DEFAULT 1, status TEXT DEFAULT 'Open',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT, job_id INTEGER NOT NULL,
        name TEXT NOT NULL, email TEXT, stage TEXT DEFAULT 'Sourced', 
        evaluator_id INTEGER, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (job_id) REFERENCES jobs (id)
    )''')

    # 7. 财务及发票表
    cursor.execute('''CREATE TABLE IF NOT EXISTS invoices (
        id INTEGER PRIMARY KEY AUTOINCREMENT, invoice_no TEXT NOT NULL,
        employee_id INTEGER, category TEXT, amount REAL, date TEXT,
        status TEXT DEFAULT 'Pending', attachment TEXT,
        FOREIGN KEY (employee_id) REFERENCES employees(id)
    )''')

    # 8. 请假表
    cursor.execute('''CREATE TABLE IF NOT EXISTS leaves (
        id INTEGER PRIMARY KEY AUTOINCREMENT, emp_id INTEGER,
        leave_type TEXT, start_date TEXT, end_date TEXT, reason TEXT,
        status TEXT DEFAULT 'Pending', FOREIGN KEY (emp_id) REFERENCES employees(id)
    )''')

    # 9. 项目及日历表
    cursor.execute('''CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL,
        description TEXT, start_date TEXT, end_date TEXT, status TEXT DEFAULT 'Active'
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS calendar_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL,
        start_date TEXT NOT NULL, end_date TEXT, type TEXT, color TEXT
    )''')

    # 10. 通知及设置表
    cursor.execute('''CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT, message TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP, is_read INTEGER DEFAULT 0
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS settings (
        setting_key TEXT PRIMARY KEY, setting_value TEXT
    )''')

    # 🌟🌟🌟 最关键的救命稻草：保存所有操作！🌟🌟🌟
    conn.commit()
    conn.close()
    print("✅ 核心业务数据表 (init_db) 检查/更新/保存成功！")

def setup_user_table():
    conn = sqlite3.connect('company.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL, role TEXT DEFAULT 'admin'
    )''')
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin123')")
    except sqlite3.IntegrityError:
        pass 
    conn.commit()
    conn.close()
    print("✅ 用户登录表 (setup_user_table) 创建并保存成功！")


if __name__ == '__main__':
    # 按照顺序执行建库操作
    init_db()
    setup_user_table()
    print("🚀🚀🚀 恭喜！所有数据库表及初始配置已经完美建成！ 🚀🚀🚀")