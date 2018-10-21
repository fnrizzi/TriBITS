# @HEADER
# ************************************************************************
#
#            TriBITS: Tribal Build, Integrate, and Test System
#                    Copyright 2013 Sandia Corporation
#
# Under the terms of Contract DE-AC04-94AL85000 with Sandia Corporation,
# the U.S. Government retains certain rights in this software.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the Corporation nor the names of the
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY SANDIA CORPORATION "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL SANDIA CORPORATION OR THE
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# ************************************************************************
# @HEADER

import os
import sys
import copy
import shutil
import unittest
import pprint

from FindCISupportDir import *
from CDashQueryAnalizeReport import *

g_testBaseDir = getScriptBaseDir()

tribitsBaseDir=os.path.abspath(g_testBaseDir+"/../../tribits")
mockProjectBaseDir=os.path.abspath(tribitsBaseDir+"/examples/MockTrilinos")

g_pp = pprint.PrettyPrinter(indent=4)


#
# Helper functions and classes
#


# Mock function object for getting data off of CDash as a stand-in for the
# function extractCDashApiQueryData().
class MockExtractCDashApiQueryDataFuctor(object):
  def __init__(self, cdashApiQueryUrl_expected, dataToReturn):
    self.cdashApiQueryUrl_expected = cdashApiQueryUrl_expected
    self.dataToReturn = dataToReturn
  def __call__(self, cdashApiQueryUrl):
    if cdashApiQueryUrl != self.cdashApiQueryUrl_expected:
      raise Exception(
        "Error, cdashApiQueryUrl='"+cdashApiQueryUrl+"' !="+\
        " cdashApiQueryUrl_expected='"+cdashApiQueryUrl_expected+"'!")
    return self.dataToReturn


# Helper script for creating test directories
def deleteThenCreateTestDir(testDir):
    outputCacheDir="test_getAndCacheCDashQueryDataOrReadFromCache_write_cache"
    if os.path.exists(testDir): shutil.rmtree(testDir)
    os.mkdir(testDir)


#############################################################################
#
# Test CDashQueryAnalizeReport.validateYYYYMMDD_pass1()
#
#############################################################################

class test_validateYYYYMMDD(unittest.TestCase):

  def test_pass1(self):
    yyyyymmdd = validateYYYYMMDD("2015-12-21")
    self.assertEqual(str(yyyyymmdd), "2015-12-21 00:00:00")

  def test_pass2(self):
    yyyyymmdd = validateYYYYMMDD("2015-12-01")
    self.assertEqual(str(yyyyymmdd), "2015-12-01 00:00:00")

  def test_pass3(self):
    yyyyymmdd = validateYYYYMMDD("2015-12-1")
    self.assertEqual(str(yyyyymmdd), "2015-12-01 00:00:00")

  def test_pass4(self):
    yyyyymmdd = validateYYYYMMDD("2015-01-1")
    self.assertEqual(str(yyyyymmdd), "2015-01-01 00:00:00")

  def test_pass4(self):
    yyyyymmdd = validateYYYYMMDD("2015-1-9")
    self.assertEqual(str(yyyyymmdd), "2015-01-09 00:00:00")

  def test_fail_empty(self):
    self.assertRaises(ValueError, validateYYYYMMDD,  "")

  def test_fail1(self):
    self.assertRaises(ValueError, validateYYYYMMDD,  "201512-21")

  def test_fail1(self):
    #yyyyymmdd = validateYYYYMMDD("201512-21")
    self.assertRaises(ValueError, validateYYYYMMDD,  "201512-21")


#############################################################################
#
# Test CDashQueryAnalizeReport.readCsvFileIntoListOfDicts()
#
#############################################################################

