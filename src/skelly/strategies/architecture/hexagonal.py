from skelly.strategies.base import ArchitectureStrategy


class HexagonalArchitecture(ArchitectureStrategy):
    """
    Hexagonal Architecture (Ports and Adapters).

    Structure based on inbound/domain/outbound separation:
    - inbound: DTOs, RestController, MessageConsumer, Security
    - domain: Entity, Service, Repository Interface, Client Interface, MessageProducer Interface
    - outbound: JpaRepositoryImpl, RestClientImpl, MessageProducerImpl
    """

    def __init__(self, project_name: str, base_package: str = "src"):
        self.project_name = project_name.lower().replace(" ", "")
        self.base_package = base_package

    def get_folders(self) -> list[str]:
        if self.base_package == "java":
            base = f"server/src/main/java/com/example/{self.project_name}"
        else:
            base = f"server/{self.base_package}"

        return [
            # === INBOUND (Driving Adapters) ===
            f"{base}/inbound/dto",
            f"{base}/inbound/rest",
            f"{base}/inbound/messaging",
            f"{base}/inbound/security",

            # === DOMAIN (Core Business Logic) ===
            f"{base}/domain/model",
            f"{base}/domain/service",
            f"{base}/domain/repository",      # Repository interfaces
            f"{base}/domain/client",          # External service client interfaces
            f"{base}/domain/messaging",       # MessageProducer interfaces

            # === OUTBOUND (Driven Adapters) ===
            f"{base}/outbound/persistence",   # JPA Repository implementations
            f"{base}/outbound/restclient",    # HTTP client implementations
            f"{base}/outbound/messaging",     # RabbitMQ/Kafka implementations

            # === CONFIG ===
            f"{base}/config",
        ]

    def get_name(self) -> str:
        return "Hexagonal Architecture"
