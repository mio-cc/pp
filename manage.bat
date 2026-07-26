@echo off
setlocal EnableExtensions EnableDelayedExpansion

REM ============================================================================
REM AI视觉设计与提示词工程百科 —— 一键运维管理脚本（Windows 版）
REM 用于管理 Python FastAPI 知识库服务
REM
REM 使用方式:
REM   manage.bat setup          一键环境初始化
REM   manage.bat start [port]   启动 API 服务（默认端口 8000，后台运行）
REM   manage.bat stop           停止服务
REM   manage.bat restart [port] 重启服务
REM   manage.bat status         查看服务状态
REM   manage.bat build          重建知识库
REM   manage.bat frontend       构建前端
REM   manage.bat validate       验证知识库
REM   manage.bat search <keyword> 命令行搜索
REM   manage.bat update         拉取更新、重建、重启
REM   manage.bat logs [lines]   查看服务日志
REM   manage.bat help           显示帮助
REM
REM 环境要求: Windows + cmd + Python 3.8+
REM 编码: 本文件以 GBK 保存，匹配中文 Windows 控制台默认代码页，无需 chcp。
REM ============================================================================

REM --- 项目根目录 - 脚本所在目录即为项目根目录 ---
set "PROJECT_ROOT=%~dp0"
if "%PROJECT_ROOT:~-1%"=="\" set "PROJECT_ROOT=%PROJECT_ROOT:~0,-1%"

REM --- 虚拟环境路径（Windows 下解释器在 Scripts\python.exe）---
set "VENV_DIR=%PROJECT_ROOT%\.venv"
set "VENV_SCRIPTS=%VENV_DIR%\Scripts"
set "PYTHON_BIN=%VENV_SCRIPTS%\python.exe"
set "PIP_BIN=%VENV_SCRIPTS%\pip.exe"

REM --- 数据库路径 ---
set "DB_PATH=%PROJECT_ROOT%\data\kb\visual_prompt_terms.sqlite"

REM --- PID 文件和日志文件 ---
set "PID_FILE=%PROJECT_ROOT%\.pid"
set "LOG_DIR=%PROJECT_ROOT%\logs"
set "LOG_FILE=%LOG_DIR%\api.log"
set "ERROR_LOG=%LOG_DIR%\api.error.log"

REM --- Python 脚本路径 ---
set "BUILD_SCRIPT=%PROJECT_ROOT%\scripts\rebuild.py"
set "VALIDATE_SCRIPT=%PROJECT_ROOT%\scripts\validate_kb.py"
set "SEARCH_SCRIPT=%PROJECT_ROOT%\scripts\search_terms.py"
set "API_SCRIPT=%PROJECT_ROOT%\api\app.py"

REM --- API 配置 ---
set "DEFAULT_PORT=8000"
set "API_HOST=0.0.0.0"

REM --- 前端目录 ---
set "FRONTEND_DIR=%PROJECT_ROOT%\frontend"
set "WEB_DIR=%PROJECT_ROOT%\web"

REM ============================================================================
REM 主程序入口 - Main Entry Point
REM ============================================================================

REM 检测是否为双击启动：双击时 %CMDCMDLINE% 形如  cmd /c "...\manage.bat"
REM （同时含 /c 与本脚本名）；从已有 cmd 窗口调用时 CMDCMDLINE 是交互式 shell
REM 本身、不含本脚本名，故不 pause，避免管道/重定向场景下 pause 阻塞挂起。
set "DBLCLICK=0"
echo %CMDCMDLINE% | findstr /I /C:" /c " >nul 2>&1
if not errorlevel 1 (
    echo %CMDCMDLINE% | findstr /I /C:"%~nx0" >nul 2>&1
    if not errorlevel 1 set "DBLCLICK=1"
)

if not exist "%PROJECT_ROOT%\scripts" (
    call :print_error "请在项目根目录执行此脚本"
    goto :finish
)

set "COMMAND=%~1"
if "%COMMAND%"=="" set "COMMAND=help"

