from typing import List
from questionary import Choice

class FrontendFactory:

    _AVAILABLE_LIBRARIES = {
        "React": [
            Choice(title="Redux Toolkit", value="@reduxjs/toolkit react-redux"),
            Choice(title="React Router", value="react-router-dom"),
            Choice(title="TanStack Query", value="@tanstack/react-query"),
            Choice(title="Tailwind CSS", value="tailwindcss postcss autoprefixer"),
            Choice(title="Material UI", value="@mui/material @emotion/react @emotion/styled")
        ],
        "Lit": [
            Choice(title="Lit Router", value="@lit-labs/router"),
            # ...
        ],
        "Angular": [
            Choice(title="Angular Material", value="@angular/material"),
            # ...
        ]
    }

    @staticmethod
    def get_supported_libraries(stack: str) -> List[Choice]:
        return FrontendFactory._AVAILABLE_LIBRARIES.get(stack, [])