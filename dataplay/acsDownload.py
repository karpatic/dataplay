# AUTOGENERATED! DO NOT EDIT! File to edit: notebooks/01_ACS_Explore_and_Download.ipynb (unless otherwise specified).

__all__ = ['retrieve_acs_data']

# Cell
# @title Run: Import Modules

# Once installed we need to..

# import and configure the Widgets
import ipywidgets as widgets
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = 'all'
import ipywidgets as widgets
from ipywidgets import interact, interact_manual

# About importing data
import urllib.request as urllib
from urllib.parse import urlencode
# This Prevents Timeouts when Importing
import socket
socket.setdefaulttimeout(10.0)

# Pandas Data Manipulation Libraries
import pandas as pd
# Show entire column widths
pd.set_option('display.max_colwidth', -1)
# Working with Json Data
import json
# Data Processing
import numpy as np
# Reading Json Data into Pandas
from pandas.io.json import json_normalize

# Export data as CSV
import csv


# Geo-Formatting
# Postgres-Conversion
import geopandas as gpd
from geopandas import GeoDataFrame
import psycopg2,pandas,numpy
from shapely import wkb
from shapely.wkt import loads
import os
import sys

# In case file is KML
# enable KML support; disabled by default
import fiona
fiona.drvsupport.supported_drivers['kml'] = 'rw'
fiona.drvsupport.supported_drivers['KML'] = 'rw'

# load libraries
# from shapely.wkt import loads
# from pandas import ExcelWriter
# from pandas import ExcelFile
import matplotlib.pyplot as plt
import glob
import imageio

# Cell
# @title Run: Create retrieve_acs_data()

#File: retrieveAcsData.py
#Author: Charles Karpati
#Date: 1/9/19
#Section: Bnia
#Email: karpati1@umbc.edu
#Description:
#This file returns ACS data given an ID and Year
# The county total is given a tract of '010000'

#def retrieve_acs_data():
#purpose: Retrieves ACS data from the web
#input:
# state (required)
# county (required)
# tract (required)
# tableId (required)
# year (required)
# includeCountyAgg (True)(todo)
# replaceColumnNames (False)(todo)
# save (required)
#output:
# Acs Data.
# Prints to ../../data/2_cleaned/acs/