if /i "%COMMAND%"=="setup"      goto cmd_setup
if /i "%COMMAND%"=="start"      goto cmd_start
if /i "%COMMAND%"=="stop"       goto cmd_stop
if /i "%COMMAND%"=="restart"    goto cmd_restart
if /i "%COMMAND%"=="status"     goto cmd_status
if /i "%COMMAND%"=="build"      goto cmd_build
if /i "%COMMAND%"=="frontend"   goto cmd_frontend
if /i "%COMMAND%"=="validate"   goto cmd_validate
if /i "%COMMAND%"=="search"     goto cmd_search
if /i "%COMMAND%"=="update"     goto cmd_update
if /i "%COMMAND%"=="logs"       goto cmd_logs
if /i "%COMMAND%"=="help"       goto cmd_help
if /i "%COMMAND%"=="--help"     goto cmd_help
if /i "%COMMAND%"=="-h"         goto cmd_help

call :print_error "未知命令: %COMMAND%"
echo.
goto cmd_help
exit /b 1

REM ============================================================================
REM 命令分发 - Command Dispatch
REM ============================================================================

:cmd_setup
call :check_prerequisites || exit /b 1
call :setup_venv || exit /b 1
call :install_dependencies || exit /b 1
call :build_kb || exit /b 1
call :print_success "环境初始化完成！请执行 manage.bat start 启动服务"
goto :eof

:cmd_start
set "PORT=%~2"
if "%PORT%"=="" set "PORT=%DEFAULT_PORT%"
call :start_server "%PORT%"
goto :eof

:cmd_stop
call :stop_server
goto :eof

:cmd_restart
set "PORT=%~2"
if "%PORT%"=="" set "PORT=%DEFAULT_PORT%"
call :stop_server >nul 2>&1
ping -n 2 127.0.0.1 >nul
call :start_server "%PORT%"
goto :eof

:cmd_status
call :get_status
goto :eof

:cmd_build
call :setup_venv || exit /b 1
call :install_dependencies || exit /b 1
call :build_kb
goto :eof

:cmd_frontend
call :build_frontend
goto :eof

:cmd_validate
call :setup_venv || exit /b 1
call :install_dependencies || exit /b 1
call :validate_kb
goto :eof

:cmd_search
call :setup_venv || exit /b 1
call :search_terms "%~2"
goto :eof

:cmd_update
call :setup_venv || exit /b 1
call :install_dependencies || exit /b 1
call :update_project
goto :eof

:cmd_logs
set "LINES=%~2"
if "%LINES%"=="" set "LINES=50"
call :show_logs "%LINES%"
goto :eof

:cmd_help
call :show_help
goto :finish

REM ============================================================================
REM 工具函数 - Utility Functions
REM ============================================================================

:print_success
echo [OK] %~1
goto :eof

:print_error
echo [X]  %~1 >&2
goto :eof

:print_warning
REM 注意：EnableDelayedExpansion 下 ! 是特殊字符，标签用 [W] 而非 [!] 避免被吞
echo [W]  %~1
goto :eof

:print_info
echo [i]  %~1
goto :eof

:print_step
echo.
echo [-] %~1
goto :eof

REM 创建日志目录
:ensure_log_dir
if not exist "%LOG_DIR%" (
    mkdir "%LOG_DIR%" >nul 2>&1
    call :print_info "已创建日志目录: %LOG_DIR%"
)
goto :eof

REM ============================================================================
REM 核心操作函数 - Core Operation Functions
REM ============================================================================

REM 检查前置条件
:check_prerequisites
call :print_step "检查前置条件"

where py >nul 2>&1
if not errorlevel 1 (
    py -3 --version >nul 2>&1
    if not errorlevel 1 (
        for /f "delims=" %%v in ('py -3 --version 2^>^&1') do set "PY_VER=%%v"
        call :print_success "%PY_VER%"
        goto :prereq_ok
    )
)

where python >nul 2>&1
if not errorlevel 1 (
    for /f "delims=" %%v in ('python --version 2^>^&1') do set "PY_VER=%%v"
    call :print_success "%PY_VER%"
    goto :prereq_ok
)

call :print_error "未找到 Python3，请先安装 Python 3.8 或更高版本"
exit /b 1

:prereq_ok
python -m pip --version >nul 2>&1
if errorlevel 1 (
    call :print_error "pip 不可用"
    exit /b 1
)
call :print_success "pip 可用"

REM 检查项目结构
for %%d in (scripts api data data\kb web) do (
    if not exist "%PROJECT_ROOT%\%%d" (
        call :print_error "缺少必要目录: %%d"
        exit /b 1
    )
)
call :print_success "项目结构完整"
goto :eof

REM 创建或升级虚拟环境
:setup_venv
call :print_step "设置虚拟环境"

