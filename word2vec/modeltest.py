from gensim.models import word2vec
def main():
	model=word2vec.Word2Vec.load(u'/Users/yaphets/Desktop/dealwith/word2vec_zhwiki_model_00')
	model.most_similar(positive=['女人'],negative=['男人'])
	print(model.similarity(u'妹子',u'女孩'))
	print(model.most_similar(u'女人'))
	print(model[u'繁衍'])


if __name__ == '__main__':
	main()