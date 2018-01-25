import wtforms

class ComboBoxWidget(object):

    def __call__(self, field, **kwargs):
        kwargs.setdefault('type', 'text')
        kwargs.setdefault('value', field.data or '')
        input_params = dict(kwargs, name=field.name, list=field.name)
        input = '<input {}>'.format(
            wtforms.widgets.html_params(**input_params))
        datalist = '<datalist id="{}">'.format(field.name)
        for option in field.options:
            datalist += '\n<option value="{}">'.format(option)
        datalist += '\n</datalist>'

        return wtforms.widgets.HTMLString('\n'.join([input, datalist]))

class ComboBoxField(wtforms.Field):

    def __init__(self, label='', validators=None, options=[], **kwargs):
        super().__init__(label, validators, **kwargs)
        self.options = options
        self.widget = ComboBoxWidget()

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = valuelist[0]
        else:
            self.data = ''
