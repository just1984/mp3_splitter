import os

def split_mp3_files(input_folder, output_folder, max_chunk_size=3 * 1024 * 1024):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".mp3"):
            input_path = os.path.join(input_folder, filename)
            base_name = os.path.splitext(filename)[0]
            
            # Unterordner mit dem Namen der Originaldatei
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

def main():
    input_folder = "/home/just161/code/Tonie/input"
    output_folder = "/home/just161/code/Tonie/output"
    split_mp3_files(input_folder, output_folder)

if __name__ == "__main__":
    main()
