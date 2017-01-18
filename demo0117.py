# this script is a revision of demo0116_2.py
# it should help me generate pie chart labeled with drug name
# and show 5 pie chart among 5 years to show the trend.
# steps:
# 1. load drug file
# 2. per year,
#   2.1 load OO-CD records, construct patientl
#   2.2 draw pie chart and print demo report .
import json
import os
import re
import sys
from Operations import *
import drugBag
import patient
import NHIRDSelector
import NHIRDParser
import NHIRDPieChart
from colors import red
#define NHIRD fmt
myHV_fmt = [
    ('ID',1,32),
    ('ICD9CM_CODE',33,37),
    ('DEATH_MARK', 54, 54),
    ('DEATH_DATE', 55, 62),
    ('APPL_DATE', 38, 45),
    ('RECV_DATE', 46, 53),
    ('VALID_E_DATE', 63, 70),
]
myCD101_fmt = [
    ['ID_STR', 1, 57], 
    ['ID', 58, 89], 
    ['ACODE_ICD9_1', 90, 104], 
    ['ACODE_ICD9_2',105, 119], 
    ['ACODE_ICD9_3', 120, 134]
] 
myCD93to100_fmt = [
    ['ID_STR', 1, 57], 
    ['ID', 58, 89], 
    ['ACODE_ICD9_1', 90, 94], 
    ['ACODE_ICD9_2',95, 99], 
    ['ACODE_ICD9_3', 100, 104]
]
myOO101_fmt=[
    ['ID_STR', 1, 57], 
    ['ORDER_TYPE', 58, 58], 
    ['DRUG_NO', 59, 70],
    ['APPL_DATE',42,49]
] 
myOO96to100_fmt= [
    ['ID_STR', 1, 57], 
    ['ORDER_TYPE', 58, 58], 
    ['DRUG_NO', 59, 70],
    ['APPL_DATE',42,49]
]
#define my rule to filter data
ICD9_include = {
    'breast cancer':set((
        '174',
        '1740',
        '1741',
        '1742',
        '1743',
        '1744',
        '1745',
        '1746',
        '1748',
        '1749',
        '175',
        '1750',
        '1759',
    )),
    'lung cancer': set((
        '162', 
        '1620', 
        '1622', 
        '1623', 
        '1624', 
        '1625', 
        '1628', 
        '1629', 
    )),
    }
ICD9_include['total'] = ICD9_include['breast cancer'] | ICD9_include['lung cancer']
def getThisYearCD(yr, datadir):
    global patientl
    def checkNewPatient(l):
        Id = npc_cd.parser.getByTag(l,'ID')
        if not patientl.get(Id,None):
            patientl[Id] = patient.patient(Id,drugMode = 'drugHandler')
    if int(yr) >= 2012:
        cdparser = NHIRDParser.NHIRDParser(myCD101_fmt)
    else:
        cdparser = NHIRDParser.NHIRDParser(myCD93to100_fmt)
    npc_cd =  NHIRDPieChart.NHIRDPieChart(cdparser)
    npc_cd.ontheflyA = checkNewPatient
    regex = '^R.*%4s$' % yr
    for d in filter(
        lambda x : re.match(regex,x),
        os.listdir(datadir)
        ):
        npc_cd.read(
            '/'.join([
            datadir,
            d,'cd.dat'])
        )
    return npc_cd
def getThisYearOO(yr, datadir,CDmapID):
    global patientl
    global dh
    def updatedrug(l):
        Id, drug_name = \
            CDmapID[npc_oo.parser.getByTag(l, 'ID_STR')],\
            dh.name(npc_oo.parser.getByTag(l, 'DRUG_NO').strip())
        if not drug_name:
            sys.stderr.write('unexpected drug no : %s\n' % \
                npc_oo.parser.getByTag(l, 'DRUG_NO')
            )
            return
        drugset = patientl[Id].drugs()
        drugset |= set([drug_name])

    if int(yr) >= 2012:
        ooparser = NHIRDParser.NHIRDParser(myOO101_fmt)
    else:
        ooparser = NHIRDParser.NHIRDParser(myOO96to100_fmt)
    seqs = set(CDmapID.keys())
    regex = '^R.*%4s$' % yr
    npc_oo =  NHIRDPieChart.NHIRDPieChart(ooparser)
    npc_oo.ontheflyA = updatedrug
    for d in filter(
        lambda x : re.match(regex,x),
        os.listdir(datadir)
        ):
        npc_oo.read(
            '/'.join([
            datadir,
            d,'oo.dat'])
        )
    return npc_oo
    

if len(sys.argv)<4 :
    #  argv[1] : drugnames.txt argv[2] : data dir argv[3] : output json file as
    #  report argv[4]: plot file dir 
    sys.stderr.write('at least three input files/ one output file need\n')
    exit(7)
print 'in this script, we don\'t interested in patient count.' 
dh = drugBag.drugHandler(json.load(open(sys.argv[1])))
patientl = {}
res = {}
# use 2010-2013 CDOO construct d - d transition
for year in ['2009','2010','2011','2012','2013',]:
    #though the strategy of CD-OO file extraction here is not very efficient,
    #in order to meet the requirement of agile development spirit, I decide to
    #omit the minor defect.
    patientl = {}
    cd = getThisYearCD(year,sys.argv[2])
    CDmapID = {}
    for r in cd.repo:
        i = cd.parser.getByTag(r, 'ID')
        CDmapID[cd.parser.getByTag(r,'ID_STR')] = i
        patientl[i].addCD(r)
    oo = getThisYearOO(year,sys.argv[2],CDmapID)
    #arrange patienl into barchart accept format
    res[year] = {}
    for p in patientl.values():
        if len(p.drugs()) > 1:        
            tag = '_%skinds' % len(p.drugs())
            res[year][tag] = res[year].get(tag,0) + 1
        else:
            tag = list(p.drugs())[0]
            res[year][tag] = res[year].get(tag,0) + 1
#    BarChartFromDict(res[year], sys.argv[4] + '/' + year + '.png')
    PieChartFromDict(res[year], sys.argv[4] + '/' + year + '.png')
    #store into res
    res[year]['_total'] = len(patientl.keys())

# conclude d - d interactions into reports
# store report in json format
outjson = open(sys.argv[3], 'w')
json.dump(res,outjson,sort_keys=True,indent=4)
outjson.close()
