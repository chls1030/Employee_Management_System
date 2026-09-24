// ================= 1. 登录页面交互逻辑与权限控制 =================
async function handleLogin() {
    const userInp = document.getElementById('login-username').value;
    const passInp = document.getElementById('login-password').value;
    const errorMsg = document.getElementById('login-error-msg');
    
    // 基础的前端验证
    if(!userInp || !passInp) {
        errorMsg.innerText = "Please enter both username and password!";
        return;
    }
    
    // 按钮进入 Loading 状态
    errorMsg.innerText = "";
    const loginBtn = document.querySelector('.btn-login');
    loginBtn.innerText = "Verifying...";
    loginBtn.disabled = true;

    // 调用 Python 后端验证逻辑
    let response = await eel.verify_login(userInp, passInp)();
    
    // 恢复按钮状态
    loginBtn.innerText = "Sign In";
    loginBtn.disabled = false;

    if (response.status === "success") {
        // 1. 隐藏登录框，显示主仪表盘
        document.getElementById('login-container').style.display = 'none';
        document.getElementById('main-dashboard-container').style.display = 'block';
        
        // 2. RBAC 权限控制逻辑
        const userRole = response.role; 
        console.log("Sign in successful! Role:", userRole);

        const menuPayrolls = document.getElementById('menu-payrolls');
        const menuInvoices = document.getElementById('menu-invoices');
        const menuEmployees = document.getElementById('menu-employees');
        const menuRecruitment = document.getElementById('menu-recruitment');
        const menuTeamLabel = document.getElementById('menu-team-label');

        if (userRole === 'admin' || userRole === 'HR') {
            if(menuPayrolls) menuPayrolls.style.display = 'block';
            if(menuInvoices) menuInvoices.style.display = 'block';
            if(menuEmployees) menuEmployees.style.display = 'block';
            if(menuRecruitment) menuRecruitment.style.display = 'block';
            if(menuTeamLabel) menuTeamLabel.style.display = 'block';
        } else {
            if(menuPayrolls) menuPayrolls.style.display = 'none';
            if(menuInvoices) menuInvoices.style.display = 'none';
            if(menuEmployees) menuEmployees.style.display = 'none';
            if(menuRecruitment) menuRecruitment.style.display = 'none';
            if(menuTeamLabel) menuTeamLabel.style.display = 'none';
        }

        // 3. 加载仪表盘图表数据
        // 3. 加载仪表盘图表数据（加上 500 毫秒延迟，等待 Eel 通道连接）
setTimeout(() => {
    if (typeof initDashboard === 'function') {
        initDashboard();
    }
    if (typeof loadJobLevelsForDropdown === 'function') {
        loadJobLevelsForDropdown();
    }
}, 500);
    } else {
        // 登录失败：显示错误信息
        errorMsg.innerText = response.msg;
    }
} // <--- 刚才很可能就是不小心删掉了这个关键的、用来闭合 handleLogin 的大括号！

// 监听登录框的回车键事件，按回车直接登录
setTimeout(() => {
    const passInput = document.getElementById('login-password');
    if(passInput) {
        passInput.addEventListener('keypress', function (e) {
            if (e.key === 'Enter') {
                handleLogin();
            }
        });
    }
}, 500); 
// =============================================================

// ================= 2. 切换登录/注册表单 =================
function toggleAuthForm(target) {
    const loginArea = document.getElementById('login-form-area');
    const regArea = document.getElementById('register-form-area');
    const title = document.getElementById('form-title');
    const subtitle = document.getElementById('form-subtitle');

    document.getElementById('login-error-msg').innerText = "";
    document.getElementById('reg-error-msg').innerText = "";
    document.getElementById('login-password').value = "";
    document.getElementById('reg-password').value = "";
    document.getElementById('reg-confirm-password').value = "";

    if (target === 'register') {
        loginArea.style.display = 'none';
        regArea.style.display = 'block';
        title.innerText = 'Create Account';
        subtitle.innerText = 'Sign up to get started with HRM.';
    } else {
        loginArea.style.display = 'block';
        regArea.style.display = 'none';
        title.innerText = 'Welcome Back';
        subtitle.innerText = 'Please enter your details to sign in.';
    }
}

// ================= 3. 处理注册逻辑 =================
async function handleRegister() {
    const userInp = document.getElementById('reg-username').value;
    const passInp = document.getElementById('reg-password').value;
    const passConfirmInp = document.getElementById('reg-confirm-password').value;
    const roleInp = document.getElementById('reg-role').value; 
    const errorMsg = document.getElementById('reg-error-msg');
    
    
    if(!userInp || !passInp || !passConfirmInp) {
        errorMsg.innerText = "Please fill in all fields!";
        return;
    }
    if (passInp !== passConfirmInp) {
        errorMsg.innerText = "Passwords do not match!";
        return;
    }
    if (passInp.length < 5) {
        errorMsg.innerText = "Password must be at least 5 characters long!";
        return;
    }
    
    errorMsg.innerText = "";
    errorMsg.style.color = "#e53e3e"; 
    const regBtn = document.getElementById('btn-register');
    regBtn.innerText = "Creating...";
    regBtn.disabled = true;

   
    let response = await eel.register_user(userInp, passInp, roleInp)();
    regBtn.innerText = "Create Account";
    regBtn.disabled = false;

    if (response.status === "success") {
        errorMsg.style.color = "#38a169"; 
        errorMsg.innerText = response.msg;
        
        setTimeout(() => {
            toggleAuthForm('login');
            document.getElementById('login-username').value = userInp;
        }, 1500);
    } else {
        errorMsg.innerText = response.msg;
    }
}

// ================= 下面是你原本的 window.onload 和其他的代码 =================
window.onload = function() {
    // 空着
};
// ================= 新增：处理注册逻辑 =================

// ================= 下面是你原本的 loadJobLevelsForDropdown 等代码，保持不动 =================

// === 修改后的函数：同时填充所有职级下拉框 ===
async function loadJobLevelsForDropdown() {
    try {
        // 1. 调用 Python 函数 (注意函数名要和你 main_eel.py 里的 @eel.expose 名字一致)
        let levels = await eel.get_job_levels()(); 
        
        // 2. 准备 HTML 内容
        let selectHtml = '<option value="">-- Select Level --</option>';
        if (levels && levels.length > 0) {
            levels.forEach(level => {
                // value 设为 level.code (如 'P1')，显示设为 level.name (如 'P1 - Junior')
                selectHtml += `<option value="${level.code}">${level.name}</option>`;
            });
        }
        
        // 3. 同时更新“员工编辑页”和“晋升弹窗”里的下拉框
        // 假设编辑页的 ID 是 emp-level，晋升弹窗的 ID 是 promo-new-level
        const selectors = ['emp-level', 'promo-new-level'];
        
        selectors.forEach(id => {
            const selectElem = document.getElementById(id);
            if (selectElem) {
                selectElem.innerHTML = selectHtml;
                console.log(`Dropdown ${id} updated with ${levels.length} levels.`);
            }
        });
    } catch (error) {
        console.error("Failed to load the job level drop-down menu", error);
    }
}


