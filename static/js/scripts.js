 // get 10 requests
 $(document).ready(function() {
     load_requests = function () {
         $.ajax({
             type: 'GET',
             url: '/request_list/',
             error: function (xhr, textStatus) {
                 alert([xhr.status, textStatus]);
             },
             success: function (msg) {
                 var result = "";
                 var i = 0;
                 $.each(msg, function (key) {
                     $.each(msg[key]['fields'], function (k, val) {
                         if (k === 'request' || k === 'pub_date' || k === 'priority') {

                         } else {
                             if (i==0) {
                                 document.title=val + '-' + msg[key]['pk'] + " Main";
                                 result += val + '-' + msg[key]['pk'] + ' ' + '<a href=\'/request_detail/' + msg[key]['pk'] + '/\'>click here to see details</a> <br>';
                             } else {

                                 result += val + '-' + msg[key]['pk'] + ' ' + '<a href=\'/request_detail/' + msg[key]['pk'] + '/\'>click here to see details</a> <br>';
                             }
                             i++;
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