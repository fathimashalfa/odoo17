import logging
from odoo import http
from odoo.http import request
_logger = logging.getlogger(__name__)


class XmlApiTest(http.Controller):
    @http.route('/demo/request',type='http',auth='public',methods=['POST'],
                csrf=False)
    def test_xml_api(self,*args,**kwargs):
        _logger.info(request.httprequest.get_data().decode('utf-8'))
