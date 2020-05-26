#!/bin/bash
# $1='commit message'

hugo

cd public
# remove additional files and folders from the member folder
rm member/index.*
rm -rf member/page/

git add --all
if [ "$1" != "" ] 
    then
        git commit -m "$1"
    else
        git commit -m "update"
    fi
git push 

cd .. 

git add --all 
if [ "$1" != "" ] 
    then
        git commit -m "$1"
    else
        git commit -m "update"
    fi
git push 



