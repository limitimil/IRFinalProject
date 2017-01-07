import sys
import NHIRDSelector
import NHIRDParser
import NHIRDPieChart
import matplotlib.pyplot as plt
#define HV fmt
HV_fmt = [
    ('ID',1,32),
    ('ICD9CM_CODE',33,37),
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


if len(sys.argv)<2 :
    sys.stderr.write('at least one input file need\n')
    exit(7)

npc = NHIRDPieChart.NHIRDPieChart(
    NHIRDParser.NHIRDParser(HV_fmt)
)
npc.Filter = lambda x : npc.parser.getByTag(x, 'ICD9CM_CODE').strip()  in\
ICD9_include
npc.read(sys.argv[1])
labels,sizes = npc.pieInformation('ICD9CM_CODE')

plt.pie(
    sizes,
    labels = labels,
    autopct = '%1.1f%%',
    startangle =140
)
plt.axis('equal')
plt.show()
