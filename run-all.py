import os
import glob
import sumbasic

for method in sumbasic.METHODS:
    for i in range(1,5):
        for f in glob.glob("./docs/doc{0}-*.txt".format(i)):
            os.system('py sumbasic.py {2} {0} > {2}-{1}.txt'.format(f, i, method))
