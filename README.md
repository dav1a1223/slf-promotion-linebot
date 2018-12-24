# slf-promotion-linebot

![QR code](https://raw.githubusercontent.com/dav1a1223/slf-promotion-linebot/master/QRcode.jpg)

我實作了兩種模式（但其中一種因為 Heroku Slug Size 限制無法 Demo）\
我主要使用的資料集是我自己在Facebook Messenger上的聊天記錄作為基礎資料。\

## Promote Mode
我先寫定好幾個常被問到的問題（興趣, 專長, 自我介紹, 學歷等等）\
透過我的全部聊天記錄用 jieba 斷詞後，使用 gensim word2vec 做預訓練，得到每一個詞的 256 維向量\
當收到文字訊息後，將這個訊息轉換成一個句向量去和每個候選回答做相似度計算，高於一個 threshold 就回傳最高相似度回答，若每一候選句的相似度都低於 threshold 則回覆無法理解\
而得到句向量的方法是：因為每一個詞的重要性不一，因此我用 TFIDF 作為權重乘上該詞的向量加總，因此對於 TFIDF 較高的詞會給予較多考慮，避免被 stopword 影響。

## Chat Mode
(因Heroku Slug Size限制，無法在上面運行PyTorch而無法Demo)\
我利用我的全部聊天記錄預處理成QA的形式（Q為別人，A為我的回答），大約有26萬筆資料\
使用 [Transformer](https://arxiv.org/abs/1706.03762) Model 訓練 Sequence-to-Sequence Model
能獲得基礎的聊天功能：\
Q: "要睡覺了嗎？" A: "好啊"

## 檔案介紹
1. `src/` 存放我的 jupyter notebook file，包含我的預處理以及訓練模型的檔案
2. `models/` 存放我訓練好的各種模型
3. `main.py` 為主要處理 line bot api 的檔案，並會呼叫其他的 module 來回答
4. `simi_extract.py` promote mode 的程式碼
5. `chatter.py` chat mode 的程式碼 

