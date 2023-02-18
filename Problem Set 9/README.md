# C$50 Finance

This problem set’s distribution code has recently changed. If you downloaded the distribution code prior to Thursday, December 1, 2022 at 12:00 AM EST, run the following terminal commands in your finance directory to download the latest version of the distribution code.

```
$ rm helpers.py
$ wget https://cdn.cs50.net/2021/fall/psets/9/finance/helpers.py
```

Implement a website via which users can “buy” and “sell” stocks, a la the below.

![image](https://user-images.githubusercontent.com/104181918/219743116-f578185e-e11e-4823-8cfe-03c48a74100d.png)

## Background

If you’re not quite sure what it means to buy and sell stocks (i.e., shares of a company), head here for a tutorial.

You’re about to implement C$50 Finance, a web app via which you can manage portfolios of stocks. Not only will this tool allow you to check real stocks’ actual prices and portfolios’ values, it will also let you buy (okay, “buy”) and sell (okay, “sell”) stocks by querying IEX for stocks’ prices.

Indeed, IEX lets you download stock quotes via their API (application programming interface) using URLs like https://api.iex.cloud/v1/data/core/quote/nflx?token=API_KEY. Notice how Netflix’s symbol (NFLX) is embedded in this URL; that’s how IEX knows whose data to return. That link won’t actually return any data because IEX requires you to use an API key (more about that in a bit), but if it did, you’d see a response in JSON (JavaScript Object Notation) format like this:

```
{
  "avgTotalVolume": 4329597,
  "calculationPrice": "tops",
  "change": 1.21,
  "changePercent": 0.00186,
  "closeSource": "official",
  "companyName": "NetFlix Inc",
  "currency": "USD",
  "iexAskPrice": 662.59,
  "iexAskSize": 8080,
  "iexBidPrice": 652.65,
  "iexBidSize": 102,
  "iexClose": 652.66,
  "iexCloseTime": 1636479523133,
  "iexLastUpdated": 1636479523133,
  "iexMarketPercent": 0.03419734093274243,
  "iexOpen": 652.66,
  "iexOpenTime": 1636479523133,
  "iexRealtimePrice": 652.66,
  "iexRealtimeSize": 30,
  "iexVolume": 43968,
  "lastTradeTime": 1636479523133,
  "latestPrice": 652.66,
  "latestSource": "IEX real time price",
  "latestTime": "12:38:43 PM",
  "latestUpdate": 1636479523133,
  "marketCap": 288341929921,
  "openSource": "official",
  "peRatio": 58.85,
  "previousClose": 651.45,
  "previousVolume": 2887523,
  "primaryExchange": "NASDAQ",
  "symbol": "NFLX",
  "week52High": 690.97,
  "week52Low": 463.41,
  "ytdChange": 0.2066202315388457
}
```

Notice how, between the curly braces, there’s a comma-separated list of key-value pairs, with a colon separating each key from its value.

Let’s turn our attention now to getting this problem’s distribution code!

## Specification

### register

Complete the implementation of register in such a way that it allows a user to register for an account via a form.

- Require that a user input a username, implemented as a text field whose name is username. Render an apology if the user’s input is blank or the username already exists.
- Require that a user input a password, implemented as a text field whose name is password, and then that same password again, implemented as a text field whose name is confirmation. Render an apology if either input is blank or the passwords do not match.
- Submit the user’s input via POST to /register.
- INSERT the new user into users, storing a hash of the user’s password, not the password itself. Hash the user’s password with generate_password_hash Odds are you’ll want to create a new template (e.g., register.html) that’s quite similar to login.html.
- Once you’ve implemented register correctly, you should be able to register for an account and log in (since login and logout already work)! And you should be able to see your rows via phpLiteAdmin or sqlite3.

### quote

Complete the implementation of quote in such a way that it allows a user to look up a stock’s current price.

- Require that a user input a stock’s symbol, implemented as a text field whose name is symbol.
- Submit the user’s input via POST to /quote.
- Odds are you’ll want to create two new templates (e.g., quote.html and quoted.html). When a user visits /quote via GET, render one of those templates, inside of which should be an HTML form that submits to /quote via POST. In response to a POST, quote can render that second template, embedding within it one or more values from lookup.

### buy

Complete the implementation of buy in such a way that it enables a user to buy stocks.

- Require that a user input a stock’s symbol, implemented as a text field whose name is symbol. Render an apology if the input is blank or the symbol does not exist (as per the return value of lookup).
- Require that a user input a number of shares, implemented as a field whose name is shares. Render an apology if the input is not a positive integer.
- Submit the user’s input via POST to /buy.
- Upon completion, redirect the user to the home page.
- Odds are you’ll want to call lookup to look up a stock’s current price.
- Odds are you’ll want to SELECT how much cash the user currently has in users.
- Add one or more new tables to finance.db via which to keep track of the purchase. Store enough information so that you know who bought what at what price and when.
  - Use appropriate SQLite types.
  - Define UNIQUE indexes on any fields that should be unique.
  - Define (non-UNIQUE) indexes on any fields via which you will search (as via SELECT with WHERE).
- Render an apology, without completing a purchase, if the user cannot afford the number of shares at the current price.
- You don’t need to worry about race conditions (or use transactions).

Once you’ve implemented buy correctly, you should be able to see users’ purchases in your new table(s) via phpLiteAdmin or sqlite3.

### index
Complete the implementation of index in such a way that it displays an HTML table summarizing, for the user currently logged in, which stocks the user owns, the numbers of shares owned, the current price of each stock, and the total value of each holding (i.e., shares times price). Also display the user’s current cash balance along with a grand total (i.e., stocks’ total value plus cash).

- Odds are you’ll want to execute multiple SELECTs. Depending on how you implement your table(s), you might find GROUP BY HAVING SUM and/or WHERE of interest.
- Odds are you’ll want to call lookup for each stock.

### sell

Complete the implementation of sell in such a way that it enables a user to sell shares of a stock (that he or she owns).

- Require that a user input a stock’s symbol, implemented as a select menu whose name is symbol. Render an apology if the user fails to select a stock or if (somehow, once submitted) the user does not own any shares of that stock.
- Require that a user input a number of shares, implemented as a field whose name is shares. Render an apology if the input is not a positive integer or if the user does not own that many shares of the stock.
- Submit the user’s input via POST to /sell.
- Upon completion, redirect the user to the home page.
- You don’t need to worry about race conditions (or use transactions).

### history

Complete the implementation of history in such a way that it displays an HTML table summarizing all of a user’s transactions ever, listing row by row each and every buy and every sell.

- For each row, make clear whether a stock was bought or sold and include the stock’s symbol, the (purchase or sale) price, the number of shares bought or sold, and the date and time at which the transaction occurred.
- You might need to alter the table you created for buy or supplement it with an additional table. Try to minimize redundancies.

### personal touch

Implement at least one personal touch of your choice:

- Allow users to change their passwords.
- Allow users to add additional cash to their account.
- Allow users to buy more shares or sell shares of stocks they already own via index itself, without having to type stocks’ symbols manually.
- Require users’ passwords to have some number of letters, numbers, and/or symbols.
- Implement some other feature of comparable scope.
