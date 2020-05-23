function update() {
    document.querySelector('#total').innerHTML=total;
}

function startTime() {
    var today = new Date();
    var h = today.getHours();
    var m = today.getMinutes();
    var s = today.getSeconds();
    m = checkTime(m);
    s = checkTime(s);
    var suf = "AM"
    if (h >= 12) {
    h = h - 12;
    suf = "PM";
  }
    document.getElementById('txt').innerHTML =
    h + ":" + m + ":" + s + " "+ suf;
    var t = setTimeout(startTime, 500);
  }
  function checkTime(i) {
    if (i < 10) {i = "0" + i};  // add zero in front of numbers < 10
    return i;
  }

$(document).ready(function() {
  $('#formin').on('submit', function(event) {

    $.ajax({
      data : {
        type : $("#inBtn").val()
      },
      type : 'POST',
      url : '/process'
    })
    .done(function(data) {

      $('#total').text(data.total);

    })

    event.preventDefault();

  }
});