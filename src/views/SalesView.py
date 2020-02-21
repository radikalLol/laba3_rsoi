
from flask import request, g, Blueprint, json, Response,render_template, redirect, url_for, flash
from ..shared.Authentication import Auth
from ..models.SalesModel import SalesModel, SaleSchema

sales_api = Blueprint('sale_api', __name__)
sales_schema = SaleSchema()


@sales_api.route('/', methods=['POST'])
@Auth.auth_required
def create():


    req_data = request.get_json() or {'sale': request.form.get('sale')}
    req_data['owner_id'] = g.user.get('id')
    data, error = sales_schema.load(req_data)
    if error:
        return custom_response(error, 400)
    sale = SalesModel(data)
    sale.save()
    data = sales_schema.dump(sale).data
    return custom_response(data, 201)

@sales_api.route('/', methods=['GET'])
def get_all():

    sales = SalesModel.get_all_sales()
    data = sales_schema.dump(sales, many=True).data
    return custom_response(data, 200)


@sales_api.route('/<int:sale_id>' or '/<id>', methods=['GET'])
def get_one(sale_id):

    post = SalesModel.get_one_sale(sale_id) #or request.form.get('sale_id')
    if not post:
        return custom_response({'error': 'sale not found'}, 404)
    data = sales_schema.dump(post).data
    return custom_response(data, 200)

@sales_api.route('/delete', methods=['POST'])
@Auth.auth_required
def dell():
    id = request.form.get('id')
    sale = SalesModel.get_one_sale(id)
    if not sale:
        return custom_response({'error': 'sale not found'}, 404)
    data = sales_schema.dump(sale).data
    if data.get('owner_id') != g.user.get('id'):
        return custom_response({'error': 'permission denied'}, 400)
    sale.delete()
    return custom_response({'message': 'deleted'}, 204)  # , redirect(url_for("sales"))


@sales_api.route('/<int:sale_id>', methods=['DELETE'])
@Auth.auth_required
def delete(sale_id):
    """
  Delete
  """
    sale = SalesModel.get_one_sale(sale_id) or SalesModel.get_one_sale(id)
    if not sale:
        return custom_response({'error': 'sale not found'}, 404)
    data = sales_schema.dump(sale).data
    if data.get('owner_id') != g.user.get('id'):
        return custom_response({'error': 'permission denied'}, 400)

    sale.delete()
    return custom_response({'message': 'deleted'}, 204) #, redirect(url_for("sales"))

def custom_response(res, status_code):

    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )
