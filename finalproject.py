
import math

def clean_text(txt):
    """ helper function that returns a list of lower case words
        without punctuation from string txt"""
    txt = txt.replace('.', '')
    txt = txt.replace(',', '')
    txt = txt.replace('?', '')
    txt = txt.replace('!', '')
    txt = txt.replace(':', '')
    txt = txt.replace(';', '')
    txt = txt.replace('"', '')
    txt = txt.replace("'", '')
    txt = txt.lower()
    txt = txt.split()
    return txt

def stem(s):
    """ returns stem of string word s """
    if s[-3: ] == 'ing':
        return s[ :-3]
    elif s[-2: ] == 'ed':
        return s[ :-2]
    elif s[-4: ] == 'tion':
        return s[ :-4]
    elif s[-2: ] == 'es':
        return s[ :-2]
    elif s[-2: ] == 'er':
        return s[ :-2]
    elif s[-3: ] == 'ers':
        return s[ :-3]
    elif s[-3: ] == 'est':
        return s[ :-3]
    elif s[-3: ] == 'acy':
        return s[ :-3]
    elif s[-2: ] == 'al':
        return s[ :-2]
    elif s[-4: ] == 'ance' or s[-4: ] == 'ence':
        return s[ :-4]
    elif s[-3: ] == 'ate':
        return s[ :-3]
    elif s[-2: ] == 'en':
        return s[ :-2]
    elif s[-3: ] == 'ify':
        return s[ :-3]
    elif s[-2: ] == 'fy':
        return s[ :-2]
    elif s[-4: ] == 'able' or s[-4: ] == 'ible':
        return s[ :-4]
    elif s[-5: ] == 'esque':
        return s[ :-5]
    elif s[-1] == 'y':
        return s[ :-1] + 'i'
    else:
        return s

def compare_dictionaries(d1, d2):
    """ returns similarlity score between two feature dictionaries d1 and d2 """
    total = 0
    for word in d1:
        total += d1[word]
    log_sim_score = 0
    for word in d2:
        if word in d1:
            log_sim_score += math.log(d1[word] / total) * d2[word]
        else:
            log_sim_score += math.log(.5 / total) * d2[word]
    return log_sim_score
    

