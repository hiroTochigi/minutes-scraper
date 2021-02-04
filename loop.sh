for f in *.pdf; do
  new_f=$(echo $f | sed 's/pdf/txt/')
  p_f="../stat_finish/texted-pdf/"
  echo ${p_f}${new_f}
  python ../pdfminer.six/tools/pdf2txt.py "$f" >> "${p_f}${new_f}"
done