class test_readCsvFileIntoListOfDicts(unittest.TestCase):

  def test_col_3_row_2_expected_cols__pass(self):
    csvFileStr=\
        "col_0, col_1, col_2\n"+\
        "val_00, val_01, val_02\n"+\
        "val_10, val_11, val_12\n\n\n"  # Add extra blanks line for extra test!
    csvFileName = "readCsvFileIntoListOfDicts_col_3_row_2_expeced_cols_pass.csv"
    with open(csvFileName, 'w') as csvFileToWrite:
      csvFileToWrite.write(csvFileStr)
    listOfDicts = readCsvFileIntoListOfDicts(csvFileName, ['col_0', 'col_1', 'col_2'])
    listOfDicts_expected = \
      [
        { 'col_0' : 'val_00', 'col_1' : 'val_01', 'col_2' : 'val_02' },
        { 'col_0' : 'val_10', 'col_1' : 'val_11', 'col_2' : 'val_12' },
        ]
    self.assertEqual(len(listOfDicts), 2)
    for i in range(len(listOfDicts_expected)):
      self.assertEqual(listOfDicts[i], listOfDicts_expected[i])

  def test_col_3_row_2_no_expected_cols_pass(self):
    csvFileStr=\
        "col_0, col_1, col_2\n"+\
        "val_00, val_01, val_02\n"+\
        "val_10, val_11, val_12\n\n\n"  # Add extra blanks line for extra test!
    csvFileName = "readCsvFileIntoListOfDicts_col_3_row_2_no_expected_cols_pass.csv"
    with open(csvFileName, 'w') as csvFileToWrite:
      csvFileToWrite.write(csvFileStr)
    listOfDicts = readCsvFileIntoListOfDicts(csvFileName)
    listOfDicts_expected = \
      [
        { 'col_0' : 'val_00', 'col_1' : 'val_01', 'col_2' : 'val_02' },
        { 'col_0' : 'val_10', 'col_1' : 'val_11', 'col_2' : 'val_12' },
        ]
    self.assertEqual(len(listOfDicts), 2)
    for i in range(len(listOfDicts_expected)):
      self.assertEqual(listOfDicts[i], listOfDicts_expected[i])

  def test_too_few_expected_headers_fail(self):
    csvFileStr=\
        "wrong col, col_1, col_2\n"+\
        "val_00, val_01, val_02\n"
    csvFileName = "readCsvFileIntoListOfDicts_too_few_expected_headers_fail.csv"
    with open(csvFileName, 'w') as csvFileToWrite:
      csvFileToWrite.write(csvFileStr)
    #listOfDicts = readCsvFileIntoListOfDicts(csvFileName, ['col_0', 'col_1'])
    self.assertRaises(Exception, readCsvFileIntoListOfDicts,
      csvFileName, ['col_0', 'col_1'])

  def test_too_many_expected_headers_fail(self):
    csvFileStr=\
        "wrong col, col_1, col_2\n"+\
        "val_00, val_01, val_02\n"
    csvFileName = "readCsvFileIntoListOfDicts_too_many_expected_headers_fail.csv"
    with open(csvFileName, 'w') as csvFileToWrite:
      csvFileToWrite.write(csvFileStr)
    #listOfDicts = readCsvFileIntoListOfDicts(csvFileName,
    #  ['col_0', 'col_1', 'col_2', 'col3'])
    self.assertRaises(Exception, readCsvFileIntoListOfDicts,
      csvFileName, ['col_0', 'col_1', 'col_2', 'col3'])

  def test_wrong_expected_col_0_fail(self):
    csvFileStr=\
        "wrong col, col_1, col_2\n"+\
        "val_00, val_01, val_02\n"
    csvFileName = "readCsvFileIntoListOfDicts_wrong_expected_col_0_fail.csv"
    with open(csvFileName, 'w') as csvFileToWrite:
      csvFileToWrite.write(csvFileStr)
    #listOfDicts = readCsvFileIntoListOfDicts(csvFileName, ['col_0', 'col_1', 'col_2'])
    self.assertRaises(Exception, readCsvFileIntoListOfDicts,
      csvFileName, ['col_0', 'col_1', 'col_2'])

  def test_wrong_expected_col_1_fail(self):
    csvFileStr=\
        "col_0, wrong col, col_2\n"+\
        "val_00, val_01, val_02\n"
    csvFileName = "readCsvFileIntoListOfDicts_wrong_expected_col_1_fail.csv"
    with open(csvFileName, 'w') as csvFileToWrite:
      csvFileToWrite.write(csvFileStr)
    #listOfDicts = readCsvFileIntoListOfDicts(csvFileName, ['col_0', 'col_1', 'col_2'])
    self.assertRaises(Exception, readCsvFileIntoListOfDicts,
      csvFileName, ['col_0', 'col_1', 'col_2'])

  def test_col_3_row_2_bad_row_len_fail(self):
    csvFileStr=\
        "col_0, col_1, col_2\n"+\
        "val_00, val_01, val_02\n"+\
        "val_10, val_11, val_12, extra\n"
    csvFileName = "readCsvFileIntoListOfDicts_col_3_row_2_bad_row_len_fail.csv"
    with open(csvFileName, 'w') as csvFileToWrite:
      csvFileToWrite.write(csvFileStr)
    #listOfDicts = readCsvFileIntoListOfDicts(csvFileName)
    self.assertRaises(Exception, readCsvFileIntoListOfDicts, csvFileName)

  # ToDo: Add test for reading a CSV file with no rows

  # ToDo: Add test for reading an empty CSV file (no column headers)


#############################################################################
#
# Test CDashQueryAnalizeReport.getExpectedBuildsListfromCsvFile()
#
#############################################################################

class test_getExpectedBuildsListfromCsvFile(unittest.TestCase):

  def test_getExpectedBuildsListfromCsvFile(self):
    expectedBuildsCsvFileStr=\
        "group, site, buildname\n"+\
        "group1, site1, buildname1\n"+\
        "group1, site1, buildname2\n"+\
        "group2, site2, buildname2\n\n\n\n"
    csvFileName = "test_getExpectedBuildsListfromCsvFile.csv"
    with open(csvFileName, 'w') as csvFileToWrite:
      csvFileToWrite.write(expectedBuildsCsvFileStr)
    expectedBuildsList = getExpectedBuildsListfromCsvFile(csvFileName)
    expectedBuildsList_expected = \
      [
        { 'group' : 'group1', 'site' : 'site1', 'buildname' : 'buildname1' },
        { 'group' : 'group1', 'site' : 'site1', 'buildname' : 'buildname2' },
        { 'group' : 'group2', 'site' : 'site2', 'buildname' : 'buildname2' },
        ]
    self.assertEqual(len(expectedBuildsList), 3)
    for i in range(len(expectedBuildsList_expected)):
      self.assertEqual(expectedBuildsList[i], expectedBuildsList_expected[i])


#############################################################################
#
# Test CDashQueryAnalizeReport.getAndCacheCDashQueryDataOrReadFromCache()
#
#############################################################################

g_getAndCacheCDashQueryDataOrReadFromCache_data = {
  'keyname1' : "value1",
  'keyname2' : "value2",
   }

def dummyGetCDashData_for_getAndCacheCDashQueryDataOrReadFromCache(
  cdashQueryUrl_expected \
  ):
  if cdashQueryUrl_expected != "dummy-cdash-url":
    raise Exception("Error, cdashQueryUrl_expected != \'dummy-cdash-url\'")  
  return g_getAndCacheCDashQueryDataOrReadFromCache_data

