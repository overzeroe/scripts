# Create a system of marks and jumps for a shell, like marks and jumps in Vim
# Created with love by OverZeroe. Enjoy! (C) 2009 OverZeroe.

# Temporarilyl mark a directory (default to marking "MARK_DEFAULT_A")
function tm {
local jmp_name=$1;
if [ $# = 0 ]; then
	jmp_name=MARK_DEFAULT_A
fi
eval "${jmp_name}=\"$(pwd)\""	
}

# Save a directory mark
function m {
local jmp_name=$1;
if [ $# = 0 ]; then
	jmp_name=MARK_DEFAULT_A
fi   
eval "${jmp_name}=\"$(pwd)\""	
echo "${jmp_name}=\"$(pwd)\"" >> ~/.bash_saved_jumps	
}

# Jump to a directory (default to marking "MARK_DEFAULT_A")
function j {
local jmp_name=$1;
if [ $# = 0 ]; then
	jmp_name=MARK_DEFAULT_A
fi
eval $(printf "cd \"$%s%s%s\"" "{" ${jmp_name} "}")	
}

# Import saved jumps
eval $(cat ~/.bash_saved_jumps)

