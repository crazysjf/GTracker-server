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

    hMargin: 30, // 表之间水平和垂直间隙
    vMargin: 20,

    columnNr: 4,

    dayRange: 30, // 时间范围30天

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
            return {good_id: k, sales: data['sales'], max: max, min: min};
        });
        this.data = dataset
        this.initChart();
    },

    initChart: function () {
        var that = this;

        this.xScale = d3.scale.linear()
            .domain([0, that.dayRange -1])
            .range([0, this.chartWidth]);

        n = Math.ceil(this.data.length / 4)
        this.svgHeight = n * (this.chartHeight + this.vMargin * 2)
        this.svgWidth = this.columnNr * (this.chartWidth + this.hMargin * 2)

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
                xOffset = that.hMargin + (i % that.columnNr) * (that.chartWidth + that.hMargin)
                yOffset = that.vMargin + parseInt(i / that.columnNr) * (that.chartHeight + that.vMargin)
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
            t = d3.select(this) // this即为当前的元素。这个元素必须要做成一个selection才能够进行后面的操作。
            var monthScale = d3.scale.ordinal()
                .rangePoints([0, that.chartWidth]);
            var xAxis = d3.svg.axis()
                .scale(monthScale)
                .orient('bottom');
            var yScale = yScaleGen(d.min, d.max)

            var yAxis = d3.svg.axis()
                .scale(yScale)
                .orient('left')

            axes = t.append('g').classed('axes', true)
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
                if (d.year === that.uiState.selectedDatum.year) index = i;
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