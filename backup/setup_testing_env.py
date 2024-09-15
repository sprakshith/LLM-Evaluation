import os
import json
import shutil
import subprocess
import pandas as pd
from database.utils import *
from datetime import datetime


class Sandbox:
    def __init__(self):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.sandbox_path = os.path.join(self.dir_path, 'EvaluationSanbox')

    def __create_sandbox(self):
        if os.path.exists(self.sandbox_path):
            shutil.rmtree(self.sandbox_path)

        if not os.path.exists(self.sandbox_path):
            os.makedirs(self.sandbox_path)

    def __create_virtual_env(self):
        venv_path = os.path.join(self.sandbox_path, 'evaluation-venv')
        subprocess.run(['python', '-m', 'venv', venv_path])
        open(os.path.join(self.sandbox_path, 'testing.txt'), 'w')

    def __create_all_table(self):
        delete_database()

        blogs = pd.read_csv(os.path.join(
            self.dir_path, 'Datasets/BlogsTextReduced.csv'))

        session = get_db_session()

        for row in blogs.itertuples():
            blog = Blog(id=row.id, gender=row.gender, age=row.age, topic=row.topic,
                        text=row.text, created_date=datetime.strptime(row.created_date, '%Y-%m-%d'))

            session.add(blog)

        cart = json.load(open('Datasets/E-commerce/SsCluster_cart.json', 'r'))

        for c in cart:
            id = c['_id']['$oid']
            user_id = c['user_id']
            product_id = c['product_id']
            quantity = c['quantity']

            new_cart = Cart(id=id, user_id=user_id,
                            product_id=product_id, quantity=quantity)

            session.add(new_cart)

        order_details = json.load(
            open('Datasets/E-commerce/SsCluster_order_details.json', 'r'))

        for od in order_details:
            id = od['_id']['$oid']
            user_id = od['user_id']
            total = od['total']
            payment_details_id = od['payment_details_id']

            new_order_details = OrderDetails(
                id=id, user_id=user_id, total=total, payment_details_id=payment_details_id)

            session.add(new_order_details)

        order_items = json.load(
            open('Datasets/E-commerce/SsCluster_order_items.json', 'r'))

        for oi in order_items:
            id = oi['_id']['$oid']
            order_details_id = oi['order_details_id']
            product_id = oi['product_id']
            quantity = oi['quantity']

            new_order_items = OrderItems(
                id=id, order_details_id=order_details_id, product_id=product_id, quantity=quantity)

            session.add(new_order_items)

        payment_details = json.load(
            open('Datasets/E-commerce/SsCluster_payment_details.json', 'r'))

        for prd in payment_details:
            id = prd['_id']['$oid']
            amount = prd['amount']
            status = prd['status']

            new_payment_details = PaymentDetails(
                id=id, amount=amount, status=status)

            session.add(new_payment_details)

        products = json.load(
            open('Datasets/E-commerce/SsCluster_products.json', 'r'))

        for product in products:
            id = product['_id']['$oid']
            name = product['name']
            description = product['description']
            category = product['category']
            price = product['price']
            rating = product['rating']
            inventory = product['inventory']
            sold_qtn = product['sold_qtn']

            new_product = Product(id=id, name=name, description=description, category=category,
                                  price=price, rating=rating, inventory=inventory, sold_qtn=sold_qtn)

            session.add(new_product)

        user_address = json.load(
            open('Datasets/E-commerce/SsCluster_user_address.json', 'r'))

        for ua in user_address:
            id = ua['_id']['$oid']
            user_id = ua['user_id']
            address = ua['address']
            city_id = ua['city_id']
            postal = ua['postal']
            mobile = ua['mobile']

            new_user_address = UserAddress(
                id=id, user_id=user_id, address=address, city_id=city_id, postal=postal, mobile=mobile)

            session.add(new_user_address)

        user = json.load(open('Datasets/E-commerce/SsCluster_user.json', 'r'))

        for u in user:
            id = u['_id']['$oid']
            username = u['username']
            password = u['password']
            first_name = u['first_name']
            last_name = u['last_name']

            new_user = User(id=id, username=username, password=password,
                            first_name=first_name, last_name=last_name)

            session.add(new_user)

        session.commit()
        session.close()

    def initiate_sanbox(self):
        # self.__create_sandbox()
        # self.__create_virtual_env()
        self.__create_all_table()

    def run_simple_test(self):
        subprocess.run(['python', 'simple_test.py'], cwd=self.sandbox_path)


def run():
    sandbox = Sandbox()
    sandbox.initiate_sanbox()
    # sandbox.run_simple_test()


if __name__ == '__main__':
    run()
