# seed_data.py
import sqlite3
import random

def insert_fake_departments(cursor):
    """插入缺失的部门假数据"""
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    ''')
    cursor.execute("SELECT COUNT(*) FROM departments")
    if cursor.fetchone()[0] > 0:
        print("[-] 部门表已有数据，跳过。")
        return
        
    depts = [('Team Projects',), ('Head of Projects',), ('Client & Team Work',), ('Case Study',)]
    cursor.executemany("INSERT INTO departments (name) VALUES (?)", depts)
    print("[+] 成功：部门数据已注入。")

def insert_default_job_levels(cursor):
    """插入标准的职级体系数据"""
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS job_levels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            career_track TEXT, level_code TEXT, level_name TEXT, min_salary REAL, max_salary REAL
        )
    ''')
    
    cursor.execute("SELECT COUNT(*) FROM job_levels")
    if cursor.fetchone()[0] > 0:
        print("[-] 职级表已有数据，跳过。")
        return

   
    levels_data = [
        ('Technical', 'P3', 'Junior Specialist', 5000, 8000),
        ('Technical', 'P4', 'Specialist', 8000, 15000),
        ('Technical', 'P5', 'Senior Specialist', 15000, 25000),
        ('Technical', 'P6', 'Principal Expert', 25000, 40000),
        ('Management', 'M1', 'Supervisor', 20000, 35000),
        ('Management', 'M2', 'Manager', 30000, 50000),
        ('Management', 'M3', 'Director', 50000, 80000)
    ]
    cursor.executemany('''
        INSERT INTO job_levels (career_track, level_code, level_name, min_salary, max_salary)
        VALUES (?, ?, ?, ?, ?)
    ''', levels_data)
    print("[+] 成功：标准 P/M 职级体系数据已注入。")

def insert_fake_employees(cursor):
    """插入员工假数据"""
    cursor.execute("SELECT COUNT(*) FROM employees")
    if cursor.fetchone()[0] > 0:
        print("[-] 员工表已有数据，跳过。")
        return

    # 【修改 1】：给每个员工的括号里最后加上一个评级数据，比如 'S', 'A', 'B' 等
    # 这样可以方便你测试各种晋升规则是否生效
    employees_data = [
        ('Justin Vetrovs', 'justinve@gmail.com', 'Team Projects', 'Project Manager', 'Full-time', 'M1', 'Management', '2023-01-15', 'S'),
        ('Ahmad Kenter', 'kenterah@gmail.com', 'Head of Projects', 'Web Designer', 'Full-time', 'P4', 'Technical', '2022-11-20', 'A'),
        ('Davis Herwitz', 'davishe@gmail.com', 'Client & Team Work', 'Marketing Coordinator', 'Full-time', 'M2', 'Management', '2023-05-10', 'B'),
        ('Marcus George', 'marcusg@gmail.com', 'Case Study', 'Product Designer', 'Freelance', 'P6', 'Technical', '2021-08-01', 'C'),
        ('Leo Stanton', 'leostan@gmail.com', 'Team Projects', 'Backend Developer', 'Full-time', 'P4', 'Technical', '2023-10-05', 'S'),
    ]

    # 【修改 2 & 3】：
    # 1. 字段列表最后加上 , performance_rating
    # 2. VALUES 括号里原本有 8 个 ?，现在加上 1 个变成 9 个 ?
    cursor.executemany('''
        INSERT INTO employees (name, email, department, role, employment_type, current_level, career_track, last_promotion_date, performance_rating)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', employees_data)
    print("[+] 成功：5条员工假数据已注入。")

def insert_fake_performance(cursor):
    """插入绩效假数据"""
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS performance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            emp_id INTEGER, punctuality INTEGER, quality INTEGER, review_date DATE
        )
    ''')
    
    cursor.execute("SELECT COUNT(*) FROM performance")
    if cursor.fetchone()[0] > 0:
        print("[-] 绩效表已有数据，跳过。")
        return

    perf_data = []
    for emp_id in range(1, 6):
        punctuality = random.randint(70, 100) 
        quality = random.randint(75, 100)     
        perf_data.append((emp_id, punctuality, quality, '2024-01-10'))

    cursor.executemany('''
        INSERT INTO performance (emp_id, punctuality, quality, review_date)
        VALUES (?, ?, ?, ?)
    ''', perf_data)
    print("[+] 成功：员工绩效画图数据已注入。")

def insert_fake_recruitment(cursor):
   
    # 检查是否已经有数据
    cursor.execute("SELECT COUNT(*) FROM jobs")
    if cursor.fetchone()[0] == 0:
        # 1. 插入两条招聘岗位
        jobs_data = [
            ("Frontend Developer", "Team Projects", "P4", 2, "Open"),
            ("Product Manager", "Case Study", "M2", 1, "Open"),
            ("UI/UX Designer", "Client & Team Work", "P3", 1, "Closed")
        ]
        cursor.executemany('''
            INSERT INTO jobs (title, department, level_target, headcount, status)
            VALUES (?, ?, ?, ?, ?)
        ''', jobs_data)

        # 2. 插入一些候选人
        candidates_data = [
            (1, "Alice Chen", "alice@example.com", "Sourced"),
            (1, "Bob Smith", "bob@example.com", "Interviewing"),
            (1, "John Wick", "wick@continental.com", "Sourced"),
            (1, "Sarah Connor", "sarah@skynet.com", "Interviewing"),
            (2, "David Lee", "david@example.com", "Sourced"),
            (2, "Tony Stark", "stark@starkintl.com", "Sourced"),
            (2, "Peter Parker", "peter@dailybugle.com", "Offered"),
            (3, "Bruce Wayne", "bruce@waynecorp.com", "Interviewing")
        ]
        
        cursor.executemany('''
            INSERT INTO candidates (job_id, name, email, stage)
            VALUES (?, ?, ?, ?)
        ''', candidates_data)

        print("[+] 成功: 招聘模块(职位与候选人)假数据已注入。")

def run_seeder():
    conn = sqlite3.connect('company.db')
    cursor = conn.cursor()

    try:
        print("=== 开始注入假数据 ===")
        insert_fake_departments(cursor)  
        insert_default_job_levels(cursor)
        insert_fake_employees(cursor)
        insert_fake_performance(cursor)
        insert_fake_recruitment(cursor)

        conn.commit()
        print("=== 所有假数据注入完毕！===")
    except Exception as e:
        print(f"插入数据出错: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    run_seeder()