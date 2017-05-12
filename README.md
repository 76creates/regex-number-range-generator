# regex-number-range-generator

##### REGEX NUMBER RANGE GENERATOR

name: re_range_gen<br>
author: Dusan Gligoric<br>
email: dusan76shi@gmail.com<br>
date: May 12th 2017<br>
version: 1.0<br>
python version: 2.7 and 3.4 tested<br>
lincese : GNU General Public License v3.0<br>

#### DESCRIPION<br>
This script will generate regex number range selector based<br>
uppon arguments pased, it prints out expression ready to use<br>
for whole line validating(start to end), you could modify this<br>
to fit into any regex expression that would preceed or have<br>
something behind the range validator.<br>

#### RANGE ARGUMENTS<br>
range<br>
&nbsp;&nbsp;&nbsp;x:y<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;range define, x has to be greater than y, ranges that<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;overlap will be merged, one could define as many <br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ranges as needed<br>

#### EXAMPLE<br>
  &nbsp;&nbsp;&nbsp;python re_range_gen.py 1:100<br>
  &nbsp;&nbsp;&nbsp;python re_range_gen.py 10:40 60:1240 3000:1251251<br>

#### OUTPUT EXAMPLE<br>
  &nbsp;&nbsp;&nbsp;python re_range_gen.py 10:100 60:200 500:1000<br>
  &nbsp;&nbsp;&nbsp;^(1000|[5-9][0-9]{2}|200|1[0-9]{2}|[1-9][0-9])$<br>

