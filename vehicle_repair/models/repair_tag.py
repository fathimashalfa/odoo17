# -*- coding: utf-8 -*-

from odoo import fields, models


class RepairTags(models.Model):
    """fields for repair tags and sql constraints to check unique"""
    _name = 'repair.tag'
    _description = 'Vehicle Tag'

    name = fields.Char('Tag Name', required=True)
    color = fields.Integer('Color')

    _sql_constraints = [('name_uniq', 'unique (name)', "Tag name already exists!")]