// ==========================================
// 1. Dashboard 与图表逻辑 (保留你原有的不变)
// ==========================================

/**
 * 初始化 Dashboard 数据
 */
async function initDashboard() {
    try {
        // 1. 从 Python 获取综合数据
        const data = await eel.fetch_dashboard_data()(); 
        
        // 2. 更新统计数字 (对应图3的样式)
        const totalEmpEl = document.getElementById('total-employees');
        if (totalEmpEl && data.stats) {
            totalEmpEl.innerHTML = data.stats.total; 
        }
        
        // 3. 渲染首页的员工表格概览
        if (data.employees) {
            renderEmployeeTable(data.employees);
        }

        // 4. 初始化图表
        initCharts();
    } catch (error) {
        console.error("The initialization of Dashboard data failed:", error);
    }
}
/**
 * 渲染首页表格函数 (保留原有风格)
 */
function renderEmployeeTable(employees) {
    let tbody = document.getElementById("employeeTableBody");
    if (!tbody) return;
    
    tbody.innerHTML = "";

    // 首页只取前 5 条展示作为预览
    let previewEmployees = employees.slice(0, 5);

    previewEmployees.forEach((emp) => {
        const statusClass = emp.status === 'Full-time' ? 'status-fulltime' : 'status-freelance';
        const avatarUrl = `https://i.pravatar.cc/40?u=${emp.id}`;

        let row = `
            <tr>
                <td class="text-muted">#${emp.id}</td>
                <td>
                    
            <td style="cursor: pointer;" onclick="openEmployeeProfile(${emp.id})" title="Click to view full profile">
                <div class="d-flex align-items-center gap-3">
                    <img src="${avatarUrl}" class="rounded-circle" width="35">
                  
                    <span class="fw-bold" style="color: #4361ee; text-decoration: underline dotted;">${emp.name}</span>
                </div>
            </td>
         
                </td>
                <td class="text-muted">${emp.email || '-'}</td>
                <td>${emp.role || '-'}</td>
                <td><span class="badge bg-light text-dark border-0 shadow-sm">${emp.dept || 'Unassigned'}</span></td>
                <td><span class="status-pill ${statusClass}">${emp.status}</span></td>
                <td>
                    <button class="btn btn-sm text-muted" onclick="switchPage('employees', null); setTimeout(()=>openModal('edit', ${emp.id}), 300);"><i class="fa-regular fa-eye"></i></button>
                    <button class="btn btn-sm text-muted"><i class="fa-solid fa-ellipsis-vertical"></i></button>
                </td>
            </tr>
        `;
        tbody.innerHTML += row;
    });
}

/**
 * 图表初始化函数 (保留原有)
 */
async function initCharts() {
    const primaryColor = '#6366f1'; 
    const secondaryColor = '#3DDAB4'; 

    // A. 绩效评分图
    const perfCanvas = document.getElementById('performanceChart');
    if (perfCanvas) {
        const perfCtx = perfCanvas.getContext('2d');
        try {
            const perfData = await eel.get_performance_stats()(); // 注意：对应你后端的函数名
            
            // 避免重复创建图表导致重影
            if(window.perfChartObj) window.perfChartObj.destroy();
            
            window.perfChartObj = new Chart(perfCtx, {
                type: 'bar',
                data: {
                    labels: perfData.map(d => d.name),
                    datasets:[
                        { label: 'Punctuality', data: perfData.map(d => d.p), backgroundColor: primaryColor, borderRadius: 5 },
                        { label: 'Quality', data: perfData.map(d => d.q), backgroundColor: secondaryColor, borderRadius: 5 }
                    ]
                },
                options: {
                    indexAxis: 'y', responsive: true, maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: { x: { grid: { display: false }, max: 100 }, y: { grid: { display: false } } }
                }
            });
        } catch (e) { console.error("加载绩效图表失败", e); }
    }

    // B. 收入统计图 (静态数据)
    const incomeCanvas = document.getElementById('incomeChart');
    if (incomeCanvas) {
        const incomeCtx = incomeCanvas.getContext('2d');
        if(window.incomeChartObj) window.incomeChartObj.destroy();
        window.incomeChartObj = new Chart(incomeCtx, {
            type: 'bar',
            data: {
                labels:['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
                datasets: [{ label: 'Income', data:[5000, 7000, 6000, 8000, 9500, 7000, 8500], backgroundColor: primaryColor, borderRadius: 8, barThickness: 20 }]
            },
            options: {
                responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } },
                scales: { y: { beginAtZero: true, grid: { color: '#F1F4F9' } }, x: { grid: { display: false } } }
            }
        });
    }

    // C. 设备统计小图 (静态数据)
    const deviceCanvas = document.getElementById('deviceChart');
    if (deviceCanvas) {
        const deviceCtx = deviceCanvas.getContext('2d');
        if(window.deviceChartObj) window.deviceChartObj.destroy();
        window.deviceChartObj = new Chart(deviceCtx, {
            type: 'doughnut',
            data: { labels: ['Mac', 'PC', 'Other'], datasets: [{ data: [80, 13, 7], backgroundColor:[primaryColor, '#FFB020', '#F1F4F9'], borderWidth: 0 }] },
            options: { cutout: '75%', responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } } }
        });
    }
}



// ==========================================
// 2. 页面切换控制
// ==========================================

function switchPage(pageId, clickedElement) {
    document.querySelectorAll('.page-view').forEach(p => p.style.display = 'none');
    const targetPage = document.getElementById('view-' + pageId);
    if (targetPage) targetPage.style.display = 'block';

    if (clickedElement) {
        document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
        clickedElement.classList.add('active');
    }

    const titleMap = {
        'dashboard': 'Good Morning, Justin Vetrovs',
        'employees': 'Employee Management',
        'leave': 'Leave Requests',
        'performance': 'Performance Analytics',
        'projects': 'Project Overview',
        'payrolls': 'Salary Adjustments & Payrolls',
        'calendar': 'Company Calendar',
        'settings': 'System Settings',
        'notification': 'Notifications Center',
        'help': 'Help & Support',
        'promotions': 'Smart Promotion Engine'
    };
    const titleEl = document.getElementById('page-title');
    if (titleEl) {
        titleEl.innerText = titleMap[pageId] || (pageId.charAt(0).toUpperCase() + pageId.slice(1));
    }

    if (pageId === 'dashboard') {
        window.dispatchEvent(new Event('resize')); 
        initDashboard(); // 切回首页时刷新数据
    }
    
    // === 核心关联：切到员工页时，自动加载完整表格 ===
    if (pageId === 'employees') {
        loadEmployeesTable(); 
    }

    // === 切到绩效页时，自动加载绩效数据 ===
    if (pageId === 'performance') {
        loadPerformanceData(); 
    }

    // === 👇 新增这一段：切到调薪页时，准备加载调薪数据 👇 ===
    if (pageId === 'payrolls') {
         loadPayrollsData(); 
        // 注意：这行我先用 // 注释掉了，因为我们还没写这个函数。
        // 等我们下一步写完数据获取逻辑后，再把它打开，不然现在控制台会报错。
    }
    if (pageId === 'calendar') {
            // 加一个极短的延迟(50毫秒)，确保 div 已经彻底变成 display: block 再渲染日历
            // 否则 FullCalendar 计算不到宽高，会显示空白
            setTimeout(() => {
                if (typeof renderCalendar === 'function') {
                    renderCalendar();
                }
            }, 50);
        }

// === 👇 新增这一段：切到招聘页时，加载招聘数据 👇 ===
    if (pageId === 'recruitment') {
        // 给 100ms 延迟，确保页面容器已经显示，并且 WebSocket 连接稳定
        setTimeout(() => {
            if (typeof loadJobsData === 'function') {
                loadJobsData();
            }
        }, 100);
    }
    }
