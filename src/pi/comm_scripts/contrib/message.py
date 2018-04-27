import re

from helpers.helpers import get_attributes, find_last


def main():
    message = Message("<t attribute =' value' attribute2='v\\\'al' attribute3=\"why\">192.168.1.2</t>"
                      "<t attr =' value'>192.168.1.3</t>"
                      "<f>192.168.1.3</f>"
                      "<s>2018_2_18_0_0_0_0</s>")
    attr_example = message.find_values("t", {"attribute": "value", "attribute2": "v\\\'al", "attribute3": "why"})
    print("Searching with attributes: " + str(attr_example))
    search_example = message.find_values("t")
    print("Searching without attributes: " + str(search_example))


class Message:
    """Wrapper class for sending messages as strings over
    a network.

    """
    def __init__(self, content):
        """
        Initialize the message with content
        :param content: String representing message's content
        :return: None
        """
        self.content = content

    def find_values(self, key, attributes=None):
        """
        Find and return values in `self.content` that are wrapped by the key
        `key`. If attributes is specified, only return values where the
        key also has attributes that match `attributes`
        :param key: A string representing the key to search for in `self.content`
        :param attributes: A dictionary of strings to strings specifying the attributes and values of those
        attributes that the target key must have to match.
        :return: A list containing all of the found values as strings.
        """
        if attributes is None:
            values = re.findall(r"<" + key + ".*?>(.*?)</" + key + ">", self.content, re.DOTALL)
            return values
        else:
            values = []
            key_vals = re.findall(r"<" + key + "(.*?>.*?)</" + key + ">", self.content)
            for key_val in key_vals:
                keys_attributes = get_attributes(key_val)
                add_value = True
                for attr in attributes:
                    if attr not in keys_attributes or attributes[attr] != keys_attributes[attr]:
                        add_value = False
                if add_value:
                    ind = find_last(">", key_val)
                    if ind != -1:
                        values.append(key_val[ind+1:])
            return values

    def __str__(self):
        return self.content


if __name__ == "__main__":
    main()
