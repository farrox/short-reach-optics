#!/bin/bash

# Clean auxiliary files
# rm -f *.aux *.log *.toc *.out *.pdf *.bbl *.blg *.nav *.snm *.vrb *.run.xml *.thm *.lot *.lof 

# Compile with more verbose output
xelatex -interaction=nonstopmode -file-line-error main.tex
xelatex -interaction=nonstopmode -file-line-error main.tex
xelatex -interaction=nonstopmode -file-line-error main.tex
