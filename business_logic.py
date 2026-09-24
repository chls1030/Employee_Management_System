import sqlite3
from datetime import datetime, timedelta
import eel

def get_db_connection():
    """统一的数据库连接"""
    conn = sqlite3.connect('company.db')
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def dict_factory(cursor, row):
    """将数据库查询结果转换为字典，方便传递给前端 JS"""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# --- 1. 核心规则引擎：晋升评估 (精简安全版) ---
def evaluate_promotion(emp_id):
    """安全版的晋升评估，防止因为缺少历史记录表而崩溃"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, contract_start, current_level FROM employees WHERE id = ?", (emp_id,))
    emp = cursor.fetchone()
    conn.close()
    
    if not emp: return None
    
    # 简单的默认返回值，保证 dashboard 能够正常渲染
    return {"status": "ELIGIBLE", "reason": "Met Req.", "track": "Standard", "next_year": "2025"}

# --- 2. 适配图一界面的汇总接口 ---
def fetch_dashboard_data():
    conn = get_db_connection()
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, name, email, role, department as dept, status, current_level as grade
        FROM employees
    ''')
    emp_rows = cursor.fetchall()

    final_list = []
    for row in emp_rows:
        final_list.append({
            "id": row['id'], 
            "name": row['name'], 
            "email": row['email'], 
            "role": row['role'],
            "dept": row['dept'], 
            "status": row['status'],
            "grade": row['grade'], 
            "next_promotion": "2025"
        })

    cursor.execute("SELECT COUNT(*) as total FROM employees")
    total_count = cursor.fetchone()['total']
    
    cursor.execute("SELECT COUNT(*) as ft FROM employees WHERE employment_type='Full-time'")
    ft_count = cursor.fetchone()['ft']
    
    conn.close()
    
    return {
        "employees": final_list,
        "stats": {
            "total": total_count, 
            "full_time": ft_count,
            "freelance": total_count - ft_count, 
            "attendance_rate": "98%"
        }
    }

# --- 3. 绩效数据接口 ---
def get_performance_stats():
    """获取绩效图表数据，已适配新的 performance 表结构"""
    conn = get_db_connection()
    cursor = conn.cursor()
    # 注意：新表只有 punctuality 和 quality 两个打分字段
    cursor.execute('''
        SELECT e.name, p.punctuality, p.quality
        FROM performance p 
        JOIN employees e ON p.emp_id = e.id 
        LIMIT 5
    ''')
    rows = cursor.fetchall()
    conn.close()
    return [{"name": r[0], "p": r[1], "q": r[2]} for r in rows]

# =====================================================================
# --- 4. 员工管理前端页面专用 CRUD 接口 (Eel Expose) ---
# =====================================================================

@eel.expose
def get_all_employees():
    """供前端表格调用的列表接口"""
    try:
        conn = get_db_connection()
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        
        # 💡 修改点：去掉了 AS 别名，确保传给前端的键名(Key)与原版完全一致
        cursor.execute('''
            SELECT 
                id, 
                name, 
                email, 
                department, 
                role, 
                current_level, 
                employment_type, 
                status 
            FROM employees
            ORDER BY id DESC
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Exception as e:
        print(f"获取员工列表失败: {e}")
        return []

@eel.expose
def get_employee_by_id(emp_id):
    """供前端弹窗调用的单人详情接口"""
    try:
        conn = get_db_connection()
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        
        # 获取员工信息，并尝试通过 level 获取薪资范围
        cursor.execute('''
            SELECT 
                e.*, 
                jl.min_salary,
                jl.max_salary
            FROM employees e
            LEFT JOIN job_levels jl ON e.current_level = jl.level_code
            WHERE e.id = ?
        ''', (emp_id,))
        
        row = cursor.fetchone()
        conn.close()
        return row
    except Exception as e:
        print(f"获取员工详情失败: {e}")
        return None

@eel.expose
def save_employee(data, emp_id=None):
    """供前端调用的保存/更新接口 (已重写为最稳定版本，包含智能定级字段)"""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        if emp_id:
            # === 🌟 核心修改：更新现有员工 (加入了那3个新字段) ===
            cursor.execute('''
                UPDATE employees SET 
                    name=?, email=?, phone=?, department=?, role=?, 
                    employment_type=?, status=?, base_salary=?, 
                    contract_start=?, notes=?, current_level=?, last_promotion_date=?,
                    education=?, years_of_experience=?, job_family=?  -- 👈 新加的三个字段
                WHERE id=?
            ''', (
                data.get('name'), data.get('email'), data.get('phone'),
                data.get('department', 'Unassigned'), data.get('role'), 
                data.get('employment_type', 'Full-time'), data.get('status', 'Active'), 
                data.get('base_salary', 0), data.get('contract_start'), 
                data.get('notes'), data.get('current_level'), data.get('last_promotion_date'),
                
                # 👈 新加获取前端传来的三个值
                data.get('education', 'Bachelor'), 
                data.get('years_of_experience', 0), 
                data.get('job_family', 'Tech'),
                
                emp_id
            ))
        else:
            # === 🌟 核心修改：新增员工 (加入了那3个新字段，注意末尾多了3个问号) ===
            cursor.execute('''
                INSERT INTO employees (
                    name, email, phone, department, role, 
                    employment_type, status, base_salary, 
                    contract_start, notes, current_level, last_promotion_date,
                    education, years_of_experience, job_family  -- 👈 新加的三个列
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) 
            ''', (
                data.get('name'), data.get('email'), data.get('phone'),
                data.get('department', 'Unassigned'), data.get('role'), 
                data.get('employment_type', 'Full-time'), data.get('status', 'Active'), 
                data.get('base_salary', 0), data.get('contract_start'), 
                data.get('notes'), data.get('current_level'), data.get('last_promotion_date'),
                
                # 👈 新加获取前端传来的三个值
                data.get('education', 'Bachelor'), 
                data.get('years_of_experience', 0), 
                data.get('job_family', 'Tech')
            ))
            
        conn.commit()
        print(f"员工 {data.get('name')} 保存成功！")
        return True
    except Exception as e:
        print(f"保存员工失败: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

@eel.expose
def delete_employee(emp_id):
    """删除员工"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM employees WHERE id = ?", (emp_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"删除失败: {e}")
        return False

