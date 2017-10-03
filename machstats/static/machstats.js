function blinker() {
  $('.blinking').fadeOut(500);
  $('.blinking').fadeIn(500);
}
setInterval(blinker, 1000);

document.getElementById('squarez').style.display = "none";
document.getElementById('squarez2').style.display = "none";

function mains() {
    var host = window.location.host;
    var ws = new WebSocket('ws://'+host+'/mach_sock');
    ws.onmessage = function (event) {
        var event_data = JSON.parse(event.data);
        if (event_data == "null") {
            document.getElementById('squarez').style.display = "none";
            document.getElementById('squarez2').style.display = "none";
            document.getElementById('nomach').style.display = "inline";
        } else {
            document.getElementById('nomach').style.display = "none";
            var newCount = event_data.length;
            var strangz = '';
            for (var i = 0; i < newCount; i++) {
                var state = '';
                var titlestate = '';
                if (event_data[i].StateName == "Up") {
                    titlestate = 'panel-success';
                    state = 'alert alert-success';
                } else if (event_data[i].StateName == "Down") {
                    titlestate = 'panel-info';
                    state = 'alert alert-info';
                } else if (event_data[i].StateName == "Between") {
                    titlestate = 'panel-default';
                    state = 'alert alert-success';
                }
                strangz = strangz + '<a href="http://' + event_data[i].IPAddress + '"><div class="col-sm-2 col-centered boxes panel ' + titlestate + '" style="padding: 15px; border-color: black;"><div class="panel-heading text-center"><strong>' + event_data[i].MachineName + '</strong><div class="panel-body text-center black ' + state + '"><strong>' + event_data[i].StateName + '</strong></div></div></div></a>';

            }
            if (document.getElementById('squarez2').style.display == "none") {
                var div = document.createElement('div');
                div.innerHTML = strangz;
                document.getElementById('squarez2').appendChild(div);
                document.getElementById('squarez').style.display = "none";
                document.getElementById('squarez2').style.display = "inline";
                document.getElementById('squarez').innerHTML = '';
                console.log("going to display 2");
            } else if (document.getElementById('squarez2').style.display == "inline") {
                var div = document.createElement('div');
                div.innerHTML = strangz;
                document.getElementById('squarez').appendChild(div);
                document.getElementById('squarez2').style.display = "none";
                document.getElementById('squarez').style.display = "inline";
                document.getElementById('squarez2').innerHTML = '';
                console.log("going to display 1");
            }

            }
        }
    ws.onclose = function(e) {
        console.log('closed reconnecting ...', e.reason);
        setTimeout(function() {
            mains();
        }, 1000);
        }
    ws.onerror = function(err) {
        console.error('Socket encountered error: ', err.message, 'Closing socket');
        ws.close();
      }
    }


window.onload = mains;
