rm -rf submission/

mkdir -p submission/
mkdir -p submission/part1/

cp part1/*.py submission/part1
cp part1/stream.txt submission/part1

mkdir -p submission/part2/
cp part2/*.py submission/part2
cp part2/block.txt submission/part2

cd report/
pdflatex report.tex -output-directory=report/
bibtex references.bib
pdflatex report.tex -output-directory=report/
pdflatex report.tex -output-directory=report/
cp report.pdf ../submission/