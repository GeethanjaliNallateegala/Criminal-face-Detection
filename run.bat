@echo off
echo ========================================
echo   Criminal Face Detection
echo   Hybrid Java + Python Version
echo   99% Accuracy Face Recognition
echo ========================================
echo.
cd /d D:\CriminalFaceDetectionHybrid
mvn compile exec:java -Djava.library.path="C:\OpenCV\opencv\build\java\x64"
pause
