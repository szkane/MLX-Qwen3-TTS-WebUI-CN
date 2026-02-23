import os
from datetime import datetime
import soundfile as sf
import numpy as np
from mlx_audio.tts.utils import load_model

# 1. 准备输出目录
os.makedirs("output", exist_ok=True)

# 2. 生成时间戳文件名
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_path = f"output/chatterbox_{timestamp}.wav"

# 3. 调用 TTS 生成音频

model=load_model("../models/Chatterbox-Turbo-FP16")
results = list(model.generate(
       text=(
        "Tom was a small boy. [hmm]"
        "Tom had ten sheep."
        "He took the sheep up a hill."
        "Tom sat on a rock."
        "He felt bored. [sigh]"
        "No fun, he said."
        "Tom had an idea. [chuckle]"
        "I will play a trick, he said."
        "Tom ran down the hill."
        "'Wolf! Wolf!' he yelled. [gasp]"
        "Help me! A wolf is here! he said."
        "The people ran to Tom."
        "They looked and looked."
        "But there was no wolf."
        "Tom laughed. [chuckle]"
        "It was a trick! he said."
        "The people did not laugh."
        "The next day, Tom sat on the hill."
        "He felt bored again."
        "He wanted to play."
        "Tom ran down the hill."
        "'Wolf! Wolf!' he yelled."
        "'Help me!' he said."
        "The people ran to Tom."
        "But there was no wolf."
        "Tom laughed again. [hehe]"
        "The people frowned."
        "On the third day, Tom sat with his sheep."
        "A real wolf came out of the trees. [gasp]"
        "The wolf showed its teeth."
        "Tom was scared."
        "He ran down the hill."
        "Wolf! Wolf! Help me! he cried."
        "But the people did not run."
        "Tom tricks us, they said."
        "We will not go, they said."
        "Tom went back up the hill."
        "The wolf was gone."
        "The sheep were gone too."
        "Tom sat on the rock."
        "He felt sad. [sniff]"
        "I will not trick people again, he said."
    ),
    ref_audio="voice_ref/hilson.wav",
    ))


# 4. 提取音频并保存为 WAV
if results:
    audio_data = np.array(results[0].audio)
    sf.write(output_path, audio_data, model.sample_rate)
    print(f"Saved to: {output_path}")
