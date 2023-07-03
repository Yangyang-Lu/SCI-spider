


def Comparison_key_words(paper_title_list, paper_url_list, paper_abstract_list):
    paper_title = []
    paper_url = []
    paper_abstract = []
    key = []
    #key_words = ["friction", "Friction", "wear", "Wear", "abrasion", "Abrasion", "lubrication", "Lubrication", "energy dissipation", "phonon", "charge","potential energy surface", "Potential energy surface", "Potential Energy Surface", "PES","superlubricity", "ultralow friction", "tribology", "nanotribology", "interfacial slide", "2D materials", "Two-dimensional materials", "van der Waals"]
    key_words = ["friction", "Friction", "wear", "Wear", "abrasion", "Abrasion", "lubrication", "Lubrication",
                 "energy dissipation", "phonon", "charge", "potential energy surface", "Potential energy surface",
                 "Potential Energy Surface", "PES", "superlubricity", "ultralow friction", "tribology", "nanotribology",
                 "interfacial slide", "2D materials", "Two-dimensional materials", "van der Waals"]

    for i in range(0, len(paper_abstract_list)):
        com_key_words = ""
        key_words_num = 0
        for k in range(0, len(key_words)):
            if str(key_words[k]) in str(paper_abstract_list[i]):
                com_key_words = com_key_words + " " + str(key_words[k])
                key_words_num = 1
        if key_words_num == 1:
            paper_title.append(paper_title_list[i])
            paper_url.append(paper_url_list[i])
            paper_abstract.append(paper_abstract_list[i])
            key.append(com_key_words)
    return paper_title, paper_url, paper_abstract, key

