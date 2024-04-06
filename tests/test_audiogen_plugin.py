# -*- encoding: utf-8 -*-
"""Tests for the Nendo AudioGen plugin."""
import unittest

from nendo import Nendo, NendoConfig

nd = Nendo(
    config=NendoConfig(
        library_path="./library",
        log_level="INFO",
        plugins=["nendo_plugin_audiogen"],
    )
)


class AudioGenPluginTest(unittest.TestCase):
    def test_run_audiogen_generation(self):
        nd.library.reset(force=True)
        track = nd.library.add_track(file_path="tests/assets/test.wav")
        gen_collection = nd.plugins.audiogen(
            track=track,
            n_samples=2,
            prompt="dog barking",
            model="facebook/audiogen-medium",
            duration=1,
            conditioning_length=1,
        )

        self.assertEqual(len(nd.library.get_collection_tracks(gen_collection.id)), 2)
        self.assertEqual(len(nd.library.get_tracks()), 3)

    def test_run_process_audiogen_generation(self):
        nd.library.reset(force=True)
        track = nd.library.add_track(file_path="tests/assets/test.wav")
        gen_collection = track.process(
            "nendo_plugin_audiogen",
            n_samples=2,
            prompt="dog barking",
            model="facebook/audiogen-medium",
            duration=1,
            conditioning_length=1,
        )

        self.assertEqual(len(nd.library.get_collection_tracks(gen_collection.id)), 2)
        self.assertEqual(len(nd.library.get_tracks()), 3)

    def test_run_audiogen_unconditional(self):
        nd.library.reset(force=True)

        gen_collection = nd.plugins.audiogen(
            n_samples=2,
            prompt="rnb, funky, fast, futuristic",
            bpm=116,
            key="C",
            scale="Major",
            model="GrandaddyShmax/musicgen-medium",
            duration=5,
        )

        self.assertEqual(len(nd.library.get_collection_tracks(gen_collection.id)), 2)
        self.assertEqual(len(nd.library.get_tracks()), 2)

    
if __name__ == "__main__":
    unittest.main()
