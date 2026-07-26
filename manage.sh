#!/bin/bash

################################################################################
# AI视觉设计与提示词工程百科 —— 一键运维管理脚本（交互菜单版）
#
# 两种用法：
#   ./manage.sh              # 无参数 → 进入数字菜单，按 1/2/3 选择
#   ./manage.sh <命令>       # 带参数 → 直接执行（供 crontab / 自动化使用）
#
# 常用命令: deploy start stop restart status doctor build update logs
#           frontend validate search help
#
# 环境要求: Linux/macOS + Bash + Python 3.8+
# 环境变量: API_HOST（默认 0.0.0.0；置 127.0.0.1 可只允许本机+反代访问）
#           API_PORT（默认 8000）
################################################################################

set -o pipefail

# ============================================================================
# 配置常量
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${SCRIPT_DIR}"

VENV_DIR="${PROJECT_ROOT}/.venv"
VENV_BIN="${VENV_DIR}/bin"
PYTHON_BIN="${VENV_BIN}/python"
PIP_BIN="${VENV_BIN}/pip"

DB_PATH="${PROJECT_ROOT}/data/kb/visual_prompt_terms.sqlite"

PID_FILE="${PROJECT_ROOT}/.pid"
LOG_DIR="${PROJECT_ROOT}/logs"
LOG_FILE="${LOG_DIR}/api.log"
ERROR_LOG="${LOG_DIR}/api.error.log"

BUILD_SCRIPT="${PROJECT_ROOT}/scripts/rebuild.py"   # 临时目录构建再回写，兼容受限挂载
VALIDATE_SCRIPT="${PROJECT_ROOT}/scripts/validate_kb.py"
SEARCH_SCRIPT="${PROJECT_ROOT}/scripts/search_terms.py"

DEFAULT_PORT="${API_PORT:-8000}"
API_HOST="${API_HOST:-0.0.0.0}"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
BLUE='\033[0;34m'; CYAN='\033[0;36m'; NC='\033[0m'

# ============================================================================
# 工具函数
# ============================================================================

print_success() { echo -e "${GREEN}✓${NC} $1"; }
print_error()   { echo -e "${RED}✗${NC} $1" >&2; }
print_warning() { echo -e "${YELLOW}⚠${NC} $1"; }
print_info()    { echo -e "${BLUE}ℹ${NC} $1"; }
print_step()    { echo -e "\n${CYAN}→${NC} $1"; }

check_command() { command -v "$1" &> /dev/null; }

ensure_log_dir() { [ -d "${LOG_DIR}" ] || mkdir -p "${LOG_DIR}"; }

# 术语计数（优先 sqlite3 CLI，缺失则用 venv Python 兜底）
term_count() {
    if check_command sqlite3; then
        sqlite3 "${DB_PATH}" "SELECT COUNT(*) FROM terms;" 2>/dev/null && return 0
    fi
    if [ -f "${PYTHON_BIN}" ]; then
        "${PYTHON_BIN}" - <<PY 2>/dev/null
import sqlite3
print(sqlite3.connect("${DB_PATH}").execute("SELECT COUNT(*) FROM terms").fetchone()[0])
PY
        return 0
    fi
    echo "未知"
}

check_port_in_use() {
    local port="$1"
    ss -tuln 2>/dev/null | grep -q ":${port} " && return 0
    netstat -tuln 2>/dev/null | grep -q ":${port} " && return 0
    if check_command lsof; then
        lsof -Pi ":${port}" -sTCP:LISTEN -t >/dev/null 2>&1 && return 0
    fi
    return 1
}

service_pid() {
    [ -f "${PID_FILE}" ] || return 1
    local pid
    pid=$(cat "${PID_FILE}")
    ps -p "${pid}" > /dev/null 2>&1 && echo "${pid}" && return 0
    return 1
}

# ============================================================================
# 核心操作
# ============================================================================

check_prerequisites() {
    print_step "检查前置条件"
    if ! check_command python3; then
        print_error "未找到 Python3，请先安装：apt install -y python3 python3-venv python3-pip"
        return 1
    fi
    print_success "Python 版本: $(python3 --version 2>&1 | awk '{print $2}')"
    if ! python3 -m venv --help &> /dev/null; then
        print_error "python3-venv 不可用，请安装：apt install -y python3-venv"
        return 1
    fi
    local required_dirs=("scripts" "api" "data" "web")
    for dir in "${required_dirs[@]}"; do
        if [ ! -d "${PROJECT_ROOT}/${dir}" ]; then
            print_error "缺少必要目录: ${dir}（请确认在项目根目录）"
            return 1
        fi
    done
    print_success "项目结构完整"
    return 0
}

