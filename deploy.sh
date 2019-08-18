#!/bin/bash

if ([ $TRAVIS_BRANCH == "master" ] && [ $TRAVIS_PULL_REQUEST == "false" ])
then
  eval "$(ssh-agent)"
  chmod 600 $HOME/.ssh/id_rsa
  ssh-add $HOME/.ssh/id_rsa
  rsync -avz --delete -e 'ssh -i ~/.ssh/id_rsa -p 6822' _build/html/ $docs_server:/var/www/training.plone.org/5
  echo 'Website published successfully.'
else
  echo "Build successful, but not publishing!"
fi
