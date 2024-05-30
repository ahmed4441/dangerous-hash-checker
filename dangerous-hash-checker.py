import os
import zipfile
import patoolib # type: ignore
from pyunpack import Archive
import hashlib

file_path_mal_hashes = str(input('enter the mal-hashes.txt path: '))
files_path = str(input('enter the directory path that contains all zipped files: '))

available_algorithms = hashlib.algorithms_available
hash_algorithms = sorted(available_algorithms)

mal_hashes = []
def check_lines(files_path):
    with open(files_path, 'r') as file:
        for line in file:
            line = line.replace('(Mal)',"")
            line = line.replace('-',"")
            line = line.strip()
            mal_hashes.append(line)
check_lines(file_path_mal_hashes)
#print(mal_hashes)

def extract_files(files_path):
    for root, dirs, files in os.walk(files_path):
            for file in files:
                x = os.path.join(root, file)

                if x.endswith(('.zip')):
                    with zipfile.ZipFile(x, 'r') as zf:
                        zf.extractall(files_path)

                elif x.endswith(('.rar')):
                    try:
                        #Archive(x).extractall(files_path)
                        patoolib.extract_archive(x, outdir=files_path)
                    except:pass
extract_files(files_path)

files_to_check = []                
for root, dirs, files in os.walk(files_path):
        for file in files:
            f = os.path.join(root, file)
            if not f.endswith(('.rar', '.zip')):
                files_to_check.append(f)

#print(files_to_check)
hash_results = {}
def hash_file(file_path):
    with open(file_path, 'rb') as file:
        file_content = file.read()
    for algo in hash_algorithms:
        hash_calc = hashlib.new(algo)
        hash_calc.update(file_content)
        if algo.startswith('shake_'):
            hash_results[algo] = hash_calc.hexdigest(64)
        else:
            hash_results[algo] = hash_calc.hexdigest()
    hash_list=list(hash_results.values())
    for i in hash_list:
        for k in range(len(mal_hashes)):
            if i == mal_hashes[k]:
                print("MALWARE", file_path )
                break

for i in files_to_check:
    hash_file(i)



#print(hash_results)