// ==========================================
// 3. 员工管理 CRUD (新增逻辑)
// ==========================================

/**
 * 加载并渲染完整的员工管理表格
 */
/**
 * 加载并渲染完整的员工管理表格
 */
async function loadEmployeesTable() {
    let tbody = document.getElementById('employee-tbody');
    if(!tbody) return;
    
    tbody.innerHTML = '<tr><td colspan="8" class="text-center text-muted py-4">Loading employees...</td></tr>';
    
    try {
        // 调用后端接口获取全量详情数据
        let employees = await eel.get_all_employees()();
        tbody.innerHTML = '';
        
        if(employees.length === 0) {
            tbody.innerHTML = '<tr><td colspan="8" class="text-center text-muted py-4">No employees found. Click "Add New Employee" to start.</td></tr>';
            return;
        }

       employees.forEach(emp => {
            const avatarUrl = `https://i.pravatar.cc/40?u=${emp.id}`;
            // 离职状态加上红色背景
            const statusStyle = emp.status === 'Terminated' ? 'background: #fee2e2; color: #991b1b;' : '';

            // 处理职级为空的情况
            const levelText = emp.current_level ? emp.current_level : '-';

            let tr = `
                <tr>
                    <td class="text-muted">#${emp.id}</td>
                    
                    <!-- 👉 【注意看这里！我帮你加上了 onclick 和蓝色下划线样式】 👈 -->
                    <td style="cursor: pointer;" onclick="openEmployeeProfile(${emp.id})" title="Click to view full profile">
                        <div class="d-flex align-items-center gap-3">
                            <img src="${avatarUrl}" class="rounded-circle" width="35">
                            <span class="fw-bold" style="color: #4361ee; text-decoration: underline dotted;">${emp.name}</span>
                        </div>
                    </td>
                    <!-- 👉 【修改结束】 👈 -->

                    <td class="text-muted">${emp.email || '-'}</td>
                    <td><span class="badge-dept">${emp.department || 'Unassigned'}</span></td>
                    <td>${emp.role || '-'}</td>
                    
                    <!-- === 这里是我们新增的 Level 职级列 === -->
                    <td>
                        <span style="background-color: #f0f0ff; color: #5b5cfa; padding: 4px 8px; border-radius: 6px; font-weight: bold; font-size: 13px;">
                            ${levelText}
                        </span>
                    </td>
                    <!-- =================================== -->

                    <td>${emp.employment_type || '-'}</td>
                    <td><span class="badge-status" style="${statusStyle}">${emp.status}</span></td>
                    <td class="text-end">
                        <!-- === 新增的晋升/调薪按钮 === -->
                        <button onclick="openPromotionModal(${emp.id}, '${emp.name}', '${levelText}', ${emp.base_salary || 0})" class="btn btn-sm btn-light me-1" title="Promote / Adjust Salary">
                            <i class="fa-solid fa-arrow-trend-up text-success"></i>
                        </button>
                        
                        <!-- 原本的编辑按钮 -->
                        <button onclick="openModal('edit', ${emp.id})" class="btn btn-sm btn-light me-1" title="Edit Profile">
                            <i class="fa-solid fa-pen text-primary"></i>
                        </button>
                        <!-- 原本的删除按钮 -->
                        <button onclick="deleteEmployeeBtn(${emp.id})" class="btn btn-sm btn-light" title="Delete">
                            <i class="fa-solid fa-trash text-danger"></i>
                        </button>
                    </td>
                </tr>
            `;
            
            tbody.insertAdjacentHTML('beforeend', tr);
        });
    } catch (e) {
        console.error("加载员工列表失败:", e);
        tbody.innerHTML = '<tr><td colspan="8" class="text-center text-danger py-4">Failed to load database connection.</td></tr>';
    }
}
/**
 * 打开新增/编辑弹窗
 */
async function openModal(mode, empId = null) {
    const modal = document.getElementById('employeeModal');
    const title = document.getElementById('modal-title');
    
    // 重置表单
    document.getElementById('employee-form').reset();
    document.getElementById('emp-id').value = '';

    if (mode === 'add') {
        title.innerText = "Add New Employee";
    } else if (mode === 'edit') {
        title.innerText = "Edit Employee Profile";
        try {
            // 从 Python 获取详细档案
            let emp = await eel.get_employee_by_id(empId)();
            if (emp) {
                document.getElementById('emp-id').value = emp.id;
                document.getElementById('emp-name').value = emp.name;
                document.getElementById('emp-email').value = emp.email || '';
                document.getElementById('emp-department').value = emp.department || 'Executive';
                document.getElementById('emp-role').value = emp.role || '';
                document.getElementById('emp-type').value = emp.employment_type || 'Full-time';
                document.getElementById('emp-status').value = emp.status || 'Active';
                document.getElementById('emp-contact').value = emp.phone || emp.emergency_contact || '';
                document.getElementById('emp-salary').value = emp.base_salary || '';
                const salaryHint = document.getElementById('salary-band-hint');
if (salaryHint) {
    if (emp.min_salary && emp.max_salary) {
        salaryHint.innerText = `Band: $${emp.min_salary} - $${emp.max_salary}`;
        salaryHint.style.color = '#6c757d'; // 变成灰色小字
    } else {
        salaryHint.innerText = ''; // 如果没有职级就不显示
    }
}
                document.getElementById('emp-start').value = emp.contract_start || '';
                document.getElementById('emp-last-promo').value = emp.last_promotion_date || '';

                document.getElementById('emp-notes').value = emp.notes || '';
                document.getElementById('emp-level').value = emp.job_level_id || '';
            }
        } catch (e) {
            console.error("获取员工详情失败:", e);
        }
    }
    
    // 初始化美丽的日期选择器，强制英文格式 (Y-m-d 代表 YYYY-MM-DD)
flatpickr("#emp-start", { dateFormat: "Y-m-d" });
flatpickr("#emp-last-promo", { dateFormat: "Y-m-d" });

    // 显示弹窗 (配合我之前给你的 css class)
    modal.style.display = 'flex';
}

/**
 * 关闭弹窗
 */
function closeModal() {
    document.getElementById('employeeModal').style.display = 'none';
}

/**
 * 提交保存员工表单 (新增或修改)
 */
