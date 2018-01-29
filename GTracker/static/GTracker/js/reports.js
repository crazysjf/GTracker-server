$(document).ready(function() {
    $("#search-button").click(function(event){
        event.preventDefault();
        var employee 	= $("#employee-select  option:selected").text();
        var startDate 	= $('#start-date-picker').val();
        var endDate   	= $('#end-date-picker').val();
        var ucode 		= $('#ucode-input').val();
        var requestData = { employee: 	employee,
                            startDate: 	startDate,
                            endDate: 	endDate,
                            ucode: 		ucode }
  		$.get('/QCLogger/records/', requestData, function(data) {
			setRecordTableContent($("div.ucode-table"), data)

			var counts = {}
			for (var i in data['ucodeList']) {
				var e = data['employeeList'][i] 
				var c = counts[e]
				counts[e] = typeof(c)=="undefined" ? 1 : c+1  
			}

			updateSumaryTable(counts)
        })
    });

    function updateSumaryTable(counts) {
    	var tr = ""
	  	for (var i  in counts) {
	        tr += '<tr><td>';
	        tr += i
	        tr += '</td><td>';
	        tr += counts[i]
	        tr += '</td></tr>'
	    }


	    $("table#summary-table tbody").html(tr)
    }

    var p = {
    	dateFormat:"yy-mm-dd"
    }

    var a = [$("#start-date-picker"), $("#end-date-picker")]
	for (var i in a) {
		a[i].datepicker(p).attr("readonly","readonly")
		a[i].val(getDateStr())
	}
	
	function getDateStr() {
		var date = new Date();
		var year=date.getFullYear();
		var month=date.getMonth()+1;
		var day=date.getDate();
		var str=year+'-'+month+'-'+day;
		return str	
	}
})

