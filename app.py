from flask import Flask ,render_template,request,redirect, url_for
from wordSearcher import *
import os, shutil 


# flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "./pdfs"


# some global variables
paras = []
wordsList = []
index = dict()

# utility function - combining result 
def combine(tempParas, tempWordsList, tempIndex):
    global paras,wordsList,index

    # storing previous number of paragraph
    n = len(paras)

    paras += tempParas
    wordsList += tempWordsList
    if index == {}:
        index = tempIndex
    else :
        for word, lis in tempIndex.items():
            if word in index :
                index[word] += lis
            else :
                index[word] = [0]*n + lis

# api - index 
# will index paragraphs from text and pdf input
# calculating index for a text and combining result
@app.route('/index/', methods=["GET", "POST"])
def indexing():    
    if request.method == "POST" :
        
        if 'file' not in request.files:
            text = request.form['docs']
            tempParas = parasFromText(text)
            tempWordsList = wordsListFromParas(tempParas)
            tempIndex = invertedIndex(tempWordsList)

            # now combining
            combine(tempParas, tempWordsList, tempIndex)

        else :
            f = request.files['file']
            
            if f.filename == "":
                return "Please upload valid file."

            else :
                if not os.path.exists("os.path.dirname(os.path.realpath(__file__)) + '/pdfs"):
                    os.mkdir("pdfs")
                    
                path = os.path.dirname(os.path.realpath(__file__)) + '/pdfs/'+f.filename
                print("saving file in pdfs directory...")
                f.save(path)  

                tempParas = parasFromPdf(path)
                tempWordsList = wordsListFromParas(tempParas)
                tempIndex = invertedIndex(tempWordsList)
                
                # now combining
                combine(tempParas, tempWordsList, tempIndex)                
    
    return render_template('index.html')

# api - search
# search paragraphs containing given word
@app.route('/search/', methods=["GET", "POST"])
def search():

    if request.method == "POST" :
        word = request.form['word'].lower()
        if word == "" :
            return "Please enter correct word"

        ind = parasIndex(index,word)
        paraList = [paras[i] for i in ind]
        
        return render_template("result.html",paraList = paraList)

    return render_template('search.html')

# api - clear
# will clear both the indexes and any stored documents
@app.route('/clear/')
def clear():
    global paras,wordsList,index

    paras = []
    wordsList = []
    index = dict()
    if os.path.exists("os.path.dirname(os.path.realpath(__file__)) + '/pdfs"):
        shutil.rmtree("pdfs")
        os.mkdir("pdfs")

    return redirect(url_for('indexing'))

