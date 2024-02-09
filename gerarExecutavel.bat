pyinstaller --onefile --icon=./storage/img/irvtbot.png login.py
xcopy /s /i /e /q /y .\storage .\dist\storage\
xcopy /y .\useragents.txt .\dist\
