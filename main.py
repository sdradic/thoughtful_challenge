from enum import Enum

from pydantic import BaseModel, field_validator


class PackageCategory(Enum):
    BULKY = "BULKY"
    HEAVY = "HEAVY"
    STANDARD = "STANDARD"


class PackageStack(Enum):
    STANDARD = "STANDARD"
    SPECIAL = "SPECIAL"
    REJECTED = "REJECTED"


class PackagePayload(BaseModel):
    width: int  # in cm
    height: int  # in cm
    length: int  # in cm
    mass: int  # in kg

    @field_validator("width", "height", "length")
    def validate_dimensions(cls, v):
        if v < 0:
            raise ValueError("Dimension cannot be negative")
        if not isinstance(v, int):
            raise ValueError("Dimension must be an integer")
        return v


def categorize_package(payload: PackagePayload) -> PackageCategory:
    """
    Categorize a package based on its payload.
    - A package is **bulky** if its volume (Width x Height x Length) is greater than or equal to 1,000,000 cm³ or when one of its dimensions is greater or equal to 150 cm.
    - A package is **heavy** when its mass is greater or equal to 20 kg.

    Return: package_category: ENUM("bulky", "heavy", "standard")
    """
    try:
        volume = payload.width * payload.height * payload.length
        is_volume_large = volume >= 1000000
        is_dimension_large = (
            payload.width >= 150 or payload.height >= 150 or payload.length >= 150
        )

        if is_volume_large or is_dimension_large:
            return PackageCategory.BULKY
        elif payload.mass >= 20:
            return PackageCategory.HEAVY
        else:
            return PackageCategory.STANDARD
    except Exception as e:
        raise Exception(f"Error categorizing package: {e}")


def sort(payload: PackagePayload) -> str:
    """
    Sort a package based on its payload.
    Return: package_stack: ENUM("standard", "special", "rejected")
    """
    try:
        category = categorize_package(payload)
        print(f"Package Category is {category.value}")
        match category:
            case PackageCategory.BULKY:
                return PackageStack.SPECIAL.value
            case PackageCategory.HEAVY:
                return PackageStack.SPECIAL.value
            case PackageCategory.STANDARD:
                return PackageStack.STANDARD.value
            case _:
                raise Exception("Invalid package category")
    except Exception as e:
        raise e


def main() -> str:
    payload_width = input("Enter the width of the package: ")
    payload_height = input("Enter the height of the package: ")
    payload_length = input("Enter the length of the package: ")
    payload_mass = input("Enter the mass of the package: ")
    payload = PackagePayload(
        width=payload_width,
        height=payload_height,
        length=payload_length,
        mass=payload_mass,
    )
    return sort(payload)


if __name__ == "__main__":
    print(main())
