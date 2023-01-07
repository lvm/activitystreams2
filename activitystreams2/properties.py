# Object properties
ATTACHMENT = "attachment"
ATTRIBUTED_TO = "attributedTo"
AUDIENCE = "audience"
CONTENT = "content"
CONTEXT = "context"
NAME = "name"
START_TIME = "startTime"
END_TIME = "endTime"
GENERATOR = "generator"
ICON = "icon"
IMAGE = "image"
IN_REPLY_TO = "inReplyTo"
LOCATION = "location"
PREVIEW = "preview"
PUBLISHED = "published"
REPLIES = "replies"
SUMMARY = "summary"
TAG = "tag"
UPDATED = "updated"
URL = "url"
TO = "to"
BTO = "bto"
CC = "cc"
BCC = "bcc"
MEDIA_TYPE = "mediaType"
DURATION = "duration"

# Link properties
HREF = "href"
REL = "rel"
HREFLANG = "hreflang"
HEIGHT = "height"
WIDTH = "width"
PREVIEW = "preview"

# Activity properties
ACTOR = "actor"
OBJECT_PROPERTY = "object"
TARGET = "target"
RESULT = "result"
ORIGIN = "origin"
INSTRUMENT = "instrument"

# Collection properties
TOTAL_ITEMS = "totalItems"
CURRENT = "current"
FIRST = "first"
LAST = "last"
ITEMS = "items"

# CollectionPage properties
PART_OF = "partOf"
NEXT = "next"
PREV = "prev"

# OrderedCollectionPage properties
START_INDEX = "startIndex"

# Extended: Place properties
ACCURACY = "accuracy"
ALTITUDE = "altitude"
LATITUDE = "latitude"
LONGITUDE = "longitude"
RADIUS = "radius"
UNITS = "units"

# Mastodon Props
# https://docs.joinmastodon.org/spec/activitypub/

INBOX = "inbox"
OUTBOX = "outbox"
FOLLOWING = "following"
FOLLOWERS = "followers"
PREFERRED_USERNAME = "preferredUsername"
PUBLIC_KEY = "publicKey"

ID = "id"


# Grouped Properties
OBJECT_PROPERTIES = [
    ID,
    ATTACHMENT,
    ATTRIBUTED_TO,
    AUDIENCE,
    CONTENT,
    CONTEXT,
    NAME,
    END_TIME,
    GENERATOR,
    ICON,
    IMAGE,
    IN_REPLY_TO,
    LOCATION,
    PREVIEW,
    PUBLISHED,
    REPLIES,
    START_TIME,
    SUMMARY,
    TAG,
    UPDATED,
    URL,
    TO,
    BTO,
    CC,
    BCC,
    MEDIA_TYPE,
    DURATION,
]


LINK_PROPERTIES = [
    HREF,
    REL,
    MEDIA_TYPE,
    NAME,
    HREFLANG,
    HEIGHT,
    WIDTH,
    PREVIEW,
]


ACTIVITY_PROPERTIES = INTRANSITIVY_ACTIVITY_PROPERTIES = OBJECT_PROPERTIES + [
    ACTOR,
    OBJECT_PROPERTY,
    TARGET,
    RESULT,
    ORIGIN,
    INSTRUMENT,
]


COLLECTION_PROPERTIES = ORDERED_COLLECTION_PROPERTIES = OBJECT_PROPERTIES + [
    TOTAL_ITEMS,
    CURRENT,
    ITEMS,
    FIRST,
    LAST,
]


COLLECTION_PAGE_PROPERTIES = COLLECTION_PROPERTIES + [
    PART_OF,
    NEXT,
    PREV,
]

ORDERED_COLLECTION_PAGE_PROPERTIES = COLLECTION_PAGE_PROPERTIES + [START_INDEX]
