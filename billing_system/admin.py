from django.contrib import admin

from billing_system.models.debt import Debt
from billing_system.models.invoice import Invoice

admin.site.register(Debt)
admin.site.register(Invoice)
