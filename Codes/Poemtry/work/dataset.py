from .setting import *

disallowed_words = DISALLOWED_WORDS
max_len = MAX_LEN
min_word_frequency = MIN_WORD_FREQUENCY
batch_size = BATCH_SIZE


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
