from flask import Flask, render_template, request

# Flaskオブジェクトの生成
app = Flask(__name__)

#辞書型で各手数料を定義
#JCBクレジットカード,100円当たりの手数料
JCB_Annual_list={
    "2回払い":0,"3回払い":2.51,"5回払い":3.78,"6回払い":4.42,"10回払い":7,"12回払い":8.31,"15回払い":10.29,
    "18回払い":12.29,"20回払い":13.64,"24回払い":16.37,"30回払い":100,"36回払い":100,"48回払い":100
}
#Yahooクレジットカード,100円当たりの手数料
Yahoo_Annual_list= {
    "2回払い":0,"3回払い":2.04, "5回払い":3.04, "6回払い":4.08,"10回払い":6.8,"12回払い":8.16,"15回払い":10.2,
    "18回払い":12.24,"20回払い":13.6,"24回払い":16.32,"30回払い":20.4,"36回払い":24.48,"48回払い":32.64
}
#三井住友クレジットカード,100円当たりの手数料
Sumitomo_Annual_list =  {
    "2回払い":0,"3回払い":2.01, "5回払い":3.35, "6回払い":4.02,"10回払い":6.7,"12回払い":8.04,"15回払い":10.5,
    "18回払い":12.6,"20回払い":13.4,"24回払い":16.08,"30回払い":100,"36回払い":100,"48回払い":100
}
#楽天クレジットカード&REX CARD,100円当たりの手数料
Rakuten_Annual_list= {
    "2回払い":0,"3回払い":2.04, "5回払い":3.4, "6回払い":4.08,"10回払い":6.8,"12回払い":8.16,"15回払い":10.2,
    "18回払い":12.24,"20回払い":13.6,"24回払い":16.32,"30回払い":20.4,"36回払い":24.48,"48回払い":100
}
#AEONカード,100円当たりの手数料
AEON_Annual_list= {
    "2回払い":0,"3回払い":1.68, "5回払い":2.8, "6回払い":3.36,"10回払い":5.6,"12回払い":6.72,"15回払い":8.4,
    "18回払い":10.08,"20回払い":11.2,"24回払い":13.44,"30回払い":16.8,"36回払い":20.16,"48回払い":23.52
}
#Viasoカード&ライフカード,100円当たりの手数料
Viaso_Life_Annual_list= {
    "2回払い":0,"3回払い":2.04, "5回払い":3.4, "6回払い":4.08,"10回払い":6.8,"12回払い":8.16,"15回払い":10.2,
    "18回払い":12.24,"20回払い":13.6,"24回払い":16.32,"30回払い":100,"36回払い":100,"48回払い":100
}
#D CARD,100円当たりの手数料
Docomo_Annual_list =  {
    "2回払い":0,"3回払い":2.01, "5回払い":3.35, "6回払い":4.02,"10回払い":6.7,"12回払い":8.04,"15回払い":10.5,
    "18回払い":12.6,"20回払い":13.4,"24回払い":16.08,"30回払い":24.1,"36回払い":24.12,"48回払い":100
}
#支払い回数
Annual_datalist = {
    "2回払い":2,"3回払い":3, "5回払い":5, "6回払い":6, "10回払い":10, "12回払い":12, "15回払い":15, "18回払い":18, 
    "20回払い":20, "24回払い":24, "30回払い":30, "36回払い":36, "48回払い":48
}

#上限以上の支払回数が指定された場合のエラー処理
Error = False

#支払額などの計算専用関数
def Annual(Annual_data,Count_data,money):  
    #100円あたりの手数料が100である場合はその支払回数は存在しないと判断しErrorをTrueにする
    if Annual_data == 100:
        #誤った計算結果が出ないように結果を全て0にする
        Fee,Total_Pay,Monthly_Pay=0,0,0
        Error = True
        return Fee,Total_Pay,Monthly_Pay,Count_data,Error
    else:
        Fee = round(money*(Annual_data/100))
        Total_Pay = round(money+Fee)
        Monthly_Pay = round(Total_Pay/Count_data)
        Error = False
        return Fee,Total_Pay,Monthly_Pay,Count_data,Error

#完成後にTry文を使えばよかったと後悔しました...
#ErrorがTrueの場合はカード会社名にエラーメッセージを代入
def ERROR(card,Error):
    if Error == True:
        card="ご希望の支払回数に対応しておりません"
        return card
    else:
        return card

@app.route("/")
def index():
    return render_template('index.html')  

