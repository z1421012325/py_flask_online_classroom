import re
import sys
from gunicorn.app.wsgiapp import run
if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script/.pyw|/.exe)?$','',sys.argv[0])
    sys.exit(run())
	
// python 该文件.py -w 4 -b 127.0.0.1:9001 run:app 