import os
import shutil
from subprocess import call


class LatexMerger:
    def __init__(self):
        pass

    def pdf_to_eps(self, pdf_folder):
        self.remove_files(folder_name=os.path.join('compiled-project', 'eps'))
        try:
            os.mkdir(os.path.join('compiled-project', 'eps'))
            print("directory created")
        except Exception as e:
            print(e)
        # all pdf images to eps images
        if os.path.exists(pdf_folder):
            try:
                files = os.listdir(pdf_folder)
                for f in files:
                    temp = os.path.join(pdf_folder, f)
                    print(temp)
                    try:
                        input_file = temp
                        output_file = os.path.join('compiled-project', 'eps', f.split('.pdf')[0] + '.eps')
                        call(["pdf2ps", input_file, output_file])
                    except Exception as e:
                        print(e)
            except Exception as e:
                print(e)
        else:
            pass

    def simple_image_copy(self, image_folder):
        self.remove_files(folder_name=os.path.join('compiled-project', 'eps'))
        try:
            os.mkdir(os.path.join('compiled-project', 'eps'))
            print("directory created")
        except Exception as e:
            print(e)
        # all pdf images to eps images
        if os.path.exists(image_folder):
            image_type = None
            try:
                files = os.listdir(image_folder)
                for f in files:
                    temp = os.path.join(image_folder, f)
                    try:
                        input_file = temp
                        image_type = input_file.split('.')[1]
                        output_file = os.path.join('compiled-project', 'eps', f)
                        self.copy_file(source=input_file, destination=output_file)
                    except Exception as e:
                        pass
                    print(output_file)
            except Exception as e:
                print(e)
            return image_type
        else:
            return None

    def remove_files(self, folder_name='datasets'):
        try:
            if os.path.exists(folder_name):
                shutil.rmtree(folder_name)
                print("deleted")
        except Exception as e:
            print(e)

    def remove_single_file(self, file_name):
        try:
            os.remove(file_name)
        except Exception as e:
            print(e)

    def copy_file(self, source, destination):
        try:
            shutil.copy(src=source, dst=destination)
        except Exception as e:
            print(e)

    def extract_file_name(self, text):
        _string = ""
        for i in range(len(text) - 1, -1, -1):
            if text[i] == '/':
                break
            _string = text[i] + _string
        return _string

    def extract_text_within_bracket(self, text):
        _string = ""
        st = False
        for i in range(len(text) - 1, -1, -1):
            if text[i] == '{':
                break
            if text[i] == '}':
                st = True
                continue
            if st is True:
                _string = text[i] + _string
        return _string

    def update_with_new_path(self, old_path, new_path):
        index = old_path.find("\includegraphics")
        st, end = None, None
        if index != -1:
            for i in range(index + 1, len(old_path)):
                if old_path[i] == '{' and st is None:
                    st = i
                elif old_path[i] == '}' and end is None:
                    end = i
                    break
            if st is not None and end is not None:
                prefix = old_path[0:st + 1]
                suffix = old_path[end:]
                old_path = prefix + new_path + suffix
        return old_path

    def write_into_file(self, file_name, lines):
        with open(file_name, 'w', encoding='utf-8') as f:
            for i in range(0, len(lines)):
                f.write(lines[i])
            f.close()

    def comment_portion_removal(self, line):
        for i in range(0, len(line)):
            if line[i] == '%':
                if i == 0:
                    return ""
                elif line[i-1] != "\\":
                    return line[0:i]
        return line

    def change_the_image_paths(self, file_name=None, old_ext=".pdf", new_ext="eps"):
        found_image_maps = []
        try:
            print(file_name)
            with open(file_name, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for i in range(0, len(lines)):
                    lines[i] = self.comment_portion_removal(line=lines[i])
                    if '\\includegraphics' in lines[i] and old_ext in lines[i]:
                        # print(lines[i])
                        temp = lines[i].split('}')[0]
                        # print(temp)
                        pdf_name = self.extract_file_name(temp)
                        eps_name = pdf_name.split(old_ext)[0] + "." + new_ext
                        if os.path.exists(os.path.join('compiled-project', 'eps', eps_name)) is True:
                            found_image_maps.append(os.path.join('compiled-project', eps_name))
                            print("exists")
                            print(pdf_name, os.path.join('compiled-project', 'eps', eps_name))
                            new_path = self.update_with_new_path(old_path=lines[i], new_path=eps_name)
                            print(lines[i], new_path)
                            lines[i] = new_path
                        else:
                            print("do not exist")
                            print(pdf_name, os.path.join('compiled-project', 'eps', eps_name))
                self.write_into_file(file_name=file_name, lines=lines)
                print("writing complete")
        except Exception as e:
            print(e)
        return found_image_maps

    def read_file(self, file_name):
        with open(file_name, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for i in range(0, len(lines)):
                lines[i] = self.comment_portion_removal(line=lines[i])
        return lines

    def update_bibliography_line(self, main_tex_file, bib_tex):
        """
            elif bibliographystyle{ in lines[i]:
                # lines[i] = '\n'
        """
        lines = self.read_file(file_name=main_tex_file)
        for i in range(len(lines)-1, -1, -1):
            if '\\bibliography{' in lines[i]:
                lines[i] = '\n'
            elif '\\end{document}' in lines[i]:
                lines[i] = "\n"
        for i in range(0, len(bib_tex)):
            lines.append(bib_tex[i])
        lines.append('\\end{document}')
        self.write_into_file(file_name=main_tex_file, lines=lines)

    def compile_section_text(self, main_file, sections):
        main_file_lines = self.read_file(file_name=main_file)
        used_section_files = []
        i = 0
        while i < len(main_file_lines):
            if ('\\input{' in main_file_lines[i]) or ('\\include{' in main_file_lines[i]):
                temp = self.extract_text_within_bracket(text=main_file_lines[i])
                temp = self.extract_file_name(text=temp)
                used_section_files.append(temp)
                f_path = os.path.join('.', 'compiled-project', temp+'.tex')
                print("f_paths ", f_path)
                if os.path.exists(f_path) is True:
                    print("f_paths ", f_path)
                    content = self.read_file(f_path)
                    main_file_lines = main_file_lines[0:i] + content + main_file_lines[i+1:]
                else:
                    print("failed")
                    print(f_path)
            i=i+1
        self.write_into_file(file_name=main_file, lines=main_file_lines)
        return used_section_files

    def remove_graphics_path_tage(self, main_tex_file):
        lines = self.read_file(file_name=main_tex_file)
        for i in range(0, len(lines)):
            if '\\graphicspath{' in lines[i]:
                lines[i] = '\n'
            elif '\\DeclareGraphicsExtensions{' in lines[i]:
                lines[i] = '\n'
        self.write_into_file(main_tex_file, lines)
        return

    def start_merge(self, overleaf_folder=None,
                    remove_old_project_flag=False,
                    style_files=None,
                    main_tex_file='main.tex',
                    construct_eps_images=False,
                    image_folder=None,
                    bibliography_style="abbrv.bst",
                    bibliography_file="sn-bibliography.bib",
                    section_folder_name='Sections',
                    package_path=None,
                    bib_tex_file=None):

        # removing old project
        if remove_old_project_flag is True:
            if remove_old_project_flag is True:
                self.remove_old_project()
        if os.path.exists('compiled-project') is False:
            os.mkdir('compiled-project')

        # Final folder
        self.remove_files(folder_name=os.path.join('.', 'compiled-project', 'merge'))
        os.mkdir(os.path.join('.', 'compiled-project', 'merge'))

        # construct eps images
        if construct_eps_images is True and image_folder is not None:
            self.pdf_to_eps(pdf_folder=os.path.join(overleaf_folder, image_folder))
        if construct_eps_images is False and image_folder is not None:
            pass

        # copy style
        for st in style_files:
            source = os.path.join(overleaf_folder, st)
            f_name = os.path.normpath(st).split(os.path.sep)[-1] # file name extracting
            destination = os.path.join('.', 'compiled-project', 'merge', f_name)
            self.copy_file(source, destination)

        # copy main tex file
        source = os.path.join(overleaf_folder, main_tex_file)
        destination = os.path.join('.', 'compiled-project', main_tex_file)
        self.copy_file(source, destination)

        # copy the bibiliography
        if bibliography_style is not None and bibliography_file is not None:
            source = os.path.join(overleaf_folder, bibliography_style)
            f_name = os.path.normpath(bibliography_style).split(os.path.sep)[-1]
            destination = os.path.join('.', 'compiled-project', 'merge', f_name)
            self.copy_file(source, destination)
            source = os.path.join(overleaf_folder, bibliography_file)
            destination = os.path.join('.', 'compiled-project', 'merge', bibliography_file)
            self.copy_file(source, destination)

        # copy package path
        if package_path is not None:
            source = os.path.join(overleaf_folder, package_path)
            destination = os.path.join('.', 'compiled-project', package_path)
            self.copy_file(source, destination)

        # copy the sections/chapters
        files = os.listdir(os.path.join(overleaf_folder, section_folder_name))
        chapters = []
        chapter_names = {}
        for f in files:
            source = os.path.join(overleaf_folder, section_folder_name, f)
            destination = os.path.join('.', 'compiled-project', f)
            chapters.append(destination)
            self.copy_file(source, destination)

        # change the image path in files
        found_image_maps = []
        for f in range(0, len(chapters)):
            path = os.path.normpath(path=chapters[f])
            path = path.split(os.sep)
            print("path ", path)
            try:
                chapter_names[path[-1].split('.tex')[0]] = self.change_the_image_paths(file_name=chapters[f])
                found_image_maps = found_image_maps + chapter_names[path[-1].split('.tex')[0]]
            except Exception as e:
                print(e)

        print("chapter names ", chapter_names)
        # compile section files
        used_section_files = self.compile_section_text(main_file=os.path.join('.', 'compiled-project', main_tex_file), sections=chapters)

        ## all copying
        # image copying
        image_files = os.listdir(os.path.join('.', 'compiled-project', 'eps'))
        for im in image_files:
            if os.path.join('compiled-project', im) in found_image_maps: # found_image_maps
                for f in range(0, len(used_section_files)):
                    try:
                        if os.path.join('compiled-project', im) in chapter_names[used_section_files[f]]:
                            self.copy_file(source=os.path.join('.', 'compiled-project', 'eps', im),
                                           destination=os.path.join('.', 'compiled-project', 'merge'))
                            break
                    except Exception as e:
                        print(e)


        if bib_tex_file is not None:
            # merging bibtex file
            bib_content = self.read_file(file_name=os.path.join(overleaf_folder, bib_tex_file))
            self.update_bibliography_line(os.path.join('.', 'compiled-project', main_tex_file), bib_tex=bib_content)

        # remove graphicpath
        self.remove_graphics_path_tage(main_tex_file=os.path.join('.', 'compiled-project', main_tex_file))

        # main latex
        self.copy_file(source=os.path.join('.', 'compiled-project', main_tex_file),
                       destination=os.path.join('.', 'compiled-project', 'merge', main_tex_file))

        # remove chapters
        for i in range(0, len(chapters)):
            self.remove_single_file(file_name=chapters[i])
        return

    def remove_old_project(self):
        self.remove_files(folder_name='compiled-project')
        try:
            os.mkdir('compiled-project')
            print("directory created")
        except Exception as e:
            print(e)



