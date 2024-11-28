path_source="/workspaces/Planification_S6_PAC/.devcontainer/.env"

# Check if the file exists
if [ -f "$path_source" ]; then
    echo "$path_source found."
    source $path_source
    echo "GITHUB credentials"
    echo "TOKEN: $GITHUB_TOKEN "
    echo "USER: $GITHUB_ID "
    /tmp/_install_python_modules.sh
    exit 0
else 
    echo "$path_source not found."
    echo "Creating a .env file in the .devcontainer folder with the following content:"
    touch $path_source
    echo "File created"
    echo "export GITHUB_TOKEN={your_token}" >> $path_source
    echo "export GITHUB_ID={your_id}" >> $path_source
    echo "Please fill the {your_token} and {your_id} fields in $path_source"
    exit 1
fi


