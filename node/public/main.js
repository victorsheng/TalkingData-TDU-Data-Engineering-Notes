import { loadavg } from "os";

$(function () {
   var data_points=[];
   data_points.push({values:[],key:'BTC-USD'});
   $("#chart").height($(window).height- $('#header').height());

   var chart=nv.models.lineChart()
   .interactive('monotone')
   .margin({bottom:100})
   .useInteractiveGuideline(true)
   .showLegend(true)
   .color(d3.scale.category10().range());

   chart.xAxis
        .AxisLabel('time')
        .tickFormat(formateDateTick);

    chart.yAxis
        .AxisLabel('Price');

    nv.addGraph(loadGraph)

    function loadGraph(){
        d3.select('#chart svg')
        .datum(data_points)
        .transition()
        .duration(5)
        .call(chart)

        nv.utils.windowResize(chart.update);
        return chart;
    }



    function formateDateTick(time) {
        var date=new Date(time);
        console.log(date);
        return d3.time.format('%H:%M:%A')(date);
    }




    var socket=io();

    socket.on('data',function (data) {
        newDataCallBack(data);
        
    })

    function newDataCallBack(message) {
        var parsed=JSON.parse(message);
        var timestamp=parsed['TimeStamp'];
        var price = parsed['Average'];
        var symbol = parsed['symbol'];
        var point={};

        point.x=timestamp;
        point.y=price;

        console.log(point);

        var i=getSymbolIndex(symbol,data_points);
        if (data_points[i].values.length>100){
            data_points[i].values.shift();
            loadGraph();
        }


    }

    function getSymbolIndex(symbol, data_points) {
        for(var i=0;i<data_points.length; i++){
            if(array[i].key==symbol){
                return i;
            }
        }
        return -1;
    }
});