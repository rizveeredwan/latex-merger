import os.path
import re


def removed_colored_texts(lines):
    track = []
    cnt = 0
    i = 0
    save = {}
    for i in range(0, len(lines)):
        save[i] = ""
    # print(lines[i])
    i = 0
    while i < len(lines):
        # print(i, lines[i])
        j = 0
        while j < len(lines[i]):
            # print("j = ", j, lines[i][j])
            if lines[i][j] == '}': # this makes the decision
                print(i, j, lines[i][j-10:j+1], track)
                if track[-1] == 'sp {':
                    track.pop() # ending of text color
                elif track[-1] == '{': # normal counter part
                    track.pop()
                    save[i] = save[i] + lines[i][j]
                j += 1
            else: # normal, \textcolor{blue}{ , just {
                st, end = search_textcolor_blue(txt=lines[i], start=j)
                if st is not None: #\textcolor case
                    #print("line ", i, j, lines[i][0:end+1], st, end, track)
                    #print("issue: ",lines[i][st:min(end+5, len(lines[i]))])
                    j = end+1
                    flag = False
                    while j < len(lines[i]):
                        if lines[i][j] == '{': # \textcolor{blue}{ starts
                            track.append('sp {')
                            flag = True
                            j += 1
                            break
                        else:
                            j += 1
                    if flag is False: # assuming in the same line
                        assert(flag is True)
                elif lines[i][j] == '{': # normal second bracket starting
                    track.append('{')
                    save[i] = save[i] + lines[i][j]
                    j += 1
                else: # normal case
                    save[i] = save[i] + lines[i][j]
                    j += 1
        i += 1

    for i in range(0, len(lines)):
        lines[i] = save[i]
    return lines


def search_textcolor_blue(txt, start):
    if txt is None:
        return None, None
    if start is None:
        start = 0
    if start+15 < len(txt):
        if txt[start:start+16] == "\\textcolor{blue}":
            return start, start+15
    return None, None


def blue_segment_remover(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        lines = removed_colored_texts(lines)
        return lines


def write_into_file(name, lines):
    with open(name, 'w', encoding='utf-8') as f:
        for i in range(0, len(lines)):
            f.write(lines[i])


lines = blue_segment_remover(file_name=os.path.join('.', 'compiled-project', 'merge', 'main_expertsys - With Color.tex'))
write_into_file(lines=lines, name='test_compilation.tex')