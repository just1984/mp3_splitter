import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
from tqdm import tqdm

def split_mp3_files(input_folder, output_folder, max_chunk_size=3 * 1024 * 1024):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".mp3"):
            input_path = os.path.join(input_folder, filename)
            base_name = os.path.splitext(filename)[0]

            target_folder = os.path.join(output_folder, base_name)
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)

            with open(input_path, "rb") as mp3_file:
                chunk_index = 1
                while True:
                    chunk = mp3_file.read(max_chunk_size)
                    if not chunk:
                        break

                    chunk_filename = f"{base_name}_{chunk_index}.mp3"
                    output_path = os.path.join(target_folder, chunk_filename)
                    
                    with open(output_path, "wb") as chunk_file:
                        chunk_file.write(chunk)

                    chunk_index += 1

            print(f"File {filename} split into {chunk_index - 1} chunks.", flush=True)

def analyze_mp3_files(input_folder, output_folder, min_silence_len=2000, silence_thresh=-40):
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".mp3"):
            input_path = os.path.join(input_folder, filename)
            base_name = os.path.splitext(filename)[0]
            print(f"\nLoading and analyzing {filename} ..", flush=True)
            audio = AudioSegment.from_mp3(input_path)
            print("Silent Segment Detection (this may take some time) ..", flush=True)
            tracks = split_on_silence(audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)
            print("Silence Analysis Complete ..", flush=True)
            print(f"\nFound {len(tracks)} potential tracks in {filename}.", flush=True)
            choice = input("Do you want to export these tracks? (y/n): ")
            if choice.lower() == "y":
                target_folder = os.path.join(output_folder, base_name)
                if not os.path.exists(target_folder):
                    os.makedirs(target_folder)
                for i, track in enumerate(tqdm(tracks, desc="\nExporting tracks", unit="track"), start=1):
                    track_filename = f"{base_name}_track_{i}.mp3"
                    output_path = os.path.join(target_folder, track_filename)
                    track.export(output_path, format="mp3")
                print(f"Export complete for {filename}.\n", flush=True)
            else:
                print(f"Skipping export for {filename}.", flush=True)

def main():
    input_folder = "/home/just161/code/Tonie/input"
    output_folder = "/home/just161/code/Tonie/output"

    print("\nOptions:")
    print("1: Split MP3 into chunks")
    print("2: Detect songs based on silent segments")
    mode = input("Your choice (1/2): ")

    if mode == "1":
        chunk_size_input = input("Please enter chunk size in MB: ")
        try:
            chunk_size_mb = float(chunk_size_input)
        except ValueError:
            print("Invalid value. Using default of 3 MB.", flush=True)
            chunk_size_mb = 3.0
        max_chunk_size = int(chunk_size_mb * 1024 * 1024)
        split_mp3_files(input_folder, output_folder, max_chunk_size)
    elif mode == "2":
        analyze_mp3_files(input_folder, output_folder)
    else:
        print("Invalid choice.", flush=True)

if __name__ == "__main__":
    main()
