from selenium import webdriver
import re

class Crypto:
  # Constructor
  def __init__(self, Name, Price, MarketCap, Volume, Change, Second24HourTradingVol, SecondVolumeMarketCap, SecondMarketDominance, SecondCirculatingSupply, SecondMarketRank):
    self.Name = Name
    self.Price = Price
    self.MarketCap = MarketCap
    self.Volume = Volume
    self.Change = Change
    self.Second24HourTradingVol = Second24HourTradingVol
    self.SecondVolumeMarketCap = SecondVolumeMarketCap
    self.SecondMarketDominance = SecondMarketDominance
    self.SecondCirculatingSupply = SecondCirculatingSupply
    self.SecondMarketRank = SecondMarketRank

# Dilwsi tou path opou vrisketai to driver tou chrome
PATH = "C:\Program Files (x86)\chromedriver.exe"

driver = webdriver.Chrome(PATH)

# Anoigma tou url tis istoselidas
driver.get('https://coinmarketcap.com/el/')

# Megenthisi tou window
driver.maximize_window()

# Stin metavliti doc vazoume ton kwdika html tis istoselidas (einai String)
doc = driver.page_source

# Dimiourgia 6 tuple opou mesa vazoume ta apotelesmata tis anazitisis tou kathe regex
CoinNames = re.findall(r'(?<=font-size="1" class="sc-1eb5slv-0 iworPT">).{0,25}(?=</p>)',doc)
CoinPrices = re.findall(r'(?<=markets/" class="cmc-link"><span>).{0,25}(?=</span>)',doc)
CoinMarketCap = re.findall(r'(?<=<span data-nosnippet="true" class="sc-1ow4cwt-1 ieFnWP">).{0,25}(?=</span>)',doc)
CoinVolume = re.findall(r'(?<=<p font-size="1" class="sc-1eb5slv-0 hykWbK font_weight_500" color="text">).{0,25}(?=</p>)',doc)
# To sigkekrimeno tuple exei mesa tin allagi tou kriptonomismatos tis teleutaies 24 wres kai tis teleutaies 7 meres
CoinChange = re.findall(r'(?<=class="sc-15yy2pl-0 hzgCfk"><span class="icon-Caret-down"></span>).{0,10}(?=<!-- -->)|(?<=class="sc-15yy2pl-0 kAXKAX"><span class="icon-Caret-up"></span>).{0,10}(?=<!-- -->)',doc)

# To sigkekrimeno tuple exei mesa to url tou kathe kriptonomismatos pou vrikame sta proigoumena regex
CoinUrl = re.findall(r'(?<=class="sc-131di3y-0 cLgOOr"><a href="/el/).{0,25}(?=markets/" class="cmc-link"><span>)',doc)

# For Debugging (Agnoiste to)
""" 
#For Debugging 
print("---------NAMES---------\n")
for count,coin in enumerate (CoinNames[9:]):
  print(count,coin)
print("\n")
print("---------Prices---------\n")
for count,coin in enumerate (CoinPrices):
  print(count,coin)
print("\n")
print("---------MarketCap---------\n")
for count,coin in enumerate (CoinMarketCap):
  print(count,coin)
print("\n")
print("---------MarketVolume---------\n")
for count,coin in enumerate (CoinVolume):
  print(count,coin)
print("\n")
print("---------Change---------\n")
index = 0
for count,coin in enumerate (CoinChange):
  if count % 2 == 0:
    print(index,coin+"%")
    index += 1
print("\n")
print("---------CoinUrl---------\n")
for count,coin in enumerate (CoinUrl):
  print(count,coin)
print("\n")
"""

# Dimiourgia List opou tha exei mesa ola ta kriptonomismata
CoinList = []

# Dimiourgia index prokeimenou na paroume mono tis teleutaies 24 wres apo to tuple tou CoinChange
CoinChangeIndex = 0

