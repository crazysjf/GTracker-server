$(document).ready(function() {
    // 自动更新navbar的active按钮
    $('.navbar-nav').find('a').each(function () {
            if (this.href == document.location.href) {
                $(this).parent().addClass('active'); // this.className = 'active';
            }
        });
})


// 生成列表里面的行
// data格式：{employeeList: [e1,e2,e3], ucodeList: [u1,u2,u3], datetimeList: [d1,d2,d3] ]
function makeRows(data) {
    var tr = ""
    employeeList = data['employeeList']
    ucodeList    = data['ucodeList']
    datetimeList = data['datetimeList']
    
    for (var i  in ucodeList) {
        tr += '<tr><td>';
        tr += employeeList[i]
        tr += '</td><td>';
        tr += ucodeList[i]
        tr += '</td><td>';
        tr += datetimeList[i]
        tr += '</td></tr>'
    }
    return tr
}

    
// 在列表中插入一行
function insertRecordToTable(tableDiv, data) {
	$("table", tableDiv).prepend(makeRows(data))
    var cntE = $("span.total-cnt", tableDiv)
    var cnt = parseInt(cntE.text()) + 1
    cntE.text(cnt)
}

// table: div元素，包含一个总数显示和一个表
function setRecordTableContent(tableDiv, data) {
	$("span.total-cnt", tableDiv).text(data['ucodeList'].length)
	$("table tbody", tableDiv).html(makeRows(data))
}

// 清除列表
function clearRecordTable(tableDiv) {
    $("span.total-cnt", tableDiv).text("")
	$("table tbody", tableDiv).html("")
}
