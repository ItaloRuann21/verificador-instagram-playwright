pyinstaller --noconsole --onefile --icon=./storage/img/irvtbot.png interface_login.py
xcopy /s /i /e /q /y .\storage .\dist\storage\
xcopy /y .\useragents.txt .\dist\