for i in range(len(CoinUrl)):
  # Anoigma tou url tis istoselidas tou kathe kriptonomismatos
  driver.get('https://coinmarketcap.com/el/'+ CoinUrl[i])
  # Vazoume ton kwdika html tis istoselidas tou kathe kriptonomismatos (einai String)
  doc = driver.page_source

  # Dimiourgia 5 tuple opou mesa vazoume ta apotelesmata tis anazitisis tou kathe regex  (ta deutera xaraktiristika)
  # Ola ta tuple exoun mesa to kathe apotelesma 2 fores
  SecondCoin24HourTradingVol = re.findall(r'(?<=hhqaJP">Trading Volume<span class="badge24h">24h</span></span></th><td><span>€).{0,30}(?=</span><div>)',doc)
  SecondCoinVolumeMarketCap = re.findall(r'(?<=<th scope="row">Volume / Market Cap</th><td>).{0,25}(?=</td></tr><tr>)',doc)
  SecondCoinMarketDominance = re.findall(r'(?<=Market Dominance</th><td><span class="">).{0,10}(?=<!-- -->)', doc)
  SecondCoinMarketRank = re.findall(r'(?<=Κατάταξη Αγοράς</th><td>).{0,10}(?=</td></tr>)', doc)
  SecondCoinCirculatingSupply = re.findall(r'(?<=<tr><th scope="row">Κυκλοφοριακή Προσφορά</th><td>)[\d,]{0,25}(?= [A-Z])', doc)

  # Stin lista CoinList prosthetoume ena stoixeio tipou Crypto me ola ta attributes tou
  # Sta onomata ksekiname apo to 9o keli giati stin arxi istoselidas iparxoun 9 kriptonomismata san highlights kai theloume na ta agnwisoume
  # Gia ta deutera xaraktiristika vazoume mesa mono to keli 0 giati to kathe tuple exei megethos 2 gia kathe epanalipsi pou oloklirwnetai kai exei to idio anagnwristiko se kathe keli
  CoinList.append(Crypto(CoinNames[i+9],CoinPrices[i],CoinMarketCap[i],CoinVolume[i],CoinChange[CoinChangeIndex]+"%",SecondCoin24HourTradingVol[0], SecondCoinVolumeMarketCap[0], SecondCoinMarketDominance[0]+"%", SecondCoinCirculatingSupply[0], SecondCoinMarketRank[0]))
  #Prosthetoume 2 sto index prokeimenou na agnoume tis perittes theseis tou CoinChange pou vriskontai oi allages twn kriptonomismatwn tis teleutaies 7 meres
  CoinChangeIndex += 2

  # For Debugging (Agnoiste to)
  """ 
  for i in range(len(SecondCoin24HourTradingVol))[1:]:
    print(SecondCoin24HourTradingVol[i])
    print(SecondCoinVolumeMarketCap[i])
    print(SecondCoinMarketDominance[i])
    print(SecondCoinMarketRank[i])
    print(SecondCoinCirculatingSupply[i])
  """

# Emfanisi apotelesmatwn apo to prwto scraping
print("--------First Scraping--------\n")
for i in CoinList:
  print("Name -> " + i.Name + " Price -> " + i.Price + " Market Cap -> " + i.MarketCap + " Volume -> " + i.Volume + " 24h Change -> " + i.Change)

print("\n")

# Emfanisi apotelesmatwn apo to deutero scraping
print("--------Second Scraping--------\n")
for i in CoinList:
  print("24h Trading Volume -> " + i.Second24HourTradingVol + " Volume Market Cap -> " + i.SecondVolumeMarketCap + " Market Dominance -> " + i.SecondMarketDominance + " Market Rank -> " + i.SecondMarketRank + " Circulating Supply -> " + i.SecondCirculatingSupply)

#Kleinei to parathiro (Ama thelete na deite an oi times einai swstes valte to se sxolio)
driver.close()

# For Debugging (Agnoiste to)
#print(doc)