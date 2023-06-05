import logging
import os
import string


def _preprocess_text(text):
    # lowercase
    text = text.lower()
    # remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))

    return text


def _slice_text_into_samples(text, sample_size=1000):
    text = text.split()
    num_samples = len(text) // sample_size
    samples = [
        text[i * sample_size : (i + 1) * sample_size] for i in range(num_samples)
    ]

    return samples


def preprocess_and_slice_text_files(
    folder_path: str, sample_size: int = 1000
) -> dict[str, list]:
    """
    Preprocess a set of text samples. Files are lowercased, split into words,
    and then broken into chunks of the selected size (default 1000 words)

    In:
        folder_path (string): Folder to read for text files. Reads all files
            with a .txt extension.
        sample_size (int=1000): Number of words per chunk. Words at the end of
            the file that do not make a full chunk are discarded.

    Returns:
        dict[str,list]: The results. Each chunk will by indexed by a name
            constructed from the filename with the chunk number, e.g. MyFile.txt
            will produce MyFile_0, MyFile_1 ... The words in the chunk are returned
            as a list.

    """
    processed_texts = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):  # i'm skipping the Mysery files
            with open(
                os.path.join(folder_path, filename), "r", encoding="latin-1"
            ) as file:
                text = file.read()
                processed_text = _preprocess_text(text)
                samples = _slice_text_into_samples(processed_text, sample_size)
                num_samples = len(samples)
                for i, sample in enumerate(samples):
                    variable_name = filename[:-4] + "_" + str(i)
                    processed_texts[variable_name] = sample
            logging.info(
                f"'{filename}' was processed and split into {num_samples} samples"
            )

    return processed_texts
