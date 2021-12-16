from flask import Flask,render_template,request,redirect,url_for
import pandas as pd
from sklearn.model_selection import train_test_split

app = Flask(__name__, template_folder='templates')

@app.route("/")
def hello():
    # new = modelRF.predict([[1,2022,100,1.52,28,85]])
    return render_template('index.html')

@app.route('/predict', methods=['GET','POST'])
def tambah():
   if request.method == 'POST':
      angin = request.form['angin']
      hujan = request.form['hujan']
      lembab = request.form['lembab']
      temperatur = request.form['temperatur']
      bulan = request.form['bulan']
      tahun = request.form['tahun']
      df = pd.read_excel("dataset.xlsx")
      df.dtypes
      
      for x in df:
        if df[x].dtypes == "int64":
            df[x] = df[x].astype(float)
            print (df[x].dtypes)
      df = df.select_dtypes(exclude=['object'])
      df=df.fillna(df.mean())
      X = df.drop('hostpot',axis=1)
      y = df['hostpot']  
      X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
      from sklearn.ensemble import RandomForestRegressor
      regressor = RandomForestRegressor(n_estimators = 1000, random_state = 42)
      modelRF = regressor.fit(X_train, y_train)
      new = modelRF.predict([[bulan,tahun,hujan,angin,temperatur,lembab]])
      rst = round(new[0])
      return render_template('result.html', new=rst)
   else:
      return render_template('tambah.html')

@app.route('/result')
def result():
   return render_template('result.html')
            
if __name__ == '__main__':
    app.run()
