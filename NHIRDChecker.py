import sys
import NHIRDPieChart
import BST
from BST import binary_insert_check_unique
class NHIRDChecker(NHIRDPieChart.NHIRDPieChart):
    def simple_uniqueCheck(self, colname):
        records = {}
        for l in self.repo:
            label = self.parser.getByTag(l, colname)
            if records.get(label, None):
                sys.stderr.write('unique check find duplicated value [%s]' %\
                label)  
                return False
            else:
                records[label] = True
        return True
    def uniqueCheck(self, colname):
        if self.parser.lengthOfTag(colname) < 128:
            return self.simple_uniqueCheck(colname)
        #construct root 
        if self.repo:
            bst = BST.Node(self.parser.getByTag(self.repo[0], colname) )
        for l in self.repo[1:]:
            label = self.parser.getByTag(l, colname)
            if binary_insert_check_unique(bst, BST.Node(label)):
                pass
            else:
                sys.stderr.write('unique check find duplicated value [%s]' %\
                label)  
                return False
        return True
if __name__ == '__main__':
    import NHIRDParser
    if len(sys.argv) < 2:
        sys.stderr.write('at least one input file need\n')  
        exit(8)
    nc = NHIRDChecker(
        NHIRDParser.NHIRDParser([ # CD101
            ('ID_STR',1,57)
        ])
    )
    nc.read(sys.argv[1])
    print nc.uniqueCheck('SEQ_NO') 
