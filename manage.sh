#!/bin/bash

################################################################################
# AI视觉设计与提示词工程百科 —— 一键运维管理脚本
# 用于管理 Python FastAPI 知识库服务
#
# 使用方式:
#   ./manage.sh setup      # 一键环境初始化
#   ./manage.sh start      # 启动 API 服务
#   ./manage.sh stop       # 停止服务
#   ./manage.sh restart    # 重启服务
#   ./manage.sh status     # 查看服务状态
#   ./manage.sh build      # 重建知识库
#   ./manage.sh validate   # 验证知识库
#   ./manage.sh search     # 命令行搜索
#   ./manage.sh update     # 拉取更新、重建、重启
#   ./manage.sh logs       # 查看服务日志
#   ./manage.sh help       # 显示帮助
#
# 环境要求: Linux/macOS + Bash + Python 3.8+
################################################################################

set -o pipefail

# ============================================================================
# 配置常量 - Configuration Constants
# ============================================================================

# 项目根目录 - 脚本所在目录即为项目根目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${SCRIPT_DIR}"

# 虚拟环境路径
VENV_DIR="${PROJECT_ROOT}/.venv"
VENV_BIN="${VENV_DIR}/bin"
PYTHON_BIN="${VENV_BIN}/python"
PIP_BIN="${VENV_BIN}/pip"

# 数据库路径
DB_PATH="${PROJECT_ROOT}/data/kb/visual_prompt_terms.sqlite"

# PID 文件和日志文件
PID_FILE="${PROJECT_ROOT}/.pid"
LOG_DIR="${PROJECT_ROOT}/logs"
LOG_FILE="${LOG_DIR}/api.log"
ERROR_LOG="${LOG_DIR}/api.error.log"

# Python 脚本路径
BUILD_SCRIPT="${PROJECT_ROOT}/scripts/rebuild.py"  # rebuild.py 在临时目录构建再回写，兼容受限挂载
VALIDATE_SCRIPT="${PROJECT_PROJECT_ROOT}/scripts/validate_kb.py"
SEARCH_SCRIPT="${PROJECT_ROOT}/scripts/search_terms.py"
API_SCRIPT="${PROJECT_ROOT}/api/app.py"

# API 配置
DEFAULT_PORT=8000
API_HOST="0.0.0.0"

# 颜色定义 - Color Definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# ============================================================================
# 工具函数 - Utility Functions
# ============================================================================

# 打印彩色消息
print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1" >&2
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_step() {
    echo -e "\n${CYAN}→${NC} $1"
}

# 检查文件或目录是否存在
check_path() {
    if [ ! -e "$1" ]; then
        print_error "路径不存在: $1"
        return 1
    fi
    return 0
}

# 检查命令是否存在
check_command() {
    if ! command -v "$1" &> /dev/null; then
        return 1
    fi
    return 0
}

# 获取 Python 版本
get_python_version() {
    if check_command python3; then
        python3 --version 2>&1 | awk '{print $2}'
    else
        echo "未找到"
    fi
}

# 创建日志目录
ensure_log_dir() {
    if [ ! -d "${LOG_DIR}" ]; then
        mkdir -p "${LOG_DIR}"
        print_info "已创建日志目录: ${LOG_DIR}"
    fi
}

# ============================================================================
# 核心操作函数 - Core Operation Functions
# ============================================================================

# 检查前置条件 - Check Prerequisites
check_prerequisites() {
    print_step "检查前置条件"

    # 检查 Python3
    if ! check_command python3; then
        print_error "未找到 Python3，请先安装 Python 3.8 或更高版本"
        return 1
    fi

    local py_version=$(get_python_version)
    print_success "Python 版本: ${py_version}"

    # 检查 pip
    if ! python3 -m pip --version &> /dev/null; then
        print_error "pip 不可用"
        return 1
    fi
    print_success "pip 可用"

    # 检查项目结构
    local required_dirs=("scripts" "api" "data" "data/kb" "web")
    for dir in "${required_dirs[@]}"; do
        if [ ! -d "${PROJECT_ROOT}/${dir}" ]; then
            print_error "缺少必要目录: ${dir}"
            return 1
        fi
    done
    print_success "项目结构完整"

    return 0
}

