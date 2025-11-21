MKVBatcher is a lightweight Windows application built with Python and Tkinter. It is designed to batch-attach subtitle files to MKV videos in a fast and simple way.

Instead of re-encoding the video stream, MKVBatcher uses mkvmerge (MKVToolNix) to merge subtitle tracks directly into the MKV container. This means zero quality loss and very fast processing.

The application works with any video or audio codec that can exist inside an MKV container.

## Requirements

MKVBatcher requires MKVToolNix (mkvmerge) to be installed on your system.

Download MKVToolNix here:
https://mkvtoolnix.download/

After installation, either:
- Add mkvmerge to your system PATH
OR
- Provide the full path to mkvmerge.exe inside the app

## Supported input formats

Container (input):
- Matroska (MKV)

Subtitles:
- SubRip (SRT)

Video codecs supported inside MKV:
- H.264 / AVC (mkv, mp4)
- H.265 / HEVC (mkv, mp4)
- MPEG-2 / MPEG-4 (mpg, mp4)
- VP8 / VP9 (webm, mkv)
- AV1 (mkv, mp4)

Audio codecs supported inside MKV:
- AAC (m4a, mp4, mkv)
- AC3 / E-AC3 (mkv, mp4)
- DTS / DTS-HD (mkv)
- FLAC (mkv)
- MP3 (mp3, mkv)
- Opus (webm, mkv)
- PCM / WAV (wav, mkv)

MKVBatcher never modifies or re-encodes the original streams. It only merges them into a single MKV container using MKVToolNix.

## Key features

- Batch processing of multiple MKV files
- Smart matching of SRT files even when filenames are not identical
- No re-encoding, original quality preserved
- Support for multiple subtitle languages
- Clean and simple GUI
- Optional deletion of original files
- Custom input and output folders
- MKVToolNix integration

## Ideal for

- Large movie or TV episode collections
- Subtitles generated with Whisper or similar tools
- Fast archival or media cleanup
- Organizing multilingual video content
