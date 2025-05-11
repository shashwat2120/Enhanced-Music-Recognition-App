# Enhanced Music Recognition App

A powerful music recognition application that combines audio fingerprinting and Shazam integration to provide accurate song identification through a user-friendly Streamlit interface.

## 🌟 Features

- **Real-time Audio Recording**
  - Direct microphone input
  - Adjustable recording duration (1-10 seconds)
  - Live waveform visualization

- **File Upload Support**
  - Accepts WAV and MP3 formats
  - Batch processing capability
  - High-quality audio analysis

- **Advanced Recognition**
  - Shazam API integration for online recognition
  - Audio fingerprinting for local matching (including Indian songs)
  - High accuracy song identification

- **User Interface**
  - Clean and intuitive Streamlit interface
  - Real-time waveform visualization
  - Detailed song information display
  - Recognition confidence scoring

## 🛠️ Installation

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd music-recognition-app
   ```

2. **Create a Virtual Environment (Recommended)**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Usage

1. **Start the Application**
   ```bash
   streamlit run app.py
   ```

2. **Using the App**
   - Choose between "Record Audio" or "Upload File"
   - For recording:
     - Adjust the recording duration
     - Click "Start Recording"
     - Allow microphone access when prompted
   - For file upload:
     - Click "Browse files"
     - Select a WAV or MP3 file
     - Wait for processing

3. **View Results**
   - Audio waveform visualization
   - Song title and artist
   - Album information
   - Recognition confidence score

## 🇮🇳 Local Database for Indian Songs

You can build your own local fingerprint database for Indian (or any) songs, enabling offline recognition for tracks not found in Shazam's database.

### **A. Prepare Your Song Files**
- Collect Indian songs in WAV or MP3 format and place them in a folder, e.g., `indian_songs/`.

### **B. Build the Local Database**
1. Create a file named `build_local_db.py` with the following content:
   ```python
   import os
   import librosa
   import pickle
   from audio_fingerprint import AudioFingerprinter

   SONG_FOLDER = "indian_songs"
   DB_FILE = "indian_fingerprint_db.pkl"

   fingerprinter = AudioFingerprinter()

   for filename in os.listdir(SONG_FOLDER):
       if filename.endswith(".mp3") or filename.endswith(".wav"):
           song_path = os.path.join(SONG_FOLDER, filename)
           print(f"Processing {filename}...")
           audio_data, sr = librosa.load(song_path, sr=None)
           fingerprinter.add_song(filename, audio_data, sr)

   with open(DB_FILE, "wb") as f:
       pickle.dump(fingerprinter.database, f)

   print(f"Database saved to {DB_FILE}")
   ```
2. Place your Indian songs in the `indian_songs/` folder.
3. Run the script:
   ```bash
   python build_local_db.py
   ```
4. This will create `indian_fingerprint_db.pkl` in your project directory.

### **C. Use the Local Database in the App**
1. Load the database in your app:
   ```python
   import pickle
   from audio_fingerprint import AudioFingerprinter

   with open("indian_fingerprint_db.pkl", "rb") as f:
       db = pickle.load(f)

   fingerprinter = AudioFingerprinter()
   fingerprinter.database = db

   # To recognize a song:
   match, score = fingerprinter.recognize_song(audio_data, sr)
   if match:
       st.success(f"Local DB Match: {match} (score: {score})")
   else:
       st.info("No match found in local database.")
   ```
2. Integrate this check alongside the Shazam recognition in your Streamlit app for best results.

## 📋 Requirements

- Python 3.8 or higher
- Internet connection for Shazam integration
- Microphone access for recording feature
- Sufficient disk space for audio processing
- Modern web browser for Streamlit interface

## 🔧 Dependencies

- streamlit==1.28.0
- librosa==0.10.1
- numpy==1.24.3
- pydub==0.25.1
- scipy==1.11.3
- sounddevice==0.4.6
- shazamio==0.5.0
- python-dotenv==1.0.0
- requests==2.31.0
- matplotlib==3.7.1
- soundfile==0.12.1

## ⚠️ Troubleshooting

1. **Microphone Access Issues**
   - Ensure your microphone is properly connected
   - Check system permissions for microphone access
   - Try restarting the application

2. **Recognition Failures**
   - Verify internet connection for Shazam integration
   - Check audio quality and background noise
   - Ensure audio file format is supported (WAV/MP3)
   - For local DB, ensure your song is in the database

3. **Installation Problems**
   - Update pip: `python -m pip install --upgrade pip`
   - Install system dependencies for librosa (if needed)
   - Check Python version compatibility

4. **Performance Issues**
   - Close other resource-intensive applications
   - Reduce recording duration
   - Use smaller audio files for upload

## 🔒 Privacy & Security

- Audio recordings are processed locally
- No audio data is stored permanently
- Temporary files are automatically deleted
- Secure connection for Shazam API calls

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Shazam API for song recognition
- Streamlit for the web interface
- Librosa for audio processing
- All contributors and users of the application 