setup_venv() {
    print_step "设置虚拟环境"
    if [ -f "${PYTHON_BIN}" ]; then
        print_success "虚拟环境已存在"
        return 0
    fi
    print_info "创建虚拟环境: ${VENV_DIR}"
    python3 -m venv "${VENV_DIR}" || { print_error "创建虚拟环境失败"; return 1; }
    print_success "虚拟环境创建完成"
    return 0
}

install_dependencies() {
    print_step "安装依赖"
    ensure_log_dir
    "${PIP_BIN}" install --upgrade pip setuptools wheel >> "${LOG_FILE}" 2>&1 \
        || { print_error "pip 升级失败（详见 ${LOG_FILE}）"; return 1; }
    if [ -f "${PROJECT_ROOT}/api/requirements.txt" ]; then
        "${PIP_BIN}" install -r "${PROJECT_ROOT}/api/requirements.txt" >> "${LOG_FILE}" 2>&1 \
            || { print_error "API 依赖安装失败（详见 ${LOG_FILE}）"; return 1; }
    fi
    print_success "依赖就绪"
    return 0
}

build_kb() {
    print_step "构建知识库（SQLite 主库不随 git 分发，克隆后必须构建）"
    ensure_log_dir
    print_info "运行 rebuild.py（含向量层构建）..."
    if ! "${PYTHON_BIN}" "${BUILD_SCRIPT}" 2>&1 | tee -a "${LOG_FILE}"; then
        print_error "知识库构建失败"
        return 1
    fi
    if [ -f "${DB_PATH}" ]; then
        print_success "构建完成，数据库共 $(term_count) 条术语"
    else
        print_error "数据库文件未生成"
        return 1
    fi
    return 0
}

build_frontend() {
    print_step "构建前端（Vue 3 + Vite）"
    if ! check_command npm; then
        print_warning "未检测到 Node/npm。前端已预构建随仓库提供（web/），一般无需重建。"
        return 0
    fi
    cd "${PROJECT_ROOT}/frontend" || return 1
    npm install --no-audit --no-fund && npm run build
    local rc=$?
    cd "${PROJECT_ROOT}" || true
    [ $rc -eq 0 ] && print_success "前端构建完成 → web/" || print_error "前端构建失败"
    return $rc
}

validate_kb() {
    print_step "验证知识库"
    "${PYTHON_BIN}" "${VALIDATE_SCRIPT}"
}

start_server() {
    local port="${1:-${DEFAULT_PORT}}"
    local pid
    if pid=$(service_pid); then
        print_warning "服务已在运行 (PID: ${pid})，无需重复启动"
        return 0
    fi
    if check_port_in_use "${port}"; then
        print_error "端口 ${port} 被其他进程占用，请先排查：ss -tlnp | grep ${port}"
        return 1
    fi
    print_step "启动 API 服务 (监听 ${API_HOST}:${port})"
    ensure_log_dir
    if [ ! -f "${PYTHON_BIN}" ]; then
        print_error "虚拟环境不存在，请先执行部署（菜单 1 或 ./manage.sh deploy）"
        return 1
    fi
    if [ ! -f "${DB_PATH}" ]; then
        print_warning "主库不存在，服务可启动但接口将报 503。建议先执行构建（菜单 7）"
    fi
    nohup "${PYTHON_BIN}" -m uvicorn api.app:app \
        --host "${API_HOST}" --port "${port}" --access-log \
        > "${LOG_FILE}" 2> "${ERROR_LOG}" &
    pid=$!
    echo "${pid}" > "${PID_FILE}"
    sleep 2
    if ps -p "${pid}" > /dev/null 2>&1; then
        print_success "服务已启动 (PID: ${pid})"
        print_info "本机访问:  http://127.0.0.1:${port}/app/"
        print_info "局域网/公网: http://<服务器IP>:${port}/app/（注意手动输入 http:// 前缀）"
        return 0
    fi
    print_error "服务启动失败，最近错误日志："
    tail -10 "${ERROR_LOG}" >&2
    rm -f "${PID_FILE}"
    return 1
}

