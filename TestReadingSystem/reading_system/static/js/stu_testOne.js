$(function(){
  countTime();
  checkTime();
  uploadInfo();
})
var isStart=true;
var start=new Date();

function countTime(){
    var now=new Date();
    if(isStart)
    {
        isStart=false;
        start=now;
    }
    var differ_m = (now.getMinutes() - start.getMinutes() + 60) % 60;
    var differ_s = (now.getSeconds() - start.getSeconds() + 60) % 60;
    differ_m = checkTime(differ_m);
    differ_s = checkTime(differ_s);
    document.getElementById('differ_time').innerText = differ_m + ":" + differ_s;
    t = setTimeout(function(){countTime()},500);
}
function checkTime(i){
    if (i<10){
        i="0" + i;
    }
    return i;
}

function uploadInfo(){
    $('#start').click(function(){
        alert("向后台传输答题情况")
        console.log("向后台传输答题情况")
        $.ajax({
            url: "/stu/uploadInfo/",
            type: "post",
            data: {name:'qhx', password: '123'},
            dataType: "JSON",
            success: function (res){
                if(res.status) {
                    console.log("向后台传输答题情况成功");
                    console.log(this.data);
                }
            }
        })
    })
}