def retrieve_acs_data(state, county, tract, tableId, year, save):
    dictionary = ''
    keys = []
    vals = []
    header = []
    keys1=keys2=keys3=keys4=keys5=keys6=keys7=keys8=''
    keyCount = 0

    # Called in addKeys(), Will create the final URL for readIn()
    # These are parameters used in the API URL Query
    # This query will retrieve the census tracts
    def getParams(keys): return {
        'get': 'NAME'+keys,
        'for': 'tract:'+tract,
        'in': 'state:'+state+' county:'+county,
        'key': '829bf6f2e037372acbba32ba5731647c5127fdb0'
      }
    # Aggregate City data is best retrieved seperatly rather than as an aggregate of its constituent tracts
    def getCityParams(keys): return {
        'get': 'NAME'+keys,
        'for': 'county:'+county,
        'in': 'state:'+state,
        'key': '829bf6f2e037372acbba32ba5731647c5127fdb0'
      }
    # Called in AddKeys(). Requests data by url and preformats it.
    def readIn( url ):
        tbl = pd.read_json(url, orient='records')
        tbl.columns = tbl.iloc[0]
        return tbl

    # Called by retrieveAcsData.
    # Creates a url and retrieve the data
    # Then appends the city values as tract '010000'
    # Finaly it merges and returns the tract and city totals.
    def addKeys( table, params):
        # Get Tract and City Records For Specific Columns
        table2 = readIn( base+urlencode(getParams(params)) )
        table3 = readIn( base+urlencode(getCityParams(params)) )
        table3['tract'] = '010000'
        # Concatenate the Records
        table2.append([table2, table3], sort=False)
        table2 = pd.concat([table2, table3], ignore_index=True)
        # Merge to Master Table
        table = pd.merge(table, table2,  how='left',
                         left_on=["NAME","state","county","tract"],
                         right_on = ["NAME","state","county","tract"])
        return table

    #~~~~~~~~~~~~~~~
    # Step 1)
    # Retrieve a Meta Data Table Describing the Content of the Table
    #~~~~~~~~~~~~~~~
    url = 'https://api.census.gov/data/20'+year+'/acs/acs5/groups/'+tableId+'.json'
    metaDataTable = pd.read_json(url, orient='records')

    #~~~~~~~~~~~~~~~
    # Step 2)
    # Createa a Dictionary using the Meta Data Table
    #~~~~~~~~~~~~~~~
    # Multiple Queries may be Required.
    # Max columns returned from any given query is 50.
    # For that reasons bin the Columns into Groups of 50.
    for key in metaDataTable['variables'].keys():
      if key[-1:] == 'E':
        keyCount = keyCount + 1
        if keyCount < 40 : keys1 = keys1+','+key
        elif keyCount < 80 : keys2 = keys2+','+key
        elif keyCount < 120 : keys3 = keys3+','+key
        elif keyCount < 160 : keys4 = keys4+','+key
        elif keyCount < 200 : keys5 = keys5+','+key
        elif keyCount < 240 : keys6 = keys6+','+key
        elif keyCount < 280 : keys7 = keys7+','+key
        elif keyCount < 320 : keys8 = keys8+','+key
        keys.append(key)
        val = metaDataTable['variables'][key]['label']
        # Column name formatting
        val = key+'_'+val.replace('Estimate!!', '').replace('!!', '_').replace(' ', '_')
        vals.append(val)
    dictionary = dict(zip(keys, vals))

    #~~~~~~~~~~~~~~~
    # Step 2)
    # Get the actual Table with the data we want using
    #~~~~~~~~~~~~~~~

    # The URL we call is contingent on if the Table we want is a Detailed or Subject table
    url1 = 'https://api.census.gov/data/20'+year+'/acs/acs5?'
    url2 = 'https://api.census.gov/data/20'+year+'/acs/acs5/subject?'
    base = ''
    if tableId[:1] == 'B': base = url1
    if tableId[:1] == 'S': base = url2

    # The addKey function only works after the first set of columns has been downloaded
    # Download First set of Tract columns
    url = base+urlencode(getParams(keys1) )
    table = pd.read_json(url, orient='records')
    table.columns = table.iloc[0]
    table = table.iloc[1:]
    # Download First set of Aggregate City data
    url = base+urlencode(getCityParams(keys1))
    table2 = pd.read_json(url, orient='records')
    table2.columns = table2.iloc[0]
    table2 = table2[1:]
    table2['tract'] = '010000'

    # Merge EM
    #table = pd.concat([table, table2], keys=["NAME","state","county",], axis=0)
    table.append([table, table2], sort=False)
    table = pd.concat([table, table2], ignore_index=True)

    # Now we can repetedly use this function to add as many columns as there are keys listed from the meta data table
    if keys2 != '' : table = addKeys(table, keys2)
    if keys3 != '' : table = addKeys(table, keys3)
    if keys4 != '' : table = addKeys(table, keys4)
    if keys5 != '' : table = addKeys(table, keys5)
    if keys6 != '' : table = addKeys(table, keys6)
    if keys7 != '' : table = addKeys(table, keys7)
    if keys8 != '' : table = addKeys(table, keys8)

    #~~~~~~~~~~~~~~~
    # Step 3)
    # Prepare Column Names using the meta data table. The raw data has columnsNames in the first row, as well.
    # Replace column ID's with labels from the dictionary where applicable (should be always)
    #~~~~~~~~~~~~~~~
    print('Number of Columns', len(dictionary) )

    header = []
    for column in table.columns:
        if column in keys: header.append(dictionary[column])
        else: header.append(column)
    table.columns = header

    # Prettify Names. Only happens with Baltimore...
    table['NAME'] = table['NAME'].str.replace(', Baltimore city, Maryland', '')
    table['NAME'][table['NAME'] == 'Baltimore city, Maryland'] = 'Baltimore City'

    # Convert to Integers Columns from Strings where Applicable
    table = table.apply(pd.to_numeric, errors='ignore')

    # Set the 'NAME' Column as the index dropping the default increment
    table.set_index("NAME", inplace = True)

    if save:

      # Save the raw data as 'TABLEID_5yYEAR.csv'
      table.to_csv('./'+state+county+'_'+tableId+'_5y'+year+'_est_Original.csv', quoting=csv.QUOTE_ALL)

      # Remove the id in the column names & Save the data as 'TABLEID_5yYEAR_est.csv'
      saveThis = table.rename( columns = lambda x : ( str(x)[:] if str(x) in [
        "NAME","state","county","tract"] else str(x)[12:] )  )
      saveThis.to_csv('./'+state+county+'_'+tableId+'_5y'+year+'_est.csv', quoting=csv.QUOTE_ALL)

    return table