# 创建或升级虚拟环境
setup_venv() {
    print_step "设置虚拟环境"

    if [ -d "${VENV_DIR}" ]; then
        print_info "虚拟环境已存在，检查是否需要升级..."

        # 尝试激活虚拟环境并检查 pip
        if [ -f "${PYTHON_BIN}" ]; then
            print_success "虚拟环境有效，跳过创建"
            return 0
        fi
    fi

    # 创建新的虚拟环境
    print_info "创建虚拟环境: ${VENV_DIR}"
    if ! python3 -m venv "${VENV_DIR}"; then
        print_error "创建虚拟环境失败"
        return 1
    fi
    print_success "虚拟环境创建完成"

    return 0
}

# 安装依赖 - Install Dependencies
install_dependencies() {
    print_step "安装依赖"

    # 升级 pip, setuptools, wheel
    print_info "升级 pip, setuptools, wheel..."
    if ! "${PIP_BIN}" install --upgrade pip setuptools wheel 2>&1 | tee -a "${LOG_FILE}" > /dev/null; then
        print_error "升级失败"
        return 1
    fi
    print_success "基础工具升级完成"

    # 安装 API 依赖
    if [ -f "${PROJECT_ROOT}/api/requirements.txt" ]; then
        print_info "安装 API 依赖..."
        if ! "${PIP_BIN}" install -r "${PROJECT_ROOT}/api/requirements.txt" 2>&1 | tee -a "${LOG_FILE}" > /dev/null; then
            print_error "安装 API 依赖失败"
            return 1
        fi
        print_success "API 依赖安装完成"
    fi

    # 检查 SQLite 驱动
    print_info "检查 SQLite 驱动..."
    if ! "${PYTHON_BIN}" -c "import sqlite3; print(f'SQLite 版本: {sqlite3.sqlite_version}')" 2>&1 | tee -a "${LOG_FILE}"; then
        print_error "SQLite 驱动不可用"
        return 1
    fi
    print_success "SQLite 驱动可用"

    return 0
}

# 构建知识库 - Build Knowledge Base
build_kb() {
    print_step "构建知识库"

    ensure_log_dir

    if [ ! -f "${BUILD_SCRIPT}" ]; then
        print_error "构建脚本不存在: ${BUILD_SCRIPT}"
        return 1
    fi

    print_info "运行 rebuild.py（临时目录构建→回写主库）..."
    if ! "${PYTHON_BIN}" "${BUILD_SCRIPT}" 2>&1 | tee -a "${LOG_FILE}"; then
        print_error "知识库构建失败"
        return 1
    fi
    print_success "知识库构建完成"

    # 验证数据库
    if [ -f "${DB_PATH}" ]; then
        local term_count=$(sqlite3 "${DB_PATH}" "SELECT COUNT(*) FROM terms;" 2>/dev/null || echo "0")
        print_success "数据库中共有 ${term_count} 个术语"
    else
        print_error "数据库文件未生成"
        return 1
    fi

    return 0
}

# 构建前端 - Build Vue Frontend
build_frontend() {
    print_step "构建前端（Vue 3 + Vite + Arco Design）"

    ensure_log_dir

    if ! command -v npm >/dev/null 2>&1; then
        print_warning "未检测到 npm/Node.js。前端已预构建并随仓库提供（web/），可直接使用。"
        print_info "如需重新构建前端，请先安装 Node.js 18+ 后再执行 './manage.sh frontend'"
        return 0
    fi

    if [ ! -d "${PROJECT_ROOT}/frontend" ]; then
        print_error "前端源码目录不存在: ${PROJECT_ROOT}/frontend"
        return 1
    fi

    cd "${PROJECT_ROOT}/frontend" || return 1
    print_info "安装前端依赖（首次较慢）..."
    if ! npm install --no-audit --no-fund 2>&1 | tee -a "${LOG_FILE}"; then
        print_error "前端依赖安装失败"
        cd "${PROJECT_ROOT}" || true
        return 1
    fi
    print_info "执行 vite build，输出到 web/ ..."
    if ! npm run build 2>&1 | tee -a "${LOG_FILE}"; then
        print_error "前端构建失败"
        cd "${PROJECT_ROOT}" || true
        return 1
    fi
    cd "${PROJECT_ROOT}" || true
    print_success "前端构建完成，产物已输出到 web/"
    return 0
}

