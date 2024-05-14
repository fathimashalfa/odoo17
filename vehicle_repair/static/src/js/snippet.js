/** @odoo-module */

import PublicWidget from '@web/legacy/js/public/public_widget';
import { jsonrpc } from "@web/core/network/rpc_service";
import { renderToElement } from "@web/core/utils/render";
import { renderToFragment } from "@web/core/utils/render";


   PublicWidget.registry.NewElements = PublicWidget.Widget.extend({
        selector:'.vehicle_repair_product_snippet',
        start: function(){
        var self = this;
        jsonrpc('/latest_records').then(function(data){
            if (data.length > 0){
                data[0].is_active = true
                console.log(self)
                self.$el.find('#latest_records').html(renderToFragment("vehicle_repair.repair_snipped_carousel", {data: data}))
            }
        });
        return this._super(...arguments)
        },
   })