from questionary import Choice

from skelly.core.models import FrontendStack


class FrontendFactory:
    """
    Liefert Choice-Objekte fuer Questionary zurueck.
    Title = Was der User sieht
    Value = Was im Code ankommt (der echte Paketname)
    """

    _AVAILABLE_LIBRARIES = {
        FrontendStack.REACT: [
            Choice(title="Redux Toolkit", value="@reduxjs/toolkit react-redux"),
            Choice(title="React Router", value="react-router-dom"),
            Choice(title="TanStack Query", value="@tanstack/react-query"),
            Choice(title="Tailwind CSS", value="tailwindcss postcss autoprefixer"),
            Choice(title="Material UI", value="@mui/material @emotion/react @emotion/styled"),
        ],
        FrontendStack.LIT: [
            Choice(title="Lit Router", value="@lit-labs/router"),
        ],
        FrontendStack.ANGULAR: [
            Choice(title="Angular Material", value="@angular/material"),
        ],
    }

    @staticmethod
    def get_supported_libraries(stack: FrontendStack) -> list[Choice]:
        return FrontendFactory._AVAILABLE_LIBRARIES.get(stack, [])
