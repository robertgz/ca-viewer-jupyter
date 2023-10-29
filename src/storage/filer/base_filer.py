from dataclasses import dataclass

@dataclass(kw_only=True)
class BaseFiler:
    def get_name() -> str:
        pass

    def get_id() -> str:
        pass
