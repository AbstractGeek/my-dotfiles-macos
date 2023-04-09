# A file containing all my aliases for taskwarrior

##### Aliases #####
alias tasks_w "task status:waiting all"
alias tasks_d "task status:deleted all"
alias tasks_p "task status:pending all"
alias tasks_c "task status:completed all"

alias task_r "task +CHILD"


##### Functions #####

function task_d_m
    # defer task to tomorrow morning (wait, schedule or due)
    if test (count $argv) -lt 2
        task $argv[1] modify wait:tomorrow+8h
    else
        switch $argv[2]
            case due
                task $argv[1] modify wait:tomorrow+8h due:tomorrow+$argv[3]
            case '*'
                task $argv[1] modify wait:tomorrow+8h scheduled:tomorrow+$argv[2]
        end

    end

end

function task_d_e
    # defer task to tomorrow evening (wait, schedule or due)
    if test (count $argv) -lt 2
        task $argv[1] modify wait:tomorrow+17h
    else
        switch $argv[2]
            case due
                task $argv[1] modify wait:tomorrow+17h due:tomorrow+$argv[3]
            case '*'
                task $argv[1] modify wait:tomorrow+17h scheduled:tomorrow+$argv[2]
        end

    end

end



##### Autocomplete definitions #####
complete -c tasks_p -a "project:10_Academia project:20_Science project:30_Personal project:40_Finance project:50_Pensieve project:60_Hobbies"
complete -c tasks_w -a "project:10_Academia project:20_Science project:30_Personal project:40_Finance project:50_Pensieve project:60_Hobbies"
#complete -c task_d_m -a "due "
#complete -c task_d_e -a "due "

