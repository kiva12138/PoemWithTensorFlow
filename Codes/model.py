import tensorflow as tf
from dataset import tokenizer

model = tf.keras.Sequential([
    tf.keras.layers.Input((None, )),
    tf.keras.layers.Embedding(input_dim=tokenizer.vocab_size, output_dim=128),
    tf.keras.layers.LSTM(128, dropout=0.5, return_sequences=True),  # 输出控件维度为128
    tf.keras.layers.LSTM(128, dropout=0.5, return_sequences=True),
    tf.keras.layers.TimeDistributed(tf.keras.layers.Dense(tokenizer.vocab_size, activation='softmax'))
])
model.summary()
model.compile(optimizer=tf.keras.optimizers.Adam(), loss=tf.keras.losses.categorical_crossentropy)


# _probas = model.predict([[67], ])[0, -1, 3:10]
# print(_probas)
# p_args = _probas.argsort()[::-1]
# print(p_args)

