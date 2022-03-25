# latex-merger
A python library to compress and sort an overleaf latex project.

## How the Idea Came
Had to compile an overleaf project for a journal's article submission. But in overleaf when we
make a project, we do things in much sorted way, creating separate folders for chapters/sections, figures, figures with pdf, separate file for latex packages, etc.

But when we work for the submission of journal, we need to compress everything into one file pretty often. This process is also not a one-time shot rather incrementally gets updated with our project update and we are again back to ground zero ! Recompile and Merge everything again.

So, wrote a library to do this annoying repeating task !

## What latex-merger does,

- Convert all the **pdf images** to **eps image**
- **Update the path of images** in the latex files, in all chapters
- Compile all the chapters in **one single latex file**
- **Copy** all other necessary files, e.g, style files, bibliography based on given path
- Finally a folder named **merge** with all the required files for a journal submission

## Usage

```commandline
from latex_merger import LatexMerger
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
```

## Parameters

- overleaf_folder : The path where the overleaf folder is.
- remove_old_project_flag: If ``true``, it deletes the all the previously compiled files ``compiled_project`` directory ((can be ``False``))
- construct_eps_images: If ``true``, it constructs eps images from the pdf images (can be ``False``)
- image_folder: The folder name in overleaf project containing pdf images (can be ``None``)
- style_files: A list of file names, e.g, style files to manually copy in the final ``compiled_project/merge`` folder
- main_tex_file: The main latex file of your existing project where everything will be put
- bibliography_style: The file name of your bibliography style
- bibliography_file: The file name of your bibliography file (.bib)
- section_folder_name: The folder name under overleaf project where all of your sections/chapters are
- package_path: The file name of your ``packages.tex``, where you have kept all the imports, e.g, `\usepackage` commands (can be ``None``)

## Requirements
- I tested using ``MikTex``, a tex distribution tool for windows
- I use ``WinEdt`` as latex file editor and to build source tree
- My used python version was ``3.9``

## Remember, Remember
- If you see, that you did all things right but still the bibliography section is not generating (like myself), may be you **did not compile the project** using ``F9`` rather only tried to make pdf using ``pdf2latex`` in ``WinEdt`` through ``MikTex``.
- Try to avoid spacing as much as possible (figures, folders, during import/include etc.), rather use different symbols (_,-, etc). It reduces redundant cases system wide, also might create issue while using this library.
-
```commandline
Sometimes, when we use \usepackage{graphics}, we add the following codes or graphicspaths,

% declare the path(s) where your graphic files are
%\graphicspath{{./Figures/Pdf/}{}}
  % and their extensions so you won't have to specify these with
  % every instance of \includegraphics
%\DeclareGraphicsExtensions{.pdf,.jpeg,.png}


**Be sure to comment or remove these lines from main latex file, otherwise it might create issues.**
```

## Issues

You can let me know the issues by emailing me at
[rizveeredwan.csedu@gmail.com](mailto:rizveeredwan.csedu@gmail.com).
