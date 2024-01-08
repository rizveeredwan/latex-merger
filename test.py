from latex_merger import LatexMerger
import os

latex_merger = LatexMerger()
"""
latex_merger.start_merge(overleaf_folder=os.path.join('E:', os.sep, 'Research', 'Incremental-Sequential-Pattern-Mining',
                                                      'Incremental-Sequential-Pattern-Mining-with-SP-Tree', 'ES-IncTreeMiner'),
                         remove_old_project_flag=True,
                         construct_eps_images=True,
                         image_folder=os.path.join('Figures', 'Pdf'),
                         style_files=['elsarticle.cls', 'dirtytalk.sty'],
                         main_tex_file='main_expertsys.tex',
                         bibliography_style='model5-names.bst', # "abbrv.bst", 'model5-names.bst'
                         bibliography_file=None, # "sn-bibliography.bib"
                         section_folder_name='Sections',
                         package_path='packages.tex',
                         bib_tex_file='output.bbl')
"""

latex_merger.start_merge(overleaf_folder=os.path.join('.', 'data', 'AI'),
                         remove_old_project_flag=True,
                         construct_eps_images=True,
                         image_folder=os.path.join('figures'),
                         style_files=[os.path.join('.', 'svjour3.cls'), os.path.join('.', 'svglov3.clo')],
                         main_tex_file='ai_main.tex',
                         bibliography_style=None, # "abbrv.bst", 'model5-names.bst' None
                         bibliography_file=None, # "sn-bibliography.bib"
                         section_folder_name='chapters',
                         package_path=None, # 'packages.tex'
                         bib_tex_file='output.bbl')



