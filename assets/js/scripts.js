 // get 10 requests
 $(document).ready(function() {
     load_requests = function () {
         $('.result').html(' ');
         $.ajax({
             type: 'GET',
             url: '/request_list/',
             error: function (xhr, textStatus) {
                 alert([xhr.status, textStatus]);
             },
             success: function (msg) {
                 var result = "";
                 $.each(msg, function (key) {
                     $.each(msg[key]['fields'], function (k, val) {
                         if (k === 'request' || k === 'pub_date' || k === 'priority') {

                         } else {
                             result += val + '-' + msg[key]['pk'] + ' ' + '<a href=\'/request_detail/' + msg[key]['pk'] + '/\'>click here to see details</a> <br>';
                         }
                     });
                     $('.result').replaceWith('<div class="col-xs-12 result">' + result + '</div>');
                 });
                 setTimeout(load_requests, 3000);
             }
         });
     };
     load_requests();
 });