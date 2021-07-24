import json
import os

import hydra
from hydra.core.config_store import ConfigStore

from deepspeech_pytorch.configs.inference_config import TranscribeConfig
from deepspeech_pytorch.inference import transcribe

cs = ConfigStore.instance()
cs.store(name="config", node=TranscribeConfig)

def make_dir_if_not_exist(the_dir):

    if the_dir:
        target_dir = os.path.join('/analyze/transcript', the_dir.split('/')[-1])
        if not os.path.isdir(target_dir):
            os.mkdir(target_dir)
        return target_dir
    else:
        return the_dir
    

@hydra.main(config_name="config")
def hydra_main(cfg: TranscribeConfig):
    for root, dirs, relative_audio_path_list in os.walk("/analyze/audio/output/"):
        audio_path_list = [ os.path.join(root, audio_path) for audio_path in relative_audio_path_list ]
        transcript_dir = make_dir_if_not_exist(root)
        for audio_path in audio_path_list:
            output_path = os.path.join(transcript_dir, f"{audio_path.split('/')[-1].split('.')[0]}.txt")
            print(f"transcript {audio_path}")
            cfg.audio_path=audio_path
            cfg.model.model_path="models/deepspeech.pytorch/librispeech_pretrained_v3.ckpt"
            result = transcribe(cfg=cfg)
            transcript = result["output"][0]["transcription"]
            with open(output_path, "w") as f:
                print(f"Write transcript in {output_path}")
                f.write(transcript.lower())


if __name__ == '__main__':
    hydra_main()
