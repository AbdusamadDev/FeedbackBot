import os
import time

count = 0
while True:
    os.system("git add --all")
    inp = input("Git commit message >>>")
    os.system('git commit -m "{}"')
    count += 1
    os.system("git push -u origin main")
    time.sleep(60 * 5)

