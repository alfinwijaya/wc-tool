# Word Count Tool (wc)

A command-line word count tool. Count lines, words, characters, and bytes.

## Requirements

- Python 3.11
- Code Editor

## How to Use

For help, run:

```
python ccwc.py -h
```
- -c: byte count
- -l: line count
- -w: word count
- -m: character count

### Using Positional Argument
If no optional arguments are specified, the tool defaults to -c, -l, and -w.
```
python ccwc.py <file>
```
### Using Optional Arguments
Specify optional arguments to tailor the results:
```
python ccwc.py <option> <file>
```
example :
```
python ccwc.py -c test.txt -l test.txt -c test2.txt
```
### Using Standard Input
Utilize standard input through pipes:
```
cat <file> | python ccwc.py <option>
```
example:
```
cat test.txt | python ccwc.py -c -l -w -m
```

### Test
To run the unit test
```
python -m unittest test.py
```
