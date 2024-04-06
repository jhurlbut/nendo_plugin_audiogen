import os
import time
import yaml
import torch
import subprocess
from logging import Logger
from typing import Any, Optional, Literal
from tqdm import tqdm
import json
import audiocraft
from audiocraft.models import AudioGen
from audiocraft.utils import export
from nendo import Nendo, NendoConfig, NendoGeneratePlugin, NendoTrack, NendoCollection

from .config import NendoAudioGenConfig
from .audiogen import load_model, do_predictions

settings = NendoAudioGenConfig()


class NendoAudioGen(NendoGeneratePlugin):
    """A nendo plugin for sound generation based on AudioGen by Facebook AI Research.
    https://github.com/facebookresearch/audiocraft/

    Examples:
        ```python
        from nendo import Nendo, NendoConfig

        nendo = Nendo(config=NendoConfig(plugins=["nendo_plugin_audiogen"]))
        track = nendo.library.add_track_from_file(
            file_path="path/to/file.wav",
        )

        outpaintings = nendo.plugins.audiogen(
            track=track,
            prompt="thrash metal, distorted guitars",
            n_samples=5
        )

        outpaintings.tracks()[0].play()
        ```
    """

    nendo_instance: Nendo = None
    config: NendoConfig = None
    logger: Logger = None
    model: AudioGen = None
    current_version: str = None

    def __init__(self, **data: Any):
        """Initialize plugin."""
        super().__init__(**data)
        self.logger.info("Initializing plugin: AUDIOGEN")

    @NendoGeneratePlugin.run_track
    def generate(
        self,
        track: Optional[NendoTrack] = None,
        prompt: str = "",
        temperature: float = 1.0,
        cfg_coef: float = 3.5,
        start_time: int = 0,
        duration: int = 30,
        conditioning_length: int = 1,
        seed: int = -1,
        n_samples: int = 2,
        model: str = settings.model
    ):
        """Generate an outpainting from a track or generate a track from scratch.

        Args:
            track (Optional[NendoTrack]): Track to generate from
            prompt (Optional[str]): Prompt for the generation.
            temperature (Optional[float]): Temperature for the generation. Controls how "random" the next token will be.
            cfg_coef (Optional[float]): Coefficient for the generation. Controls how strong the prompt is used
                as a conditioning signal.
            start_time (Optional[int]): Start time for the generation.
            duration (Optional[int]): Duration of the generation.
            conditioning_length (Optional[int]): Conditioning length for the generation.
            seed (Optional[int]): Seed for the generation.
            n_samples (Optional[int]): Number of samples to generate.
            model (Optional[str]): Model version to use.

        Returns:
            List[NendoTrack]: List of generated tracks.
        """
        
        if model != self.current_version:
            self.model = load_model(version=model)
            self.current_version = model

        if track is None:
            audiogen_sample = None
            sr = None
        else:
            y, sr = track.signal, track.sr
            audiogen_sample = (sr, y[:, : sr * duration].T)

        params = {
            "prompt": prompt,
            "temperature": temperature,
            "cfg_coef": cfg_coef,
            "start_time": start_time,
            "duration": duration,
            "conditioning_length": conditioning_length,
            "seed": seed,
            "model_version": model,
        }

        outputs = do_predictions(
            model=self.model,
            logger=self.logger,
            global_prompt=prompt,
            temperature=temperature,
            sr_select=sr or settings.sample_rate,
            trim_start=start_time,
            trim_end=(
                duration
            ),
            overlay=conditioning_length,
            duration=duration,
            sample=audiogen_sample,
            cfg_coef=cfg_coef,
            seed=seed,
            n_samples=n_samples,
        )

        if track is None:
            return [
                self.nendo_instance.library.add_track_from_signal(
                    signal=output,
                    sr=settings.sample_rate,
                    meta={"generation_parameters": params or {}},
                )
                for output in outputs
            ]
        return [
            self.nendo_instance.library.add_related_track_from_signal(
                signal=output,
                sr=sr,
                track_type="audiogen",
                relationship_type="audiogen",
                related_track_id=track.id,
                track_meta={"generation_parameters": params or {}},
            )
            for output in outputs
        ]
