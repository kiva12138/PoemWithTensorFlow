import numpy as np
from .setting import MAX_LEN


# 's'为古诗的开头字符串
def generate_random_poetry(tokenizer, model, s=''):
    token_ids = tokenizer.encode(s)
    token_ids = token_ids[:-1]
    while len(token_ids) < MAX_LEN:
        _probas = model.predict([token_ids, ])[0, -1, 3:]
        # 从0开始排序 [1, 5, 4, 0, 2, 3]
        p_args = _probas.argsort()[::-1][:100]
        p = _probas[p_args]
        p = p / sum(p)
        target_index = np.random.choice(len(p), p=p)
        target = p_args[target_index] + 3
        token_ids.append(target)
        if target == 3:
            break
    return tokenizer.decode(token_ids)


def generate_acrostic(tokenizer, model, head):
    token_ids = tokenizer.encode('')
    token_ids = token_ids[:-1]
    punctuations = ['，', '。']
    punctuation_ids = {tokenizer.token_to_id(token) for token in punctuations}
    poetry = []
    for ch in head:
        poetry.append(ch)
        token_id = tokenizer.token_to_id(ch)
        token_ids.append(token_id)
        while True:
            _probas = model.predict([token_ids, ])[0, -1, 3:]
            p_args = _probas.argsort()[::-1][:100]
            p = _probas[p_args]
            p = p / sum(p)
            target_index = np.random.choice(len(p), p=p)
            target = p_args[target_index] + 3
            token_ids.append(target)
            if target > 3:
                poetry.append(tokenizer.id_to_token(target))
            if target in punctuation_ids:
                break
    return ''.join(poetry)
