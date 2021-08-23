def load_txt(path):
    
    with open(path) as f:
        text = f.read().split('\n')
    return text


def load_sample(i):
    cwd = '/'.join(__file__.split('/')[:-1])
    path = cwd + f'/SampleTexts/Sample{i}.txt'
    
    return load_txt(path)