if exist "%PYTHON_BIN%" (
    call :print_success "虚拟环境有效，跳过创建"
    goto :eof
)

if exist "%VENV_DIR%" (
    call :print_info "虚拟环境目录存在但解释器缺失，重新创建..."
    rmdir /s /q "%VENV_DIR%" >nul 2>&1
)

call :print_info "创建虚拟环境: %VENV_DIR%"

REM 优先使用 py 启动器，回退到 python
py -3 -m venv "%VENV_DIR%" >nul 2>&1
if errorlevel 1 (
    python -m venv "%VENV_DIR%"
    if errorlevel 1 (
        call :print_error "创建虚拟环境失败"
        exit /b 1
    )
)
call :print_success "虚拟环境创建完成"
goto :eof

REM 安装依赖
:install_dependencies
call :print_step "安装依赖"

call :ensure_log_dir

call :print_info "升级 pip, setuptools, wheel..."
"%PIP_BIN%" install --upgrade pip setuptools wheel >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    call :print_error "升级失败"
    exit /b 1
)
call :print_success "基础工具升级完成"

if exist "%PROJECT_ROOT%\api\requirements.txt" (
    call :print_info "安装 API 依赖..."
    "%PIP_BIN%" install -r "%PROJECT_ROOT%\api\requirements.txt" >> "%LOG_FILE%" 2>&1
    if errorlevel 1 (
        call :print_error "安装 API 依赖失败"
        exit /b 1
    )
    call :print_success "API 依赖安装完成"
)

call :print_info "检查 SQLite 驱动..."
"%PYTHON_BIN%" -c "import sqlite3; print(f'SQLite 版本: {sqlite3.sqlite_version}')" >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    call :print_error "SQLite 驱动不可用"
    exit /b 1
)
call :print_success "SQLite 驱动可用"
goto :eof

REM 构建知识库
:build_kb
call :print_step "构建知识库"

call :ensure_log_dir

if not exist "%BUILD_SCRIPT%" (
    call :print_error "构建脚本不存在: %BUILD_SCRIPT%"
    exit /b 1
)

call :print_info "运行 rebuild.py（临时目录构建后回写主库）..."
"%PYTHON_BIN%" "%BUILD_SCRIPT%" >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    call :print_error "知识库构建失败，最近日志："
    powershell -NoProfile -Command "Get-Content -Tail 15 '%LOG_FILE%'"
    exit /b 1
)
call :print_success "知识库构建完成"

REM 验证数据库（用 Python 的 sqlite3 模块，不依赖 sqlite3.exe CLI）
if exist "%DB_PATH%" (
    call :count_terms
    if "!TERM_COUNT!"=="" set "TERM_COUNT=未知"
    call :print_success "数据库中共有 !TERM_COUNT! 个术语"
) else (
    call :print_error "数据库文件未生成"
    exit /b 1
)
goto :eof

REM 构建前端
:build_frontend
call :print_step "构建前端（Vue 3 + Vite + Arco Design）"

call :ensure_log_dir

where npm >nul 2>&1
if errorlevel 1 (
    call :print_warning "未检测到 npm/Node.js。前端已预构建并随仓库提供（web/），可直接使用。"
    call :print_info "如需重新构建前端，请先安装 Node.js 18+ 后再执行 manage.bat frontend"
    goto :eof
)

if not exist "%FRONTEND_DIR%" (
    call :print_error "前端源码目录不存在: %FRONTEND_DIR%"
    exit /b 1
)

pushd "%FRONTEND_DIR%"
call :print_info "安装前端依赖（首次较慢）..."
call npm install --no-audit --no-fund >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    call :print_error "前端依赖安装失败"
    popd
    exit /b 1
)
call :print_info "执行 vite build，输出到 web/ ..."
call npm run build >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    call :print_error "前端构建失败"
    popd
    exit /b 1
)
popd
call :print_success "前端构建完成，产物已输出到 web/"
goto :eof

REM 验证知识库
:validate_kb
call :print_step "验证知识库"

call :ensure_log_dir

if not exist "%VALIDATE_SCRIPT%" (
    call :print_error "验证脚本不存在: %VALIDATE_SCRIPT%"
    exit /b 1
)

