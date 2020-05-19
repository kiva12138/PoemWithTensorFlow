import json
import os

import tensorflow as tf

from .dataset import Tokenizer
from .setting import BEST_MODEL_PATH, TOKENIZER_PATH
from .unitl import generate_random_poetry, generate_acrostic
print(os.getcwd())
# 加载字符集合
f = open(TOKENIZER_PATH, "r")
data_dict = dict()
for line in f:
    data_dict = json.loads(line)
f.close()

tokenizer = Tokenizer(data_dict)

# 加载训练好的模型
model = tf.keras.models.load_model(BEST_MODEL_PATH)


def writeRandom():
    return generate_random_poetry(tokenizer, model)


def writeStart(start):
    for i in start:
        if not data_dict.keys().__contains__(i):
            return "包含古诗生僻字，请重新填写"
    return generate_random_poetry(tokenizer, model, s=start)


def writeHead(head):
    for i in head:
        if not data_dict.keys().__contains__(i):
            return "包含古诗生僻字，请重新填写"
    return generate_acrostic(tokenizer, model, head=head)

