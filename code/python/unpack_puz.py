import puz
import os

BASE_DIR = os.path.abspath('../../')
CODE_DIR = os.path.join(BASE_DIR,'code/python')
DATA_DIR = os.path.join(BASE_DIR,'data')
PUZ_DIR = os.path.join(DATA_DIR,'puz')

PUZ_FILES = [os.path.join(PUZ_DIR,_) for _ in os.listdir(PUZ_DIR)]

pf = PUZ_FILES[10]
p = puz.read(pf)

