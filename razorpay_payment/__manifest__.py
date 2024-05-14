# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Payment Provider: Razorpay 2",
    'version': '1.0',
    'category': 'Accounting/Payment Providers',
    'sequence': 350,
    'summary': "A payment provider covering India.",
    'description': " ",  # Non-empty string to avoid loading the README file.
    'depends': ['payment','base','website'],
    'data': [
        'data/payment_provider_data.xml',
        'views/payment_razorpay_templates.xml',
        'data/payment_method_razorpay2_data.xml',
        'views/payment_provider_views.xml',

        # Depends on views/payment_razorpay_templates.xml
    ],

    # 'post_init_hook': 'post_init_hook',
    # 'uninstall_hook': 'uninstall_hook',
    'license': 'LGPL-3',
}
