import torch
import numpy as np
import torch.nn as nn
import torch.nn.functional as F


from music21 import *
import util

def create_multivoice_training_data(encoded_notes, encoded_durations, sequence_length=8):
    parts = list(encoded_notes.keys())
    num_parts = len(parts)

    X_notes = []
    X_durations = []
    y_notes = []
    y_durations = []

    total_len = len(next(iter(encoded_notes.values())))

    for i in range(total_len - sequence_length - 1):
        note_seq = [encoded_notes[part][i:i+sequence_length] for part in parts]
        dur_seq = [encoded_durations[part][i:i+sequence_length] for part in parts]

        # Shape: (4, seq_len) → transpose to (seq_len, 4)
        note_seq = np.array(note_seq).T
        dur_seq = np.array(dur_seq).T

        # Targets: notes and durations at t+sequence_length
        note_target = [encoded_notes[part][i+sequence_length] for part in parts]
        dur_target = [encoded_durations[part][i+sequence_length] for part in parts]

        X_notes.append(note_seq)
        X_durations.append(dur_seq)
        y_notes.append(note_target)
        y_durations.append(dur_target)

    return (
        torch.tensor(X_notes, dtype=torch.long),
        torch.tensor(X_durations, dtype=torch.long),
        torch.tensor(y_notes, dtype=torch.long),
        torch.tensor(y_durations, dtype=torch.long)
    )

class MultiPartGenerator(nn.Module):
    def __init__(self, note_vocab_size, dur_vocab_size, embed_dim=32, lstm_hidden=128, num_parts=4):
        super(MultiPartGenerator, self).__init__()
        self.note_embed = nn.Embedding(note_vocab_size, embed_dim)
        self.dur_embed = nn.Embedding(dur_vocab_size, embed_dim)

        input_dim = embed_dim * 2 * num_parts
        self.lstm = nn.LSTM(input_dim, lstm_hidden, batch_first=True)

        self.note_out = nn.Linear(lstm_hidden, note_vocab_size * num_parts)
        self.dur_out = nn.Linear(lstm_hidden, dur_vocab_size * num_parts)
        self.num_parts = num_parts
        self.note_vocab_size = note_vocab_size
        self.dur_vocab_size = dur_vocab_size

    def forward(self, notes_in, durs_in):
        # Shape: (B, T, 4)
        emb_notes = self.note_embed(notes_in)   # → (B, T, 4, D)
        emb_durs = self.dur_embed(durs_in)      # → (B, T, 4, D)

        combined = torch.cat([emb_notes, emb_durs], dim=-1)  # → (B, T, 4, 2D)
        combined = combined.view(combined.shape[0], combined.shape[1], -1)  # → (B, T, 4*2D)

        lstm_out, _ = self.lstm(combined)      # → (B, T, H)
        final = lstm_out[:, -1, :]             # → (B, H)

        note_logits = self.note_out(final).view(-1, self.num_parts, self.note_vocab_size)  # (B, 4, Vn)
        dur_logits = self.dur_out(final).view(-1, self.num_parts, self.dur_vocab_size)     # (B, 4, Vd)

        return note_logits, dur_logits
    
    
def train_model(model, Xn, Xd, yn, yd, epochs=10, lr=0.001):
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    loss_fn = nn.CrossEntropyLoss()

    model.train()
    for epoch in range(epochs):
        optimizer.zero_grad()
        out_notes, out_durs = model(Xn, Xd)

        # Reshape targets to match predictions: (B, 4)
        loss_note = sum([loss_fn(out_notes[:, i], yn[:, i]) for i in range(4)])
        loss_dur = sum([loss_fn(out_durs[:, i], yd[:, i]) for i in range(4)])
        loss = loss_note + loss_dur

        loss.backward()
        optimizer.step()
        
        print(f"Epoch {epoch+1}/{epochs}, Loss: {loss.item():.4f}")
        
        
def predict_next_all_parts(model, note_seq, dur_seq):
    model.eval()
    with torch.no_grad():
        note_seq = note_seq.unsqueeze(0)  # shape (1, T, 4)
        dur_seq = dur_seq.unsqueeze(0)
        note_logits, dur_logits = model(note_seq, dur_seq)

        note_preds = torch.argmax(note_logits, dim=-1).squeeze(0).tolist()
        dur_preds = torch.argmax(dur_logits, dim=-1).squeeze(0).tolist()

    return note_preds, dur_preds
        
if __name__=='__main__':
    
    paths = corpus.getComposer('bach')

    for path in paths:
       
        sBach = corpus.parse(str(path))
        if len(sBach.parts) == 4:
            break
        
    note_dict, duration_dict = util.extract_notes_and_durations_cont(sBach)
    pitch2idx, duration2idx, encoded_notes, encoded_durations = util.encode_sequences(note_dict, duration_dict)

    # # Prepare tensors
    # Xn, Xd, yn, yd = create_multivoice_training_data(encoded_notes, encoded_durations, sequence_length=8)
    
    # # Model
    # note_vocab_size = len(pitch2idx)
    # dur_vocab_size = len(duration2idx)
    
    # model = MultiPartGenerator(note_vocab_size, dur_vocab_size)
    # train_model(model, Xn, Xd, yn, yd, epochs=20)