# 验证知识库 - Validate Knowledge Base
validate_kb() {
    print_step "验证知识库"

    ensure_log_dir

    if [ ! -f "${VALIDATE_SCRIPT}" ]; then
        print_error "验证脚本不存在: ${VALIDATE_SCRIPT}"
        return 1
    fi

    print_info "运行 validate_kb.py..."
    if ! "${PYTHON_BIN}" "${VALIDATE_SCRIPT}" 2>&1 | tee -a "${LOG_FILE}"; then
        print_error "知识库验证失败"
        return 1
    fi

    print_success "知识库验证完成"

    return 0
}

# 启动 API 服务 - Start API Server
start_server() {
    local port="${1:-${DEFAULT_PORT}}"

    # 检查端口是否已被占用
    if check_port_in_use "${port}"; then
        print_warning "端口 ${port} 已被占用，尝试从 PID 文件恢复..."

        if [ -f "${PID_FILE}" ]; then
            local old_pid=$(cat "${PID_FILE}")
            if ps -p "${old_pid}" > /dev/null 2>&1; then
                print_warning "已有服务运行 (PID: ${old_pid})，请先执行 stop 命令"
                return 1
            else
                # PID 无效，删除文件
                rm -f "${PID_FILE}"
                print_info "清理了无效的 PID 文件"
            fi
        else
            print_error "端口被占用但找不到 PID 文件，请手动检查占用情况"
            return 1
        fi
    fi

    print_step "启动 API 服务 (端口: ${port})"

    ensure_log_dir

    # 检查虚拟环境
    if [ ! -f "${PYTHON_BIN}" ]; then
        print_error "虚拟环境不存在，请先执行 setup"
        return 1
    fi

    # 检查 API 脚本
    if [ ! -f "${API_SCRIPT}" ]; then
        print_error "API 脚本不存在: ${API_SCRIPT}"
        return 1
    fi

    print_info "使用 nohup 启动服务..."

    # 启动服务 - 重定向输出到日志文件
    nohup "${PYTHON_BIN}" -m uvicorn api.app:app \
        --host "${API_HOST}" \
        --port "${port}" \
        --access-log \
        > "${LOG_FILE}" 2> "${ERROR_LOG}" &

    local pid=$!
    echo "${pid}" > "${PID_FILE}"

    # 等待服务启动
    sleep 2

    # 验证服务是否成功启动
    if ps -p "${pid}" > /dev/null 2>&1; then
        print_success "服务已启动 (PID: ${pid}, 端口: ${port})"
        print_info "Web UI: http://localhost:${port}/app/"
        print_info "API 文档: http://localhost:${port}/docs"
        return 0
    else
        print_error "服务启动失败，查看错误日志:"
        tail -10 "${ERROR_LOG}" >&2
        rm -f "${PID_FILE}"
        return 1
    fi
}

# 停止 API 服务 - Stop API Server
stop_server() {
    print_step "停止 API 服务"

    if [ ! -f "${PID_FILE}" ]; then
        print_warning "未找到 PID 文件，服务可能未运行"
        return 0
    fi

    local pid=$(cat "${PID_FILE}")

    if ! ps -p "${pid}" > /dev/null 2>&1; then
        print_warning "进程 ${pid} 未运行，清理 PID 文件"
        rm -f "${PID_FILE}"
        return 0
    fi

    print_info "停止进程 ${pid}..."

    # 先尝试优雅关闭
    kill "${pid}" 2>/dev/null || true

    # 等待进程关闭
    local count=0
    while ps -p "${pid}" > /dev/null 2>&1 && [ "${count}" -lt 10 ]; do
        sleep 0.5
        ((count++))
    done

    # 如果还没关闭，强制杀死
    if ps -p "${pid}" > /dev/null 2>&1; then
        print_info "进程未及时关闭，执行强制杀死..."
        kill -9 "${pid}" 2>/dev/null || true
        sleep 1
    fi

    rm -f "${PID_FILE}"
    print_success "服务已停止"

    return 0
}

# 重启服务 - Restart Server
restart_server() {
    local port="${1:-${DEFAULT_PORT}}"

    print_step "重启服务"

    if ! stop_server; then
        print_error "停止服务失败"
        return 1
    fi

    sleep 1

    if ! start_server "${port}"; then
        print_error "启动服务失败"
        return 1
    fi

    return 0
}

