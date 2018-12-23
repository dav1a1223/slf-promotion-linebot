from sklearn import feature_extraction
from sklearn.feature_extraction.text import CountVectorizer 
from sklearn.feature_extraction.text import TfidfTransformer
import jieba as jb
import pickle
from gensim.models import word2vec
from scipy import spatial

class CandReplyer:
	def __init__(self):
		self.vectorizer = pickle.load(open("vectorizer", "rb"))
		self.transformer = pickle.load(open("tfidf", "rb"))
		self.wmodel = word2vec.Word2Vec.load("wmodel.w2v")
		self.thres = 0.4
		self.candidate_replies = {
		    "興趣，喜好": "我的興趣是打羽毛球與打爵士鼓",
		    "未來，發展，目標": "未來希望能夠從事AI相關的開發，特別是NLP的領域，將新技術融入產品之中",
		    "動機": "LINE是一間擁有龐大資料的公司，特別是文字方面的資料，因此在NLP領域有很大的潛力",
		    "應徵，職位": "希望未來能夠應徵貴公司的NLP Engineer職位，實習也希望能加入NLP Team協助開發",
		    "專長，擅長": "我的專長是打羽毛球，從高中開始打了9年",
		    "程式，寫code": "我比較擅長Python與Ruby, 擅長的深度學習工具是PyTorch",
		    "學歷，大學，研究所": "我大學念台大資管，目前繼續就讀台大資管所碩二",
		    "論文，研究": "我的碩士論文主要研究Machine Reading Comprehension的技術",
		    "工作經驗，實習": "大學時曾經在iCook實習一年擔任後端工程師, 碩一暑假在台達電擔任NLP工程師",
		    "工作內容": "iCook時設計與建置API, 台達電時研究前沿的自動摘要技術",
		    "自我介紹": "目前就讀台灣大學資訊管理學系碩二，研究所期間主要在研究Deep Learning NLP領域中的閱讀理解問題，實際實作過許多論文中的模型，並正在撰寫碩士論文目標投稿ACL 2019。工作經驗有在台達電子做過自動摘要技術的研究，以及大學部期間擁有一年的後端開發實習經驗，熟悉設計與實作基礎的網頁系統與API。",
		    "預設": "抱歉我不懂您的意思"
		}

	def sent2vec(self, sent):
	    sent_split = jb.lcut(sent)
	    sent_blank = " ".join(sent_split)
	    sent_tfidf = self.transformer.transform(self.vectorizer.transform([sent_blank])).toarray()[0]
	    sent_vec = []
	    for word in sent_split:
	        if word in self.wmodel.wv.vocab:
	            if word in self.vectorizer.vocabulary_:
	                weight = sent_tfidf[self.vectorizer.vocabulary_[word]]
	            else:
	                weight = 0.05
	            if len(sent_vec) == 0:
	                sent_vec = weight * self.wmodel.wv[word]
	            else:
	                sent_vec += weight * self.wmodel.wv[word]
	    return sent_vec / len(sent_split)

	def reply(self, query):
		query_vec = self.sent2vec(query)
		max_similarity = -1
		cur_cand = "預設"
		for cand in self.candidate_replies.keys():
		    # print(cand, ": ", end="")
		    cand_vec = self.sent2vec(cand)
		    simi = 1 - spatial.distance.cosine(query_vec, cand_vec)
		    # print(simi)
		    if simi > max_similarity and simi > self.thres:
		        max_similarity = simi
		        cur_cand = cand
		return self.candidate_replies[cur_cand]
