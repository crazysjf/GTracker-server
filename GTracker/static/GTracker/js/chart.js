$(document).ready(function() {

var myConfig ={
 	type: "area",
 	stacked: true,
 	title:{
 	  text: "Monthly Apparel Sales",
 	  fontColor: "#424242",
 	  adjustLayout: true,
 	  marginTop: 15
 	},
 	subtitle:{
 	  text: "In thousands (k)",
 	  fontColor: "#616161",
 	  adjustLayout: true,
 	  marginTop: 45
 	},
 	plot:{
 	  aspect: "spline",
 	  alphaArea: 0.6,
 	  lineWidth : "1px",
 	  marker : {
 	    visible : true,
 	    "size": 2,
 	  },
 	},
 	plotarea:{
 	  margin: "dynamic"
 	},
 	tooltip:{visible:false},
 	scaleY:{
 	  short:true,
 	  shortUnit:'k',
 	  lineColor: "#AAA5A5",
 	  tick:{
 	    lineColor: "#AAA5A5"
 	  },
 	  item:{
 	    fontColor: "#616161",
 	    paddingRight: 5
 	  },
 	  guide:{
 	    lineStyle: "dotted",
 	    lineColor: "#AAA5A5"
 	  },
 	  label:{
 	    text: "Quantity",
 	    fontColor: "#616161"
 	  }
 	},
 	scaleX:{
 	  lineColor: "#AAA5A5",
 	  labels:["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug"],
 	  tick:{
 	    lineColor: "#AAA5A5"
 	  },
 	  item:{
 	    fontColor: "#616161",
 	    paddingTop: 5
 	  },
 	  label:{
 	    text: "2016",
 	    fontColor: "#616161"
 	  }
 	},
 	crosshairX:{
 	  lineColor: "#AAA5A5",
 	  plotLabel:{
 	    backgroundColor:"#EBEBEC",
 	    borderColor: "#AAA5A5",
 	    borderWidth: 2,
 	    borderRadius: 2,
 	    thousandsSeparator:',',
 	    fontColor:'#616161'
 	  },
 	  scaleLabel:{
 	    backgroundColor: "#EBEBEC",
 	    borderColor: "#AAA5A5",
 	    fontColor: "#424242"
 	  }
 	},
};


var requestData = {}
$.get('/GTracker/records/', requestData, function(data) {
    myConfig.series = data
    zingchart.render({
	    id : 'chartDiv',
	    data : myConfig,
	    height: '1000',
	    width: '800'
    });

    }
    )
})