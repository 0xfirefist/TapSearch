import heapq, re, string, subprocess

# get paras from given text
def parasFromText(text):
    text = re.sub('\r|\x0b|\x0c|\t','',text)
    text = re.sub(' +',' ',text)

    paras = text.lower().split("\n\n")
    for i in range(len(paras)):
        paras[i] = re.sub("\n",'',paras[i])

    return paras

# get paras from pdf
def parasFromPdf(pdfName):

    # run a command to extract data from pdfName
    process = subprocess.Popen(['pdf2txt.py', pdfName], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, _ = process.communicate()

    text = stdout.decode('utf-8')

    return parasFromText(text)

# list of words corresponding to each paragraph
def wordsListFromParas(paras):
    return [ re.sub('['+string.punctuation+']', '', para).split() for para in paras ]

# function to generate inverted index of form 
# { word : [value equal to number of occurence of word in paragraph corresponding to the index] }
def invertedIndex(wordsList):
    index = {}

    for i in range(len(wordsList)) :
        words = wordsList[i]
        for word in words :    
            if word not in index :
                index[word] = [0] * len(wordsList)
                index[word][i] += 1
            else :
                index[word][i] += 1

    return index

# return a list of indexes with top n values
def listTopNInd(lis, n):
    if(len(lis) <= n):
        return [i for i in range(len(lis))]

    return heapq.nlargest(n, range(len(lis)), lis.__getitem__)

# return paragraph indexes corresponding to the word
def parasIndex(index, word):
    
    word = word.lower()
    if word not in index :
        return []

    parasInd = index[word]
    top10 = listTopNInd(parasInd,10)

    top = []
    for i in top10:
        if parasInd[i]!=0 :
            top += [i]

    return top



    
