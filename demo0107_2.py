import sys
import NHIRDSelector
import NHIRDParser
import NHIRDPieChart
import matplotlib.pyplot as plt
#define NHIRD fmt
CD101_fmt = [
    ('ACODE_ICD9_1',132,146),
    ('ACODE_ICD9_2',147,161),
    ('ACODE_ICD9_3',162,176),
    ('SEQ_NO', 52, 57),
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
    NHIRDParser.NHIRDParser(CD101_fmt)
)
npc.Filter = lambda x :\
npc.parser.getByTag(x, 'ACODE_ICD9_1').strip()  in ICD9_include or\
npc.parser.getByTag(x, 'ACODE_ICD9_2').strip()  in ICD9_include or\
npc.parser.getByTag(x, 'ACODE_ICD9_3').strip()  in ICD9_include 

npc.read(sys.argv[1])
labels,sizes = npc.pieInformation('ACODE_ICD9_1')

plt.pie(
    sizes,
    labels = labels,
    autopct = '%1.1f%%',
    startangle =140
)
plt.axis('equal')
plt.show()
