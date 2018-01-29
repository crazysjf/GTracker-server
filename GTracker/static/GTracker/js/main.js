
$(document).ready(function() {
    // 自动更新navbar的active按钮
    $('.navbar-nav').find('a').each(function () {
            if (this.href == document.location.href) {
                $(this).parent().addClass('active'); // this.className = 'active';
            }
        });

    // 唯一码输入处理
    $('#ucode-input').bind('keypress',function(event){
      if(event.keyCode == "13") {
        event.preventDefault();
        var employee = $("#employee-select  option:selected").text();
        var ucode = $('#ucode-input').val();
        // 无输入则无动作
        if (ucode == "")
            return
        if (employee == "") {
        	showError("请先选择质检员")
        	return
        }
        
        var requestData = {ucode: ucode,
                            employee: employee }


        $.post('/QCLogger/log/', requestData, function(data) {
            if (data['error']) {
                // 数据重复
                showError("唯一码重复：" + data['e-employee'] + "，" + data['e-datetime'])
                $('#ucode-input').select()
            } else {
            	// 唯一码正常
            	insertRecordToTable($("div.ucode-table"), data)
            	clearError()
                $('#okAudio')[0].play()
                $('#ucode-input').val("")
            }
        });

       //$("#ucode-table").prepend('<tr><td>'+ $('#ucode-input').val() + '</td><td>'+'日期' + '</td></tr>');

      }
    });

    // 员工选择变化处理
    $("#employee-select").change(function(){
            var employee = $("#employee-select  option:selected").text();

            // 如果选择空，则清空列表
            if (employee == "") {
				clearRecordTable()
                return
            }


            var requestData = {employee: employee}
            $.get('QCLogger/records/', requestData, function(data) {
                setRecordTableContent($("div.ucode-table"), data) 
            })
    })

    function showError(msg) {
    	var a = $('#errorAudio')[0]
    	a.currentTime = 0 // 音频重叠时后面的播放无效。流传这样有效，实际无效
		a.play()
		$("#error-info").text(msg)
    }

    function clearError(msg) {
		$("#error-info").text("")
    }
});