async function submitEmployee() {
    let nameInput = document.getElementById('emp-name').value;
    if (!nameInput) {
        alert("Employee Name is required!");
        return;
    }

    let data = {
        name: nameInput,
        email: document.getElementById('emp-email').value,
        phone: document.getElementById('emp-contact').value,
        emergency_contact: document.getElementById('emp-contact').value,
        department: document.getElementById('emp-department').value,
        role: document.getElementById('emp-role').value,
        employment_type: document.getElementById('emp-type').value,
        status: document.getElementById('emp-status').value,
        base_salary: document.getElementById('emp-salary').value || 0,
        contract_start: document.getElementById('emp-start').value,
        contract_end: "", 
        notes: document.getElementById('emp-notes').value,
        last_promotion_date: document.getElementById('emp-last-promo').value,
        current_level: document.getElementById('emp-level').value,
        
        // 🌟🌟🌟 新增：收集智能定级的三个字段 🌟🌟🌟
        education: document.getElementById('emp-education') ? document.getElementById('emp-education').value : 'Bachelor',
        years_of_experience: document.getElementById('emp-experience') ? parseFloat(document.getElementById('emp-experience').value) : 0,
        job_family: document.getElementById('emp-job-family') ? document.getElementById('emp-job-family').value : 'Tech'
        // 🌟🌟🌟 新增结束 🌟🌟🌟
    };

    let empId = document.getElementById('emp-id').value;
    
    try {
        // 调用后端保存接口
        let result = await eel.save_employee(data, empId ? parseInt(empId) : null)();
        if (result) {
            closeModal();
            loadEmployeesTable(); // 刷新当前页列表
        }
    } catch (e) {
        console.error("保存失败:", e);
        alert("Failed to save employee data. Please check Python console.");
    }
}
/**
 * 删除员工按钮点击事件
 */
async function deleteEmployeeBtn(empId) {
    if(confirm("Are you sure you want to completely remove this employee from the system?")) {
        try {
            await eel.delete_employee(empId)();
            loadEmployeesTable(); // 刷新当前页列表
        } catch (e) {
            console.error("删除失败:", e);
        }
    }
}
// ==========================================
// 数据导出功能
// ==========================================
async function handleExport() {
    const btn = document.getElementById('exportBtn');
    
    try {
        // 1. 改变按钮状态，给用户视觉反馈
        const originalContent = btn.innerHTML;
        btn.disabled = true;
        btn.innerHTML = `<i class="fa-solid fa-spinner fa-spin me-2"></i>Exporting...`;

        // 2. 调用 Python 的导出函数 (我们在 main_eel.py 中写的函数)
        // 注意：eel.export_employee_data()() 返回的是一个 Promise
        const result = await eel.export_employee_data()();

        // 3. 根据返回结果处理
        if (result.status === "success") {
            alert("✅ 导出成功！\n文件保存路径: " + result.path);
        } else if (result.status === "error") {
            alert("❌ 导出失败: " + result.message);
        } else if (result.status === "cancelled") {
            console.log("用户取消了导出操作");
        }

        // 4. 恢复按钮状态
        btn.disabled = false;
        btn.innerHTML = originalContent;

    } catch (error) {
        console.error("导出过程中发生错误:", error);
        alert("程序运行出错，请检查控制台。");
        btn.disabled = false;
        btn.innerHTML = `<i class="fa-solid fa-file-export me-2"></i>Export Data`;
    }
}

// ==========================================
// --- 新增模块：Performance (绩效管理) ---
// ==========================================

// 1. 加载绩效列表数据
async function loadPerformanceData() {
    const tableBody = document.getElementById('performance-table-body');
    tableBody.innerHTML = '<tr><td colspan="6" class="text-center text-muted py-4">Loading data...</td></tr>';
    
    const reviews = await eel.get_all_performance_reviews()();
    
    if (reviews.length === 0) {
        tableBody.innerHTML = '<tr><td colspan="6" class="text-center text-muted py-4">No performance records found.</td></tr>';
        return;
    }

    tableBody.innerHTML = '';
    reviews.forEach(review => {
        // 给不同的 Rating 设置不同的颜色标签
        let badgeClass = 'bg-secondary'; 
        if (review.rating === 'S' || review.rating === 'A') badgeClass = 'bg-success';
        if (review.rating === 'B') badgeClass = 'bg-primary';
        if (review.rating === 'C') badgeClass = 'bg-warning text-dark';
        if (review.rating === 'D') badgeClass = 'bg-danger';

        const row = `
            <tr>
                <td class="fw-bold">${review.emp_name}</td>
                <td class="text-muted">${review.department}</td>
                <td><span class="badge bg-light text-dark border">${review.review_cycle}</span></td>
                <td><span class="badge ${badgeClass} px-2 py-1">${review.rating}</span></td>
                <td class="text-muted" style="max-width: 200px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="${review.comments || ''}">${review.comments || '-'}</td>
                <td class="text-muted small">${review.evaluator_name || 'System Admin'}</td>
            </tr>
        `;
        tableBody.insertAdjacentHTML('beforeend', row);
    });
}

// 2. 打开新增绩效弹窗，并动态加载员工下拉列表
async function openReviewModal() {
    // 加载员工选项
    const empSelect = document.getElementById('review-emp-id');
    empSelect.innerHTML = '<option value="">-- Select Employee --</option>';
    
    const employees = await eel.get_employee_options()();
    employees.forEach(emp => {
        empSelect.insertAdjacentHTML('beforeend', `<option value="${emp.id}">${emp.name}</option>`);
    });

    // 显示弹窗 (兼容 Bootstrap 5 或普通 JS 显示)
    const modalElement = document.getElementById('addReviewModal');
    if (typeof bootstrap !== 'undefined') {
        const modal = new bootstrap.Modal(modalElement);
        modal.show();
    } else {
        modalElement.style.display = 'block';
        modalElement.classList.add('show');
    }
}

// 3. 关闭弹窗
function closeReviewModal() {
    const modalElement = document.getElementById('addReviewModal');
    if (typeof bootstrap !== 'undefined') {
        const modal = bootstrap.Modal.getInstance(modalElement);
        if(modal) modal.hide();
    } else {
        modalElement.style.display = 'none';
        modalElement.classList.remove('show');
    }
    document.getElementById('review-form').reset(); // 清空表单
}

// 4. 提交保存绩效记录
async function submitReview() {
    const empId = document.getElementById('review-emp-id').value;
    const cycle = document.getElementById('review-cycle').value;
    const rating = document.getElementById('review-rating').value;
    const comments = document.getElementById('review-comments').value;

    if (!empId || !cycle || !rating) {
        alert('Please fill in all required fields (*)');
        return;
    }

    const data = {
        emp_id: parseInt(empId),
        review_cycle: cycle,
        rating: rating,
        comments: comments
    };

    const success = await eel.add_performance_review(data)();
    if (success) {
        alert('Performance review saved successfully!');
        closeReviewModal();
        loadPerformanceData(); // 重新加载表格数据，显示最新添加的记录
    } else {
        alert('Failed to save review. Check terminal for errors.');
    }
}

// ==========================================
// Dashboard 图表渲染逻辑 (安全粘贴在文件末尾)
// ==========================================

var perfChartInstance = null; // 存储图表实例

