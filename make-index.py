""" Build index from directory listing

make_index.py [--directory </path/to/directory> --header <header text>]
"""

INDEX_TEMPLATE = r"""
<html>
<body>
<h2>${header} <a href="${link}" style="font-size:20px">  ⬇️ </a></h2>
<ul>
% for name in names:
    <li><a href="${name}">${name}</a></li>
% endfor
</ul>
</body>
</html>
"""
# TODO: agregar la fecha de ultima modificacion en cada index.md
EXCLUDED = ('index.html', 'index.md', '_site', '_config.yml', 'Gemfile', 'Gemfile.lock', 'README.md', 'make-index.py', '.', 'Util', 'subir-apuntes.md', 'descargar-apuntes.md', 'favicon.ico')

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
        link=subdir.replace(rootdir, "")
        link="https://downgit.github.io/#/home?url=https://github.com/Apuntes-FIUBA/Apuntes-Electronica/tree/main"+link
        newHTML=Template(INDEX_TEMPLATE).render(names=fnames, header=header, link=link)

        # TODO: que no vuelva a editar los que no cambiaron
        # ignorar el primer index.md
        if not os.path.exists(subdir+'/index.md'):
            with open(subdir+'/index.md', 'a') as f:
                print("CREANDO "+subdir+'/index.md')
                f.write(newHTML)
                f.write('<br><br><br><br><br><a href="../" style="float: left">(Volver)</a> <a href="https://apuntes-fiuba.github.io/Apuntes-Electronica" style="float: right">(Página Principal)</a>\n')
        else:
            with open(subdir+'/index.md', 'r') as f:
                data = f.readlines()
            with open(subdir+'/index.md', 'w') as f:
                f.seek(0)
                f.write(newHTML)    # Estaria bueno que lo inserte donde esta el otro bloque y no siempre al principio
                for line in data:
                    if not '<' in line : 
                        f.write(line)
                f.write('<br><br><br><br><br><a href="../" style="float: left">(Volver)</a> <a href="https://apuntes-fiuba.github.io/Apuntes-Electronica" style="float: right">(Página Principal)</a>\n')
        f.close()
if __name__ == '__main__':
    main()
