# Bolt

This browser based project let's the whisper model transcribe incoming audio in realtime.

> Translation is not possible(maybe added later)

![Screenshot](assets/screenshot.png)

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

To start

```bash
python3 main.py
```

TODO:

1. Docker file for the frontend and backend
2. The timestamp for individual words can also be extracted by extracting the timestamp after each word. 
3. I am in need of some ideas for the continous transcription. Please state any methodology: twitter:@gslaller.

## Available models and languages

There are five model sizes, four with English-only versions, offering speed and accuracy tradeoffs. Below are the names of the available models and their approximate memory requirements and relative speed.

|  Size  | Parameters | English-only model | Multilingual model | Required VRAM | Relative speed |
| :----: | :--------: | :----------------: | :----------------: | :-----------: | :------------: |
|  tiny  |    39 M    |     `tiny.en`      |       `tiny`       |     ~1 GB     |      ~32x      |
|  base  |    74 M    |     `base.en`      |       `base`       |     ~1 GB     |      ~16x      |
| small  |   244 M    |     `small.en`     |      `small`       |     ~2 GB     |      ~6x       |
| medium |   769 M    |    `medium.en`     |      `medium`      |     ~5 GB     |      ~2x       |
| large  |   1550 M   |        N/A         |      `large`       |    ~10 GB     |       1x       |

[more information about the models](model-card.md)
