class drugEdge:
    def __init__(self, From, To):
        self.e = '%-12s-%-12s' % (From[:12],To[:12])
        #According to OO fromat, DRUG_NO is 12 in length
    def source(self):
        return self.e[:12]
    def drain(self):
        return self.e[13:]
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.e == other.e
        return False
    def __ne__(self, other):
        return not self.__eq__(other)
    def __hash__(self):
        return hash(self.e)
class PDP: #patient drug pair
    def __init__(self, p, d):
        self.pair = (p,d)
        #According to OO fromat, DRUG_NO is 12 in length
    def patient(self):
        return self.pair[0]
    def drug(self):
        return self.pair[1]
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.pair[0] == other.pair[0] and \
            self.pair[1] == other.pair[1]
        return False 
    def __ne__(self, other):
        return not self.__eq__(other)
    def __hash__(self):
        return hash(self.pair)
class drugBag: 
    def __init__(self):
        self.bag = set([])
        self.edges = set([])
    def add_drug(self, drug_no):
        for d in self.bag:
            self.edges |= set([
                drugEdge(drug_no, d)
            ])

class Drug2DrugTransition: 
    def __init__(self, drugset):
        self.drugset = drugset
    def ddtAmongPatients(self, patientl): #patient is a dictionary of patients,
                                        # key is patient ID in NHIRD, value is
                                        # patient.patient() class
        res = {}
        for d in self.drugset:
            pp = filter(
                lambda x: d in x.drugs().bag,
                patientl.values()
            )
            transitions = {}
            for p in pp:
                de = filter( #drug edges
                    lambda x: d == x.source(),
                    list(p.drugs().edges)
                )
                ed = map( #edge drains
                    lambda x: x.drain(),
                    de
                )
                for dd in ed: ## dd means a single drain drug
                    transitions[dd] = transitions.get(dd, 0) + 1
            res[d] = {'patient count': len(pp), 'transitions': transitions}
        return res
class drugHandler:
    def __init__(self, drugnames):
        self.drugnames = drugnames
        self.drugset = self.preprocess(drugnames)
    def include(self, drug_no):
        return drug_no in self.drugset
    def name(self, drug_no): #if drug_no not exist, return None
        for k,v in self.drugnames.items():
            if drug_no in v:
                return k
        return None
    def preprocess(self, drugnames):
        ret = set([])
        for l in drugnames.values():
            ret |= set(l)
        return ret
    def __len__(self):
        return len(self.drugset)
if __name__ == '__main__':
    import sys
    import json
    if len(sys.argv) < 2:
        exit(17)
    dh = drugHandler(json.load(open(sys.argv[1])))
    print 'total %s, first ten %s' % (len(dh),list(dh.drugset)[:10])
    print dh.include('BC23291100')
    print dh.name   ('BC23291100')
    print dh.include('AAAAAA')
