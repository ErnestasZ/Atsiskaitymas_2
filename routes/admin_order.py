from flask import Blueprint, render_template, request, flash, redirect, url_for
import Controllers.admin_order as ar
import Services.Forms.dashboard as forms
# from Services.forms import testas
order = Blueprint('order', __name__, url_prefix='/admin/order')


def register_order_routes(app, db):

    @order.route('/')
    def index():
        # orders = dash.get_all_orders()
        orders, total = ar.get_orders()
        return render_template('admin/order/orders.html', orders=orders, total=total)

    @order.route('/edit/<int:order_id>', methods=['POST', 'GET'])
    def order_items(order_id):
        status_form = forms.StatusForm()
        if status_form.validate_on_submit():
            # print(status_form.status.data)
            ar.set_order_status(order_id, status_form.status.data)
            flash('Order status changed successfully.', 'success')
            return redirect(url_for('order.order_items', order_id=order_id))

        items, order, statuses = ar.get_order_items(order_id)
        status_form.status.data = order.status

        return render_template('admin/order/order_items.html',
                               items=items,
                               order=order,
                               statuses=statuses,
                               status_form=status_form,
                               )

    @order.route('/<int:order_id>/review/<int:item_id>', methods=['POST', 'GET'])
    def item_review(order_id, item_id):
        review, order = ar.get_item_review(item_id)
        form = forms.ReviewForm(
            rating=review.rating,
            content=review.content
        )
        if form.validate_on_submit():
            ar.set_review(item_id, form.rating.data, form.content.data)
            flash('Review updated successfully.', 'success')
            return redirect(url_for('order.item_review', order_id=order_id, item_id=item_id))

        return render_template('admin/order/item_review.html', form=form, review=review, order=order)

    @order.route('/<int:order_id>/review/<int:item_id>/delete/<int:review_id>', methods=['POST'])
    def delete_review(order_id, item_id, review_id):
        ar.remove_review(review_id)
        flash('Review deleted successfully.', 'success')
        return redirect(url_for('order.item_review', order_id=order_id, item_id=item_id))

    app.register_blueprint(order)
