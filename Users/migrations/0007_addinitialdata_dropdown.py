from django.db import migrations


def add_initial_data_drop_down(apps, schema_editor):
    DropDownCategory = apps.get_model('Users', 'DropDownCategory')
    
    # Add predefined data
    DropDownCategory.objects.create(category_name="Company_industry")
    DropDownCategory.objects.create(category_name="age_range")
    DropDownCategory.objects.create(category_name="Purpose_for_using")

def add_initial_data_drop_down_category_items(apps, schema_editor):
    DropDownCategoryItem = apps.get_model('Users', 'DropDownCategoryItem')
    
    # Add predefined data
    DropDownCategoryItem.objects.create(item_name="Packing", category_id=1)
    DropDownCategoryItem.objects.create(item_name="Chamical", category_id=1)
    DropDownCategoryItem.objects.create(item_name="Food", category_id=1)
    DropDownCategoryItem.objects.create(item_name="0-30", category_id=2)
    DropDownCategoryItem.objects.create(item_name="31-40", category_id=2)
    DropDownCategoryItem.objects.create(item_name="41-50", category_id=2)
    DropDownCategoryItem.objects.create(item_name="Automation", category_id=3)
    DropDownCategoryItem.objects.create(item_name="Business", category_id=3)
   

class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0006_dropdowncategory_dropdowncategoryitem_companydetails'),
    ]

    operations = [
        migrations.RunPython(add_initial_data_drop_down),
        migrations.RunPython(add_initial_data_drop_down_category_items)
    ]
