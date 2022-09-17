"""A module for loading XDF files recorded with TMSi amplifiers."""
import os

import mne
import numpy as np
import pyxdf

PathLike = str | os.PathLike
VerbosityLevel = str | int | bool | None


def read_raw_xdf(
    xdf_fname: PathLike,
    stream_picks: int | str = 1,
    scale: int | float = 1e-6,
    verbose: VerbosityLevel = True,
):
    """Reader for .xdf files recorded with TMSi amplifiers.

    Parameters
    ----------
    xdf_fname : str | os.PathLike
        Path to the XDF file.
    stream_picks : int | str
        Streams to load. Can be either an int corresponding to the "stream_id",
         or a str corresponding to the "name" of the stream. Note that
         "stream_id" indexing starts at 1 and NOT at 0.
    scale : int | float
        Scaling factor for data. Default scaling factor is 1e-6.
    verbose: bool | None
        Verbosity level.

    Returns
    -------
    raw : instance of RawXDF
        A Raw object containing XDF data.

    See Also
    --------
    mne.io.Raw : Documentation of attribute and methods.
    """
    return RawXDF(
        xdf_fname=xdf_fname,
        stream_picks=stream_picks,
        scale=scale,
        verbose=verbose,
    )


class RawXDF(mne.io.BaseRaw):
    """Raw object from .xdf file recorded with a TMSi amplifier.

    Parameters
    ----------
    xdf_fname : str | os.PathLike
        Path to the XDF file.
    stream_picks : int | str
        Streams to load. Can be either an int corresponding to the "stream_id",
         or a str corresponding to the "name" of the stream. Note that
         "stream_id" indexing starts at 1 and NOT at 0.
    scale : int | float
        Scaling factor for data. Default scaling factor is 1e-6.
    verbose: bool | None
        Verbosity level.

    Attributes
    ----------
    impedances : dict
        A dictionary of all electrodes and their impedances.

    See Also
    --------
    mne.io.Raw : Documentation of attribute and methods.
    """

    def __init__(
        self,
        xdf_fname: PathLike,
        stream_picks: int | str = 1,
        scale: int | float = 1e-6,
        verbose: VerbosityLevel = True,
    ) -> None:
        xdf_fname = os.path.abspath(xdf_fname)
        if verbose:
            print("Reading file:\n", xdf_fname)
        streams, _ = pyxdf.load_xdf(xdf_fname)

        stream = self._pick_streams(streams, stream_picks)
        if verbose:
            print(
                f"Number of streams in file: {len(streams)}."
                f"\nStreams being loaded: {stream_picks}."
            )

        sfreq = float(stream["info"]["nominal_srate"][0])
        ch_names, type_dict, units, impedances = self._get_channel_info(stream)
        ch_types = self._convert_types(type_dict)

        info = mne.create_info(
            ch_names=ch_names,
            sfreq=sfreq,
            ch_types=ch_types,  # type: ignore
            verbose=verbose,
        )
        info = self._add_channel_locs(stream=stream, info=info)

        orig_format = self._get_orig_format(stream)

        preload = self._data_from_stream(stream=stream, scale=scale)
        super().__init__(
            info,
            filenames=(xdf_fname,),
            orig_format=orig_format,
            preload=preload,  # type: ignore
            verbose=verbose,
            orig_units=units,
        )
        self.impedances = impedances

    def _pick_streams(
        self, streams: list[dict], stream_picks: int | str
    ) -> dict:
        """_summary_

        Parameters
        ----------
        streams : list[dict]
            _description_
        stream_picks : int | str
            _description_

        Returns
        -------
        dict
            _description_
        """
        if isinstance(stream_picks, int):
            iter_items = ("stream_id",)
        elif isinstance(stream_picks, str):
            iter_items = ("name", 0)
        else:
            raise TypeError(
                "stream_picks must be one of either int or str. Got:"
                f"{stream_picks} (type: {type(stream_picks)})."
            )
        stream_map = {}
        for ind, stream in enumerate(streams):
            stream_item = stream["info"]
            for item in iter_items:
                stream_item = stream_item[item]
            stream_map[stream_item] = ind

        id_pick = stream_map[stream_picks]
        streams_picked = streams[id_pick]
        return streams_picked

    def _data_from_stream(self, stream: dict, scale: float) -> np.ndarray:
        """Get recorded data from XDF stream.

        Parameters
        ----------
        stream : dict
            XDF stream as returned by pyxdf.load_xdf()
        scale : int | float
            Scaling factor for data. Default scaling factor is 1e-6.

        Returns
        -------
        np.ndarray
            Data in the format (n_channels, n_samples)
        """
        data = stream["time_series"].astype(np.float64).T
        data_scaled = data * scale
        return data_scaled

    def _convert_types(self, ch_types: dict[str, str]) -> list[str]:
        converted_types = []
        for _, ch_type in ch_types.items():
            ch_type = ch_type.lower()
            if ch_type not in _type_list:
                ch_type = "misc"
            converted_types.append(ch_type)
        return converted_types

    def _get_channel_info(
        self, stream: dict
    ) -> tuple[list[str], dict[str, str], dict[str, str], dict]:
        """Get information about channels from XDF stream.

        Parameters
        ----------
        stream : dict
            XDF stream as returned by pyxdf.load_xdf()

        Returns
        -------
        tuple[list[str], dict[str, str], dict[str, str], dict]
            Channel names, types, units and impedances. Types, units and
            impedances are dictionaries where each channel name is a key with
            its corresponding value.
        """
        ch_names = []
        types, units, impedances = {}, {}, {}

        channels = stream["info"]["desc"][0]["channels"][0]["channel"]
        for channel in channels:
            ch_name = str(channel["label"][0])
            ch_names.append(ch_name)
            types[ch_name] = channel["type"][0]
            units[ch_name] = channel["unit"][0]
            if channel["impedance"]:
                impedances[ch_name] = channel["impedance"][0]
            else:
                impedances[ch_name] = np.nan

        return ch_names, types, units, impedances

    def _add_channel_locs(self, stream: dict, info: mne.Info) -> mne.Info:
        """Read channel locations and convert unit from mm to m.

        Parameters
        ----------
        stream : dict
            XDF stream as returned by pyxdf.load_xdf()
        info : mne.Info
            mne.Info object.

        Returns
        -------
        mne.Info
            Modified mne.Info object.
        """
        channels = stream["info"]["desc"][0]["channels"][0]["channel"]
        for ind, ch_name in enumerate(channels):
            if ch_name["location"]:
                info["chs"][ind]["loc"][0] = (
                    float(ch_name["location"][0]["X"][0]) * 1e-3
                )
                info["chs"][ind]["loc"][1] = (
                    float(ch_name["location"][0]["Y"][0]) * 1e-3
                )
                info["chs"][ind]["loc"][2] = (
                    float(ch_name["location"][0]["Z"][0]) * 1e-3
                )
        return info

    def _get_orig_format(self, stream: dict) -> str:
        """Get original data format ("channel_format") from XDF stream.

        Parameters
        ----------
        stream : dict
            XDF stream as returned by pyxdf.load_xdf()

        Returns
        -------
        str
            Data format. Will be one of "short", "int", "single" or "double".

        Raises
        ------
        ValueError
            A ValueError is raised if "channel_format" is not one of
            "int16", "int32", "float32" or "float64".
        """
        ch_format = stream["info"]["channel_format"][0]
        if ch_format not in _format_dict:
            raise ValueError(
                "Given 'channel_format' found in XDF stream info is not"
                f" supported. Must be one of: {*_format_dict.keys(),}."
                f" Got: {ch_format}."
            )
        return _format_dict[ch_format]


_format_dict = {
    "int16": "short",
    "int32": "int",
    "float32": "single",
    "float64": "double",
}

_type_list = [
    "ecg",
    "bio",
    "stim",
    "eog",
    "misc",
    "seeg",
    "dbs",
    "ecog",
    "mag",
    "eeg",
    "ref_meg",
    "grad",
    "emg",
    "hbr",
    "hbo",
]
