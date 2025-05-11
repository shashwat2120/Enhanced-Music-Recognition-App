import streamlit as st
import numpy as np
import librosa
import sounddevice as sd
import tempfile
import os
from shazamio import Shazam
import matplotlib.pyplot as plt
from pydub import AudioSegment
import io
import asyncio
import soundfile as sf
import pathlib

# Initialize Shazam client
shazam = Shazam()

def record_audio(duration=5, sample_rate=44100):
    """Record audio from microphone"""
    try:
        st.write(f"Recording for {duration} seconds...")
        recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
        sd.wait()
        return recording.flatten()
    except Exception as e:
        st.error(f"Error recording audio: {str(e)}")
        return None

def save_audio_to_temp(audio_data, sample_rate=44100):
    """Save audio data to a temporary WAV file"""
    try:
        # Create a temporary directory if it doesn't exist
        temp_dir = pathlib.Path(tempfile.gettempdir()) / "music_recognition"
        temp_dir.mkdir(exist_ok=True)
        
        # Create a temporary file in the temp directory
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav', dir=temp_dir)
        sf.write(temp_file.name, audio_data, sample_rate)
        return temp_file.name
    except Exception as e:
        st.error(f"Error saving audio: {str(e)}")
        return None

def process_audio_file(uploaded_file):
    """Process uploaded audio file"""
    try:
        # Create a temporary directory if it doesn't exist
        temp_dir = pathlib.Path(tempfile.gettempdir()) / "music_recognition"
        temp_dir.mkdir(exist_ok=True)
        
        # Create a temporary file in the temp directory
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav', dir=temp_dir)
        
        # Write the uploaded file content
        temp_file.write(uploaded_file.getvalue())
        temp_file.close()
        
        # Convert to WAV if it's an MP3
        if uploaded_file.name.lower().endswith('.mp3'):
            audio = AudioSegment.from_mp3(temp_file.name)
            wav_path = temp_file.name.replace('.mp3', '.wav')
            audio.export(wav_path, format='wav')
            os.unlink(temp_file.name)  # Delete the original MP3
            return wav_path
        
        return temp_file.name
    except Exception as e:
        st.error(f"Error processing audio file: {str(e)}")
        return None

async def recognize_song(audio_file):
    """Recognize song using Shazam"""
    try:
        if not os.path.exists(audio_file):
            st.error(f"Audio file not found: {audio_file}")
            return None
            
        result = await shazam.recognize(audio_file)
        if result and 'track' in result:
            track = result['track']
            return {
                'title': track.get('title', 'Unknown'),
                'artist': track.get('subtitle', 'Unknown'),
                'album': track.get('sections', [{}])[0].get('metadata', [{}])[0].get('text', 'Unknown'),
                'confidence': track.get('confidence', 0)
            }
    except Exception as e:
        st.error(f"Error recognizing song: {str(e)}")
    return None

def plot_waveform(audio_data, sample_rate):
    """Plot audio waveform"""
    try:
        plt.figure(figsize=(10, 4))
        plt.plot(np.linspace(0, len(audio_data)/sample_rate, len(audio_data)), audio_data)
        plt.title('Audio Waveform')
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        return plt
    except Exception as e:
        st.error(f"Error plotting waveform: {str(e)}")
        return None

async def process_recording(duration):
    """Process recorded audio"""
    try:
        audio_data = record_audio(duration)
        if audio_data is None:
            return

        temp_file = save_audio_to_temp(audio_data)
        if temp_file is None:
            return

        # Display waveform
        plt = plot_waveform(audio_data, 44100)
        if plt:
            st.pyplot(plt)
            plt.close()
        
        # Recognize song
        with st.spinner("Recognizing song..."):
            result = await recognize_song(temp_file)
            if result:
                st.success("Song recognized!")
                st.write(f"Title: {result['title']}")
                st.write(f"Artist: {result['artist']}")
                st.write(f"Album: {result['album']}")
                st.write(f"Confidence: {result['confidence']:.2f}")
        
        # Cleanup
        try:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
        except Exception as e:
            st.warning(f"Could not delete temporary file: {str(e)}")
    except Exception as e:
        st.error(f"Error processing recording: {str(e)}")

async def process_upload(uploaded_file):
    """Process uploaded audio file"""
    try:
        temp_file = process_audio_file(uploaded_file)
        if temp_file is None:
            return

        # Load and display waveform
        audio_data, sample_rate = librosa.load(temp_file)
        plt = plot_waveform(audio_data, sample_rate)
        if plt:
            st.pyplot(plt)
            plt.close()
        
        # Recognize song
        with st.spinner("Recognizing song..."):
            result = await recognize_song(temp_file)
            if result:
                st.success("Song recognized!")
                st.write(f"Title: {result['title']}")
                st.write(f"Artist: {result['artist']}")
                st.write(f"Album: {result['album']}")
                st.write(f"Confidence: {result['confidence']:.2f}")
        
        # Cleanup
        try:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
        except Exception as e:
            st.warning(f"Could not delete temporary file: {str(e)}")
    except Exception as e:
        st.error(f"Error processing upload: {str(e)}")

def main():
    st.title("Enhanced Music Recognition App")
    st.write("Record audio or upload a file to recognize music")

    # Input method selection
    input_method = st.radio("Choose input method:", ["Record Audio", "Upload File"])

    if input_method == "Record Audio":
        duration = st.slider("Recording duration (seconds)", 1, 10, 5)
        if st.button("Start Recording"):
            asyncio.run(process_recording(duration))

    else:  # Upload File
        uploaded_file = st.file_uploader("Upload audio file", type=['wav', 'mp3'])
        if uploaded_file:
            asyncio.run(process_upload(uploaded_file))

if __name__ == "__main__":
    main() 