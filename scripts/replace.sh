#!/bin/bash

function help {
  echo "this script requires 3 parameters"
  echo " 1. word we need to replace"
  echo " 2. word we want to use"
  echo " 3. directory of kubernetes website"
  echo ""
  echo "example:"
  echo "$ ./replace.sh kluster klaster website"
  echo ""
}

[ $# -lt 3 ] && help && exit 1;

OLD=$1
NEW=$2
REPO=$3
DIR_ID=$REPO/content/id

COUNTER=0

FILES=`find $DIR_ID`
 
for FILE in $FILES
do
  if [ -f $FILE ] &&  grep -q $OLD $FILE ; then
    echo $FILE;
    sh -c "sed -i -e 's/$OLD/$NEW/g' $FILE;"
    COUNTER=$((COUNTER+1));
  fi
done

echo "found $OLD in $COUNTER different files"
