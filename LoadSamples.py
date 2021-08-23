cwd = '/'.join(__file__.split('/')[:-1])

def load_sample(i):
    path = cwd + f'/SampleTexts/Sample{i}.txt'
    
    with open(path) as f:
        text = f.read().split('\n')
    return text