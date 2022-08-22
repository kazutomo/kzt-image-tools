#!/usr/bin/env bash

bn=test
in=${bn}.png

if [! -f $in] ; then
	echo "$in not found"
	exit 1
fi

for q in 50 60 70 80 90 ; do
	echo -n "q${q}: "
	convert ${in} -quality ${q} ${bn}-q${q}.jp2
	compare -metric PSNR ${bn}.png ${bn}-q${q}.jp2 diff-q${q}.jp2
	echo
done