stop_server() {
    print_step "停止 API 服务"
    local pid
    if ! pid=$(service_pid); then
        print_warning "服务未在运行"
        rm -f "${PID_FILE}"
        return 0
    fi
    kill "${pid}" 2>/dev/null || true
    local count=0
    while ps -p "${pid}" > /dev/null 2>&1 && [ "${count}" -lt 10 ]; do
        sleep 0.5; ((count++))
    done
    if ps -p "${pid}" > /dev/null 2>&1; then
        kill -9 "${pid}" 2>/dev/null || true
        sleep 1
    fi
    rm -f "${PID_FILE}"
    print_success "服务已停止"
    return 0
}

restart_server() {
    stop_server && sleep 1 && start_server "$@"
}

get_status() {
    print_step "服务状态"
    local pid
    if pid=$(service_pid); then
        print_success "API 服务运行中 (PID: ${pid})"
        ss -tlnp 2>/dev/null | grep ":${DEFAULT_PORT} " | head -2
    else
        print_warning "服务未运行"
    fi
    if [ -f "${DB_PATH}" ]; then
        echo -e "  ${BLUE}术语数:${NC} $(term_count)"
    else
        print_warning "主库不存在（需要执行构建）"
    fi
    return 0
}

search_terms() {
    local keyword="$1"
    [ -z "${keyword}" ] && { print_error "请提供搜索关键词"; return 1; }
    "${PYTHON_BIN}" "${SEARCH_SCRIPT}" "${keyword}"
}

update_project() {
    print_step "更新项目（git pull → 重建 → 重启）"
    if [ -d "${PROJECT_ROOT}/.git" ]; then
        print_info "拉取最新代码..."
        if git -C "${PROJECT_ROOT}" pull 2>&1 | tee -a "${LOG_FILE}"; then
            print_success "代码已更新"
        else
            print_warning "git pull 失败（网络/凭据问题），将继续用本地代码重建"
        fi
    else
        print_info "非 Git 仓库，跳过拉取"
    fi
    build_kb || { print_error "知识库构建失败，终止更新"; return 1; }
    if service_pid > /dev/null; then
        print_info "服务运行中，执行重启..."
        restart_server || return 1
    else
        print_info "服务未运行，自动启动..."
        start_server || return 1
    fi
    print_success "项目更新完成"
    return 0
}

show_logs() {
    local lines="${1:-50}"
    echo -e "\n${BLUE}=== API 日志 (最后 ${lines} 行) ===${NC}"
    [ -f "${LOG_FILE}" ] && tail -n "${lines}" "${LOG_FILE}" || print_warning "日志文件不存在"
    if [ -f "${ERROR_LOG}" ] && [ -s "${ERROR_LOG}" ]; then
        echo -e "\n${RED}=== 错误日志 (最后 20 行) ===${NC}"
        tail -n 20 "${ERROR_LOG}"
    fi
    return 0
}

# ============================================================================
# 一键部署 与 一键诊断
# ============================================================================

deploy_all() {
    print_step "一键部署（环境 → 依赖 → 建库 → 启动 → 自检）"
    check_prerequisites && setup_venv && install_dependencies && build_kb && start_server || return 1
    sleep 1
    print_step "启动后自检"
    local resp
    resp=$(curl -s --max-time 5 "http://127.0.0.1:${DEFAULT_PORT}/api/health" 2>/dev/null)
    if echo "${resp}" | grep -q '"status"'; then
        print_success "健康检查通过: ${resp}"
        print_info "浏览器访问: http://<服务器IP>:${DEFAULT_PORT}/app/"
    else
        print_error "本机健康检查未通过，请执行诊断（菜单 6 或 ./manage.sh doctor）"
        return 1
    fi
    return 0
}

