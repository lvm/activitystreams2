from activitystreams2.factory import make_activitystream_class
from activitystreams2.properties import (
    OBJECT_PROPERTIES,
    LINK_PROPERTIES,
    ACTIVITY_PROPERTIES,
    INTRANSITIVY_ACTIVITY_PROPERTIES,
    COLLECTION_PROPERTIES,
    ORDERED_COLLECTION_PROPERTIES,
    COLLECTION_PAGE_PROPERTIES,
    ORDERED_COLLECTION_PAGE_PROPERTIES,
)


class Empty:
    """
    Generic "Empty" Activity object.
    Mimics the same functionality found in dataclasses created with `make_activitystream_class`.
    """

    def update(self, **kwargs: dict) -> None:
        ...

    def asdict(self) -> dict:
        return {}


Object = make_activitystream_class("Object", OBJECT_PROPERTIES)
Link = make_activitystream_class("Link", LINK_PROPERTIES)

Activity = make_activitystream_class("Activity", ACTIVITY_PROPERTIES)
IntransitivyActivity = make_activitystream_class(
    "IntransitivyActivity", INTRANSITIVY_ACTIVITY_PROPERTIES
)

Collection = make_activitystream_class("Collection", COLLECTION_PROPERTIES)
OrderedCollection = make_activitystream_class(
    "OrderedCollection", ORDERED_COLLECTION_PROPERTIES
)

CollectionPage = make_activitystream_class("CollectionPage", COLLECTION_PAGE_PROPERTIES)
OrderedCollectionPage = make_activitystream_class(
    "OrderedCollectionPage", ORDERED_COLLECTION_PAGE_PROPERTIES
)
