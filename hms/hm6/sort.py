from pathlib import Path
import sys
import shutil
import string
from pprint import pprint

GROUPS = {
    'images': ('JPEG', 'PNG', 'JPG', 'SVG'),
    'video': ('AVI', 'MP4', 'MOV', 'MKV'),
    'documents': ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'),
    'audio': ('MP3', 'OGG', 'WAV', 'AMR'),
    'archives': ('ZIP', 'GZ', 'TAR')
}

FILES = {
    'images': {},
    'video': {},
    'documents': {},
    'audio': {},
    'archives': {},
    'unknown':{} 
}

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

TRANS = {}
for c, t in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c.upper())] = t.upper()
    TRANS[ord(c)] = t

def normilize(s, is_file=True):
    group = None
    is_in_group = None
    if is_file:
        group = 'unknown'
        is_in_group = False
        for key, val in GROUPS.items():
            for ext in val:
                if s.split('.')[-1] == ext.lower():
                    is_in_group = True
                    group = key
                    
                
        if not is_in_group:
            return s, is_in_group, group
    
    
    s = s.translate(TRANS)
    new_s = ''
    for i in s:
        if not (i in (string.ascii_letters + string.digits+'.')):
            new_s+='_'
        else:
            new_s+=i

    return new_s, is_in_group, group


def sort(path, groups_paths):
    path_obj = Path(path)
    if not (path_obj.exists() or path_obj.is_dir()):
        print('ERROR:', path, 'does not exists')
        return
    
    
    for i in path_obj.iterdir():
        dir = Path(home_dir)
        if i.is_file():
            norm, is_in_group, group = normilize(i.name) # asd.jpg
            
            test =  list(i.parts)
            dir = list(dir.parts)
            new_test = []
            for t in test[len(dir):-1]:
                if group != 'unknown':
                    new_test.append(normilize(t, is_file=False)[0])
                else:
                    new_test.append(t)
            if group == 'unknown':
                res = Path(*dir).joinpath(Path(*new_test).joinpath(norm))
            else:
                res = Path(*dir).joinpath(Path(group).joinpath(Path(*new_test).joinpath(norm)))
                
            FILES[group][str(i)] = str(res)

        
        if i.is_dir():
            sort(str(i), groups_paths)
            

def copy():
    for i in FILES:
        if i == 'archives':
            for key, val in FILES[i].items():
                filename_ext = val.split('\\')
                t = filename_ext[:-1]
                path = Path('\\'.join(t))
                if not path.exists():
                    path.mkdir(parents=True, exist_ok=True)
                
                shutil.unpack_archive(key, str(path)+'\\'+filename_ext[-1].split('.')[0], filename_ext[-1].split('.')[-1])
            continue
        if i != 'unknown':
            for key, val in FILES[i].items():
                t = val.split('\\')[:-1]
                path = Path('\\'.join(t))
                if not path.exists():
                    path.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(key, val)




# a = Path('D:\\Uni\\UNI\\4 course\\VII semester\\МОС')


'''
how to use example:

py sort.py "D:\Uni\UNI\4 course\VII semester\МОС"
python sort.py "D:\Uni\UNI\4 course\VII semester\МОС"
'''
if __name__ == '__main__':
    if len(sys.argv)>=2:
        path = sys.argv[1]
        print(path)
        groups_paths = [Path(path).joinpath(i) for i in GROUPS]

        for i in groups_paths:
            if not(i.exists()):
                i.mkdir()

        home_dir = path
        sort(home_dir, groups_paths)
        # pprint(FILES)
        copy()
        
        
    else:
        print('ERROR: path missing')