async function loadPerformanceChart() {
    // 1. 调用 Python 后端函数
    let response = await eel.get_performance_distribution()();

    if (response.status === "success") {
        const data = response.data; 
        const labels = Object.keys(data); // ['S', 'A', 'B', 'C']
        const values = Object.values(data); // [数量...]

        // 2. 获取画布
        const canvas = document.getElementById('performanceChart');
        if (!canvas) return; // 如果找不到画布，说明还没渲染，直接返回
        const ctx = canvas.getContext('2d');

        // 3. 销毁旧图表，防止重叠闪烁
        if (perfChartInstance) {
            perfChartInstance.destroy();
        }

        // 4. 渲染图表
        perfChartInstance = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: values,
                    backgroundColor: ['#4C6FFF', '#00C875', '#FFCB00', '#E2445C'],
                    borderWidth: 0,
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                cutout: '65%',
                 layout: {
                    padding: 10            // 3. 【新增】给图表四周加点内边距，防止贴边
                },
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { usePointStyle: true, boxWidth: 8, padding: 15 }
                    }
                }
            }
        });
    } else {
        console.error("加载绩效数据失败:", response.message);
    }
}
// 使用事件监听器，确保不会覆盖现有的 window.onload
document.addEventListener('DOMContentLoaded', (event) => {
    // 页面DOM加载完毕后尝试画一次图表
    loadPerformanceChart();
});

// ==========================================
// 触发晋升弹窗 (打开 Modal 并进行资格审查)
// ==========================================
async function openPromotionModal(id, name, currentLevel, currentSalary) {
    // 1. 填充基础数据 (保留你原来的逻辑)
    document.getElementById('promo-emp-id').value = id;
    document.getElementById('promo-emp-name').value = name;
    document.getElementById('promo-old-level').value = (currentLevel && currentLevel !== '-') ? currentLevel : 'Not Assigned';
    document.getElementById('promo-old-salary').value = currentSalary;

    // 2. 清空新内容
    document.getElementById('promo-new-level').value = ''; 
    document.getElementById('promo-new-salary').value = '';
    
    const reasonInput = document.getElementById('promo-reason');
    reasonInput.value = '';

    // ==================================================
    // 🌟 新增核心逻辑：向 Python 后端询问晋升资格 🌟
    // ==================================================
    try {
        // 调用我们刚才在 main_eel.py 写的函数
        let eligibility = await eel.check_promotion_eligibility(id)();
        
        // 动态获取或创建一个警告框 div (放在表单最上面)
        let modalBody = document.querySelector('#promotionModal .modal-body');
        let warningBox = document.getElementById('promo-warning-box');
        
        if (!warningBox) {
            // 如果 HTML 里没有这个 div，我们用 JS 动态建一个
            warningBox = document.createElement('div');
            warningBox.id = 'promo-warning-box';
            modalBody.insertBefore(warningBox, modalBody.firstChild);
        }

        // 根据后端的审查结果，改变 UI
        if (eligibility.eligible === true) {
            // ✅ 符合晋升条件
            warningBox.style.display = 'none'; // 隐藏警告
            reasonInput.required = false; // 理由变成选填
            reasonInput.placeholder = "Optional: Add promotion notes...";
        } else {
            // ❌ 不符合条件 (年限不够)
            warningBox.style.display = 'block'; // 显示警告
            // 利用 Bootstrap 的漂亮样式 (淡黄色背景，暗黄色字)
            warningBox.className = 'alert alert-warning mb-3'; 
            warningBox.innerHTML = `⚠️ <b>Policy Notice:</b> ${eligibility.msg}`;
            
            reasonInput.required = true; // 强制要求填写破格理由！
            reasonInput.placeholder = "REQUIRED: Enter reason for policy override...";
        }
    } catch (error) {
        console.error("Failed to check eligibility:", error);
    }
    // ==================================================

    // 3. 显示弹窗 (保留你原来的逻辑)
    const modalElement = document.getElementById('promotionModal');
    const modalInstance = new bootstrap.Modal(modalElement);
    modalInstance.show();
}

// ==========================================
// 1. 提交晋升弹窗数据发给后端
// ==========================================
async function submitPromotion() {
    const empId = document.getElementById('promo-emp-id').value;
    const empName = document.getElementById('promo-emp-name').value;
    const oldLevel = document.getElementById('promo-old-level').value;
    const newLevel = document.getElementById('promo-new-level').value; 
    const oldSalary = document.getElementById('promo-old-salary').value;
    const newSalary = document.getElementById('promo-new-salary').value;
    
    const reasonInput = document.getElementById('promo-reason');
    const reason = reasonInput.value.trim();

    // 基础必填校验
    if (!newLevel || !newSalary) {
        alert("Please fill in New Level and New Salary.");
        return;
    }

    // 🌟 新增逻辑：如果是“破格晋升”，拦截空理由
    if (reasonInput.required && reason === "") {
        alert("⚠️ This promotion overrides standard policy. You MUST provide a reason.");
        reasonInput.focus(); // 让光标跳到输入框
        return;
    }

    // 确认机制 (保留你原来的逻辑)
    const confirmMsg = `Are you sure you want to promote ${empName} to ${newLevel} with a new salary of $${newSalary}?`;
    if (!confirm(confirmMsg)) {
        return; 
    }

    // 呼叫 Python 后端保存数据 (保留你原来的逻辑)
    let res = await eel.submit_promotion_adjustment(
        empId, empName, oldLevel, newLevel, oldSalary, newSalary, reason
    )();

    if (res.status === 'success') {
        const modalElement = document.getElementById('promotionModal');
        const modalInstance = bootstrap.Modal.getInstance(modalElement);
        if (modalInstance) {
            modalInstance.hide();
        }
        
        alert(res.message);
        
        if (typeof loadEmployeesTable === 'function') loadEmployeesTable(); 
        if (typeof loadPayrollsData === 'function') loadPayrollsData();
        
    } else {
        alert("Failed to promote: " + res.message);
    }
}
// ==========================================
// 2. 加载 Payrolls 页面的真实数据
// ==========================================
async function loadPayrollsData() {
    const tbody = document.getElementById('payrolls-table-body');
    if (!tbody) return;

    tbody.innerHTML = '<tr><td colspan="5" class="text-center text-muted py-4">Loading records...</td></tr>';

    let res = await eel.get_salary_adjustments()();
    console.log("Python 返回的原始数据是：", res); 

    if (res.status === 'success') {
        const records = res.data;
        tbody.innerHTML = ''; // 清空加载提示和之前的假数据

        if (records.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="text-center text-muted py-4">No adjustment records found.</td></tr>';
            return;
        }

        // 遍历真实数据并生成 HTML
        records.forEach(rec => {
            // 格式化金额，比如 10000 变成 10,000
            const formatSalary = (num) => Number(num).toLocaleString();

            let tr = `
                <tr>
                    <td class="text-muted">${rec.adjustment_date}</td>
                    <td class="fw-bold">${rec.employee_name}</td>
                    <td>
                        <span class="badge bg-secondary">${rec.old_level}</span> 
                        <i class="fa-solid fa-arrow-right mx-1 text-muted"></i> 
                        <span class="badge bg-primary">${rec.new_level}</span>
                    </td>
                    <td>
                        $${formatSalary(rec.old_salary)} 
                        <i class="fa-solid fa-arrow-right mx-1 text-muted"></i> 
                        <span class="text-success fw-bold">$${formatSalary(rec.new_salary)}</span>
                    </td>
                    <td class="text-muted small">${rec.reason}</td>
                </tr>
            `;
            tbody.insertAdjacentHTML('beforeend', tr);
        });
    } else {
        tbody.innerHTML = `<tr><td colspan="5" class="text-center text-danger py-4">Error: ${res.message}</td></tr>`;
    }
}

