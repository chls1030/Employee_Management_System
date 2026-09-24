import sqlite3

def reset_job_levels():
    # 连上你的数据库
    conn = sqlite3.connect('company.db')
    cursor = conn.cursor()
    
    try:
        # 1. 暴力清空目前混杂的旧数据
        cursor.execute('DELETE FROM job_levels')
        
        # 2. 准备最标准、最干净的一套带前缀的职级数据
        default_levels = [
            ('P1', 'P1 - Junior Specialist', 10), 
            ('P2', 'P2 - Specialist', 20),
            ('P3', 'P3 - Senior Specialist', 30), 
            ('P4', 'P4 - Expert / Lead', 40),
            ('P5', 'P5 - Senior Expert', 50), 
            ('P6', 'P6 - Principal', 60),
            ('M1', 'M1 - Team Leader', 100), 
            ('M2', 'M2 - Manager', 110),
            ('M3', 'M3 - Senior Manager', 120), 
            ('M4', 'M4 - Director', 130),
            ('M5', 'M5 - VP', 140)
        ]
        
        # 3. 重新插入数据库
        cursor.executemany("INSERT INTO job_levels (level_code, level_name, sort_order) VALUES (?, ?, ?)", default_levels)
        
        conn.commit()
        print("🎉 修复成功！职级列表已重置并清洗干净，请刷新前端页面查看。")
        
    except Exception as e:
        print(f"修复失败: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    reset_job_levels()