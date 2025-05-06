## Backburner

**Make sure to only scan websites and IPs you are authorized to scan.**
___

### What's New:
- **Color-coded output** : Easily identify open and closed ports with green and red colors.
- **Improved Docker support** : Seamless integration in containerized environments for simple deployment.
- **Optimized performance** : Faster scanning, particularly for larger port ranges, thanks to improved multithreading.

### Enhancements :
- **Clean terminal output** : Results are now more readable with better formatting.
- **Multithreaded scanning** : Faster scanning of multiple ports for improved efficiency.

___
### How to Use:
1. **Run the following Docker command (terminal/linux)** to start the tool :
   - `docker run -it klyxen/backburner:v2.7` 
   
2. **Enter the target IP or website** when prompted. `(e.g., scanme.nmap.org)`

3. **View your results** : The scan will display open and closed ports along with service names and descriptions.

### Example :
```
docker run -it klyxen/backburner:v2.3
Then, type the target (e.g., scanme.nmap.org) and see the results displayed in a color-coded format.
```
### Output
```

    _--____-__---____---______----____-___-_____-____-----___`.
    ╔════════════════════════════╗
          BACKBURNER
    ╚════════════════════════════╝
    created bt : Ky1e/Klyxen

    --__----_--___----___------____---_---_-----_----_____---`.

Enter target (domain or IP, or 'q' to quit): scanme.nmap.org
[+] Resolved scanme.nmap.org to 45.33.32.156
[*] Scanning 68 ports for 45.33.32.156 in normal mode
[+] Port 21 (FTP) is open - HIGHLY vulnerable
[+] Port 22 (SSH) is open - potentially vulnerable
[+] Port 80 (HTTP) is open - potentially vulnerable - HTTP/1.1 200 OK
Date: Mon, 05 May 2025 10:21:59 GMT
Server: Apache/2.4.7 (Ubuntu)
Accept-Ranges:
[*] Scanned 20/68 ports
[*] Scanned 40/68 ports
[*] Scanned 60/68 ports
[*] Scanned 68/68 ports

Scan results for scanme.nmap.org:
[ OPEN ] : 21 | FTP
[ OPEN ] : 22 | SSH
[ OPEN ] : 80 | HTTP | Banner: HTTP/1.1 200 OK
Date: Mon, 05 May 2025 10:21:59 GMT
Server: Apache/2.4.7 (Ubuntu)
Accept-Ranges:

[+] Scan completed for scanme.nmap.org
```
___
