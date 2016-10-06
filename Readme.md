### This is an example project for a potential employer.

The instructions for the project can be found in "Skilled Nursing Facility Project.pdf"

### Running

The code can be run in python 3 as 
```python nurse-search.py 35653```
where 35653 can be replaced with any zipcode.

This code imports numpy, pandas, json, and argparse, so make sure those are in your python distribution.

The optional arguments are '--search_radius' (or '-sr') which is the maximum radius from the given zipcode in miles, and '--min_overall_rating' (or '-mr'),
which specifies the minimum rating according to the SNF dataset. The defaults are 10 and 1, respectively.

### Efficiency

The current implementation populates a pandas dataframe with lat and long values for each 
entry in the main CSV “ProviderInfo_Download.csv” by indexing the "zip_code_centroids.csv"
as a dataframe. This is not as bad as slow as searching the latter file, but given that 
this is likely to be a function that is used many times, it would be much more efficient 
to augment the main CSV “ProviderInfo_Download.csv” with the lat and long info directly,
even just to avoid having to open and parse the other (larger) CSV. 

Further efficiency could be garnered by avoiding parsing/iterating the entire 
“ProviderInfo_Download.csv”. This would require making it into a more structured type,
such as a database. One could go as far as precomputing the indices for nearby 
results for each zip code for common distance measures. However, with the current 
number of entries this type of optimizations may be premature.