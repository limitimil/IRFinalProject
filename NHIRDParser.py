import sys
from colors import red
class NHIRDParser:
    def __init__(self, fmt):
    # fmt is a list of tuple with 3 element (col_name, begin, start)
    # this ctor will check the validity of fmt and colision
        self.fmt = {}
        for record in fmt:
            if record[0] in self.fmt.keys():
                #stderr about colision
                sys.stderr.write('name colition of label %s\n' % record[0])
            if record[1] > record[2]:
                #stderr about invalid start: end pair
                sys.stderr.write('invalid start, end pair of label %s\n' % record[0])
            self.fmt[record[0]] = (int(record[1]),int(record[2]) )
            # this transfer might lead to ValueError when the input value is invalid.
    def showInfo(self, s):
        labels = ''
        values = ''
        for x in sorted(self.fmt.items(), key=lambda x: x[0]):
            labels +=\
            ('%%-%ss' % (x[1][1] - x[1][0] + 1) ) % x[0] + '\t'
            values += s[x[1][0] -1 : x[1][1] ] + '\t'
        print labels
        print values
    def getByTag(self,s, tag):
        startend = self.fmt.get(tag,None)
        if startend:
            return s[startend[0] -1: startend[1]]
        else:
            sys.stderr.write('cannot find tag name [%s]\n' % tag)
            return None
    def getDictByTags(self, s, tags):
        ret = {}
        for t in tags:
            ret[t] = self.getByTag(s,t)
        return ret
if __name__ == '__main__':
    if len(sys.argv)<2 :
        sys.stderr.write('at least one input file need\n')
        exit(7)
    np = NHIRDParser([
        ('ID',1,32),
        ('ICD9CM_CODE',33,37),
    ])
    with open(sys.argv[1]) as f:
        for l in f:
            np.showInfo(l)
