import NHIRDSelector
class NHIRDPieChart(NHIRDSelector.NHIRDSelector):
    def pieInformation(self, colname): 
    #colname will decide which label in NHIRD data to show on pie
        retHash = {}
        for l in self.repo:
            label = self.parser.getByTag(l, colname)
            retHash[label] = retHash.get(label, 0) + 1
        return retHash.keys(), retHash.values()
if __name__ == '__main__':
    import NHIRDParser
    import sys
    if len(sys.argv)<2 :
        sys.stderr.write('at least one input file need\n')
        exit(7)
    npc = NHIRDPieChart(
        NHIRDParser.NHIRDParser([
        ('ID',1,32),
        ('ICD9CM_CODE',33,37),
    ])
    )
    npc.read(sys.argv[1])
    print npc.pieInformation('ICD9CM_CODE')
