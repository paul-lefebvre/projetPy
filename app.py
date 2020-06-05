from flask import Flask, request, redirect
from flask import render_template
from bs4 import BeautifulSoup
import requests
import json
from random import seed
from random import randint

app = Flask(__name__)


    
url = "https://api.cdiscount.com/OpenApi/json/Search"
 
params = {
          "ApiKey": "818e864c-7f59-41db-8546-6498f3d90ef0",
          "SearchRequest": {
            "Keyword": "adidas",
            "Pagination": {
              "ItemsPerPage": 10,
              "PageNumber": 1
            },
            "Filters": {
              "Price": {
                "Min": 0,
                "Max": 0
              },
              "Navigation": "Basket",
              "IncludeMarketPlace": "false"
            }
          }
        }
    
    
response = requests.post(url, data=json.dumps(params))
response = response.json()
print(response)
print("---------------")


for _ in range(9):
    rdmInt = randint(0, 9)
    
print(rdmInt)

response = response['Products'][rdmInt]


price = float(response['BestOffer']['SalePrice'])
price = int(round(price))
print(price)



#JEU
result = ["Félicitation ! Vous avez trouvé :)", "Le prix est plus petit !", "Le prix est plus élevé !", ""]
lastResultat = result[3]
nbreTestArr = [0]
nbreTest = 0
resultArray = []
lastTestedPrice = ""
testedpriceArr = []


#ROUTE
@app.route("/", methods=["GET", "POST"])
def run():
    if request.method == "POST":
        global lastResultat, nbreTestArr, resultArray, nbreTest, lastTestedPrice, testedpriceArr
        req = request.form
        lastTestedPrice = req.get("testedPrice")
        print("TEST DE PRIX : " + lastTestedPrice)
        testedpriceArr = [lastTestedPrice] + testedpriceArr

        if int(lastTestedPrice) == price:
            print("PRIX TROUVE !")
            lastResultat = result[0]
            nbreTest = nbreTest + 1
            nbreTestArr = [nbreTest] + nbreTestArr
            resultArray = resultArray + [lastResultat]

        if int(lastTestedPrice) < price:
            lastResultat = result[2]
            nbreTest = nbreTest + 1
            nbreTestArr = [nbreTest] + nbreTestArr
            resultArray = resultArray + [lastResultat]

        if int(lastTestedPrice) > price:
            lastResultat = result[1]
            nbreTest = nbreTest + 1
            nbreTestArr = [nbreTest] + nbreTestArr
            resultArray = resultArray + [lastResultat]

        return redirect(request.url)
        
    return render_template('index.html', 
    response=response, lastResultat=lastResultat, nbreTest=nbreTest, 
    nbreTestArr=nbreTestArr, resultArray=resultArray, lastTestedPrice=lastTestedPrice,
    testedpriceArr=testedpriceArr)




# run the application
if __name__ == "__main__":
    app.run(debug=True)