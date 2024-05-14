/** @odoo-module */

import {Orderline,} from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";

patch(Orderline.prototype, {
    getDisplayData() {
        return {
        	...super.getDisplayData(),
            spanish_name: this.get_product().spanish_name,

        };
    }
});