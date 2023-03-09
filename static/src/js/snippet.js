console.log('snippet')
odoo.define('travel_management.dynamic', function (require) {
   var PublicWidget = require('web.public.widget');
   console.log(PublicWidget,'public')
   var rpc = require('web.rpc');
   var core = require('web.core');
   var Qweb = core.qweb;
   var Dynamic = PublicWidget.Widget.extend({
       selector: '.dynamic_snippet_blog',
       start: function () {
           var self = this;
           console.log(self,'23456')
           rpc.query({
               route: '/travel/booking',
               params: {},
           }).then(function (result) {
               result[0].set_active=true;
               console.log(result,'jhfs12345678')
               $('.qweb_booking').append(Qweb.render('travel_management.booking_template',{result}));
           });
       },
   });

   PublicWidget.registry.dynamic_snippet_blog = Dynamic;
   return Dynamic;
});