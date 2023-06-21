from wtforms import Form, StringField, FloatField, DateField, validators

name_rules = [validators.InputRequired()]
price_rules = [validators.InputRequired(), validators.NumberRange(min=0)]
date_rules = [validators.InputRequired()]

class ExpenseForm(Form):
    name = StringField('name', validators=name_rules)
    price = FloatField('price', validators=price_rules)
    date = StringField('date', validators=date_rules)
    category = StringField('category')
