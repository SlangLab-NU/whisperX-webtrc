# BoltX

This browser based project let's the whisperX model transcribe incoming audio in realtime.

> Translation is not possible(maybe added later)

![Screenshot](assets/screenshot.png)

## Setup

Install the requirements.txt with pip. No need for ffmpeg.

```bash
# in backend
pip3 install -r requirements.txt
```
You may also need to install ffmpeg, rust etc. Follow openAI instructions here https://github.com/openai/whisper#setup.

To start

```bash
cd frontend && npm run dev
cd ../backend && python3 main.py
```

TODO:

1. Docker file for the frontend and backend
2. The timestamp for individual words can also be extracted by extracting the timestamp_token after each word.
  1. The timestamp after each token doesn't produce nice results. So I don't know how this will fare with "Scriptio continua" languages.  
4. I am in need of some ideas for the continous transcription. Please state any methodology: twitter:@gslaller.

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
