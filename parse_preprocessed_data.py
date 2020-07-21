import numpy as np
from tqdm.notebook import tqdm

def get_inputs_and_targets(corpus_txt_fpath, seq_length):
    
    data = open(corpus_txt_fpath, 'r').read()
    
    # ==================================================
    
    # a list of strings, one for each level
    level_strs = data.strip().split(')')[:-1]  # last item is an empty string
    
    # ==================================================
    
    chars = []
    for level_str in level_strs:
        chars.extend(list(level_str))
    chars = sorted(list(set(chars)))
    vocab_size = len(chars)
    print('Unique chars:', chars)
    print('Number of unique chars:', vocab_size)
    
    # ==================================================
    
    # create two dictionaries
    char_to_ix = { ch:i for i, ch in enumerate(chars) }
    ix_to_char = { i:ch for i, ch in enumerate(chars) }
    
    # ==================================================
    
    # each level_array is an 1-d array of integers
    level_arrays = []
    for level_str in level_strs:
        level_arrays.append(np.array([char_to_ix[char] for char in list(level_str)]))
    
    # ==================================================
    
    def get_inputs_and_targets_from_level_array(level_array):
    
        inputs, targets = [], []

        for i in range(len(level_array) - seq_length):
            inputs.append(level_array[i:i+seq_length])
            targets.append(level_array[i+1:i+seq_length+1])

        inputs, targets = map(np.array, [inputs, targets])
        inputs = np.eye(vocab_size)[inputs]

        return inputs, targets
    
    inputs, targets = [], []
    for level_array in tqdm(level_arrays, leave=False):
        inputs_temp, targets_temp = get_inputs_and_targets_from_level_array(level_array)
        inputs.extend(inputs_temp); targets.extend(targets_temp)
    inputs, targets = map(np.array, [inputs, targets])
    
    # # ==================================================
    
    return char_to_ix, ix_to_char, vocab_size, inputs, targets