function conda_env_x86 --description 'creates a new conda environment using x86 architecture'
	CONDA_SUBDIR=osx-64 conda create -n $argv
	conda activate $argv[1]
	conda config --env --set subdir osx-64
end