class test_getAndCacheCDashQueryDataOrReadFromCache(unittest.TestCase):

  def test_getAndCacheCDashQueryDataOrReadFromCache_write_cache(self):
    outputCacheDir="test_getAndCacheCDashQueryDataOrReadFromCache_write_cache"
    outputCacheFile=outputCacheDir+"/cachedCDashQueryData.json"
    deleteThenCreateTestDir(outputCacheDir)
    mockExtractCDashApiQueryDataFuctor = MockExtractCDashApiQueryDataFuctor(
       "dummy-cdash-url", g_getAndCacheCDashQueryDataOrReadFromCache_data)
    cdashQueryData = getAndCacheCDashQueryDataOrReadFromCache(
      "dummy-cdash-url", outputCacheFile,
      useCachedCDashData=False,
      printCDashUrl=False,
      extractCDashApiQueryData_in=mockExtractCDashApiQueryDataFuctor
      )
    self.assertEqual(cdashQueryData, g_getAndCacheCDashQueryDataOrReadFromCache_data)
    cdashQueryData_cache = eval(open(outputCacheFile, 'r').read())
    self.assertEqual(cdashQueryData_cache, g_getAndCacheCDashQueryDataOrReadFromCache_data)

  def test_getAndCacheCDashQueryDataOrReadFromCache_read_cache(self):
    outputCacheDir="test_getAndCacheCDashQueryDataOrReadFromCache_read_cache"
    outputCacheFile=outputCacheDir+"/cachedCDashQueryData.json"
    deleteThenCreateTestDir(outputCacheDir)
    open(outputCacheFile, 'w').write(str(g_getAndCacheCDashQueryDataOrReadFromCache_data))
    cdashQueryData = getAndCacheCDashQueryDataOrReadFromCache(
      "dummy-cdash-url", outputCacheFile,
      useCachedCDashData=True,
      printCDashUrl=False,
      )
    self.assertEqual(cdashQueryData, g_getAndCacheCDashQueryDataOrReadFromCache_data)


#############################################################################
#
# Test CDashQueryAnalizeReport URL functions
#
#############################################################################

class test_CDashQueryAnalizeReport_UrlFuncs(unittest.TestCase):

  def test_getCDashIndexQueryUrl(self):
    cdashIndexQueryUrl = getCDashIndexQueryUrl(
      "site.com/cdash", "project-name", "2015-12-21", "filtercount=1&morestuff" )
    cdashIndexQueryUrl_expected = \
      "site.com/cdash/api/v1/index.php?project=project-name&date=2015-12-21&filtercount=1&morestuff"
    self.assertEqual(cdashIndexQueryUrl, cdashIndexQueryUrl_expected)

  def test_getCDashIndexBrowserUrl(self):
    cdashIndexQueryUrl = getCDashIndexBrowserUrl(
      "site.com/cdash", "project-name", "2015-12-21", "filtercount=1&morestuff" )
    cdashIndexQueryUrl_expected = \
      "site.com/cdash/index.php?project=project-name&date=2015-12-21&filtercount=1&morestuff"
    self.assertEqual(cdashIndexQueryUrl, cdashIndexQueryUrl_expected)

  def test_getCDashQueryTestsQueryUrl(self):
    cdashIndexQueryUrl = getCDashQueryTestsQueryUrl(
      "site.com/cdash", "project-name", "2015-12-21", "filtercount=1&morestuff" )
    cdashIndexQueryUrl_expected = \
      "site.com/cdash/api/v1/queryTests.php?project=project-name&date=2015-12-21&filtercount=1&morestuff"
    self.assertEqual(cdashIndexQueryUrl, cdashIndexQueryUrl_expected)

  def test_getCDashQueryTestsBrowserUrl(self):
    cdashIndexQueryUrl = getCDashQueryTestsBrowserUrl(
      "site.com/cdash", "project-name", "2015-12-21", "filtercount=1&morestuff" )
    cdashIndexQueryUrl_expected = \
      "site.com/cdash/queryTests.php?project=project-name&date=2015-12-21&filtercount=1&morestuff"
    self.assertEqual(cdashIndexQueryUrl, cdashIndexQueryUrl_expected)


#############################################################################
#
# Test CDashQueryAnalizeReport.collectCDashIndexBuildSummaryFields()
#
#############################################################################

# This summary build has just the minimal required fields
g_singleBuildPassesSummary = {
  'group':'groupName',
  'site':'siteName',
  'buildname':"buildName",
  'update': {'errors':0},
  'configure':{'error': 0},
  'compilation':{'error':0},
  'test': {'fail':0, 'notrun':0},
  }

# Single build with extra stuff
g_singleBuildPassesRaw = {
  'site':'siteName',
  'buildname':"buildName",
  'update': {'errors':0},
  'configure':{'error': 0},
  'compilation':{'error':0},
  'test': {'fail':0, 'notrun':0},
  'extra-stuff':'stuff',
  }

class test_collectCDashIndexBuildSummaryFields(unittest.TestCase):

  def test_collectCDashIndexBuildSummaryFields_full(self):
    buildSummary = collectCDashIndexBuildSummaryFields(g_singleBuildPassesRaw, "groupName")
    self.assertEqual(buildSummary, g_singleBuildPassesSummary)

  def test_collectCDashIndexBuildSummaryFields_missing_update(self):
    fullCDashIndexBuild_in = copy.deepcopy(g_singleBuildPassesRaw)
    del fullCDashIndexBuild_in['update']
    buildSummary = collectCDashIndexBuildSummaryFields(fullCDashIndexBuild_in, "groupName")
    buildSummary_expected = copy.deepcopy(g_singleBuildPassesSummary)
    del buildSummary_expected['update']
    self.assertEqual(buildSummary, buildSummary_expected)

  def test_collectCDashIndexBuildSummaryFields_missing_configure(self):
    fullCDashIndexBuild_in = copy.deepcopy(g_singleBuildPassesRaw)
    del fullCDashIndexBuild_in['configure']
    buildSummary = collectCDashIndexBuildSummaryFields(fullCDashIndexBuild_in, "groupName")
    buildSummary_expected = copy.deepcopy(g_singleBuildPassesSummary)
    del buildSummary_expected['configure']
    self.assertEqual(buildSummary, buildSummary_expected)