call :print_info "运行 validate_kb.py..."
"%PYTHON_BIN%" "%VALIDATE_SCRIPT%" >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    call :print_error "知识库验证失败"
    exit /b 1
)
call :print_success "知识库验证完成"
goto :eof

REM 检查端口是否被占用（参数 %1=端口；errorlevel 0=被占用, 1=可用）
:check_port_in_use
netstat -ano -p tcp | findstr /R /C:":%~1 .*LISTENING" >nul 2>&1
goto :eof

REM 检查 PID 进程是否存活（参数 %1=PID；errorlevel 0=存活, 1=不存在）
REM 用 PowerShell Get-Process 检测，避开 tasklist /FI 在某些调用链下参数被破坏的问题
:is_pid_alive
powershell -NoProfile -Command "if (Get-Process -Id %~1 -ErrorAction SilentlyContinue) { exit 0 } else { exit 1 }"
goto :eof

REM 统计数据库术语数（结果写入变量 TERM_COUNT；用不到则为空）
REM Python 代码经 stdin 传入、结果写临时文件再 set /p 读取，彻底避开 cmd 的引号嵌套地狱
:count_terms
set "TERM_COUNT="
set "COUNT_TMP=%TEMP%\kb_count.tmp"
echo import sqlite3,os;print(sqlite3.connect(os.environ['DB_PATH']).execute('select count(*) from terms').fetchone()[0])| "%PYTHON_BIN%" - > "%COUNT_TMP%" 2>nul
set /p TERM_COUNT=<"%COUNT_TMP%"
del /f /q "%COUNT_TMP%" >nul 2>&1
goto :eof

REM 启动 API 服务（参数 %1=端口）
:start_server
set "PORT=%~1"

call :check_port_in_use "%PORT%"
if not errorlevel 1 (
    call :print_warning "端口 %PORT% 已被占用，尝试从 PID 文件恢复..."
    if exist "%PID_FILE%" (
        set /p OLD_PID=<"%PID_FILE%"
        call :is_pid_alive "!OLD_PID!"
        if not errorlevel 1 (
            call :print_warning "已有服务运行 (PID: !OLD_PID!)，请先执行 stop 命令"
            exit /b 1
        ) else (
            del /f /q "%PID_FILE%" >nul 2>&1
            call :print_info "清理了无效的 PID 文件"
        )
    ) else (
        call :print_error "端口被占用但找不到 PID 文件，请手动检查占用情况"
        exit /b 1
    )
)

call :print_step "启动 API 服务 (端口: %PORT%)"

call :ensure_log_dir

if not exist "%PYTHON_BIN%" (
    call :print_error "虚拟环境不存在，请先执行 setup"
    exit /b 1
)

if not exist "%API_SCRIPT%" (
    call :print_error "API 脚本不存在: %API_SCRIPT%"
    exit /b 1
)

call :print_info "以后台方式启动服务..."

REM 清空旧日志便于查看本次启动
break > "%LOG_FILE%" 2>nul
break > "%ERROR_LOG%" 2>nul

REM 用 start /B 在后台启动（无独立窗口）。
REM 注意 start 语法：第一个带引号串恒为窗口标题，其后 /B，再是程序路径。
start "KB_API" /B "%PYTHON_BIN%" -m uvicorn api.app:app --host %API_HOST% --port %PORT% --access-log >> "%LOG_FILE%" 2>> "%ERROR_LOG%"

REM 等待端口监听就绪，并从 netstat 提取监听该端口的 PID（最可靠的反查方式）
set "PID_FOUND="
set /a WAIT_TRIES=0
:wait_listen_loop
call :get_pid_by_port "%PORT%"
if not "!PID_BY_PORT!"=="" (
    set "PID_FOUND=!PID_BY_PORT!"
)
if "!PID_FOUND!"=="" (
    set /a WAIT_TRIES+=1
    if !WAIT_TRIES! LSS 15 (
        ping -n 2 127.0.0.1 >nul
        goto :wait_listen_loop
    )
)

if "!PID_FOUND!"=="" (
    call :print_error "服务启动失败，端口 %PORT% 未监听，查看错误日志："
    if exist "%ERROR_LOG%" powershell -NoProfile -Command "Get-Content -Tail 10 '%ERROR_LOG%'"
    exit /b 1
)

echo !PID_FOUND!> "%PID_FILE%"

call :print_success "服务已启动 (PID: !PID_FOUND!, 端口: %PORT%)"
call :print_info "Web UI:  http://localhost:%PORT%/app/"
call :print_info "API 文档: http://localhost:%PORT%/docs"
goto :eof

