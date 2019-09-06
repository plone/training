#!/bin/bash

if [ "$TRAVIS_BRANCH" == "master" ] && [ "$TRAVIS_PULL_REQUEST" == "false" ]
then
  eval "$(ssh-agent)"
  chmod 600 "$HOME/.ssh/id_rsa"
  ssh-add "$HOME/.ssh/id_rsa"
  if ! rsync -avz --delete -e 'ssh -i ~/.ssh/id_rsa -p 6822 -o "StrictHostKeyChecking=no"' _build/html/ "$DOCS_SERVER:/var/www/training.plone.org/5"
  then
    echo 'There was an issue publishing the training.'
    exit 1
  else
    echo 'Training published successfully.'
  fi
else
  echo "Training build successful, but will not be published!"
fi
