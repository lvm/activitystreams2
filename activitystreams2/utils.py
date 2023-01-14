from typing import Annotated

from activitystreams2.constants import MSSING_ACTIVITY_TYPE, RESERVED_PROPERTIES
from activitystreams2.models import (
    Empty,
    CoreType,
    make_activitystreams_class,
    parse_jsonld_compact_iri,
)


def parse_activitystreams_object(activity_object: dict) -> Empty | CoreType:
    """
    An "AS 2.0 Type" object converter.
    Receives an "AS 2.0 Type" object as `dict`.
    Returns a dataclass for this "AS 2.0 Type" type using `make_activitystreams_class`.
    """
    if not activity_object:
        # An Empty Type that mimics the real one.
        # A fancy way of representing "{}"
        return Empty()

    # Every "AS 2.0 Type" has a Type, unless when it doesn't.
    # in this case, we define a "MissingType" that will be removed down the road.
    activity_type: str = activity_object.get("type", MSSING_ACTIVITY_TYPE)

    # In any case, we do need an `activity_type` to name the dataclass created
    # (that's why the MISSING_ACTIVITY_TYPE/MissingType)
    activity_classname: str = (
        activity_type[0] if isinstance(activity_type, list) else activity_type
    )
    activity_property_names: list = [
        prop for prop, _ in activity_object.items() if prop not in RESERVED_PROPERTIES
    ]
    activity_cls: CoreType = make_activitystreams_class(
        activity_classname,
        activity_property_names,
    )
    activity_instance = activity_cls()
    activity_instance.update(
        {
            parse_jsonld_compact_iri(prop): value
            for prop, value in activity_object.items()
        }
    )
    if "@context" not in list(activity_object.keys()):
        activity_instance.dismiss_context()

    return activity_instance