@app.route("/manager", methods=["POST"])
def manager():
    card = str(request.form.get('card'))
    money = int(request.form['money'])
    Number = request.form.get('Number')

    if card == "none":
        Fee = 0
        Count_data = Annual_datalist[Number]
        Monthly_Pay = round(money/Count_data)
        card = "(無金利分割支払い)"
        return render_template('answer.html',card = card,Count_data=Count_data,Fee=Fee,Total_Pay=money,Monthly_Pay=Monthly_Pay,Pay=money)

    #楽天カードが選択されていた場合
 

    if card == "Yahoo":
        card = "Yahoo!カード"
        Yahoo_anser = Annual(Yahoo_Annual_list[Number],Annual_datalist[Number],money)
        Count_data,Fee,Total_Pay,Monthly_Pay,Error_data = Yahoo_anser[3],Yahoo_anser[0],Yahoo_anser[1],Yahoo_anser[2],Yahoo_anser[4]
        card = ERROR(card,Error_data)
        return render_template('answer.html',card = card,Count_data=Count_data,Fee=Fee,Total_Pay=Total_Pay,Monthly_Pay=Monthly_Pay,Pay=money) 

    elif card == "Sumitomo":
        card = "三井住友クレジットカード"
        Sumitomo_anser = Annual(Sumitomo_Annual_list[Number],Annual_datalist[Number],money)
        Count_data,Fee,Total_Pay,Monthly_Pay,Error_data = Sumitomo_anser[3],Sumitomo_anser[0],Sumitomo_anser[1],Sumitomo_anser[2],Sumitomo_anser[4]
        card = ERROR(card,Error_data)
        return render_template('answer.html',card = card,Count_data=Count_data,Fee=Fee,Total_Pay=Total_Pay,Monthly_Pay=Monthly_Pay,Pay=money)

    elif card == "JCB":
        card = "JCBクレジットカード"
        JCB_anser = Annual(JCB_Annual_list[Number],Annual_datalist[Number],money)
        Count_data,Fee,Total_Pay,Monthly_Pay,Error_data = JCB_anser[3],JCB_anser[0],JCB_anser[1],JCB_anser[2],JCB_anser[4]
        card = ERROR(card,Error_data)
        return render_template('answer.html',card = card,Count_data=Count_data,Fee=Fee,Total_Pay=Total_Pay,Monthly_Pay=Monthly_Pay,Pay=money) 
 
    elif card == "AEON":
        card = "AEON CARD"
        AEON_anser = Annual(AEON_Annual_list[Number],Annual_datalist[Number],money)
        Count_data,Fee,Total_Pay,Monthly_Pay,Error_data = AEON_anser[3],AEON_anser[0],AEON_anser[1],AEON_anser[2],AEON_anser[4]
        card = ERROR(card,Error_data)
        return render_template('answer.html',card = card,Count_data=Count_data,Fee=Fee,Total_Pay=Total_Pay,Monthly_Pay=Monthly_Pay,Pay=money) 

    elif card == "Docomo":
        card = "D CARD"
        Docomo_anser = Annual(Docomo_Annual_list[Number],Annual_datalist[Number],money)
        Count_data,Fee,Total_Pay,Monthly_Pay,Error_data = Docomo_anser[3],Docomo_anser[0],Docomo_anser[1],Docomo_anser[2],Docomo_anser[4]
        card = ERROR(card,Error_data)
        return render_template('answer.html',card = card,Count_data=Count_data,Fee=Fee,Total_Pay=Total_Pay,Monthly_Pay=Monthly_Pay,Pay=money) 

    if card == "Rakuten" or "REX":
        if card=="Rakuten":
            card = "楽天カード"
        elif card =="REX":
            card = "REX CARD"
        else:
            card = card
        #計算関数であるAnnual関数に値を代入
        Rakuten_anser = Annual(Rakuten_Annual_list[Number],Annual_datalist[Number],money)
        #関数の結果がリスト構造で出力されるのでそれぞれ抽出
        Count_data,Fee,Total_Pay,Monthly_Pay,Error_data = Rakuten_anser[3],Rakuten_anser[0],Rakuten_anser[1],Rakuten_anser[2],Rakuten_anser[4]
        #エラーが生じていた場合の為にERROR関数を通す(エラーがなければそのままのcardが戻る)
        card = ERROR(card,Error_data)
        #計算結果をanswer.html内の変数にそれぞれ代入
        return render_template('answer.html',card = card,Count_data=Count_data,Fee=Fee,Total_Pay=Total_Pay,Monthly_Pay=Monthly_Pay,Pay=money)

    #同じ手数料のカード会社が複数あった為、同時に処理する
    if card == "VIASO CARD" or "Life Card" or "Orico Card":
        Viaso_anser = Annual(Viaso_Life_Annual_list[Number],Annual_datalist[Number],money)
        Count_data,Fee,Total_Pay,Monthly_Pay,Error_data= Viaso_anser[3],Viaso_anser[0],Viaso_anser[1],Viaso_anser[2],Viaso_anser[4]
        card = ERROR(card,Error_data)
        return render_template('answer.html',card = card,Count_data=Count_data,Fee=Fee,Total_Pay=Total_Pay,Monthly_Pay=Monthly_Pay,Pay=money) 

if __name__ == "__main__":
    app.run(debug=True, port=8888)