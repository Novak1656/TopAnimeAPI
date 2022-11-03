from django.core.management import BaseCommand
from django.utils.timezone import now

from ...parser_scripts import GenresScraper
from ...models import Genre


class Command(BaseCommand):
    help = 'Create genres in database'

    def handle(self, *args, **options):
        try:
            start_create_time = now()
            g_scraper = GenresScraper()
            genres_list = g_scraper.genres_data
            new_genres = 0
            for genre_title in genres_list:
                genre, created = Genre.objects.get_or_create(title=genre_title)
                if created:
                    new_genres += 1
            end_create_time = now() - start_create_time
            self.stdout.write(self.style.SUCCESS(f'{new_genres} Genres has been created success in {end_create_time}'))
        except Exception as error:
            self.stdout.write(self.style.ERROR(f'Genres were not created: {error}'))
