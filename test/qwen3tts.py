from mlx_audio.tts.utils import load_model
import soundfile as sf
import numpy as np
import argparse
import datetime

parser = argparse.ArgumentParser(description="MLX Audio TTS Generator")
parser.add_argument("-m", "--model", type=str, default="base", help="Select model to run: base, clone, custom, design")
args = parser.parse_args()

results = []
model = None

if args.model == "base":
    # Base model with predefined voices
    model = load_model("../models/Qwen3-TTS-Base")
    results = list(model.generate(
        text="Hello, Hilson.Donn't watch Youtube.",
        voice="Aiden",
        language="English",
    ))

elif args.model == "clone":
    # Voice Clone
    model = load_model("../models/Qwen3-TTS-Base")
    results = list(model.generate(
        text="What the frog. What the frog. What the frog. what the hell. hilson is beautiful.",
        
        #ref_text="我最喜欢邱润晨。他很可爱。很久以前，在波斯的一个城里住着两兄弟，哥哥明叫卡西姆，弟弟名叫阿里巴巴。",
        ref_audio="./voice_ref/hilson.wav",
        ref_text="he girl goes to bed.The girl eats supper.The girl goes shopping.The girl goes to the movies.The girl rides in the car.The girl goes to school.The girl stays home.The girl is hungry."
    ))

elif args.model == "custom":
    # CustomVoice (Emotion Control)
    #Chinese: Vivian, Serena, Uncle_Fu, Dylan (Beijing Dialect), Eric (Sichuan Dialect)
    #English: Ryan, Aiden
    model = load_model("../models/Qwen3-TTS-Custom")
    results = list(model.generate_custom_voice(
        text="I'm so excited to meet you!",
        speaker="Vivian",
        language="English",
        instruct="Very happy and excited.",
    ))

elif args.model == "design":
    # Create any voice from a text description
    model = load_model("../models/Qwen3-TTS-Design")
    results = list(model.generate_voice_design(
        text="The girl goes to bed.The girl eats supper.The girl goes shopping.The girl goes to the movies.The girl rides in the car.The girl goes to school.The girl stays home.The girl is hungry.",
        language="English",
        # instruct="Perform as a 6 years old boy narrator. He is an British and has England as his native language.Maintain a slow, calm tempo and  with a tone of gentle curiosity.",
        instruct="Perform as a 6 years old boy narrator. He is an British and has England as his native language. A slow, soothing tempo with a joyful, softly smiling sense of curiosity.",
    ))

if results and model:
    audio = np.array(results[0].audio)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"output/qwen3_tts_{args.model}_{timestamp}.wav"
    sf.write(filename, audio, model.sample_rate)
    print(f"Audio saved to {filename}")

""""
instruct=Speaker 1 use a steady, storytelling pace to clearly set the scene for the audience. Speaker 2 use a curious and eager tone.
Speaker 1: The girl goes to bed.
Speaker 2: When can I stay up late? Dad says: When you grow up.
Speaker 1: The girl eats supper.
Speaker 2: When can I eat anything I want? Mon says: When you grow up.
Speaker 1: The girl goes shopping.
Speaker 2: When can I go shopping by myself? Dad says:  When you grow up.
Speaker 1: The girl goes to the movies.
Speaker 2: When can I go to the movies alone? Mom say: When you grow up.
Speaker 1: The girl rides in the car.
Speaker 2: When can I drive the car?  Dad says: When you grow up.
Speaker 1: The girl goes to school.
Speaker 2: When can I get a job like yours? Mon says: When you grow up.
Speaker 1: The girl stays home. 
Speaker 2: When can I go out at night? Dad says: When you grow up.
Speaker 1: The girl is hungry.
Speaker 2: When can I have cookies and milk? Dad and Mon says: Right now.
"""