import os
from pydub import AudioSegment
import streamlit as st
import shutil

def split_audio_file(audio_file, chunk_duration):
    audio = AudioSegment.from_file(audio_file)

    # Calculate the duration of each chunk in milliseconds
    chunk_length_ms = chunk_duration * 60 * 1000

    # Generate a list of start and end times for each chunk
    start_end_times = [(start, start + chunk_length_ms) for start in range(0, len(audio), chunk_length_ms)]

    # Create a directory to save the chunks
    output_dir = 'audio_chunks'
    os.makedirs(output_dir, exist_ok=True)

    # Split the audio file into chunks
    for i, (start, end) in enumerate(start_end_times):
        chunk = audio[start:end]
        chunk.export(f"{output_dir}/chunk_{i+1}.mp3", format="mp3")

    return output_dir

def main():
    st.title("ตัดไฟล์เสียงให้สั้นลงเป็นหลายไฟล์")

    # Upload the audio file
    audio_file = st.file_uploader("Upload ไฟล์เสียง", type=["mp3", "wav"])

    if audio_file is not None:
        # Specify the chunk duration in minutes
        chunk_duration = 15

        # Split the audio file into chunks
        output_dir = split_audio_file(audio_file, chunk_duration)

        st.success("Audio file successfully split into chunks!")

        # Zip the audio chunks
        shutil.make_archive("audio_chunks", "zip", output_dir)

        # Display a new expander for downloading the zip file
        with st.expander("Download Zip File"):
            file_url = "audio_chunks.zip"
            st.markdown(f"Click [here]({file_url}) to download the audio chunks.")

if name == '__main__':
    main()
