# Use official Odoo 17 image
FROM odoo:17

# Copy custom modules into Odoo
COPY ./custom_addons /mnt/extra-addons

# Copy Odoo configuration
COPY ./odoo.conf /etc/odoo/odoo.conf

# Install any extra Python dependencies
RUN pip install -r /mnt/extra-addons/requirements.txt

EXPOSE 8069

CMD ["odoo", "-c", "/etc/odoo/odoo.conf"]
