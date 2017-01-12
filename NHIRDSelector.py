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
                self.ontheflyA(l)
            else:
                self.ontheflyB(l)
            self.onthefly(l)
    def read(self, filename):
        f = open(filename)
        for l in f:
            self.reads(l)
    def selectData(self, tag, match=lambda x: bool(x)):
        ret = NHIRDSelector(self.parser)
        for r in self.repo:
            if match (self.parser.getByTag(r,tag) ):
                ret.repo.append(r)
        return ret
    def selectDataMultipleConstraint(self, tags, match=lambda x: bool(x)):
        ret = NHIRDSelector(self.parser)
        for r in self.repo:
            if match ( self.parser.getDictByTags(r, tags) ):
                ret.repo.append(r)
        return ret
    def onthefly(self, s):
        pass
    def ontheflyA(self, s):
        pass
    def ontheflyB(self, s):
        pass
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
    nr.Filter = lambda x : int(nr.parser.getByTag(x, 'ICD9CM_CODE') ) ==  13
#    f = open(sys.argv[1]).read()
#    nr.reads(f)
    nr.read(sys.argv[1])
    print nr.repo
    print 'Filter~~~'
    nr2 = nr.selectData('ID', match= lambda x:\
    x=='c82df810f0e61cd6fc687be6db1e22fb')
    print nr2.repo
