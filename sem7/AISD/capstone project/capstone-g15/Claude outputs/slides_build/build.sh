#!/usr/bin/env bash
# Puts the freeze hash on slide 4 and builds slides.pdf.
# Usage: bash build.sh <12-character hash of the D4 commit>
set -euo pipefail
cd "$(dirname "$0")"
h="${1:?give the 12-character hash of the D4 commit (git rev-parse --short=12 HEAD)}"
[[ "$h" =~ ^[0-9a-f]{12}$ ]] || { echo "not a 12-character hash: $h"; exit 1; }
sed "s/\\\\needed{freeze hash}/$h/" slides.tex > slides-final.tex
if grep -q '\\needed{' slides-final.tex; then echo "a placeholder is still left in slides-final.tex"; exit 1; fi
pdflatex -interaction=nonstopmode slides-final.tex > build.log
pdflatex -interaction=nonstopmode slides-final.tex > build.log
mv slides-final.pdf slides.pdf
rm -f slides-final.aux slides-final.log
echo "slides.pdf written, freeze HEAD $h, $(pdfinfo slides.pdf | awk '/^Pages/{print $2}') pages"
