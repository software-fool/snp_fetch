# snp_fetch
Tool to fetch rsIds from chromosome/base position information from snpdb

This is placed here mostly for anyone trying to do something similar to have something to build on, rather than needing to start from scratch.  It's also placed here in the interests of research transparency.

I wrote this tool to help my daughter with a project she was working on.  She needed to find rsIDs for a collection of PGS [https://www.pgscatalog.org/](Polygenic Score) files.  For each data row in the PGS file the chromosome and base position information was used to lookup the rsID in the [https://www.ncbi.nlm.nih.gov/snp](dbSNP).

The script takes one or more PGS files as command line arguments and produces a new version of the PGS file with the comments and headers retained but with an additional column `rsID` added at the start.  As I understand the PGS file specification this is a valid PGS file.  The original files are *not* modified.  Assuming the original file name is `PGS00XXXX.txt.gz` then the new file, with `rsID` will be `PGS00XXXX_new.txt.gz`.

There is a `-v` (`--verbose`) option that allows you to see information about what the script is doing.  This is written to standard error so should not affect ny output collected from stdout.

The script will keep track of any entries for which it is not able to find an `rsID`.  In the new file these will be empty fields.  The script also adds as comments after the end of the data rows indications of which rows were not matched to an `rsID`.  The script prints to stdout the number of entries for which an `rsID` could not be found.

It's probably very unlikely this script will be of use to anyone exactly as is.  However, for other similar tasks could prove to be useful as a starting point.  (For example it has a crude PGS reader and rewriter in it).  Probably better to use the official PGS catalog tools from [pypi](www.pypi.com).

For ease for my daughter to use, I used `cx_freeze` to turn it into a standalone zip file which can just be extracted and run.

There may well be bugs, it may not work for what you want to do, but please feel free to use if it's useful.  If you are having problems, feel free to get in touch and I'll do my best to help you.  Please bear in mind I'm a software engineer and gave up biology when I was 14, so my knowledge what any of the information actually **IS** is extremely limited.

I should also add that I do not hold this script up as a shining example of a well structured piece of code - it was something I knocked together to help my daughter not have to manually or via some hacky Excel spreadsheet look up 14,000 (potential) `rsID`s.

## Operation

Assuming you have a working Python installation:

Note that `snpvenv` is any suitable directory name and it should not exist.


1. Create the virtual environment

```
> python -m venv snpvenv
```
   
2. **Windows** Activate the virtual environment

```
> snpvenv\Scripts\Activate.ps1
(snpvenv) >
```

2. **Linux** Activate the virtual environment

```
$ source snpvenv/bin/activate
(snpvenv) $
```


3. Install the required additional Python packages

```
(snpvenv) > pip install -r requirements.txt
```

You should now be able grab a PGS file, such as [PGS003954.txt.gz](https://ftp.ebi.ac.uk/pub/databases/spot/pgs/scores/PGS003954/ScoringFiles/PGS003954.txt.gz) and run `snp_fetch.py` like this:

```
(snpvenv) > python snp_fetch.py PGS003954.txt.gz
found genome build GRCh38 using Base Position
Number of missing rsIDs 2
```


```
$ source snpvenv/bin/activate
```