REM 从 netstat 提取监听指定端口的 PID（参数 %1=端口；结果写入变量 PID_BY_PORT）
:get_pid_by_port
set "PID_BY_PORT="
for /f "tokens=5" %%a in ('netstat -ano -p tcp ^| findstr /R /C:":%~1 .*LISTENING" 2^>nul') do (
    set "PID_BY_PORT=%%a"
)
goto :eof

REM 停止 API 服务
:stop_server
call :print_step "停止 API 服务"

if not exist "%PID_FILE%" (
    call :print_warning "未找到 PID 文件，服务可能未运行"
    goto :eof
)

set /p PID=<"%PID_FILE%"

call :is_pid_alive "%PID%"
if errorlevel 1 (
    call :print_warning "进程 %PID% 未运行，清理 PID 文件"
    del /f /q "%PID_FILE%" >nul 2>&1
    goto :eof
)

call :print_info "停止进程 %PID%..."

REM 先尝试优雅关闭（taskkill 不带 /F，发送终止信号）；后台无控制台进程可能无响应
taskkill /PID %PID% /T >nul 2>&1

REM 短暂等待（最多约 3 秒），仍存活则强制杀死
set /a WAIT_COUNT=0
:stop_wait_loop
call :is_pid_alive "%PID%"
if not errorlevel 1 (
    set /a WAIT_COUNT+=1
    if !WAIT_COUNT! LSS 3 (
        ping -n 2 127.0.0.1 >nul
        goto :stop_wait_loop
    )
)

call :is_pid_alive "%PID%"
if not errorlevel 1 (
    call :print_info "进程未及时关闭，执行强制杀死..."
    taskkill /F /PID %PID% /T >nul 2>&1
    ping -n 2 127.0.0.1 >nul
)

del /f /q "%PID_FILE%" >nul 2>&1
call :print_success "服务已停止"
goto :eof

REM 获取服务状态
:get_status
call :print_step "检查服务状态"

if not exist "%PID_FILE%" (
    call :print_warning "未找到 PID 文件，服务未运行"
    goto :eof
)

set /p PID=<"%PID_FILE%"

call :is_pid_alive "%PID%"
if errorlevel 1 (
    call :print_warning "PID 文件存在但进程未运行 (PID: %PID%)"
    call :print_info "清理无效的 PID 文件..."
    del /f /q "%PID_FILE%" >nul 2>&1
    goto :eof
)

call :print_success "API 服务运行中"
echo   PID:    %PID%
echo   端口:   %DEFAULT_PORT% (默认)
echo   进程:   uvicorn api.app:app --host %API_HOST% --port %DEFAULT_PORT%

REM 检查数据库并显示术语数量
if exist "%DB_PATH%" (
    if exist "%PYTHON_BIN%" (
        call :count_terms
        if "!TERM_COUNT!"=="" set "TERM_COUNT=未知"
        echo   术语数: !TERM_COUNT!
    )
)
goto :eof

REM 搜索术语
:search_terms
set "KEYWORD=%~1"
if "%KEYWORD%"=="" (
    call :print_error "请提供搜索关键词"
    exit /b 1
)

call :print_step "搜索术语: %KEYWORD%"

if not exist "%SEARCH_SCRIPT%" (
    call :print_error "搜索脚本不存在: %SEARCH_SCRIPT%"
    exit /b 1
)

if not exist "%PYTHON_BIN%" (
    call :print_error "虚拟环境不存在，请先执行 setup"
    exit /b 1
)

call :ensure_log_dir

"%PYTHON_BIN%" "%SEARCH_SCRIPT%" "%KEYWORD%"
if errorlevel 1 (
    call :print_error "搜索失败"
    exit /b 1
)
goto :eof

REM 更新项目
:update_project
call :print_step "更新项目"

if exist "%PROJECT_ROOT%\.git" (
    call :print_info "拉取最新更改..."
    git -C "%PROJECT_ROOT%" pull >> "%LOG_FILE%" 2>&1
    if errorlevel 1 (
        call :print_warning "Git pull 失败，继续执行其他操作"
    ) else (
        call :print_success "代码已更新"
    )
) else (
    call :print_info "项目非 Git 仓库，跳过拉取"
)

