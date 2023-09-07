import psutil

def find_chrome_remote_debugging_port():
    for proc in psutil.process_iter(attrs=['pid', 'name', 'cmdline']):
        if 'chrome' in proc.info['name'].lower() and '--remote-debugging-port' in proc.info['cmdline']:
            for arg in proc.info['cmdline']:
                if arg.startswith('--remote-debugging-port='):
                    port = int(arg.split('=')[1])
                    return port
    return None

remote_debugging_port = find_chrome_remote_debugging_port()
if remote_debugging_port is None:
    print("No running Chrome instance with remote debugging found.")
else:
    print(f"Found Chrome remote debugging port: {remote_debugging_port}")
