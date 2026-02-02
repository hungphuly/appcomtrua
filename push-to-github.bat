@echo off
echo Dang push code len GitHub...
echo.

REM Thay [username] bang username GitHub cua ban
set /p username="Nhap username GitHub cua ban: "

git add .
git commit -m "App com trua - diem danh hang ngay"
git branch -M main
git remote add origin https://github.com/%username%/appcomtrua.git
git push -u origin main

echo.
echo XONG! Vao https://github.com/%username%/appcomtrua/actions de xem qua trinh build
pause
