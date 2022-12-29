# Bolt

> Translation is not possible

## Openai's Whisper

[[Blog]](https://openai.com/blog/whisper)
[[Paper]](https://arxiv.org/abs/2212.04356)
[[Model card]](model-card.md)
[[Colab example]](https://colab.research.google.com/github/openai/whisper/blob/master/notebooks/LibriSpeech.ipynb)

Whisper is a general-purpose speech recognition model. It is trained on a large dataset of diverse audio and is also a multi-task model that can perform multilingual speech recognition as well as speech translation and language identification.

## Approach

1. Use the webrtc api to transmit audio data in realtime to the backend.
2. Extend the model, so it caches the previous outputs, hence mitigating duplicate computation.
3. Make realtime transcription happen.

## Setup

Install the requirements.txt with pip. No need for ffmpeg.

```bash
pip3 install -r requirements.txt
```

TODO:

1. Docker file for the frontend and backend

## Available models and languages

There are five model sizes, four with English-only versions, offering speed and accuracy tradeoffs. Below are the names of the available models and their approximate memory requirements and relative speed.

|  Size  | Parameters | English-only model | Multilingual model | Required VRAM | Relative speed |
| :----: | :--------: | :----------------: | :----------------: | :-----------: | :------------: |
|  tiny  |    39 M    |     `tiny.en`      |       `tiny`       |     ~1 GB     |      ~32x      |
|  base  |    74 M    |     `base.en`      |       `base`       |     ~1 GB     |      ~16x      |
| small  |   244 M    |     `small.en`     |      `small`       |     ~2 GB     |      ~6x       |
| medium |   769 M    |    `medium.en`     |      `medium`      |     ~5 GB     |      ~2x       |
| large  |   1550 M   |        N/A         |      `large`       |    ~10 GB     |       1x       |

Whisper's performance varies widely depending on the language. The figure below shows a WER breakdown by languages of Fleurs dataset, using the `large-v2` model. More WER and BLEU scores corresponding to the other models and datasets can be found in Appendix D in [the paper](https://arxiv.org/abs/2212.04356).

![WER breakdown by language](language-breakdown.svg)

## Command-line usage

The following command will the start the whole server:

    python main.py
