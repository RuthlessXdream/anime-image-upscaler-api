@echo off
echo 🔥 配置Windows防火墙允许端口8000访问
echo ================================================

:: 检查管理员权限
net session >nul 2>&1
if %errorLevel% == 0 (
    echo ✅ 检测到管理员权限
) else (
    echo ❌ 需要管理员权限才能配置防火墙
    echo 💡 请右键点击此文件，选择"以管理员身份运行"
    pause
    exit /b 1
)

echo.
echo 🔧 正在添加防火墙入站规则...

:: 删除可能存在的旧规则
netsh advfirewall firewall delete rule name="动漫图片高清修复API" >nul 2>&1

:: 添加新的入站规则
netsh advfirewall firewall add rule name="动漫图片高清修复API" dir=in action=allow protocol=TCP localport=8000

if %errorLevel% == 0 (
    echo ✅ 防火墙规则添加成功！
    echo 📡 端口8000现在允许外部访问
    echo.
    echo 🌐 局域网设备现在可以访问API服务
    echo 💡 确保API服务正在运行在0.0.0.0:8000
) else (
    echo ❌ 防火墙规则添加失败
    echo 💡 请手动配置防火墙或检查权限
)

echo.
echo 📋 手动配置步骤：
echo 1. 打开"控制面板" -> "系统和安全" -> "Windows Defender防火墙"
echo 2. 点击"高级设置"
echo 3. 选择"入站规则" -> "新建规则"
echo 4. 选择"端口" -> "TCP" -> "特定本地端口" -> 输入"8000"
echo 5. 选择"允许连接" -> 完成设置

echo.
pause 