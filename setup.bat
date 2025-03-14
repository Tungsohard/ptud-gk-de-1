@echo off
rem Script cai dat va chay Blog Ca Nhan voi Flask
title Cai dat Blog Ca Nhan

echo ======================================================
echo              CAI DAT BLOG CA NHAN
echo ======================================================

rem Kiem tra Python da duoc cai dat chua
echo [1/8] Kiem tra cai dat Python...
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [LOI] Python chua duoc cai dat. Vui long cai dat Python 3.7 tro len.
    exit /b 1
)

for /f "tokens=*" %%a in ('python --version') do set PYTHON_VERSION=%%a
echo [OK] %PYTHON_VERSION% da duoc cai dat.

rem Tao va kich hoat moi truong ao
echo.
echo [2/8] Tao moi truong ao Python...
if exist venv\ (
    echo Moi truong ao da ton tai. Su dung moi truong hien co.
) else (
    python -m venv venv
    if %ERRORLEVEL% NEQ 0 (
        echo [LOI] Khong the tao moi truong ao.
        exit /b 1
    )
    echo [OK] Da tao moi truong ao thanh cong.
)

rem Kich hoat moi truong ao
echo.
echo [3/8] Kich hoat moi truong ao...
call venv\Scripts\activate
if %ERRORLEVEL% NEQ 0 (
    echo [LOI] Khong the kich hoat moi truong ao.
    exit /b 1
)
echo [OK] Da kich hoat moi truong ao.

rem Nang cap pip
echo.
echo [4/8] Nang cap pip...
python -m pip install --upgrade pip
echo [OK] Da nang cap pip.

rem Cai dat cac thu vien can thiet
echo.
echo [5/8] Cai dat cac thu vien can thiet...
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo [LOI] Co loi khi cai dat thu vien.
    exit /b 1
)
echo [OK] Da cai dat thu vien thanh cong.

rem Tao thu muc uploads neu chua co
echo.
echo [6/8] Kiem tra va tao thu muc uploads...
if not exist static\uploads mkdir static\uploads
echo [OK] Da kiem tra thu muc uploads.

rem Cap nhat database va them cot role
echo.
echo [7/8] Cap nhat co so du lieu...
python update_roles.py
echo [OK] Da cap nhat co so du lieu.

rem Tao tai khoan admin
echo.
echo [8/8] Kiem tra va tao tai khoan admin...
python create_admin.py
echo [OK] Da kiem tra tai khoan admin.

rem Hien thi thong tin
echo.
echo ======================================================
echo          CAI DAT BLOG CA NHAN HOAN TAT
echo ======================================================
echo Thong tin tai khoan admin mac dinh:
echo   - Username: admin
echo   - Password: Admin@123
echo.
echo He thong phan quyen:
echo   - Viewer: Chi co the xem bai viet va binh luan
echo   - Collaborator: Co the tao va sua bai viet
echo   - Editor: Co the tao, sua va xoa bai viet
echo   - Admin: Co moi quyen tren he thong
echo.
echo De khoi dong ung dung, chay lenh:
echo   python app.py
echo Truy cap trang web tai:
echo   http://localhost:5000

rem Hoi nguoi dung co muon chay ung dung khong
set /p start_app="Ban co muon khoi dong Blog Ca Nhan ngay bay gio khong? (y/n): "
if /i "%start_app%"=="y" (
    echo.
    echo ======================================================
    echo             DANG KHOI DONG BLOG CA NHAN
    echo ======================================================
    echo Ung dung dang chay tai http://localhost:5000
    echo Nhan Ctrl+C de dung ung dung.
    echo.
    python app.py
) else (
    echo.
    echo Cai dat hoan tat. Chay 'python app.py' khi ban muon khoi dong ung dung.
    pause
)