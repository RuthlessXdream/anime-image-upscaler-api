#!/bin/bash

# 动漫图片高清修复API启动脚本
# 简化版本，专注于基本功能

set -e

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

echo "🎨 动漫图片高清修复API启动脚本"
echo "================================"

# 检查Python环境
check_environment() {
    log_info "检查运行环境..."
    
    # 检查Python版本
    if ! command -v python3 &> /dev/null; then
        log_error "Python3未安装"
        exit 1
    fi
    
    python_version=$(python3 --version | cut -d' ' -f2)
    log_info "Python版本: $python_version"
    
    # 检查虚拟环境
    if [[ "$VIRTUAL_ENV" != "" ]]; then
        log_success "运行在虚拟环境中: $VIRTUAL_ENV"
    else
        log_warning "未检测到虚拟环境，建议使用虚拟环境"
    fi
    
    # 检查GPU支持
    if command -v nvidia-smi &> /dev/null; then
        log_success "检测到NVIDIA GPU"
        nvidia-smi --query-gpu=name,memory.total --format=csv,noheader,nounits | head -1
    else
        log_warning "未检测到NVIDIA GPU，将使用CPU模式"
    fi
}

# 安装依赖
install_dependencies() {
    log_info "检查和安装依赖..."
    
    if [ ! -f "requirements.txt" ]; then
        log_error "requirements.txt文件不存在"
        exit 1
    fi
    
    # 检查是否需要安装依赖
    if python3 -c "import fastapi, torch, cv2" 2>/dev/null; then
        log_success "主要依赖已安装"
    else
        log_info "安装Python依赖..."
        pip install -r requirements.txt
    fi
    
    # 检查Real-ESRGAN安装 - 更智能的检测
    if python3 -c "import realesrgan" 2>/dev/null; then
        log_success "Real-ESRGAN已安装，跳过重复安装"
    else
        if [ -d "Real-ESRGAN" ]; then
            log_info "安装Real-ESRGAN..."
            cd Real-ESRGAN
            pip install -e . --quiet
            cd ..
            log_success "Real-ESRGAN安装完成"
        else
            log_error "Real-ESRGAN目录不存在"
            exit 1
        fi
    fi
}

# 检查模型文件
check_models() {
    log_info "检查模型文件..."
    
    model_dir="Real-ESRGAN/weights"
    model_file="$model_dir/RealESRGAN_x4plus_anime_6B.pth"
    
    if [ ! -d "$model_dir" ]; then
        mkdir -p "$model_dir"
    fi
    
    if [ ! -f "$model_file" ]; then
        log_warning "模型文件不存在，正在下载..."
        wget -O "$model_file" "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth" || {
            log_error "模型下载失败"
            exit 1
        }
    fi
    
    log_success "模型文件检查完成"
}

# 创建必要目录
create_directories() {
    log_info "创建必要目录..."
    
    mkdir -p uploads outputs logs
    
    log_success "目录创建完成"
}

# 启动服务
start_service() {
    log_info "启动API服务..."
    
    if [ ! -f "start_modern.py" ]; then
        log_error "启动脚本start_modern.py不存在"
        exit 1
    fi
    
    # 安装net-tools以支持netstat命令
    if ! command -v netstat &> /dev/null; then
        log_info "安装网络工具..."
        apt-get update -qq && apt-get install -y -qq net-tools
    fi
    
    # 检查端口是否被占用 - 修复配置文件字段名
    port=$(grep -o 'PORT=.*' config.env 2>/dev/null | cut -d'=' -f2 || echo "3005")
    if netstat -tuln 2>/dev/null | grep -q ":$port "; then
        log_warning "端口 $port 已被占用"
        log_info "请修改config.env中的PORT配置"
    fi
    
    log_success "启动服务..."
    echo
    echo "🌐 服务将在以下地址启动:"
    echo "   - API服务: http://localhost:$port"
    echo "   - API文档: http://localhost:$port/docs"
    echo "   - 健康检查: http://localhost:$port/health"
    echo
    echo "按 Ctrl+C 停止服务"
    echo "================================"
    
    python3 start_modern.py
}

# 主函数
main() {
    case "${1:-all}" in
        "check")
            check_environment
            ;;
        "install")
            install_dependencies
            ;;
        "models")
            check_models
            ;;
        "start")
            start_service
            ;;
        "quick")
            log_info "快速启动模式（跳过环境检查）"
            start_service
            ;;
        "all")
            check_environment
            install_dependencies
            check_models
            create_directories
            start_service
            ;;
        *)
            echo "用法: $0 {check|install|models|start|quick|all}"
            echo "  check   - 检查运行环境"
            echo "  install - 安装依赖"
            echo "  models  - 检查/下载模型文件"
            echo "  start   - 启动服务"
            echo "  quick   - 快速启动（跳过检查）"
            echo "  all     - 执行所有步骤 (默认)"
            echo ""
            echo "💡 如果环境已经配置好，推荐使用："
            echo "   $0 quick"
            exit 1
            ;;
    esac
}

# 执行主函数
main "$@" 