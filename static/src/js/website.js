console.log('lll')
odoo.define('travel_management.domain', function (require) {
    "use strict";

     var publicWidget = require('web.public.widget');
     var rpc = require('web.rpc');
     console.log('hhh')


    publicWidget.registry.portalDetails = publicWidget.Widget.extend({

        selector: '.col-sm',
        events: {
            'change select[name="source_location_id"]': '_onSourceChange',
        },
    start: function () {
    console.log("kkk")
        this._super.apply(this, arguments);
        },

    _onSourceChange:function () {
    console.log('jjjjjjj')
        var self = this;
//        var destinationField = $('#destination_location_selection').find(":selected").val();
        var sourceField = $('#source_location_selection').find(":selected").val();
//        var destinationField = document.getElementById("destination_location_selection");
//        var option = document.createElement("option");
        console.log(sourceField,'ssssssss')
        rpc.query({

            model: 'location.location',
            method: 'search_read',
            args:[[['id', '!=', sourceField]], ['address', 'id']],

      }).then(function (result) {
            var destinationField = document.getElementById("destination_location_selection");
            destinationField.innerHTML = null
            for (let i=0;i<result.length;i++){
//                 option.result = "i"
                 console.log("ooooo",result)
                var option = document.createElement("option");
                   option.text = result[i].address;
                 destinationField.add(option);

                }
//                var option = document.createElement("option");
//                option.text("rec");
//                destinationField.add(option);
      });
//            console.log('gfffff',destinationField)
//        var destinationField = $('#destination_location_selection').find(":selected").val();

//        destinationField != sourceField

    },


//    $(document).ready(function () {
//        console.log('u');
//           $(document).on('click', '.btn_submit', function(){
//                console.log('enter inside')
//        })
//        function onchangeDropdown(){
//            var x = document.getElementById("source_location_selection").t-att-value;
//            console.log('pikjhg',x)
//            };
//        $("source_location_selection").on('change',function(){
//            console.log('dddddd');
//            });
//        var sourceField = $('#source_location_selection').find(":selected").val();
//            console.log('gggggggg',sourceField)
//        var destinationField = $('#destination_location_selection').find(":selected").val();
//
//            console.log('jjj',destinationField)

//        sourceField.on('change', function () {
//            console.log('cccccccccccccccccccccc')
//            var value = sourceField.val();
//            destinationField.val() != value;
//        });

//});



//$('select[name="source_location_id"]').on('change', function() {
//console.log('l')
//  var selected_value = $(this).val();
//  rpc.query({
//    model: 'booking.booking',
//    method: 'search',
//    args: [selected_value],
//  }).then(function(result) {
//    $('input[name="destination_location_id"]').val(result);
//  });
});
});
