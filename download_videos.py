## Pre-requisities: run 'pip install youtube-dl' to install the youtube-dl package.
## Specify your location of output videos and input json file.
import json
import os
from pathlib import Path
import typer

app = typer.Typer()


@app.command()
def download_videos(
    output_path: Path = typer.Option(
        "/data/COIN/videos", help="Path to save downloaded videos"
    ),
    input_json_path: Path = typer.Option(
        "./COIN.json", help="Path to the input JSON file"
    ),
    cookies_path: Path | None = typer.Option(None, help="Path to the cookies file"),
    offset: int = typer.Option(0, help="Offset to start downloading videos from"),
    limit: int = typer.Option(-1, help="Limit the number of videos to download"),
    download_tool: str = typer.Option(
        "yt-dlp",
        help="Download tool to use (youtube-dl or yt-dlp)",
    ),
):
    if not output_path.exists():
        output_path.mkdir(parents=True, exist_ok=True)

    data = json.load(open(input_json_path, "r"))["database"]
    youtube_ids = list(data.keys())

    if offset > 0:
        youtube_ids = youtube_ids[offset:]
        print(f"Offset: {offset}, starting from {youtube_ids[0]}")

    if limit > 0:
        youtube_ids = youtube_ids[:limit]
        print(f"Limit: {limit}, downloading {len(youtube_ids)} videos")

    for index, youtube_id in enumerate(youtube_ids):
        info = data[youtube_id]
        type = info["recipe_type"]
        url = info["video_url"]
        video_output_directory = output_path / str(type)
        video_output_file = video_output_directory / f"{youtube_id}.mp4"
        video_output_file.parent.mkdir(parents=True, exist_ok=True)
        if video_output_file.exists():
            print(f"File {video_output_file} already exists, skipping download.")
            continue

        command = f"{download_tool} -o {str(video_output_file)} -f best {url}"
        if cookies_path is not None and cookies_path.exists():
            command += f" --cookies {cookies_path}"

        # command = f"youtube-dl -o {str(video_output_file)} -f best {url}"
        print(f"{index + 1:03d}: Downloading {url} to {video_output_directory}")
        os.system(command)


if __name__ == "__main__":
    app()
