from collections import Counter
import math
import numpy as np
import tensorflow as tf
import setting

disallowed_words = setting.DISALLOWED_WORDS
max_len = setting.MAX_LEN
min_word_frequency = setting.MIN_WORD_FREQUENCY
batch_size = setting.BATCH_SIZE


class Tokenizer:
    def __init__(self, token_dict):
        self.token_dict = token_dict
        self.token_dict_rev = {value: key for key, value in self.token_dict.items()}
        self.vocab_size = len(self.token_dict)

    def id_to_token(self, token_id):
        return self.token_dict_rev.get(token_id)

    def token_to_id(self, token):
        return self.token_dict.get(token, self.token_dict['[UNK]'])

    def encode(self, tokens):
        token_ids = [self.token_to_id('[CLS]'), ]
        for token in tokens:
            token_ids.append(self.token_to_id(token))
        token_ids.append(self.token_to_id('[SEP]'))
        return token_ids

    def decode(self, token_ids):
        spec_tokens = {'[CLS]', '[SEP]'}
        tokens = []
        for token_id in token_ids:
            token = self.id_to_token(token_id)
            if token in spec_tokens:
                continue
            tokens.append(token)
        return ''.join(tokens)


with open(setting.DATASET_PATH, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    lines = [line.replace('：', setting.SPLIT_SYMBOL) for line in lines]

poetry = []
for line in lines:
    # There are more than one poetry in this line. So, skip this line
    if line.count(':') != 1:
        continue
    title, content = line.split(setting.SPLIT_SYMBOL)
    ignore_flag = False
    for disallowed_word in disallowed_words:
        if content.__contains__(disallowed_word):
            ignore_flag = True
            break
    if ignore_flag:
        continue
    if len(line) > max_len - 1:
        continue
    poetry.append(content.replace('\n', ''))

counter = Counter()
for line in lines:
    counter.update(line)
_tokens = [(token, count) for token, count in counter.items() if count > min_word_frequency]
_tokens = sorted(_tokens, key=lambda x: -x[1])
_tokens = [token for token, count in _tokens]
_tokens = ['[PAD]', '[UNK]', '[CLS]', '[SEP]'] + _tokens
token_id_dict = dict(zip(_tokens, range(len(_tokens))))
tokenizer = Tokenizer(token_id_dict)
np.random.shuffle(poetry)


class PoetryDataGenerator:
    def __init__(self, data, random=False):
        self.data = data
        self.batch_size = batch_size
        self.steps = int(math.floor(len(self.data) / self.batch_size))
        self.random = random

    """
    将给定数据填充到相同长度
    :param data: 待填充数据
    :param length: 填充后的长度，不传递此参数则使用data中的最大长度
    :param padding: 用于填充的数据，不传递此参数则使用[PAD]的对应编号
    :return: 填充后的数据
    """

    def sequence_padding(self, data, length=None, padding=None):
        if length is None:
            length = max(map(len, data))
        if padding is None:
            padding = tokenizer.token_to_id('[PAD]')
        outputs = []
        for line in data:
            padding_length = length - len(line)
            if padding_length > 0:
                outputs.append(np.concatenate([line, [padding] * padding_length]))
            else:
                outputs.append(line[:length])
        return np.array(outputs)

    def __len__(self):
        return self.steps

    def __iter__(self):
        total = len(self.data)
        for i in range(setting.TRAIN_EPOCH):
            if self.random:
                np.random.shuffle(self.data)
            for start in range(0, total, self.batch_size):
                end = min(start + self.batch_size, total)
                batch_data = []
                for single_data in self.data[start: end]:
                    batch_data.append(tokenizer.encode(single_data))
                batch_data = self.sequence_padding(batch_data)
                yield batch_data[:, :-1], tf.one_hot(batch_data[:, 1:], tokenizer.vocab_size)
                del batch_data

    # def for_fit(self):
    #     yield from self.__iter__()
