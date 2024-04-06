# Nendo Plugin Audiogen 

<br>
<p align="left">
    <img src="https://okio.ai/docs/assets/nendo_core_logo.png" width="350" alt="nendo core">
</p>
<br>

<p align="left">
<a href="https://okio.ai" target="_blank">
    <img src="https://img.shields.io/website/https/okio.ai" alt="Website">
</a>
<a href="https://twitter.com/okio_ai" target="_blank">
    <img src="https://img.shields.io/twitter/url/https/twitter.com/okio_ai.svg?style=social&label=Follow%20%40okio_ai" alt="Twitter">
</a>
<a href="https://discord.gg/gaZMZKzScj" target="_blank">
    <img src="https://dcbadge.vercel.app/api/server/XpkUsjwXTp?compact=true&style=flat" alt="Discord">
</a>
</p>

---

AudioGen: A state-of-the-art controllable text-to-sound model (by [Meta Research](https://github.com/facebookresearch/audiocraft))

## Features

- Generate sound effects


## Requirements

Since we depend on `audiocraft`, please make sure that you fulfill their requirements. 
You need Pytorch 2.0.0 or higher, which can be installed via

`pip install "torch>=2.0"`

> Note: On Mac OSX, the instructions for installing pytorch differ. Please refer to the [pytorch installation instructions](https://pytorch.org/get-started/locally/). For all other problems please refer to the [audiocraft repository](https://github.com/facebookresearch/audiocraft/).

To run the plugin you also need to install `audiocraft` by Meta AI Research, run:

`pip install git+https://github.com/facebookresearch/audiocraft`

## Installation

1. [Install Nendo](https://github.com/okio-ai/nendo#installation)
2. `pip install -e .`

## Usage

Take a look at a basic usage example below. 
For more detailed information, please refer to the [documentation](https://okio.ai/docs/plugins).

For more advanced examples, check out the examples folder.
or try it in colab:

<a target="_blank" href="https://colab.research.google.com/drive/1krbzz1OqwCXcLWm5JUIa-otas4TeKZCt?usp=sharing">
    <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>


```python
from nendo import Nendo, NendoConfig

nd = Nendo(config=NendoConfig(plugins=["nendo_plugin_audiogen"]))

# load track
track = nd.library.add_track(file_path='/path/to/track.mp3')

# run audiogen with custom model
generated_collection = nd.plugins.audiogen(
    track=track,
    n_samples=5,
    prompt="dog barking",
    duration=1,
    conditioning_length=1
)
generated_collection[0].play()
```

## Contributing

Visit our docs to learn all about how to contribute to Nendo: [Contributing](https://okio.ai/docs/contributing/)


## License 

Nendo: MIT License

AudioCraft: MIT License

Pretrained models: The weights are released under the CC-BY-NC 4.0 license
