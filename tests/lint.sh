#!/bin/bash
set -e


CHANGED_FILES=$(git diff-index --name-only HEAD --cached | grep \.rst$)

if [ -n "$CHANGED_FILES" ]; then
	while read -r fname; do
	    echo Testing: "$fname"
	    docker run -v "${PWD}"/"$fname":/srv/docs:rw -v "${PWD}"/.ttd-lintrc:/srv/.ttd-lintrc testthedocs/plone-lint
	    echo Running write-good checks
	    docker run -v "${PWD}":/srv testthedocs/ttd-textlint "$fname"
	done <<< "$CHANGED_FILES"
    exit 0
fi
exit 0
# Check if last commit includes a rst file
#git diff-index --name-only HEAD --cached | grep \.rst$
