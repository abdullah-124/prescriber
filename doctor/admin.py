from django.contrib import admin
from doctor.models import Doctor, DoctorApplication
from django.contrib import messages
from doctor.utility import send_approval_mail
# Register your models here.

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    # list_display = [field.name for field in Doctor._meta.fields]
    list_display = ['user',]
    exclude = ['description']
    # list_editable = ['profile_image']
    list_filter = ['specialty',]
    search_fields = ['hospital_name','qualification','contact']

@admin.register(DoctorApplication)
class Doctor_application_admin(admin.ModelAdmin):
    list_display = ['id','first_name', 'last_name','specialty','registration_no', 'status']
    list_editable = ['status']

    def save_model(self, request, obj, form, change):
        if change:
            previous = DoctorApplication.objects.get(pk=obj.pk)
            if previous.status != obj.status:
                # status has changed
                if obj.status == 'approved':
                    # create doctor
                    # update the user 
                    user = obj.user
                    user.role = 'doctor'
                    user.first_name = obj.first_name
                    user.last_name = obj.last_name
                    user.save()
                    doctor = Doctor.objects.create(
                        user = user,
                        registration_no = obj.registration_no,
                        specialty = obj.specialty,
                        qualification = obj.qualification,
                        chamber_address = obj.chamber_address,
                        contact = obj.contact,
                        hospital_name = obj.hospital_name,
                    )
                    # send application to the doctor user
                    txt = 'Your application has been approved. Welcome to Prescriber!'
                    res = send_approval_mail(obj.first_name,txt, obj.user.email)
                    if res:
                        self.message_user(request, f"Approval email sent to {obj.user.email}.", messages.SUCCESS)
                    else:
                        self.message_user(request, 'Sending email has failed', messages.ERROR)

                elif obj.status == 'rejected':
                    # inform the user 
                    txt = 'Your application has rejected.'
                    res = send_approval_mail(obj.first_name,txt, obj.user.email)
                    if res:
                        self.message_user(request, f"Rejection email sent to {obj.user.email}.", messages.WARNING)
                    else:
                        self.message_user(request, 'Sending email has failed', messages.ERROR)
                    obj.delete()
                    return

        super().save_model(request, obj, form, change)