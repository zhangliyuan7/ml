import jieba
import sys

filename = sys.argv[2]
target_filename = sys.argv[1]
fn = open(target_filename, 'r', encoding='utf-8')
f = open(filename, 'w+', encoding='utf-8')
for line in fn.readlines():
	words = jieba.cut(line)
	line_seg = ' '.join(words)
	f.write(line_seg+'\n')

f.close()
fn.close()
