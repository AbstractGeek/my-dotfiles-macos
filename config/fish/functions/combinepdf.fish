function combinepdf --description 'Combine pdfs using ghostscript'

	gs -q -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -sOutputFile=$argv[1] $argv[2..-1]

end
