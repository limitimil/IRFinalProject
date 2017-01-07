import sys
import NHIRDSelector
import NHIRDParser
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

nr = NHIRDSelector.NHIRDSelector(
    NHIRDParser.NHIRDParser(HV_fmt)
)
nr.Filter = lambda x : nr.parser.getByTag(x, 'ICD9CM_CODE').strip()  in\
ICD9_include
nr.read(sys.argv[1])
print len(nr.repo)