// 关闭抽屉
function closeProfileDrawer() {
    document.getElementById('profile-drawer').style.display = 'none';
}

// 打开抽屉并加载数据 (绑定到员工列表的点击事件上)
async function openEmployeeProfile(empId) {
    // 显示抽屉 (可以先加个 loading 效果，这里省略)
    document.getElementById('profile-drawer').style.display = 'flex';
    document.getElementById('drawer-timeline').innerHTML = '<p>Loading timeline...</p>';

    // 调用后端的 Python 函数捞数据
    let res = await eel.get_employee_profile_timeline(empId)();

    if (res.status === 'success') {
        const info = res.info;
        const timeline = res.timeline;

        // 1. 渲染左侧基础信息
        document.getElementById('drawer-name').innerText = info.name;
        document.getElementById('drawer-role-dept').innerText = `${info.role} • ${info.department}`;
        document.getElementById('drawer-email').innerText = info.email;
        document.getElementById('drawer-level').innerText = info.current_level || 'N/A';
        document.getElementById('drawer-salary').innerText = info.base_salary ? `$${info.base_salary}` : 'Not set';

        // 2. 渲染右侧时间轴
        let timelineHtml = '';
        if (timeline.length === 0) {
            timelineHtml = '<p class="text-gray">No activity history yet.</p>';
        } else {
            timeline.forEach(event => {
                timelineHtml += `
                    <div class="timeline-item">
                        <div class="timeline-icon">${event.icon}</div>
                        <div class="timeline-date">${event.date}</div>
                        <div class="timeline-title">${event.title}</div>
                        <div class="timeline-desc">${event.description}</div>
                    </div>
                `;
            });
        }
        document.getElementById('drawer-timeline').innerHTML = timelineHtml;
    } else {
        alert("Error loading profile: " + res.message);
    }
}
// ============================================================================
// 新增：员工详情右侧抽屉 & 职业时间轴逻辑 (Employee Profile Drawer & Timeline)
// ============================================================================

/**
 * 关闭右侧抽屉
 */
function closeProfileDrawer() {
    let drawer = document.getElementById('profile-drawer');
    if (drawer) {
        drawer.style.display = 'none';
    }
}

/**
 * 点击员工姓名时打开抽屉，并从数据库拉取时间轴数据
 */
async function openEmployeeProfile(empId) {
    let drawer = document.getElementById('profile-drawer');
    let timelineContainer = document.getElementById('drawer-timeline');
    
    // 1. 显示抽屉面板，并显示 Loading 状态
    drawer.style.display = 'flex';
    timelineContainer.innerHTML = '<p style="color: #888; text-align: center; margin-top: 20px;">Loading timeline data...</p>';

    try {
        // 2. 调用我们在 main_eel.py 里写的后端接口
        let res = await eel.get_employee_profile_timeline(empId)();

        if (res.status === 'success') {
            const info = res.info;
            const timeline = res.timeline;

            // 3. 填充基础信息 (姓名、职位、薪水等)
            document.getElementById('drawer-name').innerText = info.name || 'Unknown';
            document.getElementById('drawer-role-dept').innerText = `${info.role || 'Employee'} • ${info.department || 'Unassigned'}`;
            document.getElementById('drawer-email').innerText = info.email || '-';
            document.getElementById('drawer-level').innerText = info.current_level || 'N/A';
            document.getElementById('drawer-salary').innerText = info.base_salary ? `$${info.base_salary}` : '-';
            
            // 头像 (用你现有的 pravatar 接口)
            document.getElementById('drawer-avatar').innerHTML = `<img src="https://i.pravatar.cc/80?u=${info.id}" style="border-radius: 50%; width: 60px; height: 60px; object-fit: cover;">`;

            // 4. 动态生成时间轴 HTML
            let timelineHtml = '';
            if (!timeline || timeline.length === 0) {
                timelineHtml = '<p style="color: #888;">No history records found.</p>';
            } else {
                timeline.forEach(event => {
                    timelineHtml += `
                        <div class="timeline-item">
                            <div class="timeline-icon">${event.icon}</div>
                            <div class="timeline-date">${event.date}</div>
                            <div class="timeline-title">${event.title}</div>
                            <div class="timeline-desc">${event.description}</div>
                        </div>
                    `;
                });
            }
            
            // 5. 渲染时间轴
            timelineContainer.innerHTML = timelineHtml;

        } else {
            timelineContainer.innerHTML = `<p style="color: red;">Error: ${res.message}</p>`;
        }
    } catch (e) {
        console.error("Failed to load employee profile:", e);
        timelineContainer.innerHTML = '<p style="color: red;">Network or connection error.</p>';
    }
}
// 修改后的 JS 提交函数，字段名完全匹配你的 Python 代码
async function submitNewInvoice() {
    const invoiceData = {
        // 注意：这里的 key 要和 Python 里的 data['no'] 等对应
        no: document.getElementById('inv-no').value,           // 对应 Python 的 data['no']
        emp_id: document.getElementById('inv-employee').value, // 对应 Python 的 data['emp_id']
        category: document.getElementById('inv-category').value,
        amount: parseFloat(document.getElementById('inv-amount').value),
        date: document.getElementById('inv-date').value
    };

    if (!invoiceData.no || !invoiceData.emp_id || !invoiceData.amount) {
        alert("Please fill in all required fields!");
        return;
    }

    try {
        const response = await eel.add_invoice(invoiceData)();
        if (response.status === 'success') {
            closeInvoiceModal();
            await loadInvoices(); // 重新加载列表
            console.log("Invoice saved!");
        } else {
            alert("Error: " + response.message);
        }
    } catch (error) {
        console.error("Failed:", error);
    }
}

// ==========================================
// 考勤/请假管理 (Leave Management) 模块
// ==========================================

