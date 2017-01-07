import sys
import NHIRDParser
class NHIRDSelector:
    def __init__(self, parser):
        self.parser = parser
        self.repo = []
    def reads(self, s):
        for l in s.split('\n'):
            if not l:
                continue
            if self.Filter(l):
                self.repo.append(l)
    def read(self, filename):
        f = open(filename)
        for l in f:
            self.reads(l)
    def Filter(self,s):
        return bool(s)
if __name__ == '__main__':
    if len(sys.argv)<2 :
        sys.stderr.write('at least one input file need\n')
        exit(7)
    nr = NHIRDSelector(
        NHIRDParser.NHIRDParser([
            ('ID',1,32),
            ('ICD9CM_CODE',33,37),
        ])
    )
    nr.Filter = lambda x : int(nr.parser.getByTag(x, 'ICD9CM_CODE') ) ==  336
#    f = open(sys.argv[1]).read()
#    nr.reads(f)
    nr.read(sys.argv[1])
    print nr.repo