#############################################################################
#
# Test CDashQueryAnalizeReport.getCDashIndexBuildsSummary()
#
#############################################################################

# This file was taken from an actual CDash query and then modified a little to
# make for better testing.
g_fullCDashIndexBuilds = \
  eval(open(g_testBaseDir+'/cdash_index_query_data.txt', 'r').read())
#print("g_fullCDashIndexBuilds:")
#g_pp.pprint(g_fullCDashIndexBuilds)

# This file was manually created from the above file to match what the reduced
# builds should be.
g_summaryCDashIndexBuilds_expected = \
  eval(open(g_testBaseDir+'/cdash_index_query_data.summary.txt', 'r').read())
#print("g_summaryCDashIndexBuilds_expected:")
#g_pp.pprint(g_summaryCDashIndexBuilds_expected)

class test_getCDashIndexBuildsSummary(unittest.TestCase):

  def test_getCDashIndexBuildsSummary(self):
    summaryCDashIndexBuilds = getCDashIndexBuildsSummary(g_fullCDashIndexBuilds)
    #pp.pprint(summaryCDashIndexBuilds)
    self.assertEqual(
      len(summaryCDashIndexBuilds), len(g_summaryCDashIndexBuilds_expected))
    for i in range(0, len(summaryCDashIndexBuilds)):
      self.assertEqual(summaryCDashIndexBuilds[i], g_summaryCDashIndexBuilds_expected[i])


#############################################################################
#
# Test CDashQueryAnalizeReport.createBuildLookupDict()
#
#############################################################################

g_buildsListForExpectedBuilds = [
  { 'group':'group1', 'site':'site1', 'buildname':'build1', 'data':'val1' },
  { 'group':'group1', 'site':'site1', 'buildname':'build2', 'data':'val2' },
  { 'group':'group1', 'site':'site2', 'buildname':'build3', 'data':'val3' },
  { 'group':'group2', 'site':'site1', 'buildname':'build1', 'data':'val4' },
  { 'group':'group2', 'site':'site3', 'buildname':'build4', 'data':'val5' },
  ]

g_buildLookupDictForExpectedBuilds = {
  'group1' : {
    'site1' : {
      'build1':{'group':'group1','site':'site1','buildname':'build1','data':'val1'},
      'build2':{'group':'group1','site':'site1','buildname':'build2','data':'val2'},
      },
    'site2' : {
      'build3':{'group':'group1','site':'site2','buildname':'build3','data':'val3'},
      },
    },
  'group2' : {
    'site1' : {
      'build1':{'group':'group2','site':'site1','buildname':'build1','data':'val4'},
      },
    'site3' : {
      'build4':{'group':'group2','site':'site3','buildname':'build4','data':'val5'},
      },
    },
  }

class test_createBuildLookupDict(unittest.TestCase):

  def test_1(self):
    buildLookupDict = createBuildLookupDict(g_buildsListForExpectedBuilds)
    #print("\nbuildLookupDict:")
    #g_pp.pprint(buildLookupDict)
    #print("\ng_buildLookupDictForExpectedBuilds:")
    #g_pp.pprint(g_buildLookupDictForExpectedBuilds)
    self.assertEqual(buildLookupDict, g_buildLookupDictForExpectedBuilds)


#############################################################################
#
# Test CDashQueryAnalizeReport.lookupBuildSummaryGivenLookupDict()
#
#############################################################################

def gsb(groupName, siteName, buildName):
  return {'group':groupName, 'site':siteName, 'buildname':buildName}

def lookupData(groupName, siteName, buildName, buildLookupDict):
  buildDict = lookupBuildSummaryGivenLookupDict(
    gsb(groupName, siteName, buildName), buildLookupDict)
  if not buildDict : return None
  return buildDict.get('data')
     
class test_lookupBuildSummaryGivenLookupDict(unittest.TestCase):

  def test_1(self):
    blud = createBuildLookupDict(g_buildsListForExpectedBuilds)
    self.assertEqual(lookupData('group1','site1','build1', blud), 'val1')
    self.assertEqual(lookupData('group1','site1','build2', blud), 'val2')
    self.assertEqual(lookupData('group1','site2','build3', blud), 'val3')
    self.assertEqual(lookupData('group2','site1','build1', blud), 'val4')
    self.assertEqual(lookupData('group2','site3','build4', blud), 'val5')
    self.assertEqual(lookupData('group2','site3','build1', blud), None)
    self.assertEqual(lookupData('group2','site4','build1', blud), None)
    self.assertEqual(lookupData('group3','site1','build1', blud), None)


#############################################################################
#
# Test CDashQueryAnalizeReport.getMissingExpectedBuildsList()
#
#############################################################################
     