// 加载并显示请假页面
async function loadLeavePage() {
    // 1. 切换页面显示状态 (隐藏 Dashboard，显示 Leave 页面)
    // 注意：这里的 id 必须和你 HTML 里的 id 一致！
    //document.getElementById('dashboard-page').style.display = 'none';
    //document.getElementById('leave-management-page').style.display = 'block';
    
    // 如果你还有其他页面（比如 Projects），也要在这里把它们设为 'none'
    // document.getElementById('projects-page').style.display = 'none';

    // 2. 获取表格主体，显示加载状态
    const tbody = document.getElementById('leave-table-body');
    if (!tbody) return; // 防止找不到元素报错
    tbody.innerHTML = '<tr><td colspan="6" style="text-align:center; padding:20px;">Loading data...</td></tr>';

    // 3. 调用 Eel 后端接口获取数据
    try {
        const leaves = await eel.get_leave_requests()();
        
        tbody.innerHTML = ''; // 清空加载提示
        
        if (leaves.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" style="text-align:center; padding:20px;">No leave requests found.</td></tr>';
            return;
        }

        // 4. 渲染表格数据
        leaves.forEach(leave => {
            let statusColor = '#f59e0b'; // 黄色 (Pending)
            if (leave.status === 'Approved') statusColor = '#10b981'; // 绿色
            if (leave.status === 'Rejected') statusColor = '#ef4444'; // 红色

            let actionButtons = '';
            if (leave.status === 'Pending') {
                actionButtons = `
                    <button onclick="handleLeaveAction(${leave.id}, 'Approved')" class="btn btn-sm btn-success me-2">Approve</button>
                    <button onclick="handleLeaveAction(${leave.id}, 'Rejected')" class="btn btn-sm btn-danger">Reject</button>
                `;
            } else {
                actionButtons = `<span class="text-muted">Processed</span>`;
            }

            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td style="padding: 15px 10px;"><b>${leave.emp_name}</b></td>
                <td style="padding: 15px 10px;">${leave.type}</td>
                <td style="padding: 15px 10px;">${leave.start} to ${leave.end}</td>
                <td style="padding: 15px 10px; color: #666;">${leave.reason}</td>
                <td style="padding: 15px 10px;">
                    <span style="background-color: ${statusColor}20; color: ${statusColor}; padding: 4px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">
                        ${leave.status}
                    </span>
                </td>
                <td style="padding: 15px 10px;">${actionButtons}</td>
            `;
            tbody.appendChild(tr);
        });
    } catch (error) {
        console.error("Failed to load leave requests:", error);
        tbody.innerHTML = '<tr><td colspan="6" style="text-align:center; padding:20px; color:red;">Error loading data.</td></tr>';
    }
}

// 处理批准或拒绝按钮点击
async function handleLeaveAction(leaveId, newStatus) {
    if (confirm(`Are you sure you want to mark this request as ${newStatus}?`)) {
        const result = await eel.update_leave_status(leaveId, newStatus)();
        if (result.status === 'success') {
            // 操作成功后，重新加载表格刷新数据
            loadLeavePage();
        } else {
            alert("Error updating status. Please try again.");
        }
    }
}

// ==========================================
//           PROJECTS (项目管理) 模块 MVP
// ==========================================

// 1. 加载并渲染项目页面 (对应你的侧边栏点击事件)
async function loadProjectsPage() {
    // 【修改这里！】把 ID 改成 HTML 里的真实 ID
    const mainContainer = document.getElementById('view-projects'); 
    
    if (!mainContainer) {
        console.error("找不到 ID 为 view-projects 的容器！");
        return;
    }

    // 先渲染页面的基本骨架：标题、新建按钮、以及用来放卡片的容器
    mainContainer.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
            <h2>Projects</h2>
            <button onclick="showAddProjectModal()" style="padding: 10px 20px; background-color: #5b61f4; color: white; border: none; border-radius: 5px; cursor: pointer;">
                + New Project
            </button>
        </div>
        <!-- 项目卡片的网格容器 -->
        <div id="projects-grid" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px;">
            <p>Loading projects...</p>
        </div>
    `;

    // 调用 Eel 后端获取数据
    try {
        const projects = await eel.get_projects()(); // 确保 main_eel.py 中有这个函数
        const grid = document.getElementById('projects-grid');
        grid.innerHTML = ''; // 清空 loading 提示

        if (projects.length === 0) {
            grid.innerHTML = '<p style="color: #666;">No projects found. Create one!</p>';
            return;
        }

        // 遍历并渲染卡片 (类似你处理 leaves 的 forEach)
        projects.forEach(p => {
            // 简单的状态颜色判断
            let statusColor = p.status === 'Active' ? '#28a745' : (p.status === 'Completed' ? '#6c757d' : '#ffc107');

            grid.innerHTML += `
                <div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); border: 1px solid #eee;">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <h3 style="margin: 0 0 10px 0; color: #333;">${p.name}</h3>
                        <span style="background-color: ${statusColor}20; color: ${statusColor}; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold;">
                            ${p.status || 'Active'}
                        </span>
                    </div>
                    <p style="color: #666; font-size: 14px; margin-bottom: 15px; min-height: 40px;">
                        ${p.description || 'No description provided.'}
                    </p>
                    <div style="font-size: 13px; color: #999;">
                        📅 ${p.start_date || 'N/A'} - ${p.end_date || 'N/A'}
                    </div>
                </div>
            `;
        });
    } catch (error) {
        console.error("Failed to load projects:", error);
        document.getElementById('projects-grid').innerHTML = '<p style="color: red;">Error loading data.</p>';
    }
}

// 2. 显示极简的“新建项目”弹窗 (MVP阶段用最简单的原生 prompt 替代复杂的模态框)
// 为了让你能最快看到效果，这里先不用写复杂的 HTML Modal，直接用原生的 prompt。
// 等这个跑通了，你再把它换成漂亮的 HTML 弹窗。
async function showAddProjectModal() {
    const name = prompt("Enter Project Name:");
    if (!name) return; // 如果用户点击取消或没填名字

    const desc = prompt("Enter Project Description (Optional):") || "";
    const startDate = prompt("Enter Start Date (YYYY-MM-DD):") || "";
    const endDate = prompt("Enter End Date (YYYY-MM-DD):") || "";

    const projectData = {
        name: name,
        description: desc,
        start_date: startDate,
        end_date: endDate,
        status: "Active"
    };

    try {
        // 调用后端保存
        const result = await eel.add_project(projectData)(); // 确保 main_eel.py 中有这个函数
        if (result.status === 'success') {
            // 保存成功后，重新加载页面刷新数据
            loadProjectsPage();
        } else {
            alert("Error adding project: " + result.msg);
        }
    } catch (error) {
        console.error("Failed to add project:", error);
        alert("System error while adding project.");
    }
}

// ====== 渲染日历的核心函数 ======
async function renderCalendar() {
    var calendarEl = document.getElementById('calendar-wrapper');
    // 如果找不到容器，直接退出，防止报错
    if (!calendarEl) return; 

    try {
        // 去找你截图里的那个 Python 函数要数据
        let eventsData = await eel.get_calendar_events()(); 
        
        // 如果之前已经画过一次日历了，先擦掉重新画
        if (window.myCalendar) {
            window.myCalendar.destroy();
        }

        // 开始画日历！
        window.myCalendar = new FullCalendar.Calendar(calendarEl, {
            initialView: 'dayGridMonth',
            events: eventsData, // 把 Python 给的数据塞进去
            height: 600,        // 固定一个高度，防止它缩成一条缝
            headerToolbar: {
                left: 'prev,next today',
                center: 'title',
                right: 'dayGridMonth,timeGridWeek'
            }
        });
        
        window.myCalendar.render();
    } catch (e) {
        console.error("日历渲染失败:", e);
    }
} 

// ==========================================
// 🌟 新增模块：Smart Promotions (智能晋升引擎)
// ==========================================

// 1. 运行引擎：获取并渲染智能晋升候选人名单
async function loadPromotions() {
    const tbody = document.getElementById('smart-promotion-table-body');
    if (!tbody) return;

    // 显示高级的加载动画状态
    tbody.innerHTML = `
        <tr>
            <td colspan="6" class="text-center py-5">
                <i class="fa-solid fa-spinner fa-spin text-primary fs-3 mb-3"></i>
                <p class="text-muted fw-medium mb-0">AI Engine is analyzing performance and tenure data...</p>
            </td>
        </tr>
    `;

    try {
        // 呼叫后端的 Python 智能引擎
        let response = await eel.get_promotion_candidates()();

        if (response.status === 'success') {
            const candidates = response.data;
            tbody.innerHTML = ''; // 清空加载提示
            
            // 如果没有人符合条件
            if (candidates.length === 0) {
                tbody.innerHTML = `
                    <tr>
                        <td colspan="6" class="text-center py-5">
                            <div class="text-muted mb-3"><i class="fa-solid fa-box-open fs-1" style="color: #cbd5e1;"></i></div>
                            <p class="text-muted fw-medium mb-0">No eligible candidates found for this cycle based on the current policy.</p>
                        </td>
                    </tr>
                `;
                return;
            }

            // 渲染符合条件的候选人列表
            candidates.forEach(cand => {
                // 美化历史绩效徽章 (S/A 绿色, B 蓝色, C 橙色, D 红色)
                let ratingsHtml = cand.recent_ratings.map(r => {
                    let badgeClass = 'bg-secondary';
                    if (r === 'S' || r === 'A') badgeClass = 'bg-success';
                    else if (r === 'B') badgeClass = 'bg-primary';
                    else if (r === 'C') badgeClass = 'bg-warning text-dark';
                    else if (r === 'D') badgeClass = 'bg-danger';
                    return `<span class="badge ${badgeClass} me-1">${r}</span>`;
                }).join('');

                // 拼装表格行 (完美契合你的 UI 风格)
                let tr = `
                    <tr style="border-bottom: 1px solid #f8f9fa;">
                        <td class="fw-bold text-dark ps-4">
                            <div class="d-flex align-items-center gap-3">
                                <img src="https://i.pravatar.cc/40?u=${cand.id}" class="rounded-circle shadow-sm" width="32">
                                ${cand.name}
                            </div>
                        </td>
                        <td>
                            <span class="badge bg-light text-secondary border">${cand.current_level}</span>
                            <i class="fa-solid fa-arrow-right mx-2 text-muted" style="font-size: 12px;"></i>
                            <span class="badge" style="background-color: #e0e7ff; color: #4f46e5;">${cand.recommend_level}</span>
                        </td>
                        <td><span class="fw-bold">${cand.years_in_level}</span> <span class="text-muted small">Years</span></td>
                        <td>${ratingsHtml}</td>
                        <td class="text-muted small" style="max-width: 250px;">
                            <i class="fa-solid fa-circle-check text-success me-1"></i>${cand.reason}
                        </td>
                        <td class="pe-4 text-end">
                            <button class="btn btn-sm px-3 shadow-sm" style="background-color: #10b981; color: white; border: none; font-weight: 600; border-radius: 8px;" 
                                    onclick="executeSmartPromotion(${cand.id}, '${cand.recommend_level}', '${cand.name}')">
                                Approve
                            </button>
                        </td>
                    </tr>
                `;
                tbody.insertAdjacentHTML('beforeend', tr);
            });
        } else {
            tbody.innerHTML = `<tr><td colspan="6" class="text-center text-danger py-4">Engine Error: ${response.message}</td></tr>`;
        }
    } catch (error) {
        console.error("Failed to load promotions:", error);
        tbody.innerHTML = '<tr><td colspan="6" class="text-center text-danger py-4">Network or server error. Check Python console.</td></tr>';
    }
}

// 2. 执行一键晋升操作
async function executeSmartPromotion(empId, newLevel, empName) {
    const msg = `Are you sure you want to authorize the promotion for ${empName} to ${newLevel}?\n\nNote: This will update their profile and reset their promotion cooldown period to today.`;
    
    if (confirm(msg)) {
        try {
            // 调用后端的晋升执行接口
            let response = await eel.execute_smart_promotion(empId, newLevel)();
            if (response.status === 'success') {
                alert(`✅ Success: ${empName} has been promoted to ${newLevel}!`);
                
                // 重新运行引擎 (该员工因为静默期被重置，会自动从列表中消失！)
                loadPromotions(); 
                
                // 如果员工列表和薪水列表曾经被加载过，也在后台刷新一下它们的数据
                if (typeof loadEmployeesTable === 'function') loadEmployeesTable(); 
            } else {
                alert("❌ Failed: " + response.message);
            }
        } catch (error) {
            console.error("Execution failed:", error);
            alert("System error during promotion execution.");
        }
    }
}

// ==========================================
// 智能定级引擎前端交互逻辑 (Smart Leveling UI)
// ==========================================

async function autoSuggestLevel() {
    // 1. 获取界面输入值
    const edu = document.getElementById('emp-education').value;
    const exp = document.getElementById('emp-experience').value;
    const jobFamily = document.getElementById('emp-job-family').value;
    
    const btn = document.getElementById('ai_suggest_btn');
    const msgLabel = document.getElementById('ai_suggest_msg');

    // 视觉反馈：变为 Loading 状态
    const originalText = btn.innerHTML;
    btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin me-1"></i> Calculating...';
    btn.disabled = true;
    msgLabel.innerText = '';

    try {
        // 2. 调用后端的 Python 引擎
        let result = await eel.suggest_employee_level_and_role(edu, exp, jobFamily)();

        if (result.status === "success") {
            // 3. 将结果填入下方原本的输入框中
            const levelInput = document.getElementById('emp-level');
            const roleInput = document.getElementById('emp-role');
            
            levelInput.value = result.suggested_level;
            roleInput.value = result.suggested_role;
            
            // 显示成功提示
            msgLabel.style.color = "#16a34a"; // 绿色
            msgLabel.innerText = result.msg;
            
            // 炫酷体验：输入框绿光闪烁动画
            highlightInput(levelInput);
            highlightInput(roleInput);
        } else {
            msgLabel.style.color = "#dc2626"; // 红色
            msgLabel.innerText = "Engine Error: " + result.message;
        }
    } catch (error) {
        console.error("Failed to connect to Python engine:", error);
        msgLabel.style.color = "#dc2626";
        msgLabel.innerText = "Connection lost.";
    } finally {
        // 恢复按钮状态
        btn.innerHTML = originalText;
        btn.disabled = false;
    }
}

// 辅助动画函数
function highlightInput(el) {
    if(el) {
        el.style.transition = "all 0.4s ease";
        el.style.backgroundColor = "#dcfce7"; // 淡绿背景
        el.style.borderColor = "#22c55e";     // 绿色边框
        setTimeout(() => {
            el.style.backgroundColor = ""; 
            el.style.borderColor = ""; 
        }, 1200);
    }
}