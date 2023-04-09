function flattenpdf --description 'Flatten pdf using ghostscript'
    # Inputs:
    # $1 input file name
    # $2 output file name
    # Call ghost script and pass input parameters

    gs -dSAFER -dBATCH -dNOPAUSE -dNOCACHE -sDEVICE=pdfwrite \
    -dPreserveAnnots=false \
    -sOutputFile=$argv[2] $argv[1]


end
