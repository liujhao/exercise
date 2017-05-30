
function trim(str){ //删除左右两端的空格
    return str.replace(/(^\s*)|(\s*$)/g, "");
}

function addFavor(atag, newid) {
    $.ajax({
        url: "/addfavor/",
        type:'POST',
        data: {id:newid},
        success: function(r){
            var jret = jQuery.parseJSON(r);
            if(jret.status==1){
                $(atag).find("b").html(jret.data);
            }else{
                alert(jret.message)
            }
        }
    });
}

function displayReplay(newid,isShow){
    var commentDiv = $("#comment-box-area-"+newid);
    if(isShow==1){
        commentDiv.attr("isShow","1");
        commentDiv.css("display","block");
        commentDiv.find("a[lang="+newid+"]").unbind("click");
        commentDiv.find("a[lang="+newid+"]").click(function(){displayReplay(newid, 0)});
    }else if(isShow==0){
        commentDiv.attr("isShow","0");
        commentDiv.css("display","none");
    }
}

function replyItemShow(newid, flag) {
    if(flag==0){
        $("#loading-comment-top-"+newid).css("display","block");
        $("#comment-box-top-"+newid).css("display","none");
        $("#comment-list-top-"+newid).css("display","none");
        $("#huifu-top-box-"+newid).css("display","none");
        $("#hidden-comt-"+newid).css("display","none");
    }else if(flag==1){
        $("#loading-comment-top-"+newid).css("display","none");
        $("#comment-box-top-"+newid).css("display","block");
        $("#comment-list-top-"+newid).css("display","block");
        $("#huifu-top-box-"+newid).css("display","block");
        $("#hidden-comt-"+newid).css("display","block");
    }
}

function refreshReply(newid){
    $.ajax({
        url: "/newsreplytree/",
        type:'POST',
        data: {id:newid},
        success: function(r){
            jret = jQuery.parseJSON(r);
            $("#reply-count-"+newid).html(jret.length)
            $("#newestCount-"+newid).html(jret.length)
            var strhf = "";
            $.each(jret, function (k, v) {
                strhf += '<li class="items"><span class="folder" style="background: none;"><div class="comment-R comment-R-top" style="background-color: rgb(246, 246, 246);"><div class="pp"><a class="name" href="/user/emanon733/submitted/1">'+v.user__nickname+'</a><span class="p3">'+v.content+'</span><span class="into-time into-time-top">'+v.create_date+'</span></div><div class="comment-line-top" style="display: none;"></div></div></span></li>'
            })
            $("#comment-list-top-"+newid).empty();
            $("#comment-list-top-"+newid).append(strhf)
            replyItemShow(newid, 1);
        }
    });
}

function showReply(newid) {
    if($("#comment-box-area-"+newid).attr("isShow")=="0") {
        displayReplay(newid, 1);
        replyItemShow(newid, 0);
        refreshReply(newid);
        addReply(newid);        
    }else{
        displayReplay(newid,0);
    }
}

function addReply(newid){
    $("#pub-btn-top-"+newid).unbind("click");
    $("#pub-btn-top-"+newid).click(function () {
        var txthuifu  = trim($("#txt-huifu-top-"+newid).val());
        if(txthuifu != ""){
            $(this).attr("disabled",true);
            $("#pub-loading-top-"+newid).css("display","block");
            $.ajax({
                url: "/addreply/",
                type:'POST',
                data: {id:newid, content:txthuifu},
                success: function(r){
                    var jret = jQuery.parseJSON(r);
                    if(jret.status==1){
                        $("#txt-huifu-top-"+newid).val("");
                        refreshReply(newid);
                    }else{
                        alert(jret.message)
                    }
                    $("#pub-loading-top-"+newid).css("display","none");
                    $(this).attr("disabled",false);
                }
            });
        }
    });
}


window.lastChatid = 0;

$(function () {
    if($("#mCSB_1_container").size()>0){
        refreshChat();
    }
    $("#searchBtn_3").click(function () {
        doSearch();
    });
    var theUrl = window.location.href;
    var arr_url = theUrl.split("/");
    if(arr_url.length==5){
        if(arr_url[3]=="index" && arr_url[4]==""){
            setTimeout("spiderNews()",10000);
        }
    }
    $('.top-band-title a').click(function () {
        recommShow($(this).attr("id"));
    });
})

function sendChat() {
    var chatmsg = trim($("#chatmsg").val());
    if(chatmsg!=""){
        var chartDiv = $("#mCSB_1_container")
        var chartUl = $("#mCSB_1_container ul")
        $.ajax({
            url: "/sendchat/",
            type:'POST',
            async:true,
            data: {content:chatmsg},
            success: function(r){
                var jret = jQuery.parseJSON(r);
                if(jret.status==1){
                    $("#chatmsg").val("");
                    var strmsg = '';
                    strmsg += '<li class="message message-other"><div class="message-content"><div class="message-info"><a href="/user/cdu_43918428584/submitted/1" target="_blank">'+jret.data.user__nickname+'</a><span style="margin-left:7px;">'+jret.data.create_date+'</span></div><div class="message-text">'+jret.data.content.replace("\n","<br>").replace(" ","&nbsp;")+'<div class="status"></div></div></div></li>'
                    chartUl.append(strmsg);
                    chartDiv.scrollTop(chartUl.height());
                    window.lastChatid = jret.id;
                }else{
                    alert(jret.message)
                }
            }
        });
    }
}

function refreshChat() {
    var chartDiv = $("#mCSB_1_container")
    var chartUl = $("#mCSB_1_container ul")
    $.ajax({
        url: "/topchatmsg/",
        type:'POST',
        async:true,
        data:{'lastid':window.lastChatid},
        success: function(r) {
            var jret = jQuery.parseJSON(r);
            if (jret.length > 0) {
                window.lastChatid = jret[0].id;
                jret = jret.reverse();
                var strmsg = "";
                $.each(jret, function (k, v) {
                    strmsg += '<li class="message message-other"><div class="message-content"><div class="message-info"><a href="/user/cdu_43918428584/submitted/1" target="_blank">'+v.user__nickname+'</a><span style="margin-left:7px;">'+v.create_date+'</span></div><div class="message-text">'+v.content.replace("\n","<br>").replace(" ","&nbsp;")+'<div class="status"></div></div></div></li>'
                })
                chartUl.append(strmsg);
                chartDiv.scrollTop(chartUl.height());
            }
            setTimeout("refreshChat()",2000);
        }
    });
}

function doSearch() {
    var txtsearch = trim($("#txtSearch2").val());
    if(txtsearch!=""){
        $("#searchFrm2").submit();
    }
}

function spiderNews(){
    $.ajax({
        url: "/spidernews/",
        type:'POST',
        success: function(r) {
            setTimeout("spiderNews()",60000);
        }
    });
}

function recommShow(id){
    if(id=="top-title-news"){
        $('#top-title-news').attr('class','top-band-title-select');
        $('#top-title-comments').attr('class','top-band-title-default');
        $('#top-content-news').css('display','block');
        $('#top-content-comments').css('display','none');
        $('#top-bandArrow').css('left','70px')
    }else if(id=="top-title-comments"){
        $('#top-title-news').attr('class','top-band-title-default');
        $('#top-title-comments').attr('class','top-band-title-select');
        $('#top-content-news').css('display','none');
        $('#top-content-comments').css('display','block');
        $('#top-bandArrow').css('left','220px')
    }
}