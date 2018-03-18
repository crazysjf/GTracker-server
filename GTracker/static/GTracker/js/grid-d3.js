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

    hMargin: 80, // 表之间水平和垂直间隙
    vMargin: 100,

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
            return {good_id: data['gid'], sales: data['sales'], max: max, min: min, name: data['name'], shop_name:data['shop_name'], create:data['create'], main_pic:data['main_pic']};
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
        this.svgHeight = n * (this.chartHeight + this.vMargin)
        this.svgWidth  = this.columnNr * (this.chartWidth + this.hMargin)

        // YEAR LINES
        d3.select('#chart svg').remove()
        d3.select('#chart').append('svg')

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
                var yOffset =  5 + parseInt(i / that.columnNr) * (that.chartHeight + that.vMargin)
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
                .interpolate('monotone')
                .defined(function (d) {
                    if (d == null)
                        return false;
                    else
                        return true;
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
                .attr('stroke-width', 2)
                 .attr('d', function (d, i) {
                     return svgLineGen(yScale)(d.sales)
                 });
            var shortenedName = cutstr(d.name, Math.floor(that.chartWidth/that.fontSize)*2 - 2)

            t.append('a').attr('xlink:href', 'http://item.taobao.com/item.htm?id=' + d.good_id)
                .attr('target','new')

            var x_off = 60

            t.select('a').append('text')
                .classed('good-name', true)
                .attr('x',x_off)
                .attr('y',that.chartHeight + that.fontSize + 2)
                .attr('font-size', that.fontSize)
                .text(shortenedName)

            t.append('text')
                .classed('good-name', true)
                .attr('x',x_off)
                .attr('y',that.chartHeight + 2 * that.fontSize + 2)
                .attr('font-size', that.fontSize)
                .text(d.shop_name)
            t.append('text')
                .classed('good-name', true)
                .attr('x',x_off)
                .attr('y',that.chartHeight + 3 * that.fontSize + 2)
                .attr('font-size', that.fontSize)
                .text(d.create)

            t.append('image')
                .classed('good-name', true)
                .attr('x', 0)
                .attr('y', that.chartHeight)
                .attr('height', '50px')
                .attr('width', '50px')
                .attr('xlink:href',  d.main_pic)
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


function init_pagination(eleNr) {
    $(".pagination").paging(eleNr, {
        perpage: 200,
        format: '[< ncnnnnnnnn >]',     // 显示10个数字
        onSelect: function (page) {
            var shop_id = get_shop_id()
            var sort_method = get_sort_method()
            var offset = this.slice[0]
            var limit  = this.slice[1] - this.slice[0]
            d3.json("http://127.0.0.1:8000/GTracker/records/?shop_id=" + shop_id + "&sort=" + sort_method + "&offset=" + offset + "&limit=" + limit , function (data) {
                chart.data = data
                chart.init();
            })
            return false
        },
        onFormat: function (type) {
            switch (type) {
                case 'block': // n and c
                    if (!this.active)
                        return '<span class="disabled">' + this.value + '</span>';
                    else if (this.value != this.page)
                        return '<a href="#' + this.value + '">' + this.value + '</a>';
                    return '<span class="current">' + this.value + '</span>';

                case 'next': // >
                    return '<a>&gt;</a>';
                case 'prev': // <
                    return '<a>&lt;</a>';
                case 'first': // [
                    return '<a>|<</a>';
                case 'last': // ]
                    return '<a>>|<a>';
            }
        }
    });
}

function get_shop_id() {
    var shopId  = $($("#shop-select  option:selected")[0]).attr('shop_id')
    if (typeof(shopId) == "undefined")
        shopId = null
    return shopId
}

function get_sort_method() {
    var sort = $($("#sort-select  option:selected")[0]).attr('param_str')
    return sort
}

function genChart() {
    var shopId = get_shop_id()
    var sort = get_sort_method()

    d3.json("http://127.0.0.1:8000/GTracker/goods_nr/?shop_id=" + shopId + "&sort=" + sort, function (data) {
        init_pagination(data['goods_nr'])
    })
}

$(document).ready(function() {


    $("#shop-select").change(function () {
        var opt = $("#shop-select  option:selected")[0]

        var shopId = get_shop_id()
        var shopLink = 'https://shop' + shopId + ".taobao.com"
        $("#enter-shop-button").attr({'href': shopLink})
        genChart()
    })

    $("#sort-select").change(function () {
        genChart()
    })

    genChart()
})
