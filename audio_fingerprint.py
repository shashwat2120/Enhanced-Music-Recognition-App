import numpy as np
import librosa
from scipy.ndimage import maximum_filter
from scipy.ndimage import generate_binary_structure

def create_constellation_map(audio_data, sample_rate):
    """Create a constellation map from audio data"""
    # Compute spectrogram
    spec = librosa.stft(audio_data)
    mag_spec = np.abs(spec)
    
    # Find local maxima
    struct = generate_binary_structure(2, 1)
    local_max = maximum_filter(mag_spec, footprint=struct) == mag_spec
    
    # Create constellation map
    constellation_map = []
    for time_idx in range(local_max.shape[1]):
        for freq_idx in range(local_max.shape[0]):
            if local_max[freq_idx, time_idx]:
                constellation_map.append((time_idx, freq_idx))
    
    return constellation_map

def create_fingerprint(constellation_map, fan_value=15):
    """Create a fingerprint from constellation map"""
    fingerprints = []
    
    for i, (time_idx, freq_idx) in enumerate(constellation_map):
        for j in range(1, fan_value):
            if i + j < len(constellation_map):
                time_idx2, freq_idx2 = constellation_map[i + j]
                time_delta = time_idx2 - time_idx
                
                if 0 <= time_delta <= 200:  # Limit time difference
                    fingerprints.append((
                        freq_idx,
                        freq_idx2,
                        time_delta
                    ))
    
    return fingerprints

def find_matches(fingerprints, database):
    """Find matches between fingerprints and database"""
    matches = {}
    
    for fp in fingerprints:
        if fp in database:
            for song_id, offset in database[fp]:
                if song_id not in matches:
                    matches[song_id] = []
                matches[song_id].append(offset)
    
    return matches

def find_best_match(matches):
    """Find the best matching song from matches"""
    if not matches:
        return None
    
    best_match = None
    best_score = 0
    
    for song_id, offsets in matches.items():
        if len(offsets) > best_score:
            best_score = len(offsets)
            best_match = song_id
    
    return best_match, best_score

class AudioFingerprinter:
    def __init__(self):
        self.database = {}
    
    def add_song(self, song_id, audio_data, sample_rate):
        """Add a song to the database"""
        constellation_map = create_constellation_map(audio_data, sample_rate)
        fingerprints = create_fingerprint(constellation_map)
        
        for fp in fingerprints:
            if fp not in self.database:
                self.database[fp] = []
            self.database[fp].append((song_id, 0))  # Offset is 0 for database songs
    
    def recognize_song(self, audio_data, sample_rate):
        """Recognize a song from audio data"""
        constellation_map = create_constellation_map(audio_data, sample_rate)
        fingerprints = create_fingerprint(constellation_map)
        matches = find_matches(fingerprints, self.database)
        return find_best_match(matches) 