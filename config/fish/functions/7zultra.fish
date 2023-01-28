function 7zultra --wraps='7z a -t7z -m0=lzma -mx=9 -mfb=64 -md=32m -ms=on' --description 'alias 7zultra 7z a -t7z -m0=lzma -mx=9 -mfb=64 -md=32m -ms=on'
  7z a -t7z -m0=lzma -mx=9 -mfb=64 -md=32m -ms=on $argv; 
end
