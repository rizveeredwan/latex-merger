from latex_merger import LatexMerger
import os

latex_merger = LatexMerger()
latex_merger.start_merge(overleaf_folder=os.path.join('E:', os.sep, 'Research', 'Incremental-Sequential-Pattern-Mining',
                                                      'Incremental-Sequential-Pattern-Mining-with-SP-Tree', 'API-Overleaf'),
                         remove_old_project_flag=True,
                         construct_eps_images=True,
                         image_folder=os.path.join('Figures', 'Pdf'),
                         style_files=['svglov3.clo', 'svjour3.cls', 'dirtytalk.sty'],
                         main_tex_file='main_springer.tex',
                         bibliography_style=None, # "abbrv.bst"
                         bibliography_file=None, # "sn-bibliography.bib"
                         section_folder_name='Sections',
                         package_path='packages.tex',
                         bib_tex_file='output.bbl')