class test_getMissingExpectedBuildsList(unittest.TestCase):

  def test_1(self):
    blud = copy.deepcopy(createBuildLookupDict(g_buildsListForExpectedBuilds))
    blud.get('group2').get('site3').get('build4').update({'test':{'pass':1}})
    expectedBuildsList = [
      gsb('group1', 'site2', 'build3'),  # Build exists but missing tests
      gsb('group2', 'site3', 'build4'),  # Build exists and has tests
      gsb('group2', 'site3', 'build8'),  # Build missing all-together
      ]
    missingExpectedBuildsList = getMissingExpectedBuildsList(blud, expectedBuildsList)
    self.assertEqual(len(missingExpectedBuildsList), 2)
    self.assertEqual(missingExpectedBuildsList[0],
      { 'group':'group1', 'site':'site2', 'buildname':'build3',
        'status':"Build exists but no test results" } )
    self.assertEqual(missingExpectedBuildsList[1],
      { 'group':'group2', 'site':'site3', 'buildname':'build8',
        'status':"Build not found on CDash" } )


#############################################################################
#
# Test CDashQueryAnalizeReport.downloadBuildsOffCDashAndSummarize
#
#############################################################################

class test_downloadBuildsOffCDashAndSummarize(unittest.TestCase):

  def test_allBuilds(self):
    # Define dummy CDash filter data
    cdashUrl = "site.come/cdash"
    projectName = "projectName"
    date = "YYYY-MM-DD"
    buildFilters = "build&filters"
    # Define mock object to return the data
    mockExtractCDashApiQueryDataFuctor = MockExtractCDashApiQueryDataFuctor(
       getCDashIndexQueryUrl(cdashUrl,  projectName, date, buildFilters),
       g_fullCDashIndexBuilds )
    # Get the mock data off of CDash
    summaryCDashIndexBuilds = downloadBuildsOffCDashAndSummarize(
      cdashUrl,  projectName, date, buildFilters,
      verbose=False, cdashQueriesCacheDir=None,
      useCachedCDashData=False,
      extractCDashApiQueryData_in=mockExtractCDashApiQueryDataFuctor )
    # Assert the data returned is correct
    #g_pp.pprint(summaryCDashIndexBuilds)
    self.assertEqual(
      len(summaryCDashIndexBuilds), len(g_summaryCDashIndexBuilds_expected))
    for i in range(0, len(summaryCDashIndexBuilds)):
      self.assertEqual(summaryCDashIndexBuilds[i], g_summaryCDashIndexBuilds_expected[i])


#############################################################################
#
# Test CDashQueryAnalizeReport.cdashIndexBuildPasses()
#
#############################################################################

class test_cdashIndexBuildPasses(unittest.TestCase):

  def test_cdashIndexBuildPasses_pass(self):
    build = copy.deepcopy(g_singleBuildPassesSummary)
    self.assertEqual(cdashIndexBuildPasses(build), True)

  def test_cdashIndexBuildPasses_update_fail(self):
    build = copy.deepcopy(g_singleBuildPassesSummary)
    build['update']['errors'] = 1
    self.assertEqual(cdashIndexBuildPasses(build), False)

  def test_cdashIndexBuildPasses_configure_fail(self):
    build = copy.deepcopy(g_singleBuildPassesSummary)
    build['configure']['error'] = 1
    self.assertEqual(cdashIndexBuildPasses(build), False)

  def test_cdashIndexBuildPasses_compilation_fail(self):
    build = copy.deepcopy(g_singleBuildPassesSummary)
    build['compilation']['error'] = 1
    self.assertEqual(cdashIndexBuildPasses(build), False)

  def test_cdashIndexBuildPasses_test_fail_fail(self):
    build = copy.deepcopy(g_singleBuildPassesSummary)
    build['test']['fail'] = 1
    self.assertEqual(cdashIndexBuildPasses(build), False)

  def test_cdashIndexBuildPasses_test_notrun_fail(self):
    build = copy.deepcopy(g_singleBuildPassesSummary)
    build['test']['notrun'] = 1
    self.assertEqual(cdashIndexBuildPasses(build), False)

  def test_cdashIndexBuildsPass_1_pass(self):
    builds = [copy.deepcopy(g_singleBuildPassesSummary)]
    (buildPasses, buildFailedMsg) = cdashIndexBuildsPass(builds)
    self.assertEqual(buildPasses, True)
    self.assertEqual(buildFailedMsg, "")

  def test_cdashIndexBuildsPass_1_fail(self):
    build = copy.deepcopy(g_singleBuildPassesSummary)
    build['compilation']['error'] = 1
    builds = [build]
    (buildPasses, buildFailedMsg) = cdashIndexBuildsPass(builds)
    self.assertEqual(buildPasses, False)
    self.assertEqual(buildFailedMsg, "Error, the build " + sorted_dict_str(build) +
                     " failed!")

  def test_cdashIndexBuildsPass_2_pass(self):
    build = copy.deepcopy(g_singleBuildPassesSummary)
    builds = [build, build]
    (buildPasses, buildFailedMsg) = cdashIndexBuildsPass(builds)
    self.assertEqual(buildPasses, True)
    self.assertEqual(buildFailedMsg, "")

  def test_cdashIndexBuildsPass_2_fail_1(self):
    build = copy.deepcopy(g_singleBuildPassesSummary)
    buildFailed = copy.deepcopy(g_singleBuildPassesSummary)
    buildFailed['buildname'] = "failedBuild"
    buildFailed['compilation']['error'] = 1
    builds = [buildFailed, build]
    (buildPasses, buildFailedMsg) = cdashIndexBuildsPass(builds)
    self.assertEqual(buildPasses, False)
    self.assertEqual(buildFailedMsg, "Error, the build " +
                     sorted_dict_str(buildFailed) + " failed!")

  def test_cdashIndexBuildsPass_2_fail_2(self):
    build = copy.deepcopy(g_singleBuildPassesSummary)
    buildFailed = copy.deepcopy(g_singleBuildPassesSummary)
    buildFailed['buildname'] = "failedBuild"
    buildFailed['compilation']['error'] = 1
    builds = [build, buildFailed]
    (buildPasses, buildFailedMsg) = cdashIndexBuildsPass(builds)
    self.assertEqual(buildPasses, False)
    self.assertEqual(buildFailedMsg, "Error, the build " +
                     sorted_dict_str(buildFailed) + " failed!")

  def test_getCDashIndexBuildNames(self):
    build1 = copy.deepcopy(g_singleBuildPassesSummary)
    build1['buildname'] = "build1"
    build2 = copy.deepcopy(g_singleBuildPassesSummary)
    build2['buildname'] = "build2"
    build3 = copy.deepcopy(g_singleBuildPassesSummary)
    build3['buildname'] = "build3"
    builds = [build1, build2, build3]
    buildNames_expected = [ "build1", "build2", "build3" ]
    self.assertEqual(getCDashIndexBuildNames(builds), buildNames_expected)


