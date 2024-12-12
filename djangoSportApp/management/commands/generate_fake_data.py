import random
import requests
import logging
from io import BytesIO
from faker import Faker
from PIL import Image
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from djangoSportApp.models import SportStructure, SportStructureImage, Category, Tag

fake = Faker()
logger = logging.getLogger(__name__)


def create_or_get_objects(model, names):
    """Create or get objects for a given model and list of names."""
    return [model.objects.get_or_create(name=name)[0] for name in names]


class Command(BaseCommand):
    help = "Generate fake sport structures and images"

    def add_arguments(self, parser):
        parser.add_argument(
            "--structures",
            type=int,
            default=3,
            help="Number of sport structures to generate (default: 9)",
        )
        parser.add_argument(
            "--images-per-structure",
            type=int,
            default=3,
            help="Maximum number of images per structure (default: 3)",
        )

    def handle(self, *args, **kwargs):
        num_structures = kwargs["structures"]
        max_images_per_structure = kwargs["images_per_structure"]

        categories = create_or_get_objects(Category, ["Stadium", "Gym", "Pool", "Arena", "Field"])
        tags = create_or_get_objects(Tag, ["Indoors", "Outdoors", "Public", "Private", "Premium", "Free", "Membership"])

        # Generate sport structures
        for _ in range(num_structures):
            structure = SportStructure.objects.create(
                name=fake.company(),
                description=fake.text(max_nb_chars=200),
                rating=random.uniform(0, 0),
                category=random.choice(categories),
                address=fake.address(),
            )
            structure.tags.set(random.sample(tags, random.randint(1, 3)))

            # Generate images for the structure
            for _ in range(random.randint(1, max_images_per_structure)):
                image = self.generate_placeholder_image()
                SportStructureImage.objects.create(
                    sport_structure=structure,
                    image=image,
                    description=fake.sentence(),
                )

        self.stdout.write(self.style.SUCCESS("Fake sport structures and images generated!"))

    def generate_placeholder_image(self):
        """Generate a placeholder image using Lorem Picsum or Pillow."""
        try:
            response = requests.get("https://picsum.photos/400/300", stream=True)
            if response.status_code == 200:
                return ContentFile(response.content, name=f"placeholder_{fake.uuid4()}.jpg")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching placeholder image from Lorem Picsum: {e}")

        # Fallback to Pillow
        image = Image.new(
            "RGB",
            (400, 300),
            color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
        )
        image_io = BytesIO()
        image.save(image_io, format="JPEG")
        return ContentFile(image_io.getvalue(), name=f"generated_{fake.uuid4()}.jpg")