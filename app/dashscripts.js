$(document).ready(function(){
            //hides the alerts until needed
            $("#messban").hide();
            $("#alarmmess").hide();
            //currently unused, for tracking which button is pressed for graph
            var hehumopt=1;
            var watopt=1;
            rdata();//run at launch
            function rdata() {
                $.getJSON('data.json', function (data) {//repeating function to pull data from py script
                    //assign
                    //$('#wlev').text(35)
                    grayLocks(data['door']);;
                    grayAlarm(data['astat'])
                    showwater(data['water level']);
                    showheat(data['temp']);
                    dstring(data['tor']);
                    pirResponse(data['presence'],data['astat']);
                    graphHeat();
                    graphWater();
                    //pretty little humidity gauge
                    $("#humgGauge").gauge(data['humid'],{color: "#0d63ff"});
                });
            }
            function graphHeat() {//graphs heat and humidity on same graph. currently just
                //last minue, but want to give the graph other options as well
                var legendSettings = {
                    position: "nw",
                    show: true,
                    noColumns: 2};
                var recnum;
                var skipnum;
                switch (hehumopt){
                    case 1:
                        recnum=24;
                        skipnum=1;
                    break;
                    case 2:
                        recnum=1440
                        skipnum=60;
                    break;
                    case 3:
                        recnum=24*1440;
                        skipnum=60*24
                    break;
                    }
                var reqstr = "tempinfo.json?num="+recnum+"&skip="+skipnum
                //pulls data, formats it into the pairs necessary for flot
                $.getJSON(reqstr, function (tempinfo) {
                    var plotdata = [];
                    var humset = [];
                    for (i = 0; i < tempinfo["times"].length; i++) {
                        plotdata.push([tempinfo['times'][i], tempinfo["temps"][i]]);
                        humset.push([tempinfo['times'][i], tempinfo["hums"][i]]);
                    }
                    //options I like the look of fill, but we can get rid of it
                    var data = [
                        //heat
                        {color: "red", lines: {show: true, fill: true}, data: plotdata, label: "Heat"},
                        {color: "cyan", lines: {show: true, fill: true}, data: humset, label: "Humidity"}
                    ];
                    $.plot("#hehumgraph", data, {
                        legend: legendSettings,
                        xaxis: {
                            mode: "time", timeBase: "seconds", timezone: "browser",
                            min: tempinfo["times"][tempinfo["times"].length - 1],
                            max: tempinfo["times"][0]
                        },
                        yaxis: {
                            min: 0,
                            max: 100
                        }
                    });
                    $("#footer").prepend("Flot " + $.plot.version + " &ndash; ");
                    //console.log(tempinfo['temps']);
                });
            }

            function graphWater(){//same as heat, but only 1 set of data
               var legendSettings = {
                    position: "nw",
                    show: true,
                    noColumns: 2};
                var recnum;
                var skipnum;
                switch (watopt){
                    case 1:
                        recnum=24;
                        skipnum=1;
                    break;
                    case 2:
                        recnum=1440
                        skipnum=60;
                    break;
                    case 3:
                        recnum=24*1440;
                        skipnum=60*24;
                    break;
                    }
                    var reqstr = "watinfo.json?num="+recnum+"&skip="+skipnum
                $.getJSON(reqstr, function (watinfo) {
                    var plotdata = [];

                    for (i = 0; i < watinfo["times"].length; i++) {
                        plotdata.push([watinfo['times'][i], watinfo["levs"][i]]);
                    }
                    var today = new Date(1000 * watinfo["times"][0]);
                    var data = [
                        //heat
                        {color: "cyan", lines: {show: true, fill: true}, data: plotdata, label: "Gallons"}
                    ];
                    $.plot("#watgraph", data, {
                        legend: legendSettings,
                        xaxis: {
                            mode: "time", timeBase: "seconds", timezone: "browser",
                            min: watinfo["times"][watinfo["times"].length - 1],
                            max: watinfo["times"][0]
                        },
                        yaxis: {
                            min: 0,
                            max: 40
                        }
                    });
                    $("#footer").prepend("Flot " + $.plot.version + " &ndash; ");
                    //console.log(tempinfo['temps']);
                });
            }
            //function for determining the messages up top, need to migrate the turn on alarm function
            function pirResponse(near, armed){
                $("#alarmmess").removeClass("alert-warning");
                $("#alarmmess").removeClass("alert-info");
                if(near && armed)
                {
                    $("#alarmmess").show();
                    $("#alarmmess").text("Person Near, Alarm Engaged!")
                    $("#alarmmess").addClass("alert-info");
                }
                else{
                        if (near) {
                            $("#alarmmess").show();
                            $("#alarmmess").text("Person Near, Alarm System Offline!!")
                            $("#alarmmess").addClass("alert-warning");
                        } else {
                            $("#alarmmess").hide();
                        }
                }
            }
            function dstring(tor){//creates a nice string for the last update and updates it
                var tUsed = new Date(1000*tor);
                var monarr = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"];
                mon = monarr[tUsed.getMonth()];
                day = tUsed.getDate();
                min = tUsed.getMinutes();
                if (min<10)
                {
                    min = "0" + min;
                }
                var upTime = "Last Updated: " + tUsed.getHours()+":"+min+ " " +mon + " " + day;
                $("#timeread").text(upTime);
            }
            function grayLocks(lbool){//clears color classes, then assigns based off of lock state
                $('#locked').removeClass("btn-secondary");
                $('#locked').removeClass("btn-success");
                $('#notlocked').removeClass("btn-secondary");
                $('#notlocked').removeClass("btn-success");
                $('#lstatus').removeClass("bg-info");
                $('#lstatus').removeClass("bg-danger");
                if (lbool == 0)
                {
                    $('#lstatus').html("<i class='fas fa-lock'> Doors are Locked <i class='fas fa-lock'>");
                    $('#lstatus').addClass("bg-info");
                    $('#locked').addClass("btn-success");
                    $('#notlocked').addClass("btn-secondary");
                }
                else{
                    $('#lstatus').html("<i class='fas fa-lock-open'> Doors Unlocked! <i class='fas fa-lock-open'>");
                    $('#lstatus').addClass("bg-danger");
                    $('#locked').addClass("btn-secondary");
                    $('#notlocked').addClass("btn-success");
                }
            }
            function grayAlarm(albool){//clears color classes, then assigns based off of alarm state
                $('#unArmed').removeClass("btn-danger");
                $('#readyArmed').removeClass("btn-success");
                $('#readyArmed').removeClass("btn-secondary");
                $('#unArmed').removeClass("btn-success");
                $('#alarmstatus').removeClass("bg-danger");
                $('#alarmstatus').removeClass("bg-info");
                if (albool == 0)
                {
                    $('#alarmstatus').html("<i class='fas fa-bell-slash'></i>'Alarm Offline'<i class='fas fa-bell-slash'>");
                    $('#alarmstatus').addClass("bg-danger");
                    $('#unArmed').addClass("btn-success");
                    $('#readyArmed').addClass("btn-secondary");
                }
                else{
                    $('#alarmstatus').html("<i class='fas fa-bell'></i>'Alarm Armed'<i class='fas fa-bell'>");
                    $('#alarmstatus').addClass("bg-info");
                    $('#unArmed').addClass("btn-secondary");
                    $('#readyArmed').addClass("btn-success");
                }

            }
            function showwater(gall){//function to change tank level bar as water changes
                var perc = (gall/40.0)*100;
                var heistr = "height:"+perc +"%";
                $('#wlev').text(gall + ' gallons');
                $('#watbar').attr('style',heistr);


            }
            function showheat(temp){//function to change thermlevel
                var heistr = "height:"+ temp +"%";
                $('#heatbar').attr('style',heistr);
                $('#howhot').text(temp + '°F');
                $('#heatbar').removeClass("bg-danger");
                $('#heatbar').removeClass("bg-info");
                $('#heatbar').removeClass("bg-success");
                if (temp > 80 ){
                    $('#heatbar').addClass("bg-danger");
                }
                else{
                    if (temp> 65){
                        $('#heatbar').addClass("bg-success");
                    }
                    else {
                        $('#heatbar').addClass("bg-info");
                    }
                }
            }
            setInterval(rdata,10000);//refresh rate for the data

            $('#locked').click(function (){//for unlocking doors, checks to see if already unlocked, otherwise sends command to do so
                if($(this).hasClass("btn-success"))
                {
                    $.getJSON('ligoff.json', function(ligoff) {//turns on lock and displays locking message
                        $("#messban").text("Doors Unlocking");
                        $("#messban").addClass('alert-primary');
                        $("#messban").show().delay(3000).fadeOut();
                        setTimeout(function(){$("#messban").removeClass("alert-primary");}, 3000);
                    });
                }
                else
                {
                    $("#messban").text("Doors Already Unlocked!");
                    $("#messban").addClass('alert-warning');
                    $("#messban").show().delay(3000).fadeOut();
                    setTimeout(function(){$("#messban").removeClass("alert-warning");}, 3000);
                }
            })
            $('#notlocked').click(function (){//checks to see if already locked, if not locks
                if($(this).hasClass("btn-success"))
                {
                    $.getJSON('ligon.json', function(ligon) {//turns on lock and displays locking message
                        $("#messban").text("Doors Locking");
                        $("#messban").addClass('alert-primary');
                        $("#messban").show().delay(3000).fadeOut();
                        setTimeout(function(){$("#messban").removeClass("alert-primary");}, 1500);
                    });
                }
                else
                {
                    $("#messban").text("Doors Already Locked!");
                    $("#messban").addClass('alert-warning');
                    $("#messban").show().delay(3000).fadeOut();
                    setTimeout(function(){$("#messban").removeClass("alert-warning");},1500);
                }
            })
            $('#readyArmed').click(function (){//checks to see if already armed, if not arms
                if($(this).hasClass("btn-success"))
                {
                    $.getJSON('togglealarm.json', function() {//disarms alarm
                        $("#messban").text("Disarming Alarm");
                        $("#messban").addClass('alert-primary');
                        $("#messban").show().delay(3000).fadeOut();
                        setTimeout(function(){$("#messban").removeClass("alert-primary");}, 1500);
                    });
                }
                else
                {
                    $("#messban").html("Alarm Already Offline!");
                    $("#messban").addClass('alert-warning');
                    $("#messban").show().delay(1500).fadeOut();
                    setTimeout(function(){$("#messban").removeClass("alert-warning");}, 1500);
                }
                rdata();
            })
            $('#unArmed').click(function (){//checks to see if unarmed, then turns on alarm
                if($(this).hasClass("btn-success"))
                {
                    $.getJSON('togglealarm.json', function() {//turns on lock and displays locking message
                        $("#messban").text("Alarm Coming Online");
                        $("#messban").addClass('alert-primary');
                        $("#messban").show().delay(1500).fadeOut();
                        setTimeout(function(){$("#messban").removeClass("alert-primary");}, 1500);
                    });
                }
                else
                {
                    $("#messban").text("Alarm Already Online!");
                    $("#messban").addClass('alert-warning');
                    $("#messban").show().delay(1500).fadeOut();
                    setTimeout(function(){$("#messban").removeClass("alert-warning");}, 1500);
                }
                rdata();
            })
            //ignore for now, spaget for making the radio buttons
            $("#opt1").click(function (){
                hehumopt=1;
                $("#opt1").addClass("btn-info");
                $("#opt1").removeClass("btn-primary");
                $("#opt2").removeClass("btn-info");
                $("#opt3").removeClass("btn-info")
                $("#opt2").addClass("btn-primary");
                $("#opt3").addClass("btn-primary");
                rdata();
            });
            $("#opt2").click(function (){
                hehumopt=2;
                $("#opt2").addClass("btn-info");
                $("#opt2").removeClass("btn-primary");
                $("#opt1").removeClass("btn-info");
                $("#opt3").removeClass("btn-info");
                $("#opt1").addClass("btn-primary");
                $("#opt3").addClass("btn-primary");
                rdata();
            });
            $("#opt3").click(function (){
                hehumopt=3;
                $("#opt3").addClass("btn-info");
                $("#opt3").removeClass("btn-primary");
                $("#opt2").removeClass("btn-info");
                $("#opt1").removeClass("btn-info");
                $("#opt2").addClass("btn-primary");
                $("#opt1").addClass("btn-primary");
                rdata();
            });
            $("#opt21").click(function (){
                watopt=1;
                $("#opt21").addClass("btn-info");
                $("#opt21").removeClass("btn-primary");
                $("#opt22").removeClass("btn-info");
                $("#opt23").removeClass("btn-info")
                $("#opt22").addClass("btn-primary");
                $("#opt23").addClass("btn-primary");
                rdata();
            });
            $("#opt22").click(function (){
                watopt=2;
                $("#opt22").addClass("btn-info");
                $("#opt22").removeClass("btn-primary");
                $("#opt21").removeClass("btn-info");
                $("#opt23").removeClass("btn-info");
                $("#opt21").addClass("btn-primary");
                $("#opt23").addClass("btn-primary");
                rdata();
            });
            $("#opt23").click(function (){
                watopt=3;
                $("#opt23").addClass("btn-info");
                $("#opt23").removeClass("btn-primary");
                $("#opt22").removeClass("btn-info");
                $("#opt21").removeClass("btn-info");
                $("#opt22").addClass("btn-primary");
                $("#opt21").addClass("btn-primary");
                rdata();
            });
        });