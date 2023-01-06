from os.path import exists, normpath
import hashlib
import argparse
from yaml import load

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def get_hash(f_path, method='sha1', mode='bin'):
    h = hashlib.new(method)

    if mode == 'txt':
        with open(f_path, 'rt') as file:
            data = file.read()
        h.update(data.encode('utf-8'))
    else:
        with open(f_path, 'rb') as file:
            data = file.read()
        h.update(data)
    digest = h.hexdigest()
    return digest

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Check the target directory.')
    parser.add_argument('dir', type=str, help='the directory to check')
    args = parser.parse_args()

    args.dir = normpath(args.dir)

    checkfile = args.dir + '/.expected'
    if not exists(checkfile):
        print("Error: a mandatory file is missing and this script can't work.")
        exit()

    all_digests = []
    digest = get_hash(checkfile)
    all_digests.append(digest)

    with open(checkfile, 'rt') as stream:
        data = load(stream, Loader=Loader)
        for d in data:
            if exists(d):
                digest = get_hash(d, mode=d[-3:])
                print(digest, d)
                all_digests.append(digest)

    h = hashlib.new('sha1')
    h.update(''.join(all_digests).encode('utf-8'))
    digest = h.hexdigest()
    print("Final result:", digest)

