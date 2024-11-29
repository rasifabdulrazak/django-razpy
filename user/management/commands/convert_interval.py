from django.core.management.base import BaseCommand
from django.apps import apps
from datetime import timedelta
import re

def parse_interval_to_timedelta(interval_str):
    """Convert a string like '23:45:42', '39 days, 2:38:40', or '0' to a timedelta object."""
    if not interval_str or interval_str.strip() == "0":
        return timedelta(0)
    
    days, hours, minutes, seconds, microseconds = 0, 0, 0, 0, 0
    
    match = re.match(
        r'(?:(\d+)\s*days?,\s*)?(\d{1,2}):(\d{1,2})(?::(\d{1,2}))?(?:\.(\d+))?', 
        interval_str
    )
    
    if match:
        days = int(match.group(1) or 0)
        hours = int(match.group(2) or 0)
        minutes = int(match.group(3) or 0)
        seconds = int(match.group(4) or 0)
        microseconds_str = match.group(5) or "0"
        microseconds = int(microseconds_str.ljust(6, '0')[:6])
    else:
        raise ValueError(f"Invalid time interval format: '{interval_str}'")

    return timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds, microseconds=microseconds)

class Command(BaseCommand):
    help = 'Convert CharField intervals to DurationField for multiple models'

    def handle(self, *args, **kwargs):
        # Define models and fields to convert
        fields_to_convert = {
            'Order': {'app':'user','old_field': 'interval', 'new_field': 'new_interv'},
        }

        # Iterate over each model and field
        for model_name, field_info in fields_to_convert.items():
            model = apps.get_model(field_info['app'], model_name)  # Replace 'yourapp' with your actual app name
            old_field = field_info['old_field']
            new_field = field_info['new_field']

            self.stdout.write(f"Processing {model_name} for field '{old_field}' to '{new_field}'")

            # Query all objects of the model
            all_objects = model.objects.all()
            self.stdout.write(f"Total objects found: {all_objects.count()}")

            # Iterate over each object
            for obj in all_objects:
                # Check if the new field is already set; if so, skip
                if getattr(obj, new_field) is not None:
                    self.stdout.write(f"Skipping: ID {obj.id} - Already converted")
                    continue

                # Convert and update the old field to the new field
                interval_str = getattr(obj, old_field)
                self.stdout.write(f"Converting: ID {obj.id} - Original interval: '{interval_str}'")
                if interval_str:
                    try:
                        converted_value = parse_interval_to_timedelta(interval_str)
                        setattr(obj, new_field, converted_value)
                        obj.save()
                        self.stdout.write(f"Successfully converted: ID {obj.id} - New interval: '{converted_value}'")
                    except Exception as e:
                        self.stdout.write(f"Failed to convert '{interval_str}' for ID {obj.id}: {e}")