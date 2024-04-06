# Advanced Usage

## Unconditional Generation

The basic mode of usage for `nendo-plugin-audiogen` is to generate unconditional sound effects.
If no `NendoTrack` or `NendoCollection` is given when calling the plugin,
it will generate sound from scratch.

```python
from nendo import Nendo, NendoConfig

nd = Nendo(config=NendoConfig(plugins=["nendo_plugin_audiogen"]))
generated_collection = nd.plugins.audiogen(
    n_samples=5,
    prompt="dog barking",
    duration=30
)
```

## Outpainting

Outpainting is the process of generating music from a prompt and a `NendoTrack`.
The plugin will use the `NendoTrack`'s signal as a conditioning signal for the music generation
and continue the track from there.

!!! note
    A very important parameter for this mode is `conditioning_length`.
    This parameter determines how many seconds of the `NendoTrack`'s
    signal will be used for conditioning and when the outpainting starts.

```python
from nendo import Nendo, NendoConfig

nd = Nendo(config=NendoConfig(plugins=["nendo_plugin_audiogen"]))
track = nd.library.add_track(file_path='/path/to/track.mp3')

generated_collection = nd.plugins.audiogen(
    track=track,
    n_samples=5,
    prompt="dog barking",
    duration=30,
    conditioning_length=10
)


## Parameters

| Parameter               | Description                                                                                           | Default Value     |
|-------------------------|-------------------------------------------------------------------------------------------------------|-------------------|
| prompt                  | Prompt for the generation.                                                                            | "" (empty string) |
| temperature             | Temperature for the generation, controlling randomness of the next token.                             | 1.0               |
| cfg_coef                | Coefficient for the generation, influencing the strength of the prompt as a conditioning signal.      | 3.5               |
| start_time              | Start time for the generation.                                                                        | 0                 |
| duration                | Duration of the generation in seconds.                                                                | 30                |
| conditioning_length     | Conditioning length for the generation in seconds.                                                    | 6                 |
| seed                    | Seed for the generation.                                                                              | -1                |
| n_samples               | Number of samples to generate.                                                                        | 1                 |