#############################################################################
#
# Test CDashQueryAnalizeReport.doAllExpectedBuildsExist()
#
#############################################################################

class test_doAllExpectedBuildsExist(unittest.TestCase):

  def test_doAllExpectedBuildsExist_1_pass(self):
    buildNames = ["build1"]
    expectedBuildNames = ["build1"]
    (allExpectedBuildsExist, errMsg) = \
      doAllExpectedBuildsExist(buildNames, expectedBuildNames)
    self.assertEqual(errMsg, "")
    self.assertEqual(allExpectedBuildsExist, True)

  def test_doAllExpectedBuildsExist_1_fail(self):
    buildNames = ["build1"]
    expectedBuildNames = ["build2"]
    (allExpectedBuildsExist, errMsg) = \
      doAllExpectedBuildsExist(buildNames, expectedBuildNames)
    self.assertEqual(errMsg,
      "Error, the expected build 'build2' does not exist in the list of builds ['build1']")
    self.assertEqual(allExpectedBuildsExist, False)

  def test_doAllExpectedBuildsExist_2_2_a_pass(self):
    buildNames = ["build1", "build2"]
    expectedBuildNames = ["build1", "build2"]
    (allExpectedBuildsExist, errMsg) = \
      doAllExpectedBuildsExist(buildNames, expectedBuildNames)
    self.assertEqual(errMsg, "")
    self.assertEqual(allExpectedBuildsExist, True)

  def test_doAllExpectedBuildsExist_2_2_b_fail(self):
    buildNames = ["build2", "build1"]
    expectedBuildNames = ["build1", "build2"]
    (allExpectedBuildsExist, errMsg) = \
      doAllExpectedBuildsExist(buildNames, expectedBuildNames)
    self.assertEqual(errMsg, "")
    self.assertEqual(allExpectedBuildsExist, True)

  def test_doAllExpectedBuildsExist_2_1_pass(self):
    buildNames = ["build1", "build2"]
    expectedBuildNames = ["build1"]
    (allExpectedBuildsExist, errMsg) = \
      doAllExpectedBuildsExist(buildNames, expectedBuildNames)
    self.assertEqual(errMsg, "")
    self.assertEqual(allExpectedBuildsExist, True)

  def test_doAllExpectedBuildsExist_2_1_fail(self):
    buildNames = ["build1", "build2"]
    expectedBuildNames = ["build3"]
    (allExpectedBuildsExist, errMsg) = \
      doAllExpectedBuildsExist(buildNames, expectedBuildNames)
    self.assertEqual(errMsg,
      "Error, the expected build 'build3' does not exist in the list of builds ['build1', 'build2']")
    self.assertEqual(allExpectedBuildsExist, False)

  def test_doAllExpectedBuildsExist_1_2_a_fail(self):
    buildNames = ["build1"]
    expectedBuildNames = ["build1", "build2"]
    (allExpectedBuildsExist, errMsg) = \
      doAllExpectedBuildsExist(buildNames, expectedBuildNames)
    self.assertEqual(errMsg,
      "Error, the expected build 'build2' does not exist in the list of builds ['build1']")
    self.assertEqual(allExpectedBuildsExist, False)

  def test_doAllExpectedBuildsExist_1_2_b_fail(self):
    buildNames = ["build1"]
    expectedBuildNames = ["build2", "build1"]
    (allExpectedBuildsExist, errMsg) = \
      doAllExpectedBuildsExist(buildNames, expectedBuildNames)
    self.assertEqual(errMsg,
      "Error, the expected build 'build2' does not exist in the list of builds ['build1']")
    self.assertEqual(allExpectedBuildsExist, False)

  def test_cdashIndexBuildsPassAndExpectedExist_1_pass(self):
    build1 = copy.deepcopy(g_singleBuildPassesSummary)
    build1['buildname'] = "build1"
    builds = [ build1 ]
    expectedBuildNames = ["build1"]
    (cdashIndexBuildsPassAndExpectedExist_passed, errMsg) = \
      cdashIndexBuildsPassAndExpectedExist(builds, expectedBuildNames)
    self.assertEqual(errMsg,
      "")
    self.assertEqual(cdashIndexBuildsPassAndExpectedExist_passed, True)

  def test_cdashIndexBuildsPassAndExpectedExist_1_build_fail(self):
    build1 = copy.deepcopy(g_singleBuildPassesSummary)
    build1['group'] = "group1"
    build1['site'] = "site1"
    build1['buildname'] = "build1"
    build1['configure']['error'] = 5
    builds = [ build1 ]
    expectedBuildNames = ["build1"]
    (cdashIndexBuildsPassAndExpectedExist_passed, errMsg) = \
      cdashIndexBuildsPassAndExpectedExist(builds, expectedBuildNames)
    expectedErrMsg = \
      "Error, the build " + \
      sorted_dict_str({
        'group':'group1', 'site':'site1', 'buildname': 'build1',
        'test': {'notrun': 0, 'fail': 0},
        'compilation': {'error': 0}, 'update': {'errors': 0},
        'configure': {'error': 5}})+ \
      " failed!"
    self.assertEqual(errMsg, expectedErrMsg)
    self.assertEqual(cdashIndexBuildsPassAndExpectedExist_passed, False)
    # NOTE: Above we build the dict then convert to a string so that it will
    # match the print out of the dict that is produced by the code itself.
    # This is needed because the order of dict items changes between different
    # versions of Python and even different platforms (see TriBITS Issue
    # #119).

  def test_cdashIndexBuildsPassAndExpectedExist_1_missing_expected_build(self):
    build1 = copy.deepcopy(g_singleBuildPassesSummary)
    build1['buildname'] = "build1"
    builds = [ build1 ]
    expectedBuildNames = ["build2"]
    (cdashIndexBuildsPassAndExpectedExist_passed, errMsg) = \
      cdashIndexBuildsPassAndExpectedExist(builds, expectedBuildNames)
    self.assertEqual(errMsg,
      "Error, the expected build 'build2' does not exist in the list of builds ['build1']")
    self.assertEqual(cdashIndexBuildsPassAndExpectedExist_passed, False)


