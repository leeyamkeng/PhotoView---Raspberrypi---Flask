import os
from shutil import copyfile


os.system('sudo pkill -9 -f harpu.py')
copyfile('/home/pi/demo/demo.py', '/home/pi/harpu.py')
#time.sleep(2)
os.system('lxterminal -e python /home/pi/harpu.py')
demomessage = "Machine Now in Demo Mode"
print ("Done")
