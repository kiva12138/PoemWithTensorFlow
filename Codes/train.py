import tensorflow as tf
import setting
import unitl
from dataset import PoetryDataGenerator, poetry, tokenizer
from model import model


# model = tf.keras.models.load_model(setting.BEST_MODEL_PATH)
class Evaluate(tf.keras.callbacks.Callback):

    def __init__(self):
        super().__init__()
        self.lowest = 1e10  # 初始的loss

    def on_epoch_end(self, epoch, logs=None):
        if logs['loss'] <= self.lowest:
            self.lowest = logs['loss']
            model.save(setting.BEST_MODEL_PATH)
        # print()
        # for i in range(setting.SHOW_NUM):
        #     print(unitl.generate_random_poetry(tokenizer, model))


data_generator = PoetryDataGenerator(poetry, random=True)
model.fit(data_generator.__iter__(), epochs=setting.TRAIN_EPOCH,
          steps_per_epoch=data_generator.steps, callbacks=[Evaluate()])
