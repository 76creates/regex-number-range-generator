# regex-number-range-generator
==============================================================
REGEX NUMBER RANGE GENERATOR
==============================================================
name: re_range_gen
author: Dusan Gligoric
email: dusan76shi@gmail.com
date: May 12th 2017
version: 1.0
python version: 2.7 and 3.4 tested
lincese : GNU General Public License v3.0
==============================================================
DESCRIPION
This script will generate regex number range selector based
uppon arguments pased, it prints out expression ready to use
for whole line validating(start to end), you could modify this
to fit into any regex expression that would preceed or have
something behind the range validator.
==============================================================
RANGE ARGUMENTS
range
  x:y
    range define, x has to be greater than y, ranges that
    overlap will be merged, one could define as many 
    ranges as needed
==============================================================
EXAMPLE
  python re_range_gen.py 1:100
  python re_range_gen.py 10:40 60:1240 3000:1251251
==============================================================
OUTPUT EXAMPLE
  python re_range_gen.py 10:100 60:200 500:1000
  ^(1000|[5-9][0-9]{2}|200|1[0-9]{2}|[1-9][0-9])$
==============================================================
