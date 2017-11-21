#!/bin/bash
# $1='commit message'

hugo

cd public
git add --all
git commit -m "$1"
git push 

cd .. 

git add --all 
git commit -m "$1" 
git push 