run_doctor() {
    print_step "一键诊断（逐项检查，最后给结论）"
    local problems=0

    # 1. Python 与虚拟环境
    if check_command python3; then
        print_success "[1/8] Python3: $(python3 --version 2>&1 | awk '{print $2}')"
    else
        print_error "[1/8] 缺少 Python3 → apt install -y python3 python3-venv python3-pip"
        ((problems++))
    fi
    if [ -f "${PYTHON_BIN}" ]; then
        print_success "[2/8] 虚拟环境存在"
    else
        print_error "[2/8] 虚拟环境不存在 → 执行部署（菜单 1）"
        ((problems++))
    fi

    # 3. 关键依赖
    if [ -f "${PYTHON_BIN}" ] && "${PYTHON_BIN}" -c "import fastapi, uvicorn, jsonschema" 2>/dev/null; then
        print_success "[3/8] 依赖完整 (fastapi/uvicorn/jsonschema)"
    else
        print_error "[3/8] 依赖缺失 → 执行部署（菜单 1）重新安装"
        ((problems++))
    fi

    # 4. 数据库
    if [ -f "${DB_PATH}" ]; then
        print_success "[4/8] 主库存在，术语数: $(term_count)"
    else
        print_error "[4/8] 主库不存在（sqlite 不随 git 分发！）→ 重建知识库（菜单 7）"
        ((problems++))
    fi

    # 5. 进程
    local pid
    if pid=$(service_pid); then
        print_success "[5/8] 服务进程运行中 (PID: ${pid})"
    else
        print_error "[5/8] 服务进程未运行 → 启动服务（菜单 2）"
        ((problems++))
    fi

    # 6. 端口监听与绑定地址
    local listen_line
    listen_line=$(ss -tln 2>/dev/null | grep ":${DEFAULT_PORT} " | head -1)
    if [ -n "${listen_line}" ]; then
        print_success "[6/8] 端口 ${DEFAULT_PORT} 在监听: ${listen_line}"
        if echo "${listen_line}" | grep -q "127.0.0.1:${DEFAULT_PORT}"; then
            print_warning "      当前只监听 127.0.0.1，外部无法访问。需要公网访问请: API_HOST=0.0.0.0 ./manage.sh restart"
        fi
    else
        print_error "[6/8] 端口 ${DEFAULT_PORT} 无人监听 → 启动服务（菜单 2）"
        ((problems++))
    fi

    # 7. 本机 HTTP 探活
    local resp
    resp=$(curl -s --max-time 5 "http://127.0.0.1:${DEFAULT_PORT}/api/health" 2>/dev/null)
    if echo "${resp}" | grep -q '"status"'; then
        print_success "[7/8] 本机健康检查通过: ${resp}"
    else
        print_error "[7/8] 本机 HTTP 无响应（进程/端口问题，见上面第 5/6 项）"
        ((problems++))
    fi

    # 8. 防火墙（外部打不开而本机正常时，问题几乎都在这里）
    local fw_hint=0
    if check_command ufw && ufw status 2>/dev/null | grep -q "Status: active"; then
        if ufw status | grep -q "${DEFAULT_PORT}"; then
            print_success "[8/8] ufw 已放行 ${DEFAULT_PORT}"
        else
            print_error "[8/8] ufw 已启用但未放行 ${DEFAULT_PORT} → sudo ufw allow ${DEFAULT_PORT}/tcp"
            ((problems++)); fw_hint=1
        fi
    else
        print_success "[8/8] ufw 未启用（跳过）"
    fi
    if [ -d "/opt/1panel" ]; then
        print_warning "      检测到 1Panel：请到 1Panel 面板 → 主机 → 防火墙，确认放行了 ${DEFAULT_PORT} 端口（最常见的外网打不开原因）"
    fi
    if check_command iptables && iptables -L INPUT -n 2>/dev/null | grep -qE "DROP|REJECT"; then
        print_warning "      iptables INPUT 链存在 DROP/REJECT 规则，若外网仍打不开请检查: iptables -L INPUT -n --line-numbers"
    fi

    # 结论
    echo ""
    if [ ${problems} -eq 0 ]; then
        print_success "诊断结论：服务器侧一切正常。若浏览器仍打不开，问题在客户端侧："
        echo "    1) 浏览器请手动输入完整地址（含 http:// 前缀，勿让浏览器自动跳 https）"
        echo "    2) 本机代理/VPN（Clash 等）请给服务器 IP 加直连规则，或换手机流量验证"
        echo "    3) 云服务器还需检查厂商安全组是否放行 ${DEFAULT_PORT}"
    else
        print_error "诊断结论：发现 ${problems} 个问题，按上面标 ✗ 的提示逐项处理即可"
    fi
    return 0
}

# ============================================================================
# 交互菜单
# ============================================================================

