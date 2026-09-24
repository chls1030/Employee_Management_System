import sqlite3
import random

def upgrade_database():
    """升级主员工表，添加缺失的常规字段和智能定级字段"""
    conn = sqlite3.connect('company.db')
    cursor = conn.cursor()
    
    # 获取现有表的所有列名
    cursor.execute("PRAGMA table_info(employees)")
    columns = [info[1] for info in cursor.fetchall()]
    
    # 🌟 核心修改：在列表中加上了 education, years_of_experience, job_family
    new_columns = [
        "phone TEXT",
        "employment_type TEXT",
        "base_salary REAL",
        "contract_start DATE",
        "contract_end DATE",
        "emergency_contact TEXT",
        "notes TEXT",
        "education TEXT DEFAULT 'Bachelor'",        # 👈 新增：学历
        "years_of_experience REAL DEFAULT 0",       # 👈 新增：经验
        "job_family TEXT DEFAULT 'Tech'"            # 👈 新增：岗位族
    ]
    
    for col in new_columns:
        col_name = col.split()[0]
        if col_name not in columns:
            try:
                cursor.execute(f"ALTER TABLE employees ADD COLUMN {col}")
                print(f"✅ 成功添加列: {col_name}")
            except Exception as e:
                print(f"⚠️ 添加 {col_name} 时发生忽略的错误: {e}")

    conn.commit()
    conn.close()
    print("🎯 数据库 employees 表字段升级完成！")

def setup_promotion_schema():
    """建立职级和晋升相关的表结构"""
    conn = sqlite3.connect('company.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS job_levels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                career_track TEXT NOT NULL,  
                level_code TEXT NOT NULL,    
                level_name TEXT,             
                min_salary REAL,             
                max_salary REAL              
            )
        ''')
        
        # 给 employees 补充额外的晋升字段
        cursor.execute("PRAGMA table_info(employees)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if 'job_level_id' not in columns:
            cursor.execute("ALTER TABLE employees ADD COLUMN job_level_id INTEGER;")
            print("✅ 成功添加 job_level_id 字段。")
            
        if 'last_promotion_date' not in columns:
            cursor.execute("ALTER TABLE employees ADD COLUMN last_promotion_date DATE;")
            print("✅ 成功添加 last_promotion_date 字段。")

        conn.commit()
    except Exception as e:
        print(f"晋升表结构更新出错: {e}")
    finally:
        conn.close()

def add_performance_table():
    """建立绩效记录表"""
    conn = sqlite3.connect('company.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS performance_reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        emp_id INTEGER NOT NULL,          
        review_cycle TEXT NOT NULL,       
        rating TEXT NOT NULL,             
        evaluator_name TEXT,              
        comments TEXT,                    
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (emp_id) REFERENCES employees(id)
    );
    ''')
    conn.commit()
    conn.close()
    print("✅ performance_reviews 表已准备就绪！")


# --- 历史数据处理函数 (暂时保留，以防以后要用) ---
def assign_random_levels_to_employees():
    pass # 暂时屏蔽，防止覆盖你现有的测试数据

def translate_levels_to_english():
    pass # 暂时屏蔽，防止重复运行报错


# ==========================================
# 执行升级！
# ==========================================
if __name__ == '__main__':
    print("🚀 开始一键检查并升级数据库...")
    upgrade_database()         # 添加新字段 (学历、经验等)
    setup_promotion_schema()   # 检查职级表
    add_performance_table()    # 检查绩效表
    print("🎉 所有数据库结构均已升级到最新版本！现在可以安全运行 main_eel.py 了。")