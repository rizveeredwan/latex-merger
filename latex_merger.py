import os
import shutil
from subprocess import call


class LatexMerger:
    def __init__(self, remove_old_project_flag):
        if remove_old_project_flag is True:
            self.remove_old_project()
        if os.path.exists('compiled-project') is False:
            os.mkdir('compiled-project')

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

    def remove_files(self, folder_name='datasets'):
        try:
            if os.path.exists(folder_name):
                shutil.rmtree(folder_name)
                print("deleted")
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

    def change_the_image_paths(self, file_name=None):
        try:
            print(file_name)
            with open(file_name, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for i in range(0, len(lines)):
                    if '\\includegraphics' in lines[i] and '.pdf' in lines[i]:
                        # print(lines[i])
                        temp = lines[i].split('}')[0]
                        # print(temp)
                        pdf_name = self.extract_file_name(temp)
                        eps_name = pdf_name.split('.pdf')[0] + '.eps'
                        if os.path.exists(os.path.join('compiled-project', 'eps', eps_name)) is True:
                            print("exists")
                            print(pdf_name, os.path.join('compiled-project', 'eps', eps_name))
                            new_path = self.update_with_new_path(old_path=lines[i], new_path=eps_name.split('.eps')[0])
                            print(lines[i], new_path)
                            lines[i] = new_path
                        else:
                            print("do not exist")
                            print(pdf_name, os.path.join('compiled-project', 'eps', eps_name))
                self.write_into_file(file_name=file_name, lines=lines)
                print("writing complete")
        except Exception as e:
            print(e)

    def read_file(self, file_name):
        with open(file_name, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        return lines

    def update_bibliography_line(self, main_tex_file):
        lines = self.read_file(file_name=main_tex_file)
        for i in range(len(lines)-1, -1, -1):
            if '\\bibliography{' in lines[i]:
                bib_file = self.extract_text_within_bracket(text=lines[i])
                bib_file = bib_file + '.bib'
                lines[i] = '\\bibliography{'+bib_file+'}'
                break
        self.write_into_file(file_name=main_tex_file, lines=lines)

    def compile_section_text(self, main_file, sections):
        main_file_lines = self.read_file(file_name=main_file)
        i = 0
        while i < len(main_file_lines):
            if ('\\input{' in main_file_lines[i]) or ('\\include{' in main_file_lines[i]):
                temp = self.extract_text_within_bracket(text=main_file_lines[i])
                temp = self.extract_file_name(text=temp)
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

    def start_merge(self, overleaf_folder=None,
                    remove_old_project_flag=False,
                    style_files=None,
                    main_tex_file='main.tex',
                    construct_eps_images=False,
                    image_folder=None,
                    bibliography_style="abbrv.bst",
                    bibliography_file="sn-bibliography.bib",
                    section_folder_name='Sections',
                    package_path=None):

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

        # copy style
        for st in style_files:
            source = os.path.join(overleaf_folder, st)
            destination = os.path.join('.', 'compiled-project', 'merge', st)
            self.copy_file(source, destination)

        # copy main tex file
        source = os.path.join(overleaf_folder, main_tex_file)
        destination = os.path.join('.', 'compiled-project', main_tex_file)
        self.copy_file(source, destination)

        # copy the bibiliography
        source = os.path.join(overleaf_folder, bibliography_style)
        destination = os.path.join('.', 'compiled-project', 'merge', bibliography_style)
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
        for f in files:
            source = os.path.join(overleaf_folder, section_folder_name, f)
            destination = os.path.join('.', 'compiled-project', f)
            chapters.append(destination)
            self.copy_file(source, destination)

        # change the image path in files
        for f in range(0, len(chapters)):
            self.change_the_image_paths(file_name=chapters[f])

        # compile section files
        self.compile_section_text(main_file=os.path.join('.', 'compiled-project', main_tex_file), sections=chapters)

        ## all copying
        # image copying
        image_files = os.listdir(os.path.join('.', 'compiled-project', 'eps'))
        for im in image_files:
            self.copy_file(source=os.path.join('.', 'compiled-project', 'eps', im),
                           destination=os.path.join('.', 'compiled-project', 'merge'))

        # main latex
        self.copy_file(source=os.path.join('.', 'compiled-project', main_tex_file),
                       destination=os.path.join('.', 'compiled-project', 'merge', main_tex_file))
        return

    def remove_old_project(self):
        self.remove_files(folder_name='compiled-project')
        try:
            os.mkdir('compiled-project')
            print("directory created")
        except Exception as e:
            print(e)


latex_merger = LatexMerger(remove_old_project_flag=False)
# latex_merger.pdf_to_eps(pdf_folder=os.path.join('..', 'API-Overleaf', 'Figures', 'Pdf'))
latex_merger.start_merge(overleaf_folder=os.path.join('..', 'API-Overleaf'),
                         remove_old_project_flag=True,
                         construct_eps_images=True,
                         image_folder=os.path.join('Figures', 'Pdf'),
                         style_files=['svglov3.clo', 'svjour3.cls', 'dirtytalk.sty'],
                         main_tex_file='main_springer.tex',
                         bibliography_style="abbrv.bst",
                         bibliography_file="sn-bibliography.bib",
                         section_folder_name='Sections',
                         package_path='packages.tex')
