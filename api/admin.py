from django.contrib import admin
from .models import Management,Rider,User,Customer,CustomerProfile,ManagementProfile,RiderProfile,Order

admin.site.register(User)
admin.site.register(Rider)
admin.site.register(RiderProfile)
admin.site.register(Customer)
admin.site.register(CustomerProfile)
admin.site.register(Order)
admin.site.register(ManagementProfile)
admin.site.register(Management)