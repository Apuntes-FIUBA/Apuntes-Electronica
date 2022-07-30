""" Build index from directory listing

make_index.py [--directory </path/to/directory> --header <header text>]
"""

INDEX_TEMPLATE = r"""
<html>
<body>
<h2>${header}</h2>
<ul>
% for name in names:
    <li><a href="${name}">${name}</a></li>
% endfor
</ul>
</body>
</html>
"""

EXCLUDED = ('index.html', 'index.md', '_site', '_config.yml', 'Gemfile', 'Gemfile.lock', 'README.md', 'make-index.py', '.', 'Util', 'subir-apuntes.md', 'descargar-apuntes.md')

import os
import argparse

# May need to do "pip install mako"
from mako.template import Template


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory")
    parser.add_argument("--header")
    args = parser.parse_args()
    rootdir=(args.directory if args.directory else os.getcwd())
   
    for subdir, dirs, files in os.walk(rootdir):
        dirs[:] = [d for d in dirs if not d.startswith(EXCLUDED)]
        fnames = [fname for fname in sorted(os.listdir(subdir))
            if fname not in EXCLUDED and (fname[0]!='.')]
        header = (args.header if args.header else os.path.basename(subdir))
        newHTML=Template(INDEX_TEMPLATE).render(names=fnames, header=header)
        if not os.path.exists(subdir+'/index.md'):
            with open(subdir+'/index.md', 'a') as f:
                print("CREAR"+subdir+'/index.md')
                f.write(newHTML)
                #f.write("[Descargar Todo](https://downgit.github.io/#/home?url=https://github.com/Apuntes-FIUBA/Apuntes-Electronica/tree/main/)\n")
        else:
            with open(subdir+'/index.md', 'r') as f:
                data = f.readlines()
            with open(subdir+'/index.md', 'w') as f:
                f.seek(0)
                f.write(newHTML)
                for line in data:
                    if not '<' in line : 
                        f.write(line)
        f.close()
if __name__ == '__main__':
    main()