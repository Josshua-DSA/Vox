import unittest
from src.preprocessing.tokenizer import TextTokenizer
from src.preprocessing.padder import SequencePadder


class TestTokenizerPadder(unittest.TestCase):
    """Unit test untuk proses tokenisasi dan sequence padding."""

    def setUp(self) -> None:
        self.tokenizer = TextTokenizer(vocab_size=100)
        self.padder = SequencePadder(max_len=5, padding="post", pad_value=0)

    def test_fit_and_sequences(self) -> None:
        corpus = ["ujaran kebencian dilarang", "kebencian menimbulkan masalah"]
        self.tokenizer.fit(corpus)
        seqs = self.tokenizer.texts_to_sequences(["ujaran kebencian"])
        self.assertEqual(len(seqs[0]), 2)

    def test_padding_shape(self) -> None:
        seqs = [[2, 3], [2, 3, 4, 5, 6, 7]]
        padded = self.padder.pad(seqs)
        self.assertEqual(padded.shape, (2, 5))
        # Test post-padding zero
        self.assertEqual(padded[0, 2], 0)
        self.assertEqual(padded[0, 3], 0)


if __name__ == "__main__":
    unittest.main()
