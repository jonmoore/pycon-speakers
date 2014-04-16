import sexmachine.detector as gender


class GenderPipeline(object):

    def __init__(self):
        self.detector = gender.Detector()

    def process_item(self, item, spider):
        firstname = self._get_firstname(item['name'])
        item['gender'] = self.detector.get_gender(firstname)
        return item


    def _get_firstname(self, name):
        '''
        in case the first token contains dot (e.g. Dr., D., S., etc)
        take the next available token
        '''
        name_parts = name.split() 
        firstname = name_parts[0]
        if firstname.find('.') != -1 and len(name_parts) > 1:
            firstname = name_parts[1]
        return firstname

class DefaultsPipeline(object):
    """
    Set default values.

    conference is set to spider name
    """

    def process_item(self, item, spider):
        item.setdefault('conference', spider.name)
        return item
