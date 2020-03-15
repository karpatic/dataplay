# Data Handling Guidebook
> The one stop shop to learn about data intake, processing, and visualization.


This homepage will show you just some of the things you can do with data.

## Install

The code is on <a href="https://pypi.org/project/test-template/">PyPI</a> so you can just run:

```
pip install test-template geopandas
```

From the terminal to install the code and its dependencies

## How to use

Import the installed module into your code and use like so:
``` 
from test_template.acsDownload import retrieve_acs_data 
retrieve_acs_data(state, county, tract, tableId, year, saveAcs)
```

```
from test_template.acsDownload import retrieve_acs_data
```

Heres an example:

```
from test_template.acsDownload import retrieve_acs_data
```

```
# Define our download parameters.
# more information on these parameters can be found in the tutorials!
tract = '*'
county = '510'
state = '24'
tableId = 'B19001'
year = '17'
saveAcs = False
```

```
df = retrieve_acs_data(state, county, tract, tableId, year, saveAcs)
df.head()
```

    Number of Columns 17





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>B19001_001E_Total</th>
      <th>B19001_002E_Total_Less_than_$10_000</th>
      <th>B19001_003E_Total_$10_000_to_$14_999</th>
      <th>...</th>
      <th>state</th>
      <th>county</th>
      <th>tract</th>
    </tr>
    <tr>
      <th>NAME</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Census Tract 1901</th>
      <td>796</td>
      <td>237</td>
      <td>76</td>
      <td>...</td>
      <td>24</td>
      <td>510</td>
      <td>190100</td>
    </tr>
    <tr>
      <th>Census Tract 1902</th>
      <td>695</td>
      <td>63</td>
      <td>87</td>
      <td>...</td>
      <td>24</td>
      <td>510</td>
      <td>190200</td>
    </tr>
    <tr>
      <th>Census Tract 2201</th>
      <td>2208</td>
      <td>137</td>
      <td>229</td>
      <td>...</td>
      <td>24</td>
      <td>510</td>
      <td>220100</td>
    </tr>
    <tr>
      <th>Census Tract 2303</th>
      <td>632</td>
      <td>3</td>
      <td>20</td>
      <td>...</td>
      <td>24</td>
      <td>510</td>
      <td>230300</td>
    </tr>
    <tr>
      <th>Census Tract 2502.07</th>
      <td>836</td>
      <td>102</td>
      <td>28</td>
      <td>...</td>
      <td>24</td>
      <td>510</td>
      <td>250207</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 20 columns</p>
</div>


