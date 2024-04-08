@echo off
rem Tắt hiển thị thông báo trong quá trình chạy lệnh

net session >nul 2>&1
rem Kiểm tra xem phiên làm việc có quyền quản trị không
rem Nếu không có, yêu cầu quyền quản trị và chạy lại file batch với quyền quản trị

if %errorLevel% neq 0 (
    echo Đang yêu cầu quyền quản trị...
    powershell -Command "Start-Process cmd -ArgumentList '/c %~0' -Verb runAs" >nul
    exit
)

rem Kiểm tra xem Python đã được cài đặt chưa
python --version >nul 2>&1
rem Nếu đã cài đặt, thông báo Python đã được cài đặt và kết thúc quá trình

if %errorLevel% equ 0 (
    echo Python đã được cài đặt.
    goto end
)

rem Kiểm tra xem Chocolatey đã được cài đặt chưa
where choco >nul 2>&1
rem Nếu chưa cài đặt, tiến hành cài đặt Chocolatey và thêm đường dẫn vào biến môi trường PATH

if %errorLevel% neq 0 (
    echo Đang cài đặt Chocolatey...
    powershell -NoProfile -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))"
    setx PATH "%PATH%;%ALLUSERSPROFILE%\chocolatey\bin" -m
)

rem Kiểm tra lại xem Chocolatey đã được cài đặt sau quá trình cài đặt
where choco >nul 2>&1
rem Nếu không thành công, thông báo lỗi và kết thúc quá trình

if %errorLevel% neq 0 (
    echo Không thể cài đặt Chocolatey.
    goto end
)

echo Đang cài đặt Python...
choco install python -y
rem Tiến hành cài đặt Python bằng Chocolatey

:end
exit
rem Kết thúc quá trình