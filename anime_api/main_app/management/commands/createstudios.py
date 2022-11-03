from django.core.management import BaseCommand
from django.utils.timezone import now

from ...parser_scripts import StudiosScraper
from ...models import Studio


class Command(BaseCommand):
    help = 'Create studios in database'

    def handle(self, *args, **options):
        try:
            start_create_time = now()
            s_scraper = StudiosScraper()
            studios_list = s_scraper.studios_data
            new_studios = 0
            for studio_title in studios_list:
                studio, created = Studio.objects.get_or_create(title=studio_title)
                if created:
                    new_studios += 1
            end_create_time = now() - start_create_time
            self.stdout.write(
                self.style.SUCCESS(f'{new_studios} Studios has been created success in {end_create_time}')
            )
        except Exception as error:
            self.stdout.write(self.style.ERROR(f'Studios were not created: {error}'))
