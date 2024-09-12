from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Management,Rider,User,Customer,CustomerProfile,ManagementProfile,RiderProfile,Order,Email
admin.site.unregister(Group)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username","email","role","is_active"]
admin.site.register(User,UserAdmin)

class RiderProfileInline(admin.StackedInline):
    model = RiderProfile

class RiderAdmin(admin.ModelAdmin):
    model = Rider
    list_display = ["username" ,"email","is_active"]
    inlines = [RiderProfileInline]
admin.site.register(Rider,RiderAdmin)

class CustomerProfileInline(admin.StackedInline):
    model = CustomerProfile
class CustomerAdmin(admin.ModelAdmin):
    model = Customer
    list_display = ["username","email","is_active"]
    inlines = [CustomerProfileInline]

admin.site.register(Customer,CustomerAdmin)


class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ["__str__","customer","mobile",'webhook']
    search_fields = []
admin.site.register(Order,OrderAdmin)
class ManagementProfileInline(admin.StackedInline):
    model = ManagementProfile
class ManagementAdmin(admin.ModelAdmin):

    model = Management
    list_display = ["username","email","is_active"]
    search_fields = ["email"]
    inlines = [ManagementProfileInline]
    
admin.site.register(Management,ManagementAdmin)
admin.site.register(Email)