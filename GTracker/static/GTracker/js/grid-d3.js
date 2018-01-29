"use strict";


/**
 * 函数说明：获取字符串长度
 * 备注：字符串实际长度，中文2，英文1
 * @param:需要获得长度的字符串
 */
function getStrLength(str) {
    var realLength = 0, len = str.length, charCode = -1;
    for (var i = 0; i < len; i++) {
        charCode = str.charCodeAt(i);
        if (charCode >= 0 && charCode <= 128){
            realLength += 1;
        }else{
            realLength += 2;
        }
    }
    return realLength;
}
/**
 * js截取字符串，中英文都能用
 * @param str：需要截取的字符串
 * @param len: 需要截取的长度
 */
function cutstr(str, len) {
    var str_length = 0;
    var str_len = 0;
    var str_cut = new String();
    str_len = str.length;
    for (var i = 0; i < str_len; i++) {
        var a = str.charAt(i);
        str_length++;
        if (escape(a).length > 4) {
            //中文字符的长度经编码之后大于4
            str_length++;
        }
        str_cut = str_cut.concat(a);
        if (str_length >= len) {
            str_cut = str_cut.concat("...");
            return str_cut;
        }
    }
    //如果给定字符串小于指定长度，则返回源字符串；
    if (str_length < len) {
        return str;
    }
}



// Copyright 2013 Peter Cook @prcweb prcweb.co.uk
var chart = {

    data: null,
    xScale: null,
    yScale: null,

    leftMargin: 30,
    bottomMargin: 30,
    svgWidth: 1200,
    svgHeight: 800,


    lineWidth: 600,
    lineHeight: 150,

    bodyHeight: 4000, // Scroll height
    windowHeight: 0,
    scrollScale: null,

    chartHeight: 100,   // 单个表宽高
    chartWidth: 300,

    hMargin: 60, // 表之间水平和垂直间隙
    vMargin: 40,

    columnNr: 4,

    dayRange: 30, // 时间范围30天

    fontSize: 14,

    menu: [
        {'label': 'Year', 'sortBy': 'year'},
        {'label': 'Maximum', 'sortBy': 'max'},
        {'label': 'Minimum', 'sortBy': 'min'},
        {'label': 'Mean', 'sortBy': 'mean'}
    ],


    uiState: {
        selectedIndex: 0,
        selectedDatum: null, // Automatically updated
        sortBy: 'year',
        sorting: false
    },

    sortFunction: {},
    openingTimer: null,


    translate: function (x, y) {
        return 'translate(' + x + ',' + y + ')';
    },


    init: function () {
        var data = {};

        var dataset = _.map(this.data, function (data, k) {
            // var yearAve = _.reduce(data, function(m, v) {return m + v;}, 0) / 12;
            var max = _.max(data['sales']);
            var min = _.min(data['sales']);
            return {good_id: k, sales: data['sales'], max: max, min: min, name: data['name']};
        });
        this.data = dataset
        this.initChart();
    },


    initChart: function () {
        var that = this;

        this.xScale = d3.scale.linear()
            .domain([0, that.dayRange -1])
            .range([0, this.chartWidth]);

        var n = Math.ceil(this.data.length / 4)
        this.svgHeight = n * (this.chartHeight + this.vMargin * 2)
        this.svgWidth  = this.columnNr * (this.chartWidth + this.hMargin * 2)

        // YEAR LINES
        var goods = d3.select('#chart svg')
            .attr('height', that.svgHeight + 'px')
            .attr('width', that.svgWidth + 'px')
            .append('g')
            .classed('goods', true)
            //.attr('transform', this.translate(30, this.chartHeight))
            .selectAll('g.good')
            .data(this.data)
            .enter()
            .append('g')
            .attr('class', function (d, i) {
                 return 'good-' + d.good_id;
            })
            .classed('good', true)
            //.sort(this.sortFunction[this.uiState.sortBy])
            .attr('transform', function (d, i) {
                var xOffset = that.hMargin + (i % that.columnNr) * (that.chartWidth + that.hMargin)
                var yOffset = that.vMargin + parseInt(i / that.columnNr) * (that.chartHeight + that.vMargin)
                return that.translate(xOffset, yOffset);
            })


        function yScaleGen(min, max) {
            return d3.scale.linear()
                .domain([min, max])
                .range([that.chartHeight, 0]);
        }


        function svgLineGen(yScale) {
            //that = this
            return d3.svg.line()
                .interpolate('cardinal')
                .defined(function (d) {
                    return d
                })
                .x(function (d, i) {
                    return that.xScale(i);
                })
                .y(function (d) {
                    return yScale(d);
                });
        }


        function drawOneChart(d, i) {
            var t = d3.select(this) // this即为当前的元素。这个元素必须要做成一个selection才能够进行后面的操作。
            var monthScale = d3.scale.ordinal()
                .rangePoints([0, that.chartWidth]);
            var xAxis = d3.svg.axis()
                .scale(monthScale)
                .orient('bottom');
            var yScale = yScaleGen(d.min, d.max)

            var yAxis = d3.svg.axis()
                .scale(yScale)
                .orient('left')

            var axes = t.append('g').classed('axes', true)
            axes.append('g')
                .classed('axis x', true)
                .attr("transform", "translate(" + 0 + "," + that.chartHeight + ")")
                .call(xAxis)
            axes.append('g')
                .classed('axis y', true)
                .call(yAxis)

            t.append('path')
                 .attr('d', function (d, i) {
                     return svgLineGen(yScale)(d.sales)
                 });
            var shortenedName = cutstr(d.name, Math.floor(that.chartWidth/that.fontSize)*2 - 2)
            t.append('text')
                .classed('good-name', true)
                .attr('x',0)
                .attr('y',that.chartHeight + that.fontSize + 2)
                .attr('font-size', that.fontSize)
                .text(shortenedName)
        }

        goods.each(drawOneChart)
    },


    updateSort: function (sortBy) {
        var that = this;
        this.uiState.sortBy = sortBy;


        // Do the sort
        var years = d3.select('#chart .years')
            .selectAll('g.year')
            .sort(this.sortFunction[this.uiState.sortBy]);


        // Persist the chosen year: get the index of the chosen year
        d3.selectAll('#chart .years g.year')
            .each(function (d, i) {
                if (d.year === that.uiState.selectedDatum.year) var index = i;
            });
        that.uiState.selectedIndex = index;


        // Transform the axes
        d3.selectAll('.axes')
            .transition()
            .duration(2000)
            .attr('transform', that.translate(25 + index * that.perspectiveOffsetX, that.chartHeight + that.yScale(0) + -index * that.perspectiveOffsetY))
            .each('end', function () {
                that.uiState.sorting = false;
            });


        // Transform the year paths
        d3.selectAll('#chart .years .year')
            .transition()
            .duration(2000)
            .attr('transform', function (d, i) {
                return that.translate(i * that.perspectiveOffsetX, -i * that.perspectiveOffsetY);
            })
            .style('opacity', function (d, i) {
                if (i < index) return 0;
                return that.colorScale(i);
            });

        // Reset scroll
        // this.uiState.sorting = true;
        // $(window).scrollTop(this.scrollScale.invert(index));
    }
}


d3.json('http://127.0.0.1:8000/GTracker/records/?shop_id=162545180', function (data) {
    chart.data = data
    chart.init();
    //chart.updateVisibleYears();
});

$(document).ready(function(){
    $.get("api/need_log_in/",function(data,status){
        if (data == true) {
            $.get("api/log_in_frag/", function (data) {
                $("div#flash").html("" + data);
            })
        }
    });
})