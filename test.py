from latex_merger import LatexMerger
import os

latex_merger = LatexMerger()
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
