
$(function () {
   var data_points=[];
    data_points.push({ values: [], key: 'BTC-USDC' });
//    data_points.push({ values: [{ x: 1559525937, y: 1 }, { x: 1559527937, y: 200 }, { x: 1559529937, y: 30 }, { x: 1559531937, y: 30 }], key: 'demo2' });
   $("#chart svg").height($(window).height()- $('#header').height());
    $("#chart svg").width(1000)
    // $("#chart svg").height($(window).width());

   var chart=nv.models.lineChart()
   .interactive('monotone')
       .margin({left:100,bottom:100})
   .useInteractiveGuideline(true)
   .showLegend(true)
//    .color(d3.scale.category10().range());



    // var int = self.setInterval(function () {
    //     console.log(data_points)
    // }, 1000);


   chart.xAxis
       .axisLabel('Time')
       .tickFormat(formateDateTick);

    chart.yAxis
        .axisLabel('Price');

    nv.addGraph(loadGraph);

    function loadGraph(){
        d3.select('#chart svg')
            // .datum(mockData())
            .datum(data_points)
        .transition()
        .duration(5)
        .call(chart)

        nv.utils.windowResize(chart.update);
        return chart;
    }



    function formateDateTick(time) {
        var date=new Date(time);
        return d3.time.format('%H:%M:%S')(date);
    }




    var socket=io();

    socket.on('data',function (data) {
        console.log('recived msg: %s',data)
        newDataCallBack(data);
        
    })

    function newDataCallBack(message) {
        var parsed=JSON.parse(message);
        var timestamp = parsed['Timestamp'];
        var price = parsed['Average'];
        var symbol = parsed['Symbol'];
        var point={};

        point.x = timestamp;
        point.y=price;

    

        var i=getSymbolIndex(symbol,data_points);
        

        data_points[i].values.push(point);

        if (data_points[i].values.length>100){
            data_points[i].values.shift();
        }
        console.log(data_points)
        loadGraph();

    }

    function getSymbolIndex(symbol, array) {
        for (var i = 0; i < array.length; i++){
            if(array[i].key==symbol){
                return i;
            }
        }
        return -1;
    }
});


function mockData() {
    var sin = [], sin2 = [],
        cos = [];

    //Data is represented as an array of {x,y} pairs.
    for (var i = 0; i < 100; i++) {
        sin.push({ x: i, y: Math.sin(i / 10) });
        sin2.push({ x: i, y: Math.sin(i / 10) * 0.25 + 0.5 });
        cos.push({ x: i, y: .5 * Math.cos(i / 10) });
    }

    //Line chart data should be sent as an array of series objects.
    return [
        {
            values: sin,      //values - represents the array of {x,y} data points
            key: 'Sine Wave', //key  - the name of the series.
            color: '#ff7f0e'  //color - optional: choose your own line color.
        },
        {
            values: cos,
            key: 'Cosine Wave',
            color: '#2ca02c'
        },
        {
            values: sin2,
            key: 'Another sine wave',
            color: '#7777ff',
            area: true      //area - set to true if you want this line to turn into a filled area chart.
        }
    ];
}