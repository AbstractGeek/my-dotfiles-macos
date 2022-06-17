function compresspdf --description 'Compress pdf using ghostscript'
    # Inputs:
    # $1 screen or ebook or printer or prepress or default
    # $2 input file name
    # $3 output file name
    # Call ghost script and pass input parameters

    gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/$1 -dNOPAUSE -dQUIET -dBATCH -sOutputFile=$3 $2

end
