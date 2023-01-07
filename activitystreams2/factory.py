from dataclasses import field, fields, make_dataclass, MISSING
from typing import Any, List, Optional, Union
from activitystreams2.constants import (
    MSSING_ACTIVITY_TYPE,
    RESERVED_PROPERTIES,
    DEFAULT_CONTEXT,
)


def parse_jsonld_compact_iri(property_name: str) -> str:
    """
    Converts from `prefix:suffix` to `prefix__suffix`.
    Also removes `@` from properties.

    Note 1: https://www.w3.org/TR/json-ld/#dfn-compact-iri
    Note 2: Activity dataclasses contain in their fields a
    `metadata` property with the original activitystream-property.
    """
    parsed_property_name: str = property_name
    for special_char, replacement in [(":", "__"), ("@", "")]:
        parsed_property_name = parsed_property_name.replace(special_char, replacement)

    return parsed_property_name


def asdict(obj: Any) -> dict:
    """
    A dataclass Activity method.
    Converts "AS 2.0 Type" dataclasses to `dict`.
    """

    def getattr_(obj: Any, prop_name: str) -> Union[Any, list]:
        """
        Enhanced (read "hacky") `getattr` that tries to convert to
        dict if by chance property values are Activity objects.
        """
        attr: Any = getattr(obj, prop_name)
        if isinstance(attr, list) and hasattr(attr[0], "asdict"):
            return [child.asdict() for child in attr]
        return attr

    # Read Activity obj fields and returns a `dict`` with the AS2.0
    # correspondent key and its value. See also getattr_.__doc__.
    # Ignores empty (None) and MISSING properties
    activity_dict: dict = {
        prop.metadata.get("name", prop.name): getattr_(obj, prop.name)
        for prop in fields(obj)
        if getattr(obj, prop.name) not in [MISSING, None]
    }

    # In case the "AS 2.0 Type" is missing its type (ie: {"id": "..."})
    # simply remove it to avoid malformed objects.
    if activity_dict.get("type") == MSSING_ACTIVITY_TYPE:
        del activity_dict["type"]

    return activity_dict


def update_activity_properties(obj: Any, /, data: dict) -> None:
    """
    A dataclass Activity method.
    Sets values for "AS 2.0 Type" dataclasses properties.
    """
    for key, value in data.items():
        setattr(obj, key, value)


def remove_activity_property_context(obj: Any) -> None:
    """
    A dataclass Activity method.
    Sets `@context` as MISSING. Used mainly in child-activities.
    """
    setattr(obj, parse_jsonld_compact_iri("@context"), MISSING)


def make_activitystream_class(
    activity_classname: str, activity_property_names: List[str]
) -> Any:
    """
    An "AS 2.0 Type" dataclass factory.
    Receives an "AS 2.0 Type" type name (classname) and its properties.
    Returns a dataclass for this "AS 2.0 Type" type.

    Note = make_activitystream_class("Note", object_properties)

    is equivalent to

    @dataclass
    class Note:
        id: Any = field(...)
        attachment: Any = field(...)
        attributedTo: Any = field(...)
        [...]

        def update(self, **kwargs: dict) -> None: ...
        def asdict(self) -> dict: ...
    """

    # These are "reserved properties":
    # @context ->
    # Required as stated here: https://www.w3.org/TR/activitystreams-core/#jsonld
    # Can be missing from "child" AS Types.
    #
    # type ->
    # Defines the AS "object type". Can be missing.
    default_properties: list = [
        (
            parse_jsonld_compact_iri("@context"),
            Union[str, list],
            field(default=DEFAULT_CONTEXT, repr=False, metadata={"name": "@context"}),
        ),
        (
            "type",
            Union[str, list],
            field(default=activity_classname, repr=False, metadata={"name": "type"}),
        ),
    ]
    # These are the "actual properties":
    # Every other prop goes here unless it is in the "reserved" ones.
    activity_properties: list = [
        (
            parse_jsonld_compact_iri(prop),
            Optional[Any],
            field(default=None, metadata={"name": prop}),
        )
        for prop in activity_property_names
        if prop not in RESERVED_PROPERTIES
    ]
    activity_properties = default_properties + activity_properties

    # boom, dataclass magic.
    return make_dataclass(
        activity_classname,
        activity_properties,
        namespace={
            "asdict": asdict,
            "update": update_activity_properties,
            "dismiss_context": remove_activity_property_context,
        },
    )
