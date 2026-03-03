# my abbreviations

## jrnl view filters 
abbr -a jt  'jrnl -on today --export md | mdless'	# today's entries
abbr -a jr  'jrnl -n 10 --export md | mdless' # recent entries
abbr -a jcw 'jrnl -from "this monday" -to "this sunday" --export md | mdless' # current week's entries'
abbr -a jlw 'jrnl -from "last monday" -to "sunday" --export md | mdless'  # last week's entries
abbr -a jlm 'jrnl -from "last month" --export md | mdless'  # last month's entries
abbr -a jywr 'jrnl @weekly-review -from "this year" --export md | mdless'  # current year's weekly review entries
abbr -a jymr 'jrnl @monthly-review -from "this year" --export md | mdless'  # current year's weekly review entries

# jrnl review
abbr -a jdp ' jrnl < ~/.config/jrnl/weekday_plan.txt && jrnl -1 --edit'
abbr -a jws ' jrnl < ~/.config/jrnl/weekend_shutdown.txt && jrnl -1 --edit'
abbr -a jwr ' jrnl < ~/.config/jrnl/weekly_review.txt && jrnl -1 --edit'
abbr -a jmr ' jrnl < ~/.config/jrnl/monthly_review.txt && jrnl -1 --edit'
