"""Unit test untuk proses tokenisasi dan sequence padding."""


class TestTokenizerPadder:
    def test_fit_and_sequences(self, tokenizer, sample_corpus):
        tokenizer.fit(sample_corpus)
        seqs = tokenizer.texts_to_sequences(["ujaran kebencian"])
        assert len(seqs[0]) == 2

    def test_padding_shape(self, padder):
        seqs = [[2, 3], [2, 3, 4, 5, 6, 7]]
        padded = padder.pad(seqs)
        assert padded.shape == (2, 5)
        assert padded[0, 2] == 0
        assert padded[0, 3] == 0