#############################################################################
#
# Test CDashQueryAnalizeReport.queryCDashAndDeterminePassFail()
#
#############################################################################

g_extractCDashApiQueryData_builds = None

def dummyExtractCDashApiQueryData(cdashQueryUrl_expected):
  return g_extractCDashApiQueryData_builds

class test_queryCDashAndDeterminePassFail(unittest.TestCase):

  def test_queryCDashAndDeterminePassFail_1_pass(self):
    build1 = copy.deepcopy(g_singleBuildPassesSummary)
    build1['buildname'] = "build1"
    fullCDashIndexBuilds = {
      'buildgroups':[
        {'name':'group1', 'builds':[build1]}
        ]
      }
    global g_extractCDashApiQueryData_builds
    g_extractCDashApiQueryData_builds = fullCDashIndexBuilds 
    expectedBuildNames = ["build1"]
    (allPassed, errMsg) = queryCDashAndDeterminePassFail(
      "https://casl-dev.ornl.gov/testing", "VERA", "2015-12-21", "dummy-filter-fields",
      expectedBuildNames, False, dummyExtractCDashApiQueryData)
    self.assertEqual(errMsg, "")
    self.assertEqual(allPassed, True)

  def test_queryCDashAndDeterminePassFail_2_pass(self):
    build1 = copy.deepcopy(g_singleBuildPassesSummary)
    build1['buildname'] = "build1"
    build2 = copy.deepcopy(g_singleBuildPassesSummary)
    build2['buildname'] = "build2"
    fullCDashIndexBuilds = {
      'buildgroups':[
        {'name':'group1', 'builds':[build1]},
        {'name':'group2', 'builds':[build2]}
        ]
      }
    global g_extractCDashApiQueryData_builds
    g_extractCDashApiQueryData_builds = fullCDashIndexBuilds 
    expectedBuildNames = ["build1", "build2"]
    (allPassed, errMsg) = queryCDashAndDeterminePassFail(
      "https://casl-dev.ornl.gov/testing", "VERA", "2015-12-21", "dummy-filter-fields",
      expectedBuildNames, False, dummyExtractCDashApiQueryData)
    self.assertEqual(errMsg, "")
    self.assertEqual(allPassed, True)

  def test_queryCDashAndDeterminePassFail_1_missing_expected(self):
    build1 = copy.deepcopy(g_singleBuildPassesSummary)
    build1['buildname'] = "build1"
    fullCDashIndexBuilds = {
      'buildgroups':[
        {'name':'group1', 'builds':[build1]}
        ]
      }
    global g_extractCDashApiQueryData_builds
    g_extractCDashApiQueryData_builds = fullCDashIndexBuilds 
    expectedBuildNames = ["missing"]
    (allPassed, errMsg) = queryCDashAndDeterminePassFail(
      "https://casl-dev.ornl.gov/testing", "VERA", "2015-12-21", "dummy-filter-fields",
      expectedBuildNames, False, dummyExtractCDashApiQueryData)
    self.assertEqual(errMsg,
      "Error, the expected build 'missing' does not exist in the list of builds ['build1']")
    self.assertEqual(allPassed, False)

  def test_queryCDashAndDeterminePassFail_1_fail(self):
    build1 = copy.deepcopy(g_singleBuildPassesSummary)
    build1['buildname'] = "build1"
    build1['test']['fail'] = 3
    fullCDashIndexBuilds = {
      'buildgroups':[
        {'name':'group1', 'builds':[build1]}
        ]
      }
    global g_extractCDashApiQueryData_builds
    g_extractCDashApiQueryData_builds = fullCDashIndexBuilds 
    expectedBuildNames = ["build1"]
    (allPassed, errMsg) = queryCDashAndDeterminePassFail(
      "https://casl-dev.ornl.gov/testing", "VERA", "2015-12-21", "dummy-filter-fields",
      expectedBuildNames, False, dummyExtractCDashApiQueryData)
    expectedErrMsg = \
      "Error, the build " + \
      sorted_dict_str({
        u'group':'group1', u'site':'siteName', u'buildname': 'build1',
        u'test': {'fail': 3, 'notrun': 0},
        u'compilation': {'error': 0}, u'update': {'errors': 0},
        u'configure': {'error': 0}}) + \
      " failed!"
    self.assertEqual(errMsg, expectedErrMsg)
    self.assertEqual(allPassed, False)
    # NOTE: See note about dict keys ordering in above test (see TriBITS Issue
    # #119).

  def test_queryCDashAndDeterminePassFail_2_fail(self):
    build1 = copy.deepcopy(g_singleBuildPassesSummary)
    build1['buildname'] = "build1"
    build2 = copy.deepcopy(g_singleBuildPassesSummary)
    build2['buildname'] = "build2"
    build2['test']['notrun'] = 2
    fullCDashIndexBuilds = {
      'buildgroups':[
        {'name':'group1', 'builds':[build1]},
        {'name':'group2', 'builds':[build2]}
        ]
      }
    global g_extractCDashApiQueryData_builds
    g_extractCDashApiQueryData_builds = fullCDashIndexBuilds 
    expectedBuildNames = ["build1", "build2"]
    (allPassed, errMsg) = queryCDashAndDeterminePassFail(
      "https://casl-dev.ornl.gov/testing", "VERA", "2015-12-21", "dummy-filter-fields",
      expectedBuildNames, False, dummyExtractCDashApiQueryData)
    expectedErrMsg = \
      "Error, the build " + \
      sorted_dict_str({
        u'group':'group2', u'site':'siteName', u'buildname': 'build2',
        u'test': {'fail': 0, 'notrun': 2},
        u'compilation': {'error': 0}, u'update': {'errors': 0},
        u'configure': {'error': 0}}) + \
      " failed!"
    self.assertEqual(errMsg, expectedErrMsg)
    self.assertEqual(allPassed, False)
    # NOTE: See note about dict keys ordering in above test (see TriBITS Issue
    # #119).


