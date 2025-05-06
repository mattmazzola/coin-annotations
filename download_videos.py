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
    limit: int = typer.Option(10, help="Limit the number of videos to download"),
):
    if not output_path.exists():
        output_path.mkdir(parents=True, exist_ok=True)

    data = json.load(open(input_json_path, "r"))["database"]
    youtube_ids = list(data.keys())[:limit]

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

        command = f"yt-dlp -o {str(video_output_file)} -f best {url}"
        # command = f"youtube-dl -o {str(video_output_file)} -f best {url}"
        print(f"{index + 1:03d}: Downloading {url} to {video_output_directory}")
        os.system(command)


if __name__ == "__main__":
    app()
