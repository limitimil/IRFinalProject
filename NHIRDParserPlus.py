import NHIRDParser
class NHIRDParserPlus(NHIRDParser.NHIRDParser):
    def __init__(self, fmtindict = {}):
        self.fmt = fmtindict
    def formater(self):
        # extract fmt
        fmt = sorted(map(
            lambda x: [x[0],x[1][0],x[1][1]],
            self.fmt.items()
            ),
            key = lambda x: x[1]
            )
        # merge detection
        if not fmt:
            return fmt
        fmt2 = []
        fmt2.append(fmt[0])
        for i in xrange(1,len(fmt)):
            if fmt[i-1][2] < fmt[i][1]:
                fmt2.append(fmt[i])
            else:
                fmt2[-1][2] = max(fmt[i][2],fmt2[-1][2])
        fmt2 = map(
            lambda x: x[1:3],
            fmt2
        )
        return fmt2
    def reformats(self, record):
        fmt = self.formater()
        return self.reformat(record, fmt) 
    def reformatl(self, records):
        ret = []
        fmt = self.formater()
        for r in records:
            ret.append(self.reformat(r, fmt))
        return ret
    def reformat(self, s, fmt):
        ret = ''
        for f in fmt:
            ret += s[f[0]-1:f[1]]
        return ret
    def compacted_fmt(self):
        # extract fmt
        fmt = sorted(map(
            lambda x: [x[0],x[1][0],x[1][1]],
            self.fmt.items()
            ),
            key = lambda x: x[1]
            )
        # merge detection
        if not fmt:
            return fmt 
        shift = 0
        diff = fmt[0][1] - 1
        shift += diff
        fmt[0][1] -= diff 
        fmt[0][2] -= diff 
        for i in xrange(1,len(fmt)):
            fmt[i][1] -= shift
            fmt[i][2] -= shift
            if fmt[i-1][2] < fmt[i][1]:
                diff = fmt[i][1] - fmt[i-1][2] -1
                shift += diff
                fmt[i][1] -= diff
                fmt[i][2] -= diff 
        return fmt
if __name__ == '__main__':
    import sys
    if len(sys.argv)<2:
        exit(7)
    np = NHIRDParser.NHIRDParser([ #pleas use CD file to test
        ('ID_STR',1,57),
        ('SEQ_NO',52,57),
        ('ID',92,123),
        ('ACODE_ICD9_1',132,146),
        ('ACODE_ICD9_2',147,161),
        ('ACODE_ICD9_3',162,176),
        ('PART_NO',129,131),
    ])
    npp = NHIRDParserPlus( np.fmt)
    with open(sys.argv[1]) as f:
        lines = f.read().split('\n')
        print npp.reformatl(lines)
    print npp.compacted_fmt()
    with open(sys.argv[1]) as f:
        for line in f:
            print npp.reformats(line)
    
