import numpy as np
from scipy import linalg
from collections import defaultdict


# C2 W4 Assignment
def sigmoid(z):
    # sigmoid function
    return 1.0 / (1.0 + np.exp(-z))


# C2 W4 Assignment - called from another fn
def get_idx(words, word2Ind):
    idx = []
    # get list of word indexes
    for word in words:
        idx = idx + [word2Ind[word]]
    return idx


# +
# C2 W4 Assignment - called from another fn

def pack_idx_with_frequency(context_words, word2Ind):
    freq_dict = defaultdict(int)
    for word in context_words:
        freq_dict[word] += 1
        
    # call another utils fn
    idxs = get_idx(context_words, word2Ind)
    packed = []
    for i in range(len(idxs)):
        idx = idxs[i]
        # for the context word, find the freq/count of occurrences
        freq = freq_dict[context_words[i]]
        # append to the 'packed' list => tuple of index + freq
        packed.append((idx, freq))
    return packed


# -

# C2 W4 Assignment - called from another fn
def get_vectors(data, word2Ind, V, C):
    i = C
    while True:
        y = np.zeros(V)
        x = np.zeros(V)
        
        center_word = data[i]
        y[word2Ind[center_word]] = 1
        
        context_words = data[(i - C) : i] + data[(i + 1) : (i + C + 1)]
        num_ctx_words = len(context_words)
        
        # call another utils fn
        for idx, freq in pack_idx_with_frequency(context_words, word2Ind):
            x[idx] = freq / num_ctx_words
        
        # x stores probabilities of each context word appearing
        # y stores the center word's one-hot vector
        yield x, y
        
        i += 1
        if i >= len(data):
            print("i is being set to 0")
            i = 0


# C2 W4 Assignment
def get_batches(data, word2Ind, V, C, batch_size):
    batch_x = []
    batch_y = []
    for x, y in get_vectors(data, word2Ind, V, C):
        while len(batch_x) < batch_size:
            batch_x.append(x)
            batch_y.append(y)
        else:
            yield np.array(batch_x).T, np.array(batch_y).T
            # batch_x = []
            # batch_y = []


# C2 W4 Assignment
def compute_pca(data, n_components=2):
    """
    Input: 
        data: of dimension (m,n) where each row corresponds to a word vector
        n_components: Number of components you want to keep.
    Output: 
        X_reduced: data transformed in 2 dims/columns + regenerated original data
    pass in: data as 2D NumPy array
    """

    m, n = data.shape

    ### START CODE HERE ###
    
    # GET THE MEAN ACROSS ROWS PER COL => 50 COL MEANS
    # THEN SUBTRACT MEAN FROM THE CELL VALUE
    # mean center the data
    data -= data.mean(axis=0)
    
    # calculate the covariance matrix
    R = np.cov(data, rowvar=False)
    
    # calculate eigenvectors & eigenvalues of the covariance matrix
    # use 'eigh' rather than 'eig' since R is symmetric,
    # the performance gain is substantial
    evals, evecs = linalg.eigh(R)
    
    # sort eigenvalue in decreasing order
    # this returns the corresponding indices of evals and evecs
    
    # EIGENVALUES => SORT IN ASCENDING ORDER => RETRIEVE INDEXES
    # [::-1] => RETRIEVES INDEXES IN DESCENDING ORDER
    idx = np.argsort(evals)[::-1]

    # sort eigenvectors according to same index
    # RETRIEVE THE CORRESPONDING EIGENVECTORS IN THE SAME DESCENDING INDEXES ORDER
    evecs = evecs[:, idx]
    # RETRIEVE THE CORRESPONDING EIGENVALUES IN THE SAME DESCENDING INDEXES ORDER
    evals = evals[idx]
    
    # select the first n eigenvectors (n is desired dimension
    # of rescaled data array, or dims_rescaled_data)
    evecs = evecs[:, :n_components]
    ### END CODE HERE ###
    return np.dot(evecs.T, data.T).T


def get_dict(data):
    """
    Input:
        K: the number of negative samples
        data: the data you want to pull from
        indices: a list of word indices
    Output:
        word_dict: a dictionary with the weighted probabilities of each word
        word2Ind: returns dictionary mapping the word to its index
        Ind2Word: returns dictionary mapping the index to its word
    """
    #
    #     words = nltk.word_tokenize(data)
    words = sorted(list(set(data)))
    n = len(words)
    idx = 0
    # return these correctly
    word2Ind = {}
    Ind2word = {}
    for k in words:
        word2Ind[k] = idx
        Ind2word[idx] = k
        idx += 1
    return word2Ind, Ind2word
