import sys
import os
import re

def search(pattern, string):
    try:
        re.search(pattern, string).group(1)
        return True
    except (IndexError, AttributeError):
        return False

def print_result(print_header, header, print_lineno, lineno, print_line, line):
    result = ''
    if print_header:
        result += '%s' % header
    if print_lineno:
        if len(result) > 0:
            result += ':'
        result += '%d' % lineno
    if print_line:
        if len(result) > 0:
            result += ':'
        result += line
    sys.stdout.write('%s\n' % result.strip('\n'))

def grep_file(filename, pattern, print_headers, print_lineno, print_lines):
    with open(filename, 'r') as fd:
        for i, line in enumerate(fd.readlines()):
            found = search(pattern, line)
            if found:
                print_result(print_headers, filename, print_lineno, i, print_lines, line)
                if print_headers and not print_lines: # files-with-matches option
                    break

def grep_files(paths, pattern, recursive, print_headers=True, print_lineno=True, print_line=True):
    for path in paths:
        if os.path.isfile(path):
            if path.endswith(".py"):
                grep_file(path, pattern, print_headers, print_lineno, print_line)

        elif os.path.isdir(path):
            if recursive:
                more_paths = [os.path.join(path, child) for child in os.listdir(path)]
                grep_files(more_paths, pattern, recursive, print_headers, print_lineno, print_line)
            else:
                sys.stdout.write('grep: %s: Is a directory\n' % file_)
