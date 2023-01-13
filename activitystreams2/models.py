from dataclasses import MISSING, dataclass, field, fields, make_dataclass
from typing import Any, List, Optional, Protocol, TypeVar, cast

from activitystreams2.constants import (
    DEFAULT_CONTEXT,
    MSSING_ACTIVITY_TYPE,
    RESERVED_PROPERTIES,
)
from activitystreams2.properties import (
    ACTIVITY_PROPERTIES,
    COLLECTION_PAGE_PROPERTIES,
    COLLECTION_PROPERTIES,
    INTRANSITIVY_ACTIVITY_PROPERTIES,
    LINK_PROPERTIES,
    OBJECT_PROPERTIES,
    ORDERED_COLLECTION_PAGE_PROPERTIES,
    ORDERED_COLLECTION_PROPERTIES,
)


@dataclass
class GenericCoreType(Protocol):
    def update(self, **kwargs: dict) -> None:
        return None

    def asdict(self) -> dict:
        return {}


class CoreType(GenericCoreType):
    id: Optional[str]
    context: Optional[List | str]
    type: Optional[str]


class Empty(GenericCoreType):
    """
    Generic "Empty" Activity object.
    Mimics the same functionality found in dataclasses created with `make_activitystreams_class`.
    """

    ...


T_CoreType = TypeVar("T_CoreType", bound=CoreType)


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


def activitystreams_uri(obj: T_CoreType) -> str:
    as_type: str = ""
    if obj.type:
        as_type = f"#{obj.type}"

    return f"https://www.w3.org/ns/activitystreams{as_type}"


def asdict(obj: T_CoreType) -> dict:
    """
    A dataclass Activity method.
    Converts "AS 2.0 Type" dataclasses to `dict`.
    """

    def getattr_(obj: T_CoreType, prop_name: str) -> T_CoreType | list:
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


def update_activity_properties(obj: T_CoreType, /, data: dict) -> None:
    """
    A dataclass Activity method.
    Sets values for "AS 2.0 Type" dataclasses properties.
    """
    for key, value in data.items():
        setattr(obj, key, value)


def remove_activity_property_context(obj: T_CoreType) -> None:
    """
    A dataclass Activity method.
    Sets `@context` as MISSING. Used mainly in child-activities.
    """
    setattr(obj, parse_jsonld_compact_iri("@context"), MISSING)


def make_activitystreams_class(
    activity_classname: str, activity_property_names: List[str]
) -> CoreType:
    """
    An "AS 2.0 Type" dataclass factory.
    Receives an "AS 2.0 Type" type name (classname) and its properties.
    Returns a dataclass for this "AS 2.0 Type" type.

    Note = make_activitystreams_class("Note", object_properties)

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
            str | list,
            field(default=DEFAULT_CONTEXT, repr=False, metadata={"name": "@context"}),
        ),
        (
            "type",
            str | list,
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
    activitystreams_class = make_dataclass(
        activity_classname,
        activity_properties,
        namespace={
            "uri": activitystreams_uri,
            "asdict": asdict,
            "update": update_activity_properties,
            "dismiss_context": remove_activity_property_context,
        },
    )
    return cast(CoreType, activitystreams_class)


Object = make_activitystreams_class("Object", OBJECT_PROPERTIES)
Link = make_activitystreams_class("Link", LINK_PROPERTIES)

Activity = make_activitystreams_class("Activity", ACTIVITY_PROPERTIES)
IntransitivyActivity = make_activitystreams_class(
    "IntransitivyActivity", INTRANSITIVY_ACTIVITY_PROPERTIES
)

Collection = make_activitystreams_class("Collection", COLLECTION_PROPERTIES)
OrderedCollection = make_activitystreams_class(
    "OrderedCollection", ORDERED_COLLECTION_PROPERTIES
)

CollectionPage = make_activitystreams_class(
    "CollectionPage", COLLECTION_PAGE_PROPERTIES
)
OrderedCollectionPage = make_activitystreams_class(
    "OrderedCollectionPage", ORDERED_COLLECTION_PAGE_PROPERTIES
)
