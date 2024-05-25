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

latex_merger.start_merge(overleaf_folder=os.path.join('.', 'data', 'Mridul thesis shared with RAR'),
                         remove_old_project_flag=True,
                         construct_eps_images=True,
                         image_folder=os.path.join('Figures'),
                         style_files=[os.path.join('.', 'sn-jnl.cls')],
                         main_tex_file='main_sn-article.tex',
                         bibliography_style='sn-mathphys-num.bst', # "abbrv.bst", 'model5-names.bst' None
                         bibliography_file=None, # "sn-bibliography.bib"
                         section_folder_name='Chapters',
                         package_path=None, # 'packages.tex'
                         bib_tex_file='output.bbl')



