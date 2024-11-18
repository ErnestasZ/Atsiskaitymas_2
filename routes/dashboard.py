from flask import Blueprint, render_template, request, flash, redirect, url_for
import Controllers.dashboard as dash
import Services.Forms.dashboard as forms
from Misc.my_logger import my_logger

# from Services.forms import testas
dashboard = Blueprint('dashboard', __name__, url_prefix='/admin/dashboard')


def register_dashboard_routes(app, db):

    @dashboard.route('/', methods=['GET'])
    def index():
        month_sales = dash.get_sales_by_month()
        best_rated = dash.get_best_rated_products()
        best_sales = dash.get_best_sales_products()
        my_logger.info('get dashboard')
        return render_template('admin/dashboard/dashboard.html',
                               month_sales=month_sales,
                               best_rated=best_rated,
                               best_sales=best_sales)

    @dashboard.route('/orders', methods=['GET'])
    def orders():
        start_date_arg = request.args.get('start_date')
        end_date_arg = request.args.get('end_date')
        orders, total = dash.get_orders_by_days_in_range(
            start_date_arg, end_date_arg)

        return render_template('admin/dashboard/orders.html',
                               orders=orders,
                               total=total,
                               start_date=start_date_arg,
                               end_date=end_date_arg)

    @dashboard.route('/items')
    def items():
        items_start_date = request.args.get('items_start_date')
        items_end_date = request.args.get('items_end_date')
        items, total_sale = dash.get_order_items_by_days_in_range(
            items_start_date, items_end_date)
        return render_template('admin/dashboard/items.html',
                               items=items,
                               total=total_sale,
                               items_start_date=items_start_date,
                               items_end_date=items_end_date)

    # register blueprint
    app.register_blueprint(dashboard)