show_menu() {
    echo ""
    echo -e "${BLUE}╔══════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║${NC}   AI视觉术语库 · 运维菜单   (监听 ${API_HOST}:${DEFAULT_PORT})"
    echo -e "${BLUE}╚══════════════════════════════════════════════════╝${NC}"
    echo -e "  ${CYAN}1${NC}) 一键部署   （首次用这个：环境+依赖+建库+启动+自检）"
    echo -e "  ${CYAN}2${NC}) 启动服务"
    echo -e "  ${CYAN}3${NC}) 停止服务"
    echo -e "  ${CYAN}4${NC}) 重启服务"
    echo -e "  ${CYAN}5${NC}) 服务状态"
    echo -e "  ${CYAN}6${NC}) 一键诊断   （打不开就点这个，自动查原因）"
    echo -e "  ${CYAN}7${NC}) 重建知识库 （改了 CSV / 拉取代码后执行）"
    echo -e "  ${CYAN}8${NC}) 拉取更新   （git pull + 重建 + 重启）"
    echo -e "  ${CYAN}9${NC}) 查看日志"
    echo -e " ${CYAN}10${NC}) 构建前端   （需要 Node，一般不用）"
    echo -e " ${CYAN}11${NC}) 数据校验"
    echo -e " ${CYAN}12${NC}) 搜索术语"
    echo -e "  ${CYAN}0${NC}) 退出"
    echo ""
}

menu_loop() {
    while true; do
        show_menu
        local choice
        read -rp "请选择 [0-12]: " choice || exit 0
        echo ""
        case "${choice}" in
            1)  deploy_all ;;
            2)  start_server ;;
            3)  stop_server ;;
            4)  restart_server ;;
            5)  get_status ;;
            6)  run_doctor ;;
            7)  setup_venv && install_dependencies && build_kb ;;
            8)  setup_venv && install_dependencies && update_project ;;
            9)  show_logs ;;
            10) build_frontend ;;
            11) setup_venv && install_dependencies && validate_kb ;;
            12) read -rp "关键词: " kw && setup_venv && search_terms "${kw}" ;;
            0|q|Q) echo "再见"; exit 0 ;;
            *)  print_error "无效选择: ${choice}" ;;
        esac
        echo ""
        read -rp "—— 按回车返回菜单 ——" _ || exit 0
    done
}

# ============================================================================
# 帮助与入口
# ============================================================================

show_help() {
    cat << EOF

AI视觉设计与提示词工程百科 —— 运维脚本

交互模式（推荐）:
  ./manage.sh                直接运行进入数字菜单，按 1/2/3 选择

命令模式（自动化/cron 用）:
  ./manage.sh deploy         一键部署（环境+依赖+建库+启动+自检）
  ./manage.sh start [port]   启动服务（后台运行）
  ./manage.sh stop           停止服务
  ./manage.sh restart [port] 重启服务
  ./manage.sh status         查看状态
  ./manage.sh doctor         一键诊断（打不开先跑这个）
  ./manage.sh build          重建知识库
  ./manage.sh update         git pull + 重建 + 重启（cron 定时更新用）
  ./manage.sh logs [行数]    查看日志
  ./manage.sh frontend       构建前端（需 Node）
  ./manage.sh validate       数据校验
  ./manage.sh search <词>    命令行搜索
  ./manage.sh setup          仅初始化环境+建库（deploy 的不启动版）

环境变量:
  API_HOST=127.0.0.1 ./manage.sh restart   # 只允许本机+反向代理访问
  API_PORT=9000 ./manage.sh start          # 换端口

定时自动更新（crontab -e 添加）:
  0 4 * * * cd $(pwd) && ./manage.sh update >> logs/update.log 2>&1

EOF
}

main() {
    if [ ! -d "${PROJECT_ROOT}/scripts" ]; then
        print_error "请在项目根目录执行此脚本"
        exit 1
    fi

    # 无参数 + 交互终端 → 菜单模式
    if [ $# -eq 0 ]; then
        if [ -t 0 ]; then
            menu_loop
        else
            show_help
        fi
        exit 0
    fi

    local command="$1"; shift || true
    case "${command}" in
        1|deploy)        deploy_all ;;
        2|start)         start_server "$@" ;;
        3|stop)          stop_server ;;
        4|restart)       restart_server "$@" ;;
        5|status)        get_status ;;
        6|doctor)        run_doctor ;;
        7|build)         setup_venv && install_dependencies && build_kb ;;
        8|update)        setup_venv && install_dependencies && update_project ;;
        9|logs)          show_logs "$@" ;;
        10|frontend)     build_frontend ;;
        11|validate)     setup_venv && install_dependencies && validate_kb ;;
        12|search)       setup_venv && search_terms "$@" ;;
        setup)           check_prerequisites && setup_venv && install_dependencies && build_kb \
                         && print_success "初始化完成！执行 './manage.sh start' 启动服务" ;;
        help|--help|-h)  show_help ;;
        *)               print_error "未知命令: ${command}"; show_help; exit 1 ;;
    esac
    exit $?
}

main "$@"
