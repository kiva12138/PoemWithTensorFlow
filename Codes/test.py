import tensorflow as tf
from dataset import tokenizer
import setting
import unitl

# 加载训练好的模型
model = tf.keras.models.load_model(setting.BEST_MODEL_PATH)
print(unitl.generate_random_poetry(tokenizer, model))
print(unitl.generate_random_poetry(tokenizer, model, s='床前明月光，'))
print(unitl.generate_acrostic(tokenizer, model, head='海阔天空'))
