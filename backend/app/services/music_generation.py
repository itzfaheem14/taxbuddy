import numpy as np
import tensorflow as tf
from magenta import music as mm
from magenta.models.melody_rnn import melody_rnn_sequence_generator
from magenta.models.drums_rnn import drums_rnn_sequence_generator
from magenta.models.performance_rnn import performance_rnn_sequence_generator
from magenta.protobuf import generator_pb2
from magenta.protobuf import music_pb2
import tempfile
import os
from typing import Dict, List, Optional
import librosa
import soundfile as sf

class MusicGenerationService:
    """Service for AI-powered music generation using Magenta."""
    
    def __init__(self):
        self.models = {}
        self.initialized = False
        
    def initialize_models(self):
        """Initialize Magenta models for music generation."""
        try:
            # Initialize melody RNN
            melody_config = melody_rnn_sequence_generator.get_config_map()['attention_rnn']
            self.models['melody'] = melody_rnn_sequence_generator.MelodyRnnSequenceGenerator(
                model=melody_config.model,
                details=melody_config.details,
                steps_per_quarter=4,
                checkpoint=None  # Will use pre-trained model
            )
            
            # Initialize drums RNN
            drums_config = drums_rnn_sequence_generator.get_config_map()['drum_kit']
            self.models['drums'] = drums_rnn_sequence_generator.DrumsRnnSequenceGenerator(
                model=drums_config.model,
                details=drums_config.details,
                steps_per_quarter=4,
                checkpoint=None
            )
            
            self.initialized = True
            
        except Exception as e:
            print(f"Warning: Could not initialize all music generation models: {e}")
            self.initialized = False
    
    def generate_melody_by_emotion(self, emotion: str, num_steps: int = 128, temperature: float = 1.0) -> Dict:
        """Generate a melody based on emotion."""
        try:
            if not self.initialized:
                self.initialize_models()
            
            if 'melody' not in self.models:
                return {'success': False, 'error': 'Melody model not available'}
            
            # Create emotion-based generation options
            generation_options = self._get_emotion_generation_options(emotion)
            
            # Create primer sequence (starting notes)
            primer_sequence = self._create_emotion_primer(emotion)
            
            # Generate sequence
            generator_options = generator_pb2.GeneratorOptions()
            generator_options.args['temperature'].float_value = temperature
            generator_options.generate_sections.add(
                start_time=0,
                end_time=num_steps * 0.25  # Assuming 4 steps per quarter note
            )
            
            sequence = self.models['melody'].generate(
                primer_sequence,
                generator_options
            )
            
            # Convert to audio
            audio_data = self._sequence_to_audio(sequence)
            
            return {
                'success': True,
                'sequence': sequence,
                'audio_data': audio_data,
                'emotion': emotion,
                'num_notes': len(sequence.notes),
                'duration': sequence.total_time
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def generate_drum_pattern_by_emotion(self, emotion: str, num_steps: int = 32) -> Dict:
        """Generate drum patterns based on emotion."""
        try:
            if not self.initialized:
                self.initialize_models()
            
            if 'drums' not in self.models:
                return {'success': False, 'error': 'Drums model not available'}
            
            # Create emotion-based drum primer
            primer_sequence = self._create_drum_primer(emotion)
            
            # Generate sequence
            generator_options = generator_pb2.GeneratorOptions()
            generator_options.generate_sections.add(
                start_time=0,
                end_time=num_steps * 0.25
            )
            
            sequence = self.models['drums'].generate(
                primer_sequence,
                generator_options
            )
            
            return {
                'success': True,
                'sequence': sequence,
                'emotion': emotion,
                'num_drums': len(sequence.notes),
                'duration': sequence.total_time
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def create_full_track(self, emotion: str, style_params: Dict = None) -> Dict:
        """Create a full musical track with melody and drums."""
        try:
            # Default style parameters
            default_params = {
                'tempo': 120,
                'num_bars': 8,
                'key': 'C major',
                'time_signature': '4/4'
            }
            
            if style_params:
                default_params.update(style_params)
            
            # Generate melody
            melody_result = self.generate_melody_by_emotion(
                emotion, 
                num_steps=default_params['num_bars'] * 16  # 16 steps per bar
            )
            
            if not melody_result['success']:
                return melody_result
            
            # Generate drum pattern
            drums_result = self.generate_drum_pattern_by_emotion(
                emotion,
                num_steps=default_params['num_bars'] * 16
            )
            
            # Combine sequences
            combined_sequence = self._combine_sequences(
                melody_result['sequence'],
                drums_result.get('sequence') if drums_result['success'] else None
            )
            
            # Apply style parameters
            styled_sequence = self._apply_style_parameters(combined_sequence, default_params)
            
            # Convert to audio
            audio_data = self._sequence_to_audio(styled_sequence)
            
            return {
                'success': True,
                'sequence': styled_sequence,
                'audio_data': audio_data,
                'emotion': emotion,
                'style_params': default_params,
                'melody_notes': len(melody_result['sequence'].notes),
                'drum_notes': len(drums_result['sequence'].notes) if drums_result['success'] else 0,
                'duration': styled_sequence.total_time
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _get_emotion_generation_options(self, emotion: str) -> Dict:
        """Get generation parameters based on emotion."""
        emotion_params = {
            'happy': {
                'tempo': 120,
                'scale': 'major',
                'rhythm_density': 0.7,
                'note_range': (60, 84)  # C4 to C6
            },
            'sad': {
                'tempo': 70,
                'scale': 'minor',
                'rhythm_density': 0.4,
                'note_range': (48, 72)  # C3 to C5
            },
            'angry': {
                'tempo': 140,
                'scale': 'minor',
                'rhythm_density': 0.8,
                'note_range': (36, 84)  # C2 to C6
            },
            'fear': {
                'tempo': 90,
                'scale': 'minor',
                'rhythm_density': 0.3,
                'note_range': (60, 84)
            },
            'surprise': {
                'tempo': 110,
                'scale': 'major',
                'rhythm_density': 0.6,
                'note_range': (48, 96)
            },
            'neutral': {
                'tempo': 100,
                'scale': 'major',
                'rhythm_density': 0.5,
                'note_range': (48, 84)
            }
        }
        
        return emotion_params.get(emotion, emotion_params['neutral'])
    
    def _create_emotion_primer(self, emotion: str) -> music_pb2.NoteSequence:
        """Create a primer sequence based on emotion."""
        sequence = music_pb2.NoteSequence()
        sequence.tempos.add(time=0, qpm=120)
        
        # Emotion-based chord progressions
        emotion_chords = {
            'happy': [60, 64, 67],  # C major
            'sad': [60, 63, 67],    # C minor
            'angry': [58, 62, 65],  # Bb minor
            'fear': [61, 64, 68],   # Db major
            'surprise': [62, 66, 69], # D major
            'neutral': [60, 64, 67]  # C major
        }
        
        chord = emotion_chords.get(emotion, emotion_chords['neutral'])
        
        # Add primer notes
        for i, pitch in enumerate(chord):
            note = sequence.notes.add()
            note.start_time = i * 0.5
            note.end_time = (i + 1) * 0.5
            note.pitch = pitch
            note.velocity = 80
            note.instrument = 0
        
        sequence.total_time = len(chord) * 0.5
        return sequence
    
    def _create_drum_primer(self, emotion: str) -> music_pb2.NoteSequence:
        """Create drum primer based on emotion."""
        sequence = music_pb2.NoteSequence()
        sequence.tempos.add(time=0, qpm=120)
        
        # Basic kick and snare pattern
        # Kick drum (MIDI note 36)
        kick = sequence.notes.add()
        kick.start_time = 0
        kick.end_time = 0.25
        kick.pitch = 36
        kick.velocity = 100
        kick.instrument = 9  # Drum kit
        kick.is_drum = True
        
        # Snare drum (MIDI note 38)
        snare = sequence.notes.add()
        snare.start_time = 1.0
        snare.end_time = 1.25
        snare.pitch = 38
        snare.velocity = 90
        snare.instrument = 9
        snare.is_drum = True
        
        sequence.total_time = 2.0
        return sequence
    
    def _combine_sequences(self, melody_seq: music_pb2.NoteSequence, 
                          drums_seq: Optional[music_pb2.NoteSequence] = None) -> music_pb2.NoteSequence:
        """Combine melody and drum sequences."""
        combined = music_pb2.NoteSequence()
        combined.CopyFrom(melody_seq)
        
        if drums_seq:
            for note in drums_seq.notes:
                combined_note = combined.notes.add()
                combined_note.CopyFrom(note)
        
        combined.total_time = max(melody_seq.total_time, 
                                drums_seq.total_time if drums_seq else 0)
        
        return combined
    
    def _apply_style_parameters(self, sequence: music_pb2.NoteSequence, params: Dict) -> music_pb2.NoteSequence:
        """Apply style parameters to the sequence."""
        styled_sequence = music_pb2.NoteSequence()
        styled_sequence.CopyFrom(sequence)
        
        # Update tempo
        if styled_sequence.tempos:
            styled_sequence.tempos[0].qpm = params['tempo']
        else:
            styled_sequence.tempos.add(time=0, qpm=params['tempo'])
        
        return styled_sequence
    
    def _sequence_to_audio(self, sequence: music_pb2.NoteSequence, 
                          sample_rate: int = 44100) -> np.ndarray:
        """Convert MIDI sequence to audio data."""
        try:
            # Use FluidSynth to render MIDI to audio
            # This is a simplified version - in practice you'd need FluidSynth installed
            
            # For now, return a simple sine wave based on the notes
            duration = sequence.total_time
            t = np.linspace(0, duration, int(sample_rate * duration))
            audio = np.zeros_like(t)
            
            for note in sequence.notes:
                if not note.is_drum:  # Skip drum notes for melody
                    freq = 440 * (2 ** ((note.pitch - 69) / 12))  # Convert MIDI to frequency
                    start_sample = int(note.start_time * sample_rate)
                    end_sample = int(note.end_time * sample_rate)
                    
                    if end_sample <= len(audio):
                        note_samples = np.sin(2 * np.pi * freq * t[start_sample:end_sample])
                        audio[start_sample:end_sample] += note_samples * 0.3
            
            return audio
            
        except Exception as e:
            print(f"Error converting sequence to audio: {e}")
            # Return silence as fallback
            return np.zeros(int(sample_rate * 10))
    
    def save_audio(self, audio_data: np.ndarray, filename: str, sample_rate: int = 44100) -> str:
        """Save audio data to file."""
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
                sf.write(temp_file.name, audio_data, sample_rate)
                return temp_file.name
        except Exception as e:
            raise Exception(f"Error saving audio: {e}")