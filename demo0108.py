import sys
import NHIRDSelector
import NHIRDParser
import NHIRDPieChart
from colors import red
#define NHIRD fmt
HV_fmt = [
    ('ID',1,32),
    ('ICD9CM_CODE',33,37),
]
CD101_fmt = [
    ('ID',92,123),
    ('SEQ_NO',52,57)
]
CD93to100_fmt = [
    ('ID',92,123),
    ('SEQ_NO',52,57)
]
OO101_fmt= [
    ('SEQ_NO',52,57)
]
OO96to100_fmt= [
    ('SEQ_NO',52,57)
]
#define my rule to filter data
ICD9_include = (
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
)


if len(sys.argv)<3 :
    #  argv[1] : HV file argv[2] : CD file argv[3] : OO file
    sys.stderr.write('at least two input file need\n')
    exit(7)
npc_hv = NHIRDPieChart.NHIRDPieChart(
    NHIRDParser.NHIRDParser(HV_fmt)
)
npc_hv.Filter = lambda x: npc_hv.parser.getByTag(x, 'ICD9CM_CODE').strip() in\
ICD9_include
npc_hv.read(sys.argv[1])
ids = npc_hv.pieInformationDict('ID').keys()
print 'length of ids is %s ' % ids

npc_cd = NHIRDPieChart.NHIRDPieChart(
    NHIRDParser.NHIRDParser(CD101_fmt)
)
npc_cd.Filter = lambda x: npc_cd.parser.getByTag(x, 'ID') in\
ids
npc_cd.read(sys.argv[2])
seqs = npc_cd.pieInformationDict('SEQ_NO').keys()
print 'length of seqs is %s ' % seqs

# I want to handle the NHIRD record by this script rather than handing it to
# NSelector

f = open(sys.argv[3])
parser = NHIRDParser.NHIRDParser(OO101_fmt)
res = {}
for l in f:
    label = parser.getByTag(l, 'SEQ_NO')
    if label in seqs:
        res[label] = res.get(label, []) + [l]

ress = sorted(res.items(), key=lambda x: len(x[1]), reverse=True)[:10]
for r in ress:
    print red(r[0])
    for rr in r[1]:
        print rr
