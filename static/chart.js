var chart = LightweightCharts.createChart(document.getElementById("chart"), {
	width: 1000,
  	height: 500,
	layout: {
		backgroundColor: '#000000',
		textColor: 'rgba(255, 255, 255, 0.9)',
	},
	grid: {
		vertLines: {
			color: 'rgba(197, 203, 206, 0.5)',
		},
		horzLines: {
			color: 'rgba(197, 203, 206, 0.5)',
		},
	},
	crosshair: {
		mode: LightweightCharts.CrosshairMode.Normal,
	},
	rightPriceScale: {
		borderColor: 'rgba(197, 203, 206, 0.8)',
	},
	timeScale: {
		borderColor: 'rgba(197, 203, 206, 0.8)',
		timeVisible: true,
	},
});

var candleSeries = chart.addCandlestickSeries({
	upColor: '#00897B',
	downColor: '#FF5252',
	borderUpColor: '#00897B',
	borderDownColor: '#FF5252',
	wickUpColor: '#00897B',
	wickDownColor: '#FF5252',
});

fetch('http://localhost:5000/history')
	.then((r) => r.json())
	.then((response) => {
		console.log(response);
		candleSeries.setData(response);
	})

const binanceSocket = new WebSocket("wss://stream.binance.com:9443/ws/btcusdt@kline_5m");

binanceSocket.onmessage = function (event) {
	let messageObject = JSON.parse(event.data);
	let candlestick = messageObject.k;
	candleSeries.update({
		time: candlestick.t / 1000,
		open: candlestick.o,
		high: candlestick.h,
		low: candlestick.l,
		close: candlestick.c
	})
}