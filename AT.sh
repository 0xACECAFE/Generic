#!/bin/bash
#===============================================================================
#
#         FILE:  AT.sh
#
#        USAGE:  ./AT.sh 
#
#  DESCRIPTION:  
#
#      OPTIONS:  ---
# REQUIREMENTS:  ---
#         BUGS:  ---
#        NOTES:  ---
#       AUTHOR:  Theo v. Werkhoven (TWe), theo@van-werkhoven.nl
#      COMPANY:  
#      VERSION:  1.0
#      CREATED:  02/17/07 00:41:10 CET
#     REVISION:  ---
#===============================================================================

for file in *.html; do
   lynx -justify -dont-wrap-pre -width=180 --dump $file|tr -d '_' > ${file%%.html}.txt
done
/home/theo/devel/AnalyseThis.py -o ErrorsRPT.txt .

