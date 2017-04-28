from photologue.models import Photo
from simple_search import search_form_factory

SearchForm = search_form_factory(Photo.objects.all(),['title','caption','slug','id'])
#Photo(id, image, date_taken, view_count, crop_from, effect, title, slug, caption, date_added, is_public)