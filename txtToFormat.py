with open('alldocs.txt', 'wb') as ad:

    with open('data/Medium/highlights.txt', 'r') as mHighlights:
        for line_no, line in enumerate(mHighlights):
            words = line
            tag = 'mh_' + str(line_no)
            ad.write(tag + 'sepsepsepsep' + words)

    with open('data/Medium/articles.txt', 'r') as mArticles:
        for line_no, line in enumerate(mArticles):
            words = line
            tag = 'm_' + str(line_no)
            ad.write(tag + 'sepsepsepsep' + words)

    with open('data/Atlantic/articles.txt', 'r') as aArticles:
        for line_no, line in enumerate(aArticles):
            words = line
            tag = 'atlantic_' + str(line_no)
            ad.write(tag + 'sepsepsepsep' + words)
