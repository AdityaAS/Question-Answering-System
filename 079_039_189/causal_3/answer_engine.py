from __future__ import division
import math

import nltk
from nltk.corpus import wordnet

import indexer

class AnswerEngine(object):
    
    def __init__(self, index, query, start=0, num_top=10, lch=2.16):
        self.query = query
        self.start = start
        self.num_top = num_top
        self.lch = lch
        self.answers = None
        
        # Candidate Document Selection
        self.ir_query = indexer.regularize(indexer.tokenizer.tokenize(query))
        self.ir_query_tagged = None
        page_sim = index.ranked(self.ir_query)
        self.num_pages = len(page_sim)
        
        # Reduce number of pages we need to get from disk
        page_sim = page_sim[start:num_top]
        page_ids, similarity = zip(*page_sim)
        
        # Retrieve the Page objects from the list of Page.IDs
        self.pages = index.get_page(page_ids)
        
        # Tell each page the value of its similarity score
        for page, sim in zip(self.pages, similarity):
            page.cosine_sim = sim

    def _analyze_query(self):
        tagged = nltk.pos_tag(self.ir_query)
        ir_query_tagged = []
        for word, pos in tagged:
            pos = {
                pos.startswith('N'): wordnet.NOUN,
                pos.startswith('V'): wordnet.VERB,
                pos.startswith('J'): wordnet.ADJ,
                pos.startswith('R'): wordnet.ADV,
                }.get(pos, None)
            if pos:
                synsets = wordnet.synsets(word, pos=pos)
            else:
                synsets = wordnet.synsets(word)
            ir_query_tagged.append((word, synsets))
            
        # Add additional special hidden term
        ir_query_tagged.append(('cause', [wordnet.synset('cause.v.01')]))
        self.ir_query_tagged = ir_query_tagged

    def _analyze_pages(self):
        for page in self.pages:
            page.tokenize_sentences()

    def related(self, synsets, word2):
        for net1 in synsets:
            for net2 in wordnet.synsets(word2):
                try:
                    lch = net1.lch_similarity(net2)
                except:
                    continue
                # The value to compare the LCH to was found empirically.
                if lch >= self.lch:
                    return True
        return False

    def related_values(self, synsets, word2):
        related = []
        for net1 in synsets:
            for net2 in wordnet.synsets(word2):
                try:
                    lch = net1.lch_similarity(net2)
                except:
                    continue
                related.append(lch)
        return related

    def _extract_answers(self):
        answers = []
        for page in self.pages:
            page_windows = []
            for para in page.paragraphs:
                for sentence in para.sentence_tokens:
                    # if len(page_windows) == 3:
                    #     break
                    page_windows.append(Answer(page, sentence,
                                        ' '.join(sentence), self))
            answers.extend(page_windows)
        answers = [x for x in answers if x.score > 0]
        answers.sort(key=lambda answer: answer.score, reverse=True)
        # answers.sort(key=lambda answer: answer.page.cosine_sim, reverse=True)
        self.answers = answers

    def get_answers(self):
        self._analyze_query()
        self._analyze_pages()
        self._extract_answers()
        return self.answers


class Answer(object):
    

    def __init__(self, page, raw_tokens, text, ans_eng):
        self.page = page
        self.text = text
        self._features = None
        self.score = self.get_score(raw_tokens, ans_eng)

    def get_score(self, raw_tokens, ans_eng):
        
        (
         term_count,
         related,
         causal_match,
         position,
        ) = self._compute_score(raw_tokens, ans_eng)
        if term_count == 0:
            return 0
        position = math.sqrt(sum(position))
        self._features = (
                         self.page.cosine_sim,
                         term_count,
                         sum(related),
                         sum(related) / len(ans_eng.ir_query),  # average
                         causal_match,
                         position,
                         len(self.text),
                        )
        # Weights computed using logistic regression
        weights = (
                   1.8214,  # page_cosine_sim
                   0.4712,  # term_count
                   0.4206,  # related_sum
                   1.7482,  # related_average
                   0.187,  # causal_match
                   - 0.0559,  # position
                   - 0.0002,  # text_length
                   )
        score = -13.0476  # intercept
        for w, x in zip(weights, self._features):
            # Multiply each feature by its corresponding weight.
            score += w * x
        # Compute probability using the sigmoid function.
        score = 1 / (math.exp(-score) + 1)

        return score

    def _compute_score(self, raw_tokens, ans_eng):
        term_count = 0
        related = []
        causal_match = False
        position = []
        for term, synsets in ans_eng.ir_query_tagged:
            match = False
            term_related = []
            for i, page_term in enumerate(indexer.regularize(raw_tokens)):
                page_term_related = ans_eng.related_values(synsets, page_term)
                if page_term_related:
                    term_related.append((max(page_term_related), i))
                    if term == page_term or max(page_term_related) >= ans_eng.lch:
                        match = True
            if match:  # above LCH value
                term_count += 1
                if term == 'cause':
                    causal_match = True
            if term_related:
                term_related.sort(key=lambda tup: tup[0])
                term_related, i = term_related[-1]  # maximum value
                related.append(term_related)
                position.append(i)
        return term_count, related, causal_match, position


def get_answers(ans_eng):
    ans_eng.get_answers()
    ir_query_tagged = []
    for term, synsets in ans_eng.ir_query_tagged[:-1]:
        synsets = [(net.name, net.definition) for net in synsets]
        ir_query_tagged.append((term, synsets))
    return ans_eng.answers, ir_query_tagged
