---
title: Swiss Army Knife Blade - awk
date: 2017-04-25
description: "Awk's Origin - Starting with a Beauty Choosing a Boyfriend Speaking of Swiss Army knives, many people are probably tired of hearing it. Some say Emacs is a Swiss Army knife, some say Vim is also a Swiss Army knife, some say Python is a Swiss Army knife. But let's temporarily put aside our interest in Swiss Army knives and play with a small Swiss Army knife blade - awk. This little guy is a petite, special programming language."
tags: [Tips]
categories:
---

[](#Awk's-Origin---Starting-with-a-Beauty-Choosing-a-Boyfriend)Awk's Origin - Starting with a Beauty Choosing a Boyfriend
Speaking of Swiss Army knives, many people are probably tired of hearing it. Some say Emacs is a Swiss Army knife, some say Vim is also a Swiss Army knife, some say Python is a Swiss Army knife. But let's temporarily put aside our interest in Swiss Army knives and play with a small Swiss Army knife blade - awk. This little guy is a petite, special programming language.

I can't help it, I've summarized the best way to get to know new things: charge straight at it.
Look at this set of blind date data gfs.data:

1
2
3
4
5
6
Li 65 177 10000
Wang 77 180 8000
Niu 60 199  20000
Chen 64.5 168 5000
Ouyang 80 200 12000
Liu 72.5 182 9999

This small dataset contains several fields: name, weight, height, monthly income. For example, if a beauty needs to choose a boyfriend standard from here, how to select the tall, rich, handsome men with height above 177?

1
2
3
4
5
➜  tmp awk ' $3 > 177 { print $1,$3}' gfs.data
Wang 180
Niu 199
Ouyang 200
Liu 182

tmp is a temporary directory, this is a short path in zsh, ignore it. The awk program structure is pattern { action }.
It defaults to treating fields as sequences of non-whitespace characters. (So you see those quiet spaces in the middle are treated as air.) The rest, the first field name is $1, the second field weight is $2, 177, 180, 199, 168, 200, 182 these height values are $3, and so on. The entire line is $0. Everyone's looks and assets may be different, meaning the length of $n values is not necessarily consistent.

The single-quoted $3 > 177 is the condition for matching each line scan. When scanning to Wang, obviously this guy's 180 exceeds the expected value, need to look a few more times to see if he's a "true destined one" with compatible "ba zi" (eight characters), so he's selected. Following this pattern to search to the last line, Liu this buddy also won the lottery.
If this beauty has high standards and has many conditions for choosing a boyfriend, such as high income, well-proportioned weight, high IQ, etc., it's best to write her conditions into a file, named: conditions.data. Select her ideal husband at once.

```haskell
awk -f conditions.data gfs.data
```

-f means extracting the program from a file. This standard can be referenced by multiple girls. Choose, not selected? Don't want, selected? Want! Choose... choose... mass selection!

```applescript
awk -f progfile optional list of files
```

So when there are many selection conditions and you don't want to list them one by one, how do you give a range to the dating agency? Use the field count NF. NF is a built-in variable in Awk that stores and calculates the number of fields in the current line.

1
2
3
4
5
6
7
➜  tmp awk  '{ print NF, $1, $NF }' gfs.data
4 Li 10000
4 Wang 8000
4 Niu 20000
4 Chen 5000
4 Ouyang 12000
4 Liu 9999

This prints out the number of inspection conditions, name, and monthly income for each boy. Take these conditions directly to cast a net.

Print the blind date order NR of the true destined one, also a built-in variable, is the count of lines read so far, here it's the number of blind dates (assuming this girl changes partners each time).

1
2
3
4
5
6
7
➜  tmp awk '{print NR, $0}'  gfs.data
1 Li 65 177 10000
2 Wang 77 180 8000
3 Niu 60 199  20000
4 Chen 64.5 168 5000
5 Ouyang 80 200 12000
6 Liu 72.5 182 9999

What about these conditions?

1
2
3
➜  tmp awk '$4 > 10000 {print "Very rich person:", $1, " Monthly income:", $4 }' gfs.data
Very rich person: Niu  Monthly income: 20000
Very rich person: Ouyang  Monthly income: 12000

Too many people, salary digits are hard to compare, after all there are too many zeros! Filter and format it, how to do it? printf(format, val_1, val_2, val_3, …, val_n),

1
2
3
4
5
6
7
➜  tmp awk '{printf("%-8s's monthly salary is ￥%10.2f\n", $1,$4)}' gfs.data
Li     's monthly salary is ￥  10000.00
Wang    's monthly salary is ￥   8000.00
Niu     's monthly salary is ￥  20000.00
Chen    's monthly salary is ￥   5000.00
Ouyang  's monthly salary is ￥  12000.00
Liu     's monthly salary is ￥   9999.00

Oh, still can't see clearly who is a high-quality male. Come, sort their salary levels. Salary goes low, people go high! Use the pipe command sort.

1
2
3
4
5
6
7
➜  tmp awk '{printf(" %10.2f %s\n", $4, $0)}' gfs.data | sort -n
    5000.00 Chen 64.5 168 5000
    8000.00 Wang 77 180 8000
    9999.00 Liu 72.5 182 9999
   10000.00 Li 65 177 10000
   12000.00 Ouyang 80 200 12000
   20000.00 Niu 60 199  20000

So Brother Niu is the most "promising" in terms of money here! Since three people have ten-thousand-level salaries, let's lock them in first. After all, who would have trouble with money? But you can't just look at wages. What if this person is Wu Dalang or what if he's √2? No, be more cautious, start high and go low, those above 190 can pass the eye test. When they grow up, they can play volleyball like Lang Ping and Zhu Ting, or maybe produce a little Yao Ming? Add more conditions: AND, OR and NOT, using &&, || and !

1
2
3
➜  tmp awk '$4 >=10000 && $3 > 190 { print $0}' gfs.data
Niu 60 199  20000
Ouyang 80 200 12000

This output lacks a conspicuous title. Maybe some girl will mistake weight for waist circumference? To avoid unnecessary misunderstandings, let's add a header.
1
2
3
4
5
6
7
8
9
➜  tmp awk 'BEGIN {print "Name Weight Height Salary"; print ""}{print($0)}' gfs.data
Name Weight Height Salary

Li 65 177 10000
Wang 77 180 8000
Niu 60 199  20000
Chen 64.5 168 5000
Ouyang 80 200 12000
Liu 72.5 182 9999

Oh, arrived at the meeting place early, nothing to do. Maybe compare these people's average wages?

1
2
3
4
➜  tmp awk '{salary = salary + $4} END {print NR, " people";  print "Total monthly salary:", salary; print "Average monthly salary:", salary/NR}' gfs.data
6 people
Total monthly salary: 64999
Average monthly salary: 10833.2

Not bad! The people haven't arrived yet. Can all the blind date names be combined into a poem?

1
2
➜  tmp awk '{names = names $1 " "} END {print names }'  gfs.data
Li Wang Niu Chen Ouyang Liu

Well, no. How many strokes in these names? Ah no, how many letters are they composed of?

1
2
3
4
5
6
7
➜  tmp awk ' {print $1, length($1) } ' gfs.data
Li 2
Wang 4
Niu 3
Chen 4
Ouyang 6
Liu 3

[](#Knife-Flow)Knife Flow
if-else filter

1
2
3
4
5
6
7
➜  tmp awk '$4 > 10000 {n =  n + 1; salary = salary + $4 }{ if (n > 0 && $4 > 10000)  print $1, "You have a chance"; else {print $1, "You're out"} }' gfs.data
Li You're out
Wang You're out
Niu You have a chance
Chen You're out
Ouyang You have a chance
Liu You're out

while loop, comb through from the beginning
1
2
3
4
5
6
7
awk '{ line[NR] = $0 } END { i = NR ;while (i>0) { print line[i]; i = i - 1 }} ' gfs.data
Liu 72.5 182 9999
Ouyang 80 200 12000
Chen 64.5 168 5000
Niu 60 199  20000
Wang 77 180 8000
Li 65 177 10000

for nine returns to one
1
2
3
4
5
6
7
8
9
10
➜  tmp awk 'BEGIN {for (i=1; i <=9; ++i) print i}'
1
2
3
4
5
6
7
8
9

[](#Practical-"Slicer-Style")Practical "Slicer Style"
Total number of input lines

1
2
➜  tmp awk 'END { print NR}' gfs.data
6

Print the fourth line

1
2
➜  tmp awk ' NR == 4 ' gfs.data
Chen 64.5 168 5000

Output the last field of each line

1
2
3
4
5
6
7
➜  tmp awk ' {print $NF}' gfs.data
10000
8000
20000
5000
12000
9999

Print the last field of the last line

1
2
➜  tmp awk '{field = $NF} END { print field }'  gfs.data
9999

Print input lines with more than 3 fields

1
2
3
4
5
6
7
➜  tmp awk 'NF>3' gfs.data
Li 65 177 10000
Wang 77 180 8000
Niu 60 199  20000
Chen 64.5 168 5000
Ouyang 80 200 12000
Liu 72.5 182 9999

Print input lines where the last field value is greater than 10000

1
2
3
➜  tmp awk '$NF > 10000 ' gfs.data
Niu 60 199  20000
Ouyang 80 200 12000

Print the sum of field counts of all input lines

1
2
➜  tmp awk ' {nf = nf + NF} END {print nf} ' gfs.data
24

Print the count of lines containing /Niu/

1
2
➜  tmp awk ' /Niu/ {nlines = nlines + 1} END {print nlines}' gfs.data
1

Print the 4th field with maximum value, and the line containing it (assuming $1 is always positive)

1
2
➜  tmp awk '$4 > max { max=$4; maxline=$0 } END { print max, maxline }' gfs.data
20000 Niu 60 199  20000

Print lines that contain at least one field

1
2
3
4
5
6
7
➜  tmp awk 'NF > 0' gfs.data
Li 65 177 10000
Wang 77 180 8000
Niu 60 199  20000
Chen 64.5 168 5000
Ouyang 80 200 12000
Liu 72.5 182 9999

Print lines longer than 20 characters
1
2
3
4
5
➜  tmp awk 'length($0) > 16' gfs.data
Niu 60 199  20000
Chen 64.5 168 5000
Ouyang 80 200 12000
Liu 72.5 182 9999

Add the field count to the beginning of each line
1
2
3
4
5
6
7
➜  tmp awk '{print NF, $0}'  gfs.data
4 Li 65 177 10000
4 Wang 77 180 8000
4 Niu 60 199  20000
4 Chen 64.5 168 5000
4 Ouyang 80 200 12000
4 Liu 72.5 182 9999

Print the second and first fields of each line

1
2
3
4
5
6
7
➜  tmp awk '{print $2, $1}' gfs.data
65 Li
77 Wang
60 Niu
64.5 Chen
80 Ouyang
72.5 Liu

Swap a field and print the entire line

1
2
3
4
5
6
7
➜  tmp awk '{tmp = $1; $1 = $2; $2 = tmp; print}' gfs.data
65 Li 177 10000
77 Wang 180 8000
60 Niu 199 20000
64.5 Chen 168 5000
80 Ouyang 200 12000
72.5 Liu 182 9999

Replace the first field of each line with the line number

1
2
3
4
5
6
7
➜  tmp awk  '{$1 = NR; print}' gfs.data
1 65 177 10000
2 77 180 8000
3 60 199 20000
4 64.5 168 5000
5 80 200 12000
6 72.5 182 9999

Print lines with the second field deleted

1
2
3
4
5
6
7
➜  tmp awk '{$2 == ""; print}' gfs.data
Li 65 177 10000
Wang 77 180 8000
Niu 60 199  20000
Chen 64.5 168 5000
Ouyang 80 200 12000
Liu 72.5 182 9999

Print fields of each line in reverse order

1
2
3
4
5
6
7
➜  tmp awk '{ for (i=NF; i > 0; i= i-1) {printf("%s ", $i)} printf("\n")}' gfs.data
10000 177 65 Li
8000 180 77 Wang
20000 199 60 Niu
5000 168 64.5 Chen
12000 200 80 Ouyang
9999 182 72.5 Liu

Print the sum of all field values of each line

1
2
3
4
5
6
7
➜  tmp awk '{sum = 0; for (i=1; i <=NF; i=i+1) {sum = sum + $i} print sum }' gfs.data
10242
8257
20259
5232.5
12280
10253.5

Accumulate all field values of all lines

1
2
➜  tmp awk  '{for (i=1; i<=NF; ++i) sum += $i} END {print sum}' gfs.data
66524

Absolute values of all field values of all lines

1
2
3
➜  tmp awk  '{for (i=1; i<=NF; ++i) if ($i < 0) {$i = -$i} print }'
Li -65 -177 18000 # Here manually enter values with negative numbers
Li 65 177 18000 # Return

[](#Awk-Language-Radishes-and-Cabbage)Awk Language Radishes and Cabbage
Enter a file called radish.data. This file is basically like this. This section will use this radish and cabbage to stir-fry with fish and meat.
1
2
3
4
5
6
7
8
9
10
11
➜  tmp awk 'BEGIN {print "Name       Weight Unit Price Category\n"} {printf("%-10s %6.2f %2.2f %-1s\n", $1, $2, $3, $4)}' radish.data
Name       Weight Unit Price Category

Fish        30.00 8.50 Meat
Radish      14.00 1.20 Vegetables
Cabbage     24.00 1.50 Vegetables
Apple      100.00 2.50 Fruit
Onion        8.00 0.80 Vegetables
Banana      50.00 1.40 Fruit
Beef       120.00 22.00 Meat
Rice        40.00 10.00 Staple

First, it needs to be clear that Awk has these stir-fry modes. If you've seen "Awk's Origin - Starting with a Beauty Choosing a Boyfriend," you should feel a sense of déjà vu.
BEGIN {statements}
Before input is read, statements execute once - no matter if you're stir-frying or boiling, no matter if it's fish or meat, wash it first! Prepare oil, salt, sauce, vinegar bowls, it has nothing to do with your stir-frying!
END {statements}
After all input is read, statements execute once - old saying, whether you're full or not, pay up!
expression {statements}
Every time an input line is encountered where the judgment expression is true, statements execute the cooking process once. expression is true when its value is non-zero or non-empty - just check if you added salt, if there's too much oil? 70% done or 80% done?
/regular expression/ {statements}
When an input line matching the regular expression is encountered, statements execute: the input line contains a string that can be matched by regular expression. In one sentence, honestly follow the recipe. If hair or cockroach droppings are found in the dish, you're dead!
compound pattern {statements}
Multiple patterns, &&(AND), ||(OR), !(NOT), and parentheses combined. When compound pattern is true, statements execute. You can stir-fry + add vinegar, or bake, but don't give me half-cooked stuff.
pattern_1, pattern_2 {statements}
A range pattern matches multiple input lines, from pattern1 to pattern_2 (including these two lines), executing statements operations on each line. Your moment to show off might be after starting the fire and before starting the pot. This time period is your performance moment.

You can write down your 72 stir-fry methods and put them in the cooking secret book,
1
2
3
4
5
6
7
8
9
10
BEGIN {
      printf("%-10s %s %s %s\n",
          "Name", "Weight", "Unit Price", "Category")
      }
      { printf("%-10s %6.2f %6.2f %s\n", $1, $2, $3, $4)
        weight = weight + $2
        price  = price + $3*$2
      }
END   { printf("\n%10s %6.2f %6.2f\n", "Total: ", weight, price)
      }%

Next time, pass it to the one-in-a-million martial arts genius, directly call

1
2
3
4
5
6
7
8
9
10
11
12
➜  tmp awk -f cooking radish.data
Name         Weight Unit Price Category
Fish        30.00   8.50 Meat
Radish      14.00   1.20 Vegetables
Cabbage     24.00   1.50 Vegetables
Apple      100.00   2.50 Fruit
Onion        8.00   0.80 Vegetables
Banana      50.00   1.40 Fruit
Beef       120.00  22.00 Meat
Rice        40.00  10.00 Staple

      Total:  386.00 3674.20

[](#Blade-Unsheathed)Blade Unsheathed
One army knife blade, cuts down thousands!
To know what happens next, stay tuned for my next分解...
