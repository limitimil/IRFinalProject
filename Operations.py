import NHIRDParserPlus
def storeInCompactFormat( selector, filename= 'op.out', sortkey=None):
    npp = NHIRDParserPlus.NHIRDParserPlus(selector.parser.fmt)
    fmt = npp.formater()
    f = open(filename, 'w')
    if sortkey:
        repo = sorted(selector.repo, key=sortkey)
    else:
        repo = selector.repo
    for r in repo:
        f.write(npp.reformat(r, fmt))
        f.write('\n')
    return npp.compacted_fmt()
if __name__ == '__main__':
    import sys
    import NHIRDParser
    import NHIRDSelector
    if len(sys.argv)<2:
        exit(7)
    ns = NHIRDSelector.NHIRDSelector(
        NHIRDParser.NHIRDParser([ #pleas use CD file to test
            ('ID_STR',1,57),
            ('SEQ_NO',52,57),
            ('ID',92,123),
            ('ACODE_ICD9_1',132,146),
            ('ACODE_ICD9_2',147,161),
            ('ACODE_ICD9_3',162,176),
            ('PART_NO',129,131),
        ])
    )
    ns.read(sys.argv[1])
    print ns.repo
    print storeInCompactFormat( ns)
