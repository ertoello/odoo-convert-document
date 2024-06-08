from odoo import models, fields, api
from pathlib import Path
from odoo.exceptions import ValidationError
import os
import base64
import convertapi
from convertapi import BaseError


class ConvertFile(models.Model):
    _name = 'convert.file'
    _description = 'Convert File'

    convert_category = fields.Selection([
        ('ms_office', 'Microsoft Office'),
        ('img', 'Image'),
    ], string='Category', default='ms_office')

    from_format_document = fields.Selection([
        ('docx', 'DOCX'),
        ('doc', 'DOC'),
        ('xlsx', 'XLSX'),
        ('pdf', 'PDF'),
    ], string='Format')

    to_format_document = fields.Selection([
        ('docx', 'DOCX'),
        ('doc', 'DOC'),
        ('xlsx', 'XLSX'),
        ('pdf', 'PDF'),
    ], string='Format')

    from_format_image = fields.Selection([
        ('jpg', 'JPG'),
        ('png', 'PNG'),
        ('svg', 'SVG'),
        ('pdf', 'PDF'),
    ], string='From Format')

    to_format_image = fields.Selection([
        ('jpg', 'JPG'),
        ('png', 'PNG'),
        ('svg', 'SVG'),
        ('pdf', 'PDF'),
    ], string='To Format')

    name = fields.Char('Name', default='/', readonly=True)

    api_id = fields.Many2one('api.settings', string='API Account', required=True)

    convert_line = fields.One2many('convert.line', 'convert_id', string='Convert Line')

    def name_get(self):
        res = []
        for rec in self:
            if rec.from_format_document:
                from_format_file = dict(self._fields['from_format_document'].selection).get(rec.from_format_document)
            elif rec.from_format_image:
                from_format_file = dict(self._fields['from_format_image'].selection).get(rec.from_format_image)

            if rec.to_format_document:
                to_format_file = dict(self._fields['to_format_document'].selection).get(rec.to_format_document)
            elif rec.to_format_image:
                to_format_file = dict(self._fields['to_format_image'].selection).get(rec.to_format_image)

            format_category = dict(self._fields['convert_category'].selection).get(rec.convert_category)

            res.append((rec.id, '%s/%sto%s' % (format_category, from_format_file, to_format_file)))
        return res

    @api.model
    def create(self, vals):
        res = super(ConvertFile, self).create(vals)
        for rec in res:
            if rec.from_format_document:
                    from_format_file = dict(self._fields['from_format_document'].selection).get(rec.from_format_document)
            elif rec.from_format_image:
                from_format_file = dict(self._fields['from_format_image'].selection).get(rec.from_format_image)
            if rec.to_format_document:
                to_format_file = dict(self._fields['to_format_document'].selection).get(rec.to_format_document)
            elif rec.to_format_image:
                to_format_file = dict(self._fields['to_format_image'].selection).get(rec.to_format_image)
            format_category = dict(self._fields['convert_category'].selection).get(rec.convert_category)
            rec.name = '{}/{}/{}'.format(from_format_file,
            to_format_file, 
            self.env['ir.sequence'].next_by_code('convert.file'))
        return res

    def action_convert_button(self):
        for rec in self:
            for res in rec.convert_line:
                if rec.api_id.state == 'active':
                    if rec.convert_category == 'ms_office':
                        doc = base64.b64decode(res.file_original)
                        with open(res.filename_original, 'wb+') as f:
                            f.write(doc)

                        try:
                            convertapi.api_secret = rec.api_id.secret_key
                            data_folder = Path(res.filename_original)
                            outfile = Path("")
                            x = convertapi.convert(rec.to_format_document, {
                                'File': data_folder
                            }, from_format=rec.from_format_document).save_files(outfile)

                            res.filename_convert = x[0]
                            b = str(res.filename_convert).replace('./', '')
                            res.filename_convert = b
                            print(b)

                            with open(b, 'rb+') as converter_file:
                                converter_data = converter_file.read()
                                oi = base64.b64encode(converter_data)
                            res.write({'file_convert': oi})

                            print("+"*10, convertapi.user(), "+"*10)

                            os.remove(res.filename_original)
                            os.remove(b)
                        except convertapi.ApiError as e:
                            raise ValidationError(f"An error occurred: {e}")
                    elif rec.convert_category == 'img':
                        doc = base64.b64decode(res.file_original)
                        with open(res.filename_original, 'wb+') as f:
                            f.write(doc)

                        try:
                            convertapi.api_secret = rec.api_id.secret_key
                            data_folder = Path(res.filename_original)
                            outfile = Path("")
                            x = convertapi.convert(rec.to_format_image, {
                                'File': data_folder
                            }, from_format=rec.from_format_image).save_files(outfile)

                            res.filename_convert = x[0]
                            b = str(res.filename_convert).replace('./', '')
                            res.filename_convert = b
                            print(b)

                            with open(b, 'rb+') as converter_file:
                                converter_data = converter_file.read()
                                oi = base64.b64encode(converter_data)
                            res.write({'file_convert': oi})

                            os.remove(res.filename_original)
                            os.remove(b)
                        except convertapi.BaseError as e:
                            raise ValidationError(f"An error occurred: {e}")
                    else:
                        raise ValidationError("Error!! Because the API not connected or File Original is Blank")
                else:
                    raise ValidationError("Error!! Because the API not connected or File Original is Blank")


class ConvertLine(models.Model):
    _name = 'convert.line'
    _description = 'Convert Line'

    convert_id = fields.Many2one('convert.file', string='Convert ID')
    file_original = fields.Binary('File Original')
    file_convert = fields.Binary('Converted File')
    filename_original = fields.Char('File Name Original')
    filename_convert = fields.Char('Filename Converted')
