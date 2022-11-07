from django.core.management import BaseCommand
from django.db.models import Q
from django.utils.timezone import now

from ...parser_scripts import AnimeScraper
from ...models import Anime, Genre, Studio, Season


class Command(BaseCommand):
    help = 'Create anime in database'

    def add_arguments(self, parser):
        parser.add_argument('anime_count', type=int, help='Кол-во создаваемых аниме')

    def handle(self, *args, **kwargs):
        try:
            start_create_time = now()
            pages_count = kwargs.get('anime_count')
            a_scraper = AnimeScraper(pages_count=pages_count)
            anime_data = a_scraper.anime_data
            new_anime = 0
            genres = Genre.objects.all()
            studios = Studio.objects.all()
            for anime_title, anime_info in anime_data.items():
                anime, created = Anime.objects.get_or_create(
                    title=anime_title,
                    description=anime_info.get('description'),
                    score=anime_info.get('score'),
                    type=anime_info.get('type'),
                    image=anime_info.get('image')
                )
                if created:
                    studio = anime_info.get('studio')
                    if studio is not None:
                        anime.studio = studios.filter(Q(title=studio) | Q(title__icontains=studio)).first()
                    season = anime_info.get('season')
                    if season is not None:
                        anime.season, created = Season.objects.get_or_create(title=season)
                    anime_genres = genres.filter(title__in=anime_info.get('genres'))
                    anime.genres.add(*anime_genres)
                    anime.save()
                    new_anime += 1
            end_create_time = now() - start_create_time
            self.stdout.write(
                self.style.SUCCESS(f'{new_anime} Anime has been created success in {end_create_time}')
            )
        except Exception as error:
            self.stdout.write(self.style.ERROR(f'Anime were not created: {error}'))