# 获取服务状态 - Get Server Status
get_status() {
    print_step "检查服务状态"

    if [ ! -f "${PID_FILE}" ]; then
        print_warning "未找到 PID 文件，服务未运行"
        return 0
    fi

    local pid=$(cat "${PID_FILE}")

    if ps -p "${pid}" > /dev/null 2>&1; then
        # 获取进程信息
        local proc_info=$(ps -p "${pid}" -o pid=,cmd= 2>/dev/null | tail -1)

        # 提取端口号
        local port=$(echo "${proc_info}" | grep -oP '(?<=--port\s)\d+' || echo "${DEFAULT_PORT}")

        print_success "API 服务运行中"
        echo -e "  ${BLUE}PID:${NC} ${pid}"
        echo -e "  ${BLUE}端口:${NC} ${port}"
        echo -e "  ${BLUE}进程:${NC} $(echo "${proc_info}" | cut -d' ' -f2-)"

        # 检查数据库并显示术语数量
        if [ -f "${DB_PATH}" ]; then
            local term_count=$(sqlite3 "${DB_PATH}" "SELECT COUNT(*) FROM terms;" 2>/dev/null || echo "未知")
            echo -e "  ${BLUE}术语数:${NC} ${term_count}"
        fi

        # 检查日志
        if [ -f "${LOG_FILE}" ]; then
            local recent_errors=$(grep -i error "${LOG_FILE}" 2>/dev/null | tail -3 | wc -l)
            if [ "${recent_errors}" -gt 0 ]; then
                print_warning "最近日志中发现 ${recent_errors} 条错误记录"
            fi
        fi
    else
        print_warning "PID 文件存在但进程未运行 (PID: ${pid})"
        print_info "清理无效的 PID 文件..."
        rm -f "${PID_FILE}"
    fi

    return 0
}

# 检查端口是否被占用
check_port_in_use() {
    local port="$1"
    if netstat -tuln 2>/dev/null | grep -q ":${port} "; then
        return 0  # 端口被占用
    fi
    if ss -tuln 2>/dev/null | grep -q ":${port} "; then
        return 0  # 端口被占用
    fi
    # 尝试使用 lsof
    if command -v lsof &> /dev/null; then
        if lsof -Pi ":${port}" -sTCP:LISTEN -t >/dev/null 2>&1; then
            return 0  # 端口被占用
        fi
    fi
    return 1  # 端口可用
}

# 搜索术语 - Search Terms
search_terms() {
    local keyword="$1"

    if [ -z "${keyword}" ]; then
        print_error "请提供搜索关键词"
        return 1
    fi

    print_step "搜索术语: ${keyword}"

    if [ ! -f "${SEARCH_SCRIPT}" ]; then
        print_error "搜索脚本不存在: ${SEARCH_SCRIPT}"
        return 1
    fi

    if [ ! -f "${PYTHON_BIN}" ]; then
        print_error "虚拟环境不存在，请先执行 setup"
        return 1
    fi

    ensure_log_dir

    if ! "${PYTHON_BIN}" "${SEARCH_SCRIPT}" "${keyword}" 2>&1 | tee -a "${LOG_FILE}"; then
        print_error "搜索失败"
        return 1
    fi

    return 0
}

# 更新项目 - Update Project
update_project() {
    print_step "更新项目"

    # 检查是否是 Git 仓库
    if [ -d "${PROJECT_ROOT}/.git" ]; then
        print_info "拉取最新更改..."
        if ! git -C "${PROJECT_ROOT}" pull 2>&1 | tee -a "${LOG_FILE}"; then
            print_warning "Git pull 失败，继续执行其他操作"
        else
            print_success "代码已更新"
        fi
    else
        print_info "项目非 Git 仓库，跳过拉取"
    fi

    # 重建知识库
    if ! build_kb; then
        print_error "知识库构建失败"
        return 1
    fi

    # 检查服务是否运行，若运行则重启
    if [ -f "${PID_FILE}" ] && ps -p "$(cat "${PID_FILE}")" > /dev/null 2>&1; then
        print_info "服务运行中，执行重启..."
        if ! restart_server; then
            print_error "服务重启失败"
            return 1
        fi
    else
        print_info "服务未运行，跳过重启"
    fi

    print_success "项目更新完成"
    return 0
}

# 查看日志 - Show Logs
show_logs() {
    print_step "显示最近的日志"

    ensure_log_dir

    if [ ! -f "${LOG_FILE}" ]; then
        print_warning "日志文件不存在"
        return 0
    fi

    local lines="${1:-50}"

    echo -e "\n${BLUE}=== API 日志 (最后 ${lines} 行) ===${NC}"
    tail -n "${lines}" "${LOG_FILE}"

    if [ -f "${ERROR_LOG}" ] && [ -s "${ERROR_LOG}" ]; then
        echo -e "\n${RED}=== 错误日志 ===${NC}"
        tail -n 20 "${ERROR_LOG}"
    fi

    return 0
}

