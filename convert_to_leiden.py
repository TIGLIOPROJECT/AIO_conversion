import os
import sys
from leiden_plus import to_leiden_plus

from_dir = sys.argv[1]
to_dir = sys.argv[2]

for in_file_name in os.listdir(from_dir):
    with open(os.path.join(from_dir, in_file_name), 'r') as in_file:
        text = in_file.read()

    leiden = to_leiden_plus(text)
    
    with open(os.path.join(to_dir, in_file_name), 'w') as out_file:
        out_file.write(leiden)
    
