import os
from django.core.management.base import BaseCommand
from django.conf import settings
from djangoSportApp.models import SportStructureImage


class Command(BaseCommand):
    help = "Removes unreferenced files from the 'sport_structure_images' folder."

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting removal of unused files in 'sport_structure_images'...")

        referenced_files = set()
        for img_obj in SportStructureImage.objects.all():
            if img_obj.image:
                relative_path = os.path.relpath(img_obj.image.path, settings.MEDIA_ROOT)
                referenced_files.add(relative_path)

        images_dir = os.path.join(settings.MEDIA_ROOT, 'sport_structure_images')
        if not os.path.exists(images_dir):
            self.stdout.write("No 'sport_structure_images' directory found.")
            return

        for root, dirs, files in os.walk(images_dir):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                rel_path = os.path.relpath(file_path, settings.MEDIA_ROOT)

                if rel_path not in referenced_files:
                    try:
                        os.remove(file_path)
                        self.stdout.write(f"Deleted unreferenced file: {file_path}")
                    except Exception as e:
                        self.stderr.write(f"Error deleting {file_path}: {e}")

        self.stdout.write("Cleanup complete.")
