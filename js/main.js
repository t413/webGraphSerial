
var points_to_keep = 60;
var number_channels = 3;
function input_parser(incoming) {
	var res = incoming.split(",");
	if (res.length < 3
		) { return 0; }
	else { return res; }
}


$(function () {
$(document).ready(function() {
	var dataEventSource;

	var chart = new Highcharts.Chart({
		chart: {
			renderTo: 'graph_data',
			type: 'line',
            animation: false,
			marginRight: 10
		},

		title: { text: 'Incoming Live Data' },
		tooltip: { enabled: false },
		plotOptions: {
			series: { marker: { enabled: false } }
		},
		yAxis: { max:1000, min:0 },

		series: (function(){ //create series's data array on-the-go
			var series = [];
			for (var i = 1; i <= number_channels; i++) {
				series.push( { name: "Input Channel "+i, data: [] } ); 
			}
			return series;
		})()
	});//new highchart
	
	$('#startStop').toggle(function(){
		var series = chart.series;
		dataEventSource = new EventSource('/data');
		dataEventSource.onmessage = function(e) {
			var n_data = input_parser(e.data); //returns an array[] of points
			if (n_data) {
				var keep_old = (series[0].data.length > points_to_keep);
				for (var i = 0; i < n_data.length; i++) {
					series[i].addPoint( parseInt(n_data[i]),false,keep_old);
				};
				chart.redraw(); //update the changes on the chart
			} else {
				console.log(e.data);
			}
		};
		this.innerHTML = "Stop Charting";
	},function(){
		if (dataEventSource) { dataEventSource.close(); }
		this.innerHTML = "Start Charting";
	});

}); //$(document).ready
}); //anomous fcn
