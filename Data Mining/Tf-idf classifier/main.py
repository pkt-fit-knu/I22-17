import re, pymorphy2, math

class Classifier:
    def __init__(self):
        self.morph = pymorphy2.MorphAnalyzer()

    def normalize_text(self, text):
        sub_text = text.replace('.', '').replace(',', '').lower()
        new_text = []
        for word in sub_text.split(' '):
            if self.morph.parse(word)[0].tag.POS in ['NOUN', 'VERB', 'INFN']:
                # print(word, '------', self.morph.parse(word)[0].tag.POS)
                new_text.append(self.morph.parse(word)[0].normal_form)
        return new_text

    @staticmethod
    def tf_idf(term, doc, corpus):
        cnt_t = 0
        for word in doc:
            if word == term:
                cnt_t += 1
        tf = cnt_t / len(doc)
        cnt_d = 0
        for d in corpus:
            for w in d:
                if term == w:
                    cnt_d += 1
                    break
        idf = math.log(len(corpus) / cnt_d)
        return tf * idf
    
    def normalize_corpus(self, corpus):
        norm_corpus = []
        for document in corpus:
            norm_corpus.append(self.normalize_text(document))
        self.corpus = norm_corpus
        return self.corpus
    
    def build_words_vocabulary(self, corpus):
        words_set = set()
        for d in corpus:
            for w in d:
                words_set.add(w)
        self.words = list(words_set)
        return self.words
    
    def get_feature(self, document=None, text=None):
        if document:
            norm_document = document
        else:
            norm_document = self.normalize_text(text)
        curr_feature = []
        for term in self.words:
            curr_feature.append(Classifier.tf_idf(term, norm_document, self.corpus))
        print('for ',document or text,' feature:',curr_feature)
        return curr_feature
    
    def extract_features(self, corpus):
        self.doc_features = []
        for d in corpus:
            self.doc_features.append(self.get_feature(d))
        return self.doc_features
    
    def fit(self, data):
        self.categories = []
        self.corpus = []
        for category, document in data:
            self.categories.append(category)
            self.corpus.append(document)
        self.normalize_corpus(self.corpus)
        self.build_words_vocabulary(self.corpus)
        print(self.words)
        self.extract_features(self.corpus)
    
    @staticmethod
    def tanimoto_distance(feature_1, feature_2):
        scalar = 0
        feature_1_sqr = 0
        feature_2_sqr = 0
        for ind in range(len(feature_1)):
            scalar += feature_1[ind] * feature_2[ind]
            feature_1_sqr += feature_1[ind] * feature_1[ind]
            feature_2_sqr += feature_2[ind] * feature_2[ind]
        return 0 if (feature_1_sqr + feature_2_sqr - scalar == 0) else ( scalar / (feature_1_sqr + feature_2_sqr - scalar) )
    
    def get_category(self, document, k = 2):
        curr_doc_f = self.get_feature(text=document)
        print('current feature:',curr_doc_f)
        distances = []
        for index_document in range(len(self.doc_features)):
            distances.append((Classifier.tanimoto_distance(curr_doc_f, 
                                                           self.doc_features[index_document]), 
                              self.categories[index_document]))
        print('distances:',distances)
        nearest_categories = []
        while len(nearest_categories) < k and len(distances) > 0:
            best_index = 0
            for i in range(0, len(distances)):
                if distances[i][0] > distances[best_index][0]:
                    best_index = i
            nearest_categories.append( distances[best_index][1] )
            distances.pop(best_index)
        names_cats = []
        freq_cats = []
        for i in nearest_categories:
            if i not in names_cats:
                names_cats.append(i)
                freq_cats.append(1)
            else:
                ind_cat_i = names_cats.index(i)
                freq_cats[ind_cat_i] += 1
        for i in range(len(names_cats)):
            if freq_cats[i] == max(freq_cats):
                return names_cats[i]
    
a = Classifier()
import codecs
ff = codecs.open('output.txt', 'w', 'utf-8')

a.fit([('A', 'Обама вручил нобелевскую премию лучшему ученому Америки'), 
       ('A', 'Президент Америки Обама вручил премию футболистам'),
       ('B', 'Футболисты Америки опять проиграли'), 
       ('B', 'Футболисты должны забивать голы')])
print('--CATEGORY--', a.get_category('Забивать голы а то проиграешь'))