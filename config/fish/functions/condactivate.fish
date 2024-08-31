function condactivate --wraps='conda activate' --description 'conda init + activate'
  condainit 
  conda activate $argv        
end
