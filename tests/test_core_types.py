#!/usr/bin/env python3

import copy
import unittest

from activitystreams2 import (
    DEFAULT_CONTEXT,
    make_activitystream_class,
    models,
    parse_activity,
    properties,
)


class TestCoreTypes(unittest.TestCase):
    def setUp(self):
        self.note_activity_dict = {
            "@context": DEFAULT_CONTEXT,
            "type": "Note",
            "id": "https://example.com/1",
            "content": "hey!!",
            "name": "hello world",
        }

    def test_type_creation(self):
        Note = make_activitystream_class("Note", properties.OBJECT_PROPERTIES)
        note_activity = Note(
            id="https://example.com/1", name="hello world", content="hey!!"
        )
        self.assertEqual(note_activity.type, "Note")
        self.assertEqual(note_activity.asdict(), self.note_activity_dict)

        note_activity.dismiss_context()
        note_activity_dict_no_ctx = copy.deepcopy(self.note_activity_dict)
        del note_activity_dict_no_ctx["@context"]
        self.assertEqual(note_activity.asdict(), note_activity_dict_no_ctx)

    def test_parse_activity(self):
        link_activity_dct = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "type": "Link",
            "href": "https://example.com/hello-world",
            "name": "Hello World",
        }
        parsed_activity_instance = parse_activity(link_activity_dct)
        link_activity = models.Link(
            href="https://example.com/hello-world", name="Hello World"
        )

        self.assertEqual(link_activity_dct, parsed_activity_instance.asdict())
        self.assertEqual(link_activity.asdict(), parsed_activity_instance.asdict())
