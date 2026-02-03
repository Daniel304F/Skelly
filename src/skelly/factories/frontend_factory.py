from typing import List, Dict 

class FrontendFactory:

    _AVAILABLE_LIBRARIES: Dict[str, List[str]] = {
        "React": ["Redux", "React Router", "Axios", "Tanstack Query(Data Fetching)", "Tailwind CSS", "Material UI"],
        "Lit": ["Lit Router", "Lit State", "Lit Fetch"],
        "Angular": ["Bootstrap", "Angular Material",]
    }

    @staticmethod
    def get_supported_libraries(stack: str) -> List[str]:
        return FrontendFactory._AVAILABLE_LIBRARIES.get(stack, [])