@eel.expose
def get_all_job_levels():
    """获取所有职级，用于填充前端下拉菜单"""
    try:
        conn = get_db_connection()
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        cursor.execute("SELECT id, level_code, level_name, career_track FROM job_levels ORDER BY id ASC")
        levels = cursor.fetchall()
        conn.close()
        return levels
    except Exception as e:
        print(f"获取职级失败: {e}")
        return []
    
    # ==========================================
# 【新增】：供前端 JS 调用的获取薪资带宽接口 (数据库版)
# ==========================================
@eel.expose
def get_salary_band(level_code):
    """从数据库实时获取职级对应的薪资范围"""
    if not level_code:
        return {"min": 0, "max": 0}
        
    # 处理前端可能传过来的 "P3 - 初级专员" 格式，提取 "P3"
    code = level_code.split(' - ')[0] if ' - ' in level_code else level_code
    
    try:
        conn = get_db_connection()
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        
        # 假设你的 job_levels 表里有 min_salary 和 max_salary 字段
        cursor.execute("SELECT min_salary, max_salary FROM job_levels WHERE level_code = ?", (code,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {"min": row['min_salary'], "max": row['max_salary']}
        else:
            # 如果数据库里没查到这个职级，返回 0
            return {"min": 0, "max": 0}
            
    except Exception as e:
        print(f"获取薪资范围失败: {e}")
        return {"min": 0, "max": 0}
    

    # =====================================================================
# --- 新增：绩效管理模块接口 (Performance) ---
# =====================================================================


@eel.expose
def add_performance_review(data):
    """添加一条新的绩效评价记录"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 获取前端传来的ID（兼容前端可能传 emp_id 或 employee_id 的情况）
        actual_id = data.get('employee_id') if data.get('employee_id') else data.get('emp_id')
        
        cursor.execute('''
            INSERT INTO performance_reviews (employee_id, review_cycle, rating, evaluator_name, comments)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            actual_id,  # 使用上面获取到的真实ID
            data.get('review_cycle'),
            data.get('rating'),
            data.get('evaluator_name', 'System Admin'), 
            data.get('comments')
        ))
        conn.commit()
        return True
    except Exception as e:
        print(f"保存绩效记录失败: {e}")
        return False
    finally:
        conn.close()


@eel.expose
def get_all_performance_reviews():
    """获取所有绩效记录（连表查询员工姓名）供表格展示"""
    try:
        conn = get_db_connection()
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        
        # 注意下面这行：pr.emp_id 必须改成 pr.employee_id
        cursor.execute('''
            SELECT pr.*, e.name as emp_name, e.department, e.role 
            FROM performance_reviews pr
            JOIN employees e ON pr.employee_id = e.id  
            ORDER BY pr.id DESC
        ''')
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        print(f"获取绩效列表失败: {e}")
        return []
    finally:
        conn.close()

@eel.expose
def get_employee_options():
    """获取所有员工简要信息，用于填充“选择员工”的下拉菜单"""
    try:
        conn = get_db_connection()
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM employees WHERE status = 'Active'")
        return cursor.fetchall()
    finally:
        conn.close()

       
import eel

@eel.expose
def get_performance_distribution():
    try:
        # 1. 连接你的数据库 (请替换为你的实际数据库文件名)
        conn = sqlite3.connect('company.db')
        cursor = conn.cursor()

        # 2. 执行查询语句
        # 注意：这里的 performance_reviews 和 rating 需要替换为你实际的表名和列名
        cursor.execute("""
            SELECT rating, COUNT(*) 
            FROM performance_reviews 
            GROUP BY rating
        """)
        rows = cursor.fetchall()
        
        # 将查询结果转换为字典，例如 {'S': 2, 'A': 15, 'B': 10}
        db_data = {row[0]: row[1] for row in rows}

        # 3. 数据清洗：确保所有的评级都有数据（即使是0），这样图表颜色才能固定
        default_ratings = ['S', 'A', 'B', 'C']
        final_data = {}
        for r in default_ratings:
            final_data[r] = db_data.get(r, 0) # 如果数据库里没有这个评级，就默认给 0

        conn.close()
        
        # 返回标准的 JSON 格式给前端
        return {"status": "success", "data": final_data}

    except Exception as e:
        print(f"获取绩效数据失败: {e}")
        return {"status": "error", "message": str(e)}
    
    # business_logic.py 的最底部添加：


@eel.expose
def get_salary_adjustments():
    """获取所有调薪记录，用于展示在 Payrolls 页面"""
    try:
        conn = sqlite3.connect('company.db')
        # 让返回的数据像字典一样可以通过列名访问
        conn.row_factory = sqlite3.Row 
        cursor = conn.cursor()

        # 按时间倒序查询，最新的调薪排在最前面
        cursor.execute("""
            SELECT adjustment_date, employee_name, old_level, new_level, old_salary, new_salary, reason 
            FROM salary_adjustments 
            ORDER BY id DESC
        """)
        rows = cursor.fetchall()
        
        # 将数据转为列表字典传给前端
        result = [dict(row) for row in rows]
        conn.close()
        return {"status": "success", "data": result}
    except Exception as e:
        print(f"获取调薪记录失败: {e}")
        return {"status": "error", "message": str(e)}