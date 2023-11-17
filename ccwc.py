import argparse
import sys

def try_catch_wrapper(factory):
    try:
        return factory(), True
    except FileNotFoundError as e:
        print(f'ccwc: {e.filename}: No such file or directory')
    except Exception as e:
        print(f'Unknown error: {e}')
    return None, False

def count_bytes(file_path):
    with open(file_path, 'rb') as file:
        bytes = len(file.read())
        return bytes

def count_lines(file_path):
    with open(file_path, 'rb') as file:
        for count, _ in enumerate(file):
            pass
        return count + 1

def count_words(file_path):
    with open(file_path, 'rb') as file:
        words = len(file.read().split())
        return words

def count_chars(file_path):
    with open(file_path, 'rb') as file:
        chars = len(file.read().decode())
        return chars

def print_result(files, metadatas, filenames):
    total_c, total_l, total_w, total_m = 0, 0, 0, 0

    for file in files:
        str_result = ''
        if f'c#{file}' in metadatas and filenames[f'c#{file}'] == file:
            bytes = metadatas[f'c#{file}']
            str_result += f'{bytes} '
            total_c += bytes

        if f'l#{file}' in metadatas and filenames[f'l#{file}'] == file:
            count = metadatas[f'l#{file}']
            str_result += f'{count} '
            total_l += count

        if f'w#{file}' in metadatas and filenames[f'w#{file}'] == file:
            words = metadatas[f'w#{file}']
            str_result += f'{words} '
            total_w += words
        
        if f'm#{file}' in metadatas and filenames[f'm#{file}'] == file:
            chars = metadatas[f'm#{file}']
            str_result += f'{chars} '
            total_m += chars

        print(str_result + file)
    
    if len(files) > 1:
        str_c = f'{total_c} ' if total_c > 0 else ''
        str_l = f'{total_l} ' if total_l > 0 else ''
        str_w = f'{total_w } ' if total_w > 0 else ''
        str_m = f'{total_m} ' if total_m > 0 else ''

        print(str_c + str_l + str_w + str_m + 'total') 

def handle_standard_input(content: str, args):
    str_result = ''
    if '-c' in args or not args:
        bytes = content.encode()
        str_result += f'{len(bytes)} '
    
    if '-l' in args or not args:
        lines = content.count('\n')
        str_result += f'{lines} '

    if '-w' in args or not args:
        str_result += f'{len(content.split())} '

    if '-m' in args:
        str_result += f'{len(content)}'

    print(str_result)

def handle_non_standard_input(args):
    filenames, metadatas = {}, {}

    if not args.c and not args.l and not args.w and not args.m and args.file_paths:
        args.c, args.l, args.w = args.file_paths, args.file_paths, args.file_paths

    if args.c:
        for c in args.c:
            bytes, ok = try_catch_wrapper(lambda: count_bytes(c))
            if ok:
                metadatas[f'c#{c}'], filenames[f'c#{c}'] = bytes, c

    if args.l:
        for l in args.l:
            count, ok = try_catch_wrapper(lambda: count_lines(l))
            if ok:
                metadatas[f'l#{l}'], filenames[f'l#{l}'] = count, l
    
    if args.w:
        for w in args.w:
            words, ok = try_catch_wrapper(lambda: count_words(w))
            if ok:
                metadatas[f'w#{w}'], filenames[f'w#{w}'] = words, w

    if args.m:
        for m in args.m:
            chars, ok = try_catch_wrapper(lambda: count_chars(m))
            if ok:
                metadatas[f'm#{m}'], filenames[f'm#{m}'] = chars, m

    files = list(set(filenames.values()))

    print_result(files, metadatas, filenames)

def main():
    parser = argparse.ArgumentParser(description='WC Tool.')

    parser.add_argument('file_paths', metavar='F', type=str, nargs='*', default=[], help='File paths')
    parser.add_argument('-c', help='outputs the number of bytes in a file', action='extend', default=[], nargs='*')
    parser.add_argument('-l', help='outputs the number of lines in a file', action='extend', default=[], nargs='*')
    parser.add_argument('-w', help='outputs the number of words in a file', action='extend', default=[], nargs='*')
    parser.add_argument('-m', help='outputs the number of characters in a file', action='extend', default=[], nargs='*')

    args = parser.parse_args()

    if sys.stdin.isatty(): 
        handle_non_standard_input(args)
    elif not sys.stdin.isatty():
        file_content = b''.join(sys.stdin.buffer.readlines()).decode()
        sys_args = sys.argv[1:]
        handle_standard_input(file_content, sys_args)
    

if __name__ == '__main__':
    main()