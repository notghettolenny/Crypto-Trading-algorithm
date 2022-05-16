from binance.client import Client
import time
import csv
import matplotlib.pyplot as plt
import matplotlib.animation as animaiton
from matplotlib import style

api_secret = "insert secret key from binance"
api_key = "insert api key from binance"

client = Client(api_key, api_secret)


q = client.get_recent_trades(symbol="ETHUSDT")

buys = []
sells = []
buys_disc = []
sells_disc = []
a_eth_buy = []
a_eth_sell = []
price_over_time = []
times = []
derv = []
xs = []
a = []
b = []

style.use('fivethirtyeight')

def buy(prc, qty):
    USD_amount_b = prc * qty
    if USD_amount_b >= 0:
        print("BUY: ${}, PRICE: ${}, qty: {} ETH".format(USD_amount_b, prc, qty))
        buys_disc.append(["BUY:", USD_amount_b])
        buys.append(USD_amount_b)
        a_eth_buy.append(qty)
        return


def sell(prc, qty):
    USD_amount_s = prc * qty
    if USD_amount_s >= 0:
        print("SELL: ${}, PRICE: ${}, qty: {} ETH".format(USD_amount_s, prc, qty))
        sells_disc.append(["SELL:", USD_amount_s])
        sells.append(USD_amount_s)
        a_eth_sell.append(qty)
        return

def del_prev_index(arr):
    try:
        if arr[-1] == arr[-2]:
            del arr[-2]
    except:
        pass


fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)

def animate(i):
    ax1.clear()
    ax1.plot(xs, derv)


ani = animaiton.FuncAnimation(fig, animate, interval=1000)

count = 0
t_end = time.time() + 60 * 60
while time.time() < t_end:
    trades = client.get_recent_trades(symbol="ETHUSDT")
    price = float(trades[-1]['price'])
    amount = float(trades[-1]['qty'])
    is_sell = trades[-1]['isBuyerMaker']
    price_over_time.append(price)
    times.append(int(time.clock()))
    del_prev_index(price_over_time)
    del_prev_index(buys)
    del_prev_index(sells)
    del_prev_index(a_eth_buy)
    del_prev_index(a_eth_sell)
    del_prev_index(times)
    try:
        if derv[-1] == derv[-2]:
            del derv[-2]
            del xs[-1]
    except:
        pass
    try:
        if len(price_over_time) % 20 == 0 and len(derv) == len(xs):
            dx = (price_over_time[-1] - price_over_time[-20]) / (times[-1] - times[-20])
            derv.append(dx)
            for i in range(len(derv)):
                xs.append(len(derv))
                xs = list(set(xs))
        plt.pause(0.0001)
    except:
        pass
    try:
        if len(derv) % 30 == 0:
            count += 1
            average = sum(derv) / len(derv)
            a.append(average)
            b.append(count)
    except:
        pass
    if is_sell:
        sell(price, amount)
    elif not is_sell:
        buy(price, amount)


print(times)
def get_volume_USD(l):
    new_l = []
    c_sum = 0
    for elt in l:
        c_sum += elt
        new_l.append(c_sum)
    return new_l


def to_csv(data, name):
    with open("{}.csv".format(name), "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerow(("{}".format(name), ""))
        for val in data:
            writer.writerow([val])


volumes_buy = get_volume_USD(buys)
volumes_sell = get_volume_USD(sells)
volumes_eth_buy = get_volume_USD(a_eth_buy)
volumes__eth_sell = get_volume_USD(a_eth_sell)

to_csv(buys, "Buy (USD)")
to_csv(sells, "Sell (USD)")
to_csv(volumes_buy, "Volume USD (Buy)")
to_csv(volumes_sell, "Volume USD (Sell)")
to_csv(volumes_eth_buy, "Volume ETH (Buy)")
to_csv(volumes__eth_sell, "Volume ETH (Sell)")
to_csv(price_over_time, "Price (USD)")
to_csv(derv, "Derivative of Price")

avg_slope = sum(derv) / len(derv)
slope = (price_over_time[-1] - price_over_time[0]) / (times[-1] - times[0])

print("")
print("End of array slope: {}".format(derv[-1]))
print("Average slope: {}".format(avg_slope))
print("Final slope: {}".format(slope))
print("steepest slope: {}".format(max(derv)))
print("Lowest slope: {}".format(min(derv)))

print("")

print("Buys $ Amount: ${}".format(sum(buys)))
print("Sells $ Amount: ${}".format(sum(sells)))
print("Number of SELLS above or equal to 1000: {}".format(len(sells)))
print("Number of BUYS above or equal to 1000: {}".format(len(buys)))
print("Initial Price: ${}, Final Price ${}".format(price_over_time[0], price_over_time[-1]))

print("")

print("Biggest Buy $ Order: ${}".format(max(buys)))
print("Biggest Sell $ Order: ${}".format(max(sells)))

plt.plot(xs, derv)
plt.show()