#############################################################################
#
# Test CDashQueryAnalizeReport.createHtmlTableStr()
#
#############################################################################

def createTestTableRowColumnData(data1, data2, data3):
  return { 'key1':data1, 'key2':data2, 'key3':data3 }

class test_createHtmlTableStr(unittest.TestCase):
  
  # Check that the contents are put in the right place, the correct alignment,
  # correct handling of non-string data, etc.
  def test_3x3_table_correct_contents(self):
    tcd = TableColumnData
    trd = createTestTableRowColumnData
    colData = [
      tcd('key3', "Data 3"),
      tcd('key1', "Data 1"),
      tcd('key2', "Data 2", "right"),  # Alignment and non-string dat3
      ]
    rowData = [
      trd("r1d1", 1, "r1d3"),
      trd("r2d1", 2, "r2d3"),
      trd("r3d1", 3, "r3d3"),
      ]
    htmlTable = createHtmlTableStr("My great data", colData, rowData,
      htmlStyle="my_style",  # Test custom table style
      #htmlStyle=None,       # Uncomment to view this style
      #htmlTableStyle="",    # Uncomment to view this style
      )
    #print(htmlTable)
    #with open("test_3x2_table.html", 'w') as outFile: outFile.write(htmlTable)
    # NOTE: Above, uncomment the htmlStyle=None, ... line and the print and
    # file write commands to view the formatted table in a browser to see if
    # this gets the data right and you like the default table style.
    htmlTable_expected = \
r"""<style>my_style</style>
<h3>My great data</h3>
<table style="width:100%">

<tr>
<th>Data 3</th>
<th>Data 1</th>
<th>Data 2</th>
</tr>

<tr>
<td align="left">r1d3</td>
<td align="left">r1d1</td>
<td align="right">1</td>
</tr>

<tr>
<td align="left">r2d3</td>
<td align="left">r2d1</td>
<td align="right">2</td>
</tr>

<tr>
<td align="left">r3d3</td>
<td align="left">r3d1</td>
<td align="right">3</td>
</tr>

</table>
"""
    self.assertEqual(htmlTable, htmlTable_expected)

  # Check the correct default table style is set
  def test_1x2_table_correct_style(self):
    tcd = TableColumnData
    colData = [  tcd('key1', "Data 1") ]
    rowData = [ {'key1':'data1'} ]
    htmlTable = createHtmlTableStr("My great data", colData, rowData, htmlTableStyle="")
    #print(htmlTable)
    #with open("test_1x2_table_style.html", 'w') as outFile: outFile.write(htmlTable)
    # NOTE: Above, uncomment the print and file write to view the formatted
    # table in a browser to see if this gets the data right and you like the
    # default table style.
    htmlTable_expected = \
r"""<style>table, th, td {
  padding: 5px;
  border: 1px solid black;
  border-collapse: collapse;
}
tr:nth-child(even) {background-color: #eee;}
tr:nth-child(odd) {background-color: #fff;}
</style>
<h3>My great data</h3>
<table >

<tr>
<th>Data 1</th>
</tr>

<tr>
<td align="left">data1</td>
</tr>

</table>
"""
    self.assertEqual(htmlTable, htmlTable_expected)






#############################################################################
#
# Test CDashQueryAnalizeReport.createCDashDataSummaryHtmlTableStr()
#
#############################################################################

#class test_createCDashDataSummaryHtmlTableStr(unittest.TestCase):


# ToDo: Test with limitRowsToDisplay > len(rowDataList)

# ToDo: Test with limitRowsToDisplay == len(rowDataList)

# ToDo: Test with limitRowsToDisplay < len(rowDataList)

# ToDo: Test with now rows and therefore now table printed




#
# Run the unit tests!
#

if __name__ == '__main__':

  unittest.main()