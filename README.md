## Backburner 

**Make sure to only scan websites and IPs you are authorized to scan.**
___

### What's New :
- **Scanning Modes** : Introduced Ghost, Normal, and Stealth scan modes with customizable configurations to suit different scanning needs.
- **Improved Docker support** : Seamless integration in containerized environments for simple deployment.
- **Optimized performance** : Faster scanning, particularly for larger port ranges, thanks to improved multithreading.
- **Color coded Output** : Improved color identification of open and closed ports with dynamic color coding.

### Enhancements :
- **Clean terminal output** : Results are now more readable with better formatting.
- **Multithreaded scanning** : Faster scanning of multiple ports for improved efficiency.

___

### How to run Backburner :
1. **Run the following Docker command (terminal/linux)** to start the tool :
   - `docker run -it klyxen/backburner:v4.7` 
   
2. **Enter the target IP or website** when prompted. `(e.g., scanme.nmap.org)`

3. **View your results** : The scan will display open and closed ports along with service names and descriptions.

### Example :
```
docker run -it klyxen/backburner:v4.7
Then, type the target (e.g., scanme.nmap.org) and see the results displayed in a color-coded format.
```
### Output
```

   _--____-__---____---______----____-___-_____-____-----___`.
    ╔════════════════════════════╗
          BACKBURNER
    ╚════════════════════════════╝          `               `
    created by : Klyxen           ' '         '            '
    )(  )  ()   )    (     )(     (   )    (    )   (  (    ))
      )(   )(  (      )   (  )     ) (      )  (     )  )  ((
     (  ) (  )  )    )     ))     (  )     (    )   )  )   ))
    [   q : quit   |   m : modes   | -------------------------


    
Enter Target [ domain : IP ] : scanme.nmap.org
[+] Resolved scanme.nmap.org to 45.33.32.156
[*] Scanning 68 ports for 45.33.32.156 in normal mode
[+] Port 22 (SSH) is open - potentially vulnerable - SSH-2.0-OpenSSH_6.6.1p1 Ubuntu-2ubuntu2.13
[+] Port 80 (HTTP) is open - potentially vulnerable - HTTP/1.1 200 OK
Date: Fri, 09 May 2025 06:28:05 GMT
Server: Apache/2.4.7 (Ubuntu)
Accept-Ranges: 
[*] Scanned 20/68 ports
[*] Scanned 40/68 ports
[*] Scanned 60/68 ports
[*] Scanned 68/68 ports

Scan results for scanme.nmap.org:
[ OPEN ] : 22 | SSH | Banner: SSH-2.0-OpenSSH_6.6.1p1 Ubuntu-2ubuntu2.13
[ OPEN ] : 80 | HTTP | Banner: HTTP/1.1 200 OK
Date: Fri, 09 May 2025 06:28:05 GMT
Server: Apache/2.4.7 (Ubuntu)
Accept-Ranges: 

[+] Scan completed for scanme.nmap.org

Enter Target [ domain : IP ] : 
```
___

### How to Select Modes
1. **Syntax** : simply just type `m` in your terminal and choose the mode you want.

```
Modes : 
[ 0 ] : Ghost scan
[ 1 ] : Stealth scan
[ 2 ] : Normal scan
: 
```

___


### Tags to use [ old/new ]

- `v4.7`
- `v3.0`
- `v2.9`
- `v1.0`

Example : `docker run -it klyxenn/backburner:v1.0`

___





