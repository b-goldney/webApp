from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages

# Create your views here.
def home(request):
    import requests
    import json

    if request.method == 'POST':
        ticker = request.POST['ticker'] 

        # IEX API Key: pk_4c4dc8e821524b32a0b0b2fb21b4dd6c
        api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=pk_4c4dc8e821524b32a0b0b2fb21b4dd6c")
        
        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "Error pulling stock data via the API. Probably due to a bad ticker symbol"
        return render(request, 'home.html', {'api':api})
    else:
        return render(request, 'home.html', {'ticker':"Enter a Ticker Symbol Above..."})

def about(request):
    return render(request, 'about.html', {})

def add_stock(request):
    import requests
    import json
    if request.method == 'POST':
       form = StockForm(request.POST or None)

       if form.is_valid():
           form.save()
           messages.success(request, ("Stock Added"))
           return redirect('add_stock')
    else:
        ticker = Stock.objects.all()
        output = []
        for ticker_item in ticker:

            api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + str(ticker_item)+ "/quote?token=pk_4c4dc8e821524b32a0b0b2fb21b4dd6c")
            
            try:
                api = json.loads(api_request.content)
                output.append(api) 
            except Exception as e:
                api = "Error pulling stock data via the API. Probably due to a bad ticker symbol"
     
        for company in output:
            company['marketCap'] /= 1000000000 #set all market caps in billions of dollars
            #company['marketCap'] /= format(company['marketCap'], ",") 
            company['ytdChange'] *= 100
        return render(request, 'add_stock.html', {'ticker': ticker, 'output':output})


def delete(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, ("Stock deleted"))
    return redirect(delete_stock)

def delete_stock(request):
    ticker = Stock.objects.all()
    return render(request, 'delete_stock.html', {'ticker':ticker})




