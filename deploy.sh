#!/bin/bash

echo -e "\033[0;32mDeploying updates to GitHub...\033[0m"

# Build the project.
hugo -t hugo-nuo # if using a theme, replace with `hugo -t <YOURTHEME>`

# Go To Public folder
cd public
# Add changes to git.
git add .

# Commit changes.
msg="rebuilding site `date`"
if [ $# -eq 1 ]
  then msg="$1"
fi
git commit -m "$msg"


while [[ "$#" -gt 0 ]]; do case $1 in
  -f|--force)   force=1
                ;;
  *) echo "Unknown parameter passed: $1"; exit 1;;
esac; shift; done

# Push source and build repos.

if [ "$force" = "1" ]; then
	git push origin master -f
else
	git push origin master
fi


# Come Back up to the Project Root
cd ..
