from typing import List
from questionary import Choice

class BackendFactory:
    """
    Liefert Choice-Objekte für Questionary zurück.
    Title = Was der User sieht
    Value = Was im Code ankommt (der echte Paketname)
    """

    _AVAILABLE_LIBRARIES = {
        "Java": [
            Choice(title="Lombok (Boilerplate reduction)", value="lombok"),
            Choice(title="Spring Security (Auth)", value="spring-boot-starter-security"),
            Choice(title="Spring Data JPA (Database)", value="spring-boot-starter-data-jpa"),
            Choice(title="Spring Boot Actuator (Monitoring)", value="spring-boot-starter-actuator"),
            Choice(title="MapStruct (Mapper)", value="mapstruct")
        ],
        "Express": [
            Choice(title="Helmet (Security Headers)", value="helmet"),
            Choice(title="Morgan (Logging)", value="morgan"),
            Choice(title="Cors (Cross-Origin Resource Sharing)", value="cors"),
            Choice(title="Dotenv (Environment Variables)", value="dotenv"),
            Choice(title="Joi (Validation)", value="joi"),
            Choice(title="Zod (Validation)", value="zod"),
            Choice(title="Mongoose (MongoDB ODM)", value="mongoose")
        ],
        "Django": [
            Choice(title="Django REST Framework (API)", value="djangorestframework"),
            Choice(title="Django CORS Headers", value="django-cors-headers"),
            Choice(title="Django Debug Toolbar", value="django-debug-toolbar"),
            Choice(title="Celery (Async Tasks)", value="celery")
        ]
    }

    @staticmethod
    def get_supported_libraries(stack: str) -> List[Choice]:
        return BackendFactory._AVAILABLE_LIBRARIES.get(stack, [])