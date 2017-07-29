# -*- coding: utf-8 -*-
# en2ja_data_download.shで落としてきたデータから英日翻訳の訓練データを作成するスクリプト

import random

# 和文と英文を取り出す
en_sentences, ja_sentences = {}, {}
lines = open('sentences.csv').read().split('\n')
for i in range(len(lines)):
    if lines[i] == '':
        continue
    no, lang, sentence = lines[i].split('\t')
    if lang == 'eng':
        en_sentences[no] = sentence
    elif lang == 'jpn':
        ja_sentences[no] = sentence

import MeCab
mecab = MeCab.Tagger("-Owakati")

# 対訳データを作る
lines = open('jpn_indices.csv').read().split('\n')

# 今回はデータサイズを制限する
random.shuffle(lines)
data_size = 2500

with open('en.txt', 'w') as en_file, open('ja.txt', 'w') as ja_file:
    for i in range(len(lines)):
        if lines[i] == '':
            continue
        ja_no, en_no, _ = lines[i].split('\t')
        if en_no == -1:
            continue
        if en_no not in en_sentences:
            continue
        if ja_no not in ja_sentences:
            continue
        
        # 英文は小文字に
        en_file.write(en_sentences[en_no].lower())
        en_file.write('\n')
        
        # 和文は分かち書きにする
        ja_file.write(mecab.parse(ja_sentences[ja_no]))

        # 必要なデータサイズに達したので終了
        data_size -= 1
        if data_size <= 0:
            break