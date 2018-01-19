// Copyright 2013 Peter Cook @prcweb prcweb.co.uk
var chart = {

    data: null,
    xScale: null,
    yScale: null,
    svgLine: null,
    colorScale: null,

    perspectiveOffsetX: 5,
    perspectiveOffsetY: 4.5,
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

    hMargin: 20, // 表之间水平和垂直间隙
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
            // var yearMax = _.max(data);
            // var yearMin = _.min(data);
            return {good_id: k, sales: data['sales']};
        });
        this.data = dataset


        //d3.select('body')//.style('height', this.bodyHeight + 'px');
        // this.windowHeight = $(window).height();
        // this.scrollScale = d3.scale.linear().domain([0, this.bodyHeight - this.windowHeight]).range([0, this.data.length - 1]).clamp(true);

        // this.sortFunction.year = function (a, b) {
        //     return d3.descending(a.year, b.year);
        // }
        // this.sortFunction.mean = function (a, b) {
        //     return d3.descending(a.mean, b.mean);
        // }
        // this.sortFunction.max = function (a, b) {
        //     return d3.descending(a.max, b.max);
        // }
        // this.sortFunction.min = function (a, b) {
        //     return d3.ascending(a.min, b.min);
        // }

        this.initChart();
       // this.initEvents();
       // this.initMenu();
    },

    // initMenu: function () {
    //     var that = this;
    //     d3.select('#menu')
    //         .text('Sort by: ')
    //         .selectAll('span')
    //         .data(this.menu)
    //         .enter()
    //         .append('span')
    //         .html(function (d, i) {
    //             var html = '<span class="button">' + d.label + '</span>';
    //             if (i < that.menu.length - 1) html += ' / ';
    //             return html;
    //         });
    //
    //     d3.select('#menu')
    //         .selectAll('span.button')
    //         .classed('selected', function (d, i) {
    //             return i === 0;
    //         })
    //         .on('click', function () {
    //             var d = d3.select(this.parentNode).datum();
    //             console.log(d, d.sortBy);
    //
    //             d3.selectAll('#menu span.button')
    //                 .classed('selected', false);
    //
    //             d3.select(this)
    //                 .classed('selected', true);
    //
    //             that.updateSort(d.sortBy);
    //         });
    // },
    //
    // updateVisibleYears: function () {
    //     var that = chart; // Better way to do this?
    //
    //     var index = that.uiState.selectedIndex;
    //     var goods = d3.selectAll('#chart .goods g.good');
    //     goods.classed('hover', false);
    //
    //     goods
    //         .filter(function (d, i) {
    //             return i === index;
    //         })
    //         .classed('hover', true);
    //
    //     d3.select('#chart g.goods')
    //         .attr('transform', this.translate(that.leftMargin - index * that.perspectiveOffsetX, -that.bottomMargin + index * that.perspectiveOffsetY))
    //     goods
    //         .style('opacity', function (d, i) {
    //             if (i < index) return 0;
    //             return that.colorScale(i - index);
    //         });
    //
    //     var datum = goods.filter(function (d, i) {
    //         return i === index;
    //     }).datum();
    //     that.uiState.selectedDatum = datum;
    //
    //     that.updateInfo();
    // },


    // handleScroll: function () {
    //     var that = chart; // Better way to do this?
    //     if (that.uiState.sorting) return;
    //     var scroll = $(window).scrollTop();
    //     that.uiState.selectedIndex = Math.round(that.scrollScale(scroll));
    //     that.updateVisibleYears();
    // },

    // initEvents: function () {
    //     var that = this;
    //     $(window).scroll(this.handleScroll);
    //     $(window).on('touchmove', this.handleScroll);
    // },

    initChart: function () {
        var that = this;

        this.xScale = d3.scale.linear()
            .domain([0, that.dayRange -1])
            .range([0, this.chartWidth]);

        this.yScale = d3.scale.linear()
            .domain([0, 100])
            .range([this.chartHeight, 0]);

        this.svgLine = d3.svg.line()
            .interpolate('cardinal')
            .defined(function (d) {
                return d
            })
            .x(function (d, i) {
                return that.xScale(i);
            })
            .y(function (d) {
                return that.yScale(d);
            });

        n = Math.ceil(this.data.length / 4)
        this.svgHeight = n * (this.chartHeight + this.vMargin)
        this.svgWidth = this.columnNr * (this.chartWidth + this.hMargin)

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
                xOffset = (i % that.columnNr) * (that.chartWidth + that.hMargin)
                yOffset = parseInt(i / that.columnNr) * (that.chartHeight + that.vMargin)
                return that.translate(xOffset, yOffset);
            })

        // Add paths
        goods
            .append('path')
            .attr('d', function (d, i) {
                return that.svgLine(d.sales);
            });

        var monthScale = d3.scale.ordinal()
            .domain(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
            .rangePoints([0, that.chartWidth]);

        var yAxis = d3.svg.axis()
            .scale(this.yScale)
            .orient('left')

        var xAxis = d3.svg.axis()
            .scale(monthScale)
            .orient('bottom');
        goods.append('g').call(xAxis)
        goods.append('g').call(yAxis)

        //.tickValues([0, 2, 4, 6, 8, 10, 12, 14, 16]);

        // d3.select('#chart svg')
        //     .append('g')
        //     .classed('axes', true)
        //     .attr('transform', this.translate(this.leftMargin, that.svgHeight - this.bottomMargin));
        //this.renderAxes();
    },

    renderAxes: function () {
        var monthScale = d3.scale.ordinal()
            .domain(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
            .rangePoints([0, this.chartWidth]);

        var yAxis = d3.svg.axis()
            .scale(this.yScale)
            .orient('left')
        //.tickValues([0, 2, 4, 6, 8, 10, 12, 14, 16]);

        d3.select('#chart .axes')
            .append('g')
            .classed('axis y', true)
            .attr('transform', this.translate(0, -this.yScale(0)))
            .call(yAxis);

        var xAxis = d3.svg.axis()
            .scale(monthScale)
            .orient('bottom');

        d3.select('#chart .axes')
            .append('g')
            .classed('axis x', true)
            .call(xAxis);
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