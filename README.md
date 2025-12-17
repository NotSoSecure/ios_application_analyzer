# iOS Application Analyzer

The tool is used to analyze the content of the iOS application in local storage.
 <br /> <br />
- Install and run the application in virutal environment
```
python -m venv ios_application_analyzer
ios_application_analyzer\Scripts\activate
pip install -r requirement.txt
python main.py
```

##### Note: For the performance it is highly recommend to connect device  using USB and  SSH over USB using iproxy or equivalent tools
	- Windows: https://github.com/L1ghtmann/libimobiledevice/releases/
		- `iproxy.exe 22 2222`
	- Linux: sudo apt install usbmuxd libimobiledevice-utils
		- `iproxy 22 2222`
	- Mac OS: brew install libimobiledevice
		- `iproxy 22 2222`

# Tool Usage
Run iproxy tool to connect iPhone device over USB as shown in Figure:
![Usage](Usage/1.png)
<br /> <br />
It will ask for SSH Credential to connect the phone as shown in Figure:
![Usage](Usage/2.png)
<br /> <br />

# Future Enhancement
- [ ] Disply iPhone Logs to analyze the logs of the application

# References
- https://iphonedevwiki.net/index.php/SSH_Over_USB
- https://gist.github.com/johnfink8/2190472
- http://damnvulnerableiosapp.com/?paiddownloads_id=11#downloads
- https://github.com/ptoomey3/Keychain-Dumper