class TextModel:

    def __init__(self, model_name):
        """ contructor for text model object """
        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        self.stems = {}
        self.sentence_lengths = {}
        self.punc = {}

    def __repr__(self):
        """ returns string representation of text model object """
        s = ''
        s += 'text model name: ' + self.name + '\n'
        s += ' number of words: ' + str(len(self.words)) + '\n'
        s += ' number of word lengths: ' + str(len(self.word_lengths)) + '\n'
        s += ' number of stems: ' + str(len(self.stems)) + '\n'
        s += ' number of sentence lengths: ' + str(len(self.sentence_lengths)) + '\n'
        s += ' number of punctuation: ' + str(len(self.punc))
        return s

    def add_string(self, s):
        """ updates model's dictionaries to reflect added string s """
        word_list = clean_text(s)
        for w in word_list:
            if w in self.words:
                self.words[w] += 1
            else:
                self.words[w] = 1
        for w in word_list:
            if len(w) in self.word_lengths:
                self.word_lengths[len(w)] += 1
            else:
                self.word_lengths[len(w)] = 1
        for w in word_list:
            root = stem(w)
            if root in self.stems:
                self.stems[root] += 1
            else:
                self.stems[root] = 1
        punc_list = s.split()
        count = 0
        sentence_counts = []
        for w in punc_list:
            if '.' in w or '?' in w or '!' in w:
                count += 1
                sentence_counts += [count]
                count = 0
            else:
                count += 1
        for c in sentence_counts:
            if c in self.sentence_lengths:
                self.sentence_lengths[c] += 1
            else:
                self.sentence_lengths[c] = 1
        for w in punc_list:
            if '!' in w:
                if '!' in self.punc:
                    self.punc['!'] += 1
                else:
                    self.punc['!'] = 1
            elif '?' in w:
                if '?' in self.punc:
                    self.punc['?'] += 1
                else:
                    self.punc['?'] = 1
            elif '.' in w:
                if '.' in self.punc:
                    self.punc['.'] += 1
                else:
                    self.punc['.'] = 1
            elif ',' in w:
                if ',' in self.punc:
                    self.punc[','] += 1
                else:
                    self.punc[','] = 1
            elif ':' in w:
                if ':' in self.punc:
                    self.punc[':'] += 1
                else:
                    self.punc[':'] = 1
            elif ';' in w:
                if ';' in self.punc:
                    self.punc[';'] += 1
                else:
                    self.punc[';'] = 1
            
                
    def add_file(self, filename):
        """ adds text from file to model's dictionaries """
        f = open(filename, 'r', encoding='utf8', errors='ignore')
        self.add_string(f.read())

    def save_model(self):
        """ writes python dicitonary into file """
        f = open(str(self.name + '_' + 'words.txt'), 'w')
        f.write(str(self.words))
        f.close()
        f = open(str(self.name + '_' + 'word_lengths.txt'), 'w')
        f.write(str(self.word_lengths))
        f.close()
        f = open(str(self.name + '_' + 'stems.txt'), 'w')
        f.write(str(self.stems))
        f.close()
        f = open(str(self.name + '_' + 'sentence_lengths.txt'), 'w')
        f.write(str(self.sentence_lengths))
        f.close()
        f = open(str(self.name + '_' + 'punc.txt'), 'w')
        f.write(str(self.punc))
        f.close()

    def read_model(self):
        """ reads python dictionary from file and assigns
            to corresponding text model attribute """
        f = open(str(self.name + '_' + 'words.txt'), 'r')
        d_str = f.read()
        f.close()
        self.words = dict(eval(d_str))
        f = open(str(self.name + '_' + 'word_lengths.txt'), 'r')
        d_str = f.read()
        self.word_lengths = dict(eval(d_str))
        f.close()
        f = open(str(self.name + '_' + 'stems.txt'), 'r')
        d_str = f.read()
        self.stems = dict(eval(d_str))
        f.close()
        f = open(str(self.name + '_' + 'sentence_lengths.txt'), 'r')
        d_str = f.read()
        self.sentence_lengths = dict(eval(d_str))
        f.close()
        f = open(str(self.name + '_' + 'punc.txt'), 'r')
        d_str = f.read()
        self.punc = dict(eval(d_str))
        f.close()

    def similarity_scores(self, other):
        """ returns list of similarity scores for each of self model's dictionaries
            compared to other model's """
        word_score = compare_dictionaries(other.words, self.words)
        word_lengths_score = compare_dictionaries(other.word_lengths, self.word_lengths)
        stems_score = compare_dictionaries(other.stems, self.stems)
        sentence_lengths_score = compare_dictionaries(other.sentence_lengths, self.sentence_lengths)
        punc_score = compare_dictionaries(other.punc, self.punc)
        scores = [word_score, word_lengths_score, stems_score, sentence_lengths_score, punc_score]
        return scores

    def classify(self, source1, source2):
        """ determines which of the two sources source1 or source2 was most likely
            the source of the self text model """
        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)
        print('Scores for', source1.name + ':', scores1)
        print('Scores for', source2.name + ':', scores2)
        weighted_sum1 = 10 * scores1[0] + 5 * scores1[1] + 7 * scores1[2] + 6 * scores1[3] + 3 * scores1[4]
        weighted_sum2 = 10 * scores2[0] + 5 * scores2[1] + 7 * scores2[2] + 6 * scores2[3] + 3 * scores2[4]
        closest = max([weighted_sum1, weighted_sum2])
        if closest == weighted_sum1:
            print(self.name, 'is more likely to have come from', source1.name)
        else:
            print(self.name, 'is more likely to have come from', source2.name)

def test():
    """ your docstring goes here """
    source1 = TextModel('source1')
    source1.add_string('It is interesting that she is interested.')

    source2 = TextModel('source2')
    source2.add_string('I am very, very excited about this!')

    mystery = TextModel('mystery')
    mystery.add_string('Is he interested? No, but I am.')
    mystery.classify(source1, source2)

def run_tests():
    """ your docstring goes here """
    source1 = TextModel('Brothers Grimm Fairytales')
    source1.add_file('brothers_grimm.txt')

    source2 = TextModel('War and Peace')
    source2.add_file('war_peace.txt')

    new1 = TextModel('The Bible')
    new1.add_file('bible.txt')
    new1.classify(source1, source2)
    print()
    new2 = TextModel('Alice in Wonderland')
    new2.add_file('alice_wonderland.txt')
    new2.classify(source1, source2)
    print()
    new3 = TextModel('Great Expectations')
    new3.add_file('great_expectations.txt')
    new3.classify(source1, source2)
    print()
    new4 = TextModel('Pride and Prejudice')
    new4.add_file('pride_prejudice.txt')
    new4.classify(source1, source2)
    print()
    new5 = TextModel('Frankenstein')
    new5.add_file('frankenstein.txt')
    new5.classify(source1, source2)
    print()
    new6 = TextModel('The Communist Manifesto')
    new6.add_file('communist_manifesto.txt')
    new6.classify(source1, source2)
    
