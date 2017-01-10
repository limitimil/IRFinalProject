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
    ('SEQ_NO',52,57),
    ('ACODE_ICD9_1',132,146),
    ('ACODE_ICD9_2',147,161),
    ('ACODE_ICD9_3',162,176),
]
CD93to100_fmt = [
    ('ID',92,123),
    ('SEQ_NO',52,57),
    ('ACODE_ICD9_1',132,136),
    ('ACODE_ICD9_2',137,141),
    ('ACODE_ICD9_3',142,146),
]
OO101_fmt= [
    ('SEQ_NO',52,57),
    ('DRUG_NO',59,70),
]
OO96to100_fmt= [
    ('SEQ_NO',52,57),
    ('DRUG_NO',59,70),
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
ids = set(npc_hv.pieInformationDict('ID').keys())
print 'length of ids is %s ' % len(ids)

npc_cd = NHIRDPieChart.NHIRDPieChart(
    NHIRDParser.NHIRDParser(CD101_fmt)
)
npc_cd.Filter = lambda x: npc_cd.parser.getByTag(x, 'ID') in\
    ids and\
    set( map(
        lambda x: x.strip(),
        npc_cd.parser.getDictByTags(x,['ACODE_ICD9_1','ACODE_ICD9_2','ACODE_ICD9_3',]).values() 
    )) & set(
        ICD9_include
    )
npc_cd.read(sys.argv[2])
seqs = set(npc_cd.pieInformationDict('SEQ_NO').keys())
print 'length of seqs is %s ' % len(seqs)

# I want to handle the NHIRD record by this script rather than handing it to
# NSelector

f = open(sys.argv[3])
parser = NHIRDParser.NHIRDParser(OO101_fmt)
res = {}
drugs = set([])
for l in f:
    label = parser.getByTag(l, 'SEQ_NO')
    if label in seqs:
        res[label] = res.get(label, []) + [l.strip()]
        drugs |= set([parser.getByTag(l, 'DRUG_NO')])
outf = open('drug.log','w')
for d in drugs:
    outf.write('%s\n' % d)
outf.close()
