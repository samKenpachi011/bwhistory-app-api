from django.utils.translation import gettext_lazy as _ # noqa

EVENT_TYPE_CHOICES = (
        ('traditional', 'Traditional'),
        ('festive', 'Festive'),
        ('ritual', 'Ritual')
    )

CHIEF_TYPE = (
        ('paramount', 'Paramount'),
        ('subchief', 'Sub Chief'),
        ('divisional', 'Divisional')
    )


DOCUMENT_TYPE = (
        ('article', 'Article'),
        ('conference_paper', 'Conference paper'),
        ('research_paper', 'Research paper'),
        ('book', 'Book'),
        ('chapter', 'Chapter'),
    )

SITE_TYPE = (
    ('cultural', 'Cultural'),
    ('natural', 'Natural'),
)
