#!/bin/bash
# $1='commit message'

hugo

cd public
git add --all
if [ "$1" != "" ] 
    then
        git commit -m "$1"
    else
        git commit -m "update"
    fi
git push 

cd .. 

cd themes/academic

git add --all 
if [ "$1" != "" ] 
    then
        git commit -m "$1"
    else
        git commit -m "update"
    fi
git push 

cd ../..

git add --all 
if [ "$1" != "" ] 
    then
        git commit -m "$1"
    else
        git commit -m "update"
    fi
git push 