# 显示帮助信息
show_help() {
    cat << EOF
${BLUE}╔════════════════════════════════════════════════════════════════════════════════╗${NC}
${BLUE}║${NC} AI视觉设计与提示词工程百科 —— 一键运维管理脚本                              ${BLUE}║${NC}
${BLUE}╚════════════════════════════════════════════════════════════════════════════════╝${NC}

${GREEN}使用方式:${NC}
  ./manage.sh <command> [options]

${GREEN}可用命令:${NC}

  ${CYAN}setup${NC}                   一键环境初始化（检查 Python、创建虚拟环境、安装依赖、构建知识库）
  ${CYAN}start [port]${NC}            启动 API 服务（默认端口 8000，后台运行）
  ${CYAN}stop${NC}                    停止运行中的 API 服务
  ${CYAN}restart [port]${NC}          重启 API 服务
  ${CYAN}status${NC}                  显示 API 服务状态、PID、端口、术语数量
  ${CYAN}build${NC}                   重建知识库（= scripts/rebuild.py，临时构建+回写，兼容受限挂载）
  ${CYAN}frontend${NC}                构建前端（npm install + vite build，输出 web/）
  ${CYAN}validate${NC}                运行知识库验证脚本
  ${CYAN}search <keyword>${NC}        在 SQLite 中快速搜索术语
  ${CYAN}update${NC}                  拉取最新代码、重建知识库、自动重启服务
  ${CYAN}logs [lines]${NC}            显示 API 日志（默认显示最后 50 行）
  ${CYAN}help${NC}                    显示此帮助信息

${GREEN}示例:${NC}
  # 首次使用：一键初始化
  ./manage.sh setup

  # 启动服务（自定义端口）
  ./manage.sh start 8080

  # 查看状态
  ./manage.sh status

  # 搜索术语
  ./manage.sh search 景深

  # 查看最后 100 行日志
  ./manage.sh logs 100

  # 重启服务
  ./manage.sh restart

  # 更新并重启
  ./manage.sh update

${GREEN}日志与配置:${NC}
  虚拟环境:     ${VENV_DIR}
  日志目录:     ${LOG_DIR}
  数据库:       ${DB_PATH}
  PID 文件:     ${PID_FILE}

${GREEN}访问服务:${NC}
  Web UI:       http://localhost:8000/app/
  API 文档:     http://localhost:8000/docs
  Swagger 文档: http://localhost:8000/swagger

${YELLOW}提示:${NC}
  - 首次使用请执行 'setup' 命令初始化环境
  - 服务以后台守护进程运行，使用 'stop' 命令停止
  - 新增/补全术语请用注入接口（推荐）：python scripts/ingest.py add-terms <terms.json>
    （详见 docs/ai-contributor-guide.md、docs/templates/；AI 不直接改 CSV）
  - 手改 CSV 或拉取代码后，执行 'build' 或 'update' 重建知识库
  - 遇到问题请查看日志文件: ${LOG_FILE}

EOF
}

# ============================================================================
# 主程序入口 - Main Entry Point
# ============================================================================

main() {
    local command="${1:-help}"
    shift || true

    # 验证当前目录结构
    if [ ! -d "${PROJECT_ROOT}/scripts" ]; then
        print_error "请在项目根目录执行此脚本"
        exit 1
    fi

    case "${command}" in
        setup)
            check_prerequisites && \
            setup_venv && \
            install_dependencies && \
            build_kb && \
            print_success "环境初始化完成！请执行 './manage.sh start' 启动服务"
            ;;
        start)
            start_server "$@"
            ;;
        stop)
            stop_server
            ;;
        restart)
            restart_server "$@"
            ;;
        status)
            get_status
            ;;
        build)
            setup_venv && \
            install_dependencies && \
            build_kb
            ;;
        frontend)
            build_frontend
            ;;
        validate)
            setup_venv && \
            install_dependencies && \
            validate_kb
            ;;
        search)
            setup_venv && \
            search_terms "$@"
            ;;
        update)
            setup_venv && \
            install_dependencies && \
            update_project
            ;;
        logs)
            show_logs "$@"
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            print_error "未知命令: ${command}"
            echo ""
            show_help
            exit 1
            ;;
    esac

    exit $?
}

# 执行主程序
main "$@"
