/** @odoo-module **/
import { patch } from "@web/core/utils/patch";
import { Order } from "@point_of_sale/app/store/models";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { _t } from "@web/core/l10n/translation";


patch(Order.prototype, {
    calculation(){
            console.log("function",this)
            var orderlines = this.get_orderlines()
            var discount = 0
            for(let orderline of orderlines){
                var discount_amount = (orderline.discount/100) * orderline.price
                discount += discount_amount
                console.log("disc",discount)
            }

            return discount;
    },
    async pay() {
        var sessions=this.pos.config.session_name
        if(this.pos.config.discount_active){
            if(sessions.includes(this.session_id)){
                if(this.pos.config.discount_limit == 'fixed_amount'){
                    var amount = this.pos.config.discount
                    var fixed_price=this.calculation()
                    if(fixed_price > amount){
                        this.env.services.popup.add(ErrorPopup, {
                            title: _t("Alert"),
                            body: _t("Your Session Fixed Price Discount limit exceed"),
                        });
                    }
                    else{
                       return super.pay(...arguments);
                    }

                }
                if(this.pos.config.discount_limit == 'percentage'){
                    var total=this.get_total_with_tax()
                    var amount = this.pos.config.discount
                    var percentage_amount=this.calculation()
                    var total_with_discount=total+percentage_amount
                    var percentage=(percentage_amount/total_with_discount) * 100
                    if(percentage > amount){
                        this.env.services.popup.add(ErrorPopup, {
                            title: _t("Alert"),
                            body: _t("Your Session Percentage Discount limit exceed"),
                        });
                    }
                    else{
                       return super.pay(...arguments);
                    }
                }
            }
        }

    }

});
