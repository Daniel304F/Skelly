from typing import List, Dict

class BackendFactory:

    _AVAILABLE_LIBRARIES: Dict[str, List[str]] = {
        "Java": [
            "Lombok (Boilerplate reduction)",
            "Spring Security (Auth)",
            "Spring Data JPA (Database)",
            "Spring Boot Actuator (Monitoring)",
            "MapStruct (Mapper)"
        ],
        "Express": [
            "Helmet (Security Headers)",
            "Morgan (Logging)",
            "Cors (Cross-Origin Resource Sharing)",
            "Dotenv (Environment Variables)",
            "Joi (Validation)",
            "Zod (Validation)",
            "Mongoose (MongoDB ODM)"
        ],
        "Django": [
            "Django REST Framework (API)",
            "Django CORS Headers",
            "Django Debug Toolbar",
            "Celery (Async Tasks)"
        ]
    }

    @staticmethod
    def get_supported_libraries(stack: str) -> List[str]:
        return BackendFactory._AVAILABLE_LIBRARIES.get(stack, [])