#!/bin/bash

function check_fish(){
    if [ -n $FISH_VERSION]; then
        echo "Fish shell detected. Using fish syntax."
        USE_FISH="True"
    else
        echo "Bash shell detected. Using bash syntax."
        USE_BASH="True"
    fi
}

# if shell is fish, use fish syntax
function check_env_variable() {
    
    if [ -n "$USE_FISH" ]; then
        fish scripts/fish/set_env.fish $1 $2
    fi
    if [ -n "$USE_BASH" ]; then
            if [ -z "${!1}" ]; then
                export $1=$2
            fi

    fi
}

check_fish
# Get the variables from the config file
source variables.config

# iterate through all variables with the prefix DISCORD_
for var in $(compgen -A variable | grep DISCORD_); do
    check_env_variable $var ${!var}
done