call :build_kb
if errorlevel 1 (
    call :print_error "知识库构建失败"
    exit /b 1
)

REM 检查服务是否运行，若运行则重启
if exist "%PID_FILE%" (
    set /p RUN_PID=<"%PID_FILE%"
    call :is_pid_alive "!RUN_PID!"
    if not errorlevel 1 (
        call :print_info "服务运行中，执行重启..."
        call :stop_server >nul 2>&1
        ping -n 2 127.0.0.1 >nul
        call :start_server "%DEFAULT_PORT%"
        if errorlevel 1 (
            call :print_error "服务重启失败"
            exit /b 1
        )
    ) else (
        call :print_info "服务未运行，跳过重启"
    )
) else (
    call :print_info "服务未运行，跳过重启"
)

call :print_success "项目更新完成"
goto :eof

REM 查看日志
:show_logs
set "LINES=%~1"
if "%LINES%"=="" set "LINES=50"

call :ensure_log_dir

if not exist "%LOG_FILE%" (
    call :print_warning "日志文件不存在"
    goto :eof
)

echo.
echo === API 日志 (最后 %LINES% 行) ===
powershell -NoProfile -Command "Get-Content -Tail %LINES% '%LOG_FILE%'"

if exist "%ERROR_LOG%" (
    for %%S in ("%ERROR_LOG%") do if %%~zS GTR 0 (
        echo.
        echo === 错误日志 ===
        powershell -NoProfile -Command "Get-Content -Tail 20 '%ERROR_LOG%'"
    )
)
goto :eof

REM ============================================================================
REM 帮助信息 - Help
REM ============================================================================

:show_help
echo ============================================================================
echo   AI视觉设计与提示词工程百科 - 一键运维管理脚本（Windows 版）
echo ============================================================================
echo.
echo 使用方式:
echo   manage.bat ^<command^> [options]
echo.
echo 可用命令:
echo.
echo   setup                    一键环境初始化（检查 Python、创建虚拟环境、安装依赖、构建知识库）
echo   start [port]             启动 API 服务（默认端口 8000，后台运行）
echo   stop                     停止运行中的 API 服务
echo   restart [port]           重启 API 服务
echo   status                   显示 API 服务状态、PID、端口、术语数量
echo   build                    重建知识库（= scripts\rebuild.py，临时构建+回写，兼容受限挂载）
echo   frontend                 构建前端（npm install + vite build，输出 web\）
echo   validate                 运行知识库验证脚本
echo   search ^<keyword^>         在 SQLite 中快速搜索术语
echo   update                   拉取最新代码、重建知识库、自动重启服务
echo   logs [lines]             显示 API 日志（默认显示最后 50 行）
echo   help                     显示此帮助信息
echo.
echo 示例:
echo   REM 首次使用：一键初始化
echo   manage.bat setup
echo.
echo   REM 启动服务（自定义端口）
echo   manage.bat start 8080
echo.
echo   REM 查看状态
echo   manage.bat status
echo.
echo   REM 搜索术语
echo   manage.bat search 景深
echo.
echo   REM 查看最后 100 行日志
echo   manage.bat logs 100
echo.
echo   REM 重启服务
echo   manage.bat restart
echo.
echo   REM 更新并重启
echo   manage.bat update
echo.
echo 日志与配置:
echo   虚拟环境:  %VENV_DIR%
echo   日志目录:  %LOG_DIR%
echo   数据库:    %DB_PATH%
echo   PID 文件:  %PID_FILE%
echo.
echo 访问服务:
echo   Web UI:    http://localhost:8000/app/
echo   API 文档:  http://localhost:8000/docs
echo.
echo 提示:
echo   - 首次使用请执行 setup 命令初始化环境
echo   - 服务以后台进程运行，使用 stop 命令停止
echo   - 新增/补全术语请用注入接口（推荐）：python scripts\ingest.py add-terms ^<terms.json^>
echo     （详见 docs\ai-contributor-guide.md、docs\templates\；AI 不直接改 CSV）
echo   - 手改 CSV 或拉取代码后，执行 build 或 update 重建知识库
echo   - 遇到问题请查看日志文件: %LOG_FILE%
echo.
goto :eof

REM ============================================================================
REM 脚本统一结束点 - 仅双击启动时 pause，避免窗口一闪而过
REM ============================================================================
:finish
if "%DBLCLICK%"=="1" (
    echo.
    pause
)

