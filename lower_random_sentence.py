# -*- coding: UTF-8 -*-
import random
import pandas as pd
import re
import jieba
from collections import Counter  # 2-gram

choice = random.choice  # choice method return one of all

my_grammar = '''
	sentence=pronoun_phrase verb_phrase noun_phrase|noun_phrase verb_phrase noun_phrase 
	noun_phrase=Article* Adj* noun
	Article*=Article|null
	verb_phrase=adverb verb
	pronoun_phrase=Adj* pronoun
	Adj*=null | Adj Adj*
	adverb=独自地|暗暗地|充满希望地|神伤地|勇敢滴
	pronoun=他|她|它|你|我
	noun=猫|狗|地球|花|自然|草地|女孩|妹子|数字|外星人|神仙|alphago|流星|国度|人|国家|电影|政权|旋律|情节
	verb=撒拉嘿着|喜欢|看着|想象着|感受着|倾听着|坐在|践踏着|鄙视着|破坏着|勾引着
	Adj=好看的|神秘的|空中的|难以预测的|美好的|稀奇古怪的|奇异的|被毁灭的|澎湃的|热血的
	Article=一个|一只|一群|一堆|很多|那个|这个|那些|这些
'''
comment_grammar = '''
	sentence=pronoun_phrase verb_phrase noun_phrase
	noun_phrase=adj noun
	verb_phrase=adv verb
	pronoun_phrase=我|你|他|她|它|独自|那个人|那些人|这些人|某些人
	adj=特别的|澎湃的|令人泪目的|热血的|激情的|糟糕的|丑陋的|虚伪的|拜金的|好的|好|垃圾的|美丽的|优雅的|国产的|国外的|低端的|高级的|知性的|大的
	adv=不喜欢|喜欢|懒得|可能|坐着|站着|绝对
	verb=看|听|说|瞧|评论|想|思考|考虑着|成为
	noun=电影院|垃圾|电影|影评人|好莱坞大片|作者|导演|影片|大片|成本|效果|特效
'''


def create_grammar(grammar_str, split='=', line_split='\n'):
	grammar = {}
	for line in grammar_str.split(line_split):
		if not line.strip():
			continue
		exp, stmt = line.split(split)
		grammar[exp.strip()] = [s.split() for s in stmt.split('|')]  # key of sentence generate
	return grammar


print(create_grammar(my_grammar), '\n')


def generate(gram, target):
	if target not in gram:
		return target
	expand = [generate(gram, t) for t in choice(gram[target])]
	return ''.join([e for e in expand if e != 'null'])  # drop null element


# if e != '/n' else '\n'  useless

new_grammar = create_grammar(my_grammar)
print('new', new_grammar)


# print(generate(new_grammar, 'sentence'))
# return list[sentences...]  .named GetSomeRandomSentences has warned
def get_some_random_sentences(grammar, split='=', target='sentence', number=100):
	sentences = []
	for i in range(number):
		sentences.append(generate(create_grammar(grammar, split), target))
	return sentences


print(get_some_random_sentences(my_grammar, '=', 'sentence', 10))


########################

# 2-gram
# file_path = '/Users/yaphets/Desktop/movie_comments.csv'


# return list
def token(content):
	return re.findall('\w+', content)


# return list
def file_parse(file_path, coding='utf-8'):
	articles = pd.read_csv(file_path, encoding=coding, low_memory=False)['comment'].tolist()
	content = ''.join(str(articles))
	return token(content)


# from collections import Counter
# with_jieba_cut = Counter(jieba.cut(articles[1000]))
# print(with_jieba_cut.most_common()[:10])

# print(len(file_parse(file_path)))


# return word list, !!! "str" build-in  "string" not built-in
def cut(string): return list(
	jieba.cut(''.join(string[:500000])) if len(string) > 500000 else jieba.cut(''.join(string)))


# words_list = cut(file_parse(file_path))
# return map
def count_words(words_list):
	return Counter(words_list)


# words_count = Counter(words_list)

# return float
def prob_1(word, words_count, words_list):
	return words_count[word] / len(words_list)


# return 2-gram list
def gram2_list(words_list):
	if len(words_list) < 3:
		return []
	return [''.join(words_list[i:i + 2]) for i in range(len(words_list[:-2]))]


# TOKEN_2_GRAM = [''.join(words_list[i:i + 2]) for i in range(len(words_list[:-2]))]

# print(prob_1("鄙视"))

# two words
def prob_2(word1, word2, words_count, words_list):
	length = len(gram2_list(words_list))
	if word1 + word2 in words_count:
		return words_count[word1 + word2] / length
	else:
		return 1 / length


# print(prob_2('热血','澎湃'),prob_2('爱国','人'))
# return float
def get_probablity(sentence, words_count, words_list):
	words = cut(sentence)
	sentence_pro = 1
	for i, word in enumerate(words[:-1]):
		next_ = words[i + 1]
		probablity = prob_2(word, next_, words_count, words_list)
		sentence_pro += probablity
	return sentence_pro


# return map
def sort_sentences_by_probablity(sentences, words_count, words_list):
	sentences_map = {}
	for sen in sentences:
		sentences_map[sen] = get_probablity(sen, words_count, words_list)
	return sentences_map


# return sort list
def generate_best(sentences_map):
	sentences_list = sentences_map.items()
	return sorted(sentences_list, key=lambda x: x[1], reverse=True)


# main
def main():
	file_path = '/Users/yaphets/Desktop/movie_comments.csv'
	words_list = cut(file_parse(file_path))
	words_count = count_words(words_list)
	sentences = get_some_random_sentences(comment_grammar, '=', 'sentence', 10)  # 10
	print(sentences)
	print(generate_best(sort_sentences_by_probablity(sentences, words_count, words_list)))


main()
