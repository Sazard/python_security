from socket import *
import datetime

# Scan for open port
def scan(devices):
    scan_result = {}
    for device in devices:
        ip = device[2]
        print("scanning IP: ", ip)
        # First one for hostname
        open_port = [device[0]]
        print ('Starting scan on host: ', ip)
    
        # Original 50-500
        for i in range(50, 150):
            s = socket(AF_INET, SOCK_STREAM)
            
            conn = s.connect_ex((ip, i))
            if(conn == 0) :
                open_port.append(i)
                print ('Port %d: OPEN' % (i,))
            s.close()
        scan_result[device[2][0]] = open_port
    return scan_result

# Create HTML report
def create_report(scan_result):
    now = datetime.datetime.now()
    report_file = 'network_scan_report_' + now.strftime("%Y-%m-%d_%H-%M-%S") + '.html'

    with open(report_file, 'w') as f:
        f.write('<html><body><h1>Network Scan Report</h1>\n')
        f.write('<p>Scan started at ' + now.strftime("%Y-%m-%d %H:%M:%S") + '</p>\n')
        f.write('<table>\n')
        f.write('<tr><th>IP Address</th><th>Hostname</th><th>Ports</th></tr>\n')
        
        for ip, ports in scan_result.items():
            f.write('<tr><td>' + str(ip) + '</td><td>' + str(ports[0]) + '</td><td>' + str(ports[1::]) + '</td></tr>\n')
        
        f.write('</table></body></html>')

    print('Scan complete. Report saved to ' + report_file)