pyinstaller --noconsole --onefile --icon=./storage/img/irvtbot.png interface_login.py
xcopy /s /i /e /q /y .\relatorios .\dist\relatorios\
xcopy /s /i /e /q /y .\storage .\dist\storage\
xcopy /s /i /e /q /y .\logs .\dist\logs\
xcopy /y .\useragents.txt .\dist\
