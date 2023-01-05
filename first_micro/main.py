from flask import Flask, request, render_template
import logging
import requests
app = Flask(__name__)

@app.route('/', methods=["GET"])
def home():
    return render_template('home.html')

@app.route('/logger', methods=['GET'])
def logger():
    loggerLog = 'You entered logger page'
    app.logger.warning(loggerLog)
    app.logger.info(loggerLog)
    return render_template('logger.html', value=loggerLog)

@app.route('/cookie', methods=['GET', 'POST'])
def cookie():
    req=requests.get('https://www.google.com/')
    return req.cookies.get_dict()

@app.route('/cookie/analytics', methods=['GET', 'POST'])
def cookieGA():
    req=requests.get('https://analytics.google.com/analytics/web/#/p345090052/reports/intelligenthome')
    return req.text

@app.route('/googletrend', methods = ["GET", "POST"])
def chartpytrend():
    pytrends = TrendReq()
    kw_list = ['python']
    pytrends.build_payload(kw_list=kw_list, timeframe='today 5-y')
    trend_data = pytrends.interest_over_time()

    plt.plot(trend_data['python'])
    plt.xlabel('Date')
    plt.ylabel('Trend')

    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    chart_url = base64.b64encode(buf.getvalue()).decode()
    plt.clf()

    return render_template('plot.html', chart_url=chart_url)

if __name__ == '__main__':
    app.run(debug=True)
