#! -*- coding: utf-8 -*-
# bert 基础测试: MLM

import sys
sys.path.append('../bert4tf')
from bert4tf.bert import build_bert_model
from bert4tf.tokenizer import Tokenizer
from bert4tf.snippets import to_array


config_path = '/home/zxc/chinese_L-12_H-768_A-12/bert_config.json'
checkpoint_path = '/home/zxc//chinese_L-12_H-768_A-12/bert_model.ckpt'
dict_path = '/home/zxc/chinese_L-12_H-768_A-12/vocab.txt'

tokenizer = Tokenizer(dict_path, do_lower_case=True)  # 建立分词器
model = build_bert_model(config_path=config_path, checkpoint_path=checkpoint_path, with_mlm=True)  # 建立模型, 加载权重

token_ids, segment_ids = tokenizer.encode(u'科学技术是第一生产力')

# mask掉“技术”
token_ids[3] = token_ids[4] = tokenizer._token_mask_id
token_ids, segment_ids = to_array([token_ids], [segment_ids])

# 用mlm模型预测被mask掉的部分
probas = model.predict([token_ids, segment_ids])[0]
print(tokenizer.decode(probas[3:5].argmax(axis=1)))  # 结果正是“技术”