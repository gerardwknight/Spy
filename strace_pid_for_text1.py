import subprocess
import re
import sys

def format_hex_ascii_line(line):
    match = re.search(r'(?P<prefix>.*)(".*?")(?P<suffix>.*)', line)
    if match:
        prefix = match.group('prefix')
        suffix = match.group('suffix')
        hex_values = re.findall(r'\\x([0-9a-fA-F]{2})', match.group(2))
        ascii_values = [chr(int(h, 16)) if 32 <= int(h, 16) <= 126 else '.' for h in hex_values]
        formatted_hex = ' '.join(hex_values)
        formatted_ascii = ''.join(ascii_values)
        formatted_line = '{}"{}"{}'.format(prefix, formatted_hex, suffix)
        #print(formatted_line)
        print('{}   {}'.format(formatted_hex, formatted_ascii))

def monitor_process_output(pid, grep_pattern):
    process = subprocess.Popen(['strace', '-p', str(pid), '-s', '4096','-Tf', '-x', '-e', 'trace=open,read,write', '-y'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    while True:
        line = process.stdout.readline().strip()
        if not line:
            break
        if re.search(grep_pattern, line):
            print(line + '\n\n')
            format_hex_ascii_line(line)

    process.wait()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: python script.py <PID> <grep_pattern>')
        sys.exit(1)

    pid = int(sys.argv[1])
    grep_pattern = sys.argv[2]

    monitor_process_output(pid, grep_pattern)


