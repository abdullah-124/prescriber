from medication.models import Medication
# from precription.models import Prescription

def handle_medicine(med_data, prescription_id):
    """
    med_data = {
        "id": 1,
        "drugs": "Tablet Napa",
        "frequency": "1+0+1",
        "timing": "After Meal",
        "instruction": "7 Days",
        "status": "update"  # or "create", "delete"
    }
    """
    status = med_data.get("status")
    if status == "add":
        Medication.objects.get_or_create(
            prescription_id=prescription_id,
            drugs=med_data.get("drugs"),
            frequency=med_data.get("frequency"),
            timing=med_data.get("timing"),
            instruction=med_data.get("instruction")
        )
        return {"message": "Medication created"}

    elif status == "update":
        try:
            med = Medication.objects.get(id=med_data.get("id"))
            med.drugs = med_data.get("drugs")
            med.frequency = med_data.get("frequency")
            med.timing = med_data.get("timing")
            med.instruction = med_data.get("instruction")
            med.save()
            return {"message": "Medication updated"}
        except Medication.DoesNotExist:
            return {"error": "Medication not found"}

    elif status == "delete":
        try:
            med = Medication.objects.get(id=med_data.get("id"))
            med.delete()
            return {"message": "Medication deleted"}
        except Medication.DoesNotExist:
            return {"error": "Medication not found"}

    else:
        return {"